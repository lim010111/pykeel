"""커밋될 수 있는 파일에서 비밀값을 찾는다.

규칙은 docs/plan.md의 "원칙 > 비밀값" 절을 따른다.

- 기본 모드는 `git ls-files --cached --others --exclude-standard`로 고른 파일의
  작업 트리 내용을 본다. pytest가 이 모드로 돌린다.
- `--staged` 모드는 index에 올라간 내용을 본다. pre-commit hook이 이 모드로 돌린다.
  작업 트리에서 지웠어도 index에 남아 있으면 그대로 커밋되기 때문이다.

찾는 것은 두 가지다.

- 키 모양 문자열(RULES)
- 설정되어 있다면 실제 키 값. 이름이 SECRET_ENV_NAME에 맞는 환경 변수의 값이다.

찾은 값은 출력하지 않는다. 출력이 터미널, AI 협업자의 컨텍스트, CI 로그로 넘어가기 때문이다.
파일, 줄, 규칙 이름만 출력한다.

표준 라이브러리만 쓴다. hook이 `python -I`로 실행한다.
"""

import argparse
import os
import re
import subprocess
import sys
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path

RULES: dict[str, re.Pattern[bytes]] = {
    # OpenAI 키: sk-proj-, sk-svcacct-, sk-admin-, 예전 sk-
    "openai-key": re.compile(rb"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}"),
    # 형식을 모르는 키(EXAONE 등)도 curl -v 출력이나 저장한 요청 헤더에서는 이 모양으로 남는다.
    # 문서의 `Bearer <key>`, `Bearer $OPENAI_API_KEY` 같은 자리표시는 맞지 않는다.
    "bearer-token": re.compile(rb"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{20,}"),
    "github-token": re.compile(rb"\b(?:gh[pousr]|github_pat)_[A-Za-z0-9_]{30,}"),
    "private-key": re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}

SECRET_ENV_NAME = re.compile(r"(?:API_KEY|_TOKEN|_SECRET|_PASSWORD)$")
# 짧은 값은 우연히 겹치기 쉽다. 실제 API 키는 이보다 훨씬 길다.
MIN_SECRET_LEN = 16


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str


def secret_env_values(environ: Mapping[str, str]) -> dict[str, bytes]:
    return {
        name: os.fsencode(value)
        for name, value in environ.items()
        if SECRET_ENV_NAME.search(name) and len(value) >= MIN_SECRET_LEN
    }


def _line_of(data: bytes, pos: int) -> int:
    return data.count(b"\n", 0, pos) + 1


def scan_bytes(data: bytes, secrets: Mapping[str, bytes]) -> Iterator[tuple[int, str]]:
    for rule, pattern in RULES.items():
        for match in pattern.finditer(data):
            yield _line_of(data, match.start()), rule
    for name, value in secrets.items():
        pos = data.find(value)
        while pos != -1:
            yield _line_of(data, pos), f"env:{name}"
            pos = data.find(value, pos + 1)


def _git(root: Path, *args: str, stdin: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=root, input=stdin, capture_output=True, check=True
    ).stdout


def worktree_files(root: Path) -> Iterator[tuple[str, bytes]]:
    listed = _git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    # 충돌 중인 파일은 --cached에 여러 번 나온다.
    for raw in sorted(set(listed.split(b"\0")) - {b""}):
        path = os.fsdecode(raw)
        full = root / path
        if full.is_symlink():
            # 커밋되는 것은 링크가 가리키는 경로 문자열이다.
            yield path, os.fsencode(os.readlink(full))
        elif full.is_file():
            yield path, full.read_bytes()
        # 그 밖은 index에는 있지만 작업 트리에서 지운 파일이다.


def staged_files(root: Path) -> Iterator[tuple[str, bytes]]:
    listed = _git(root, "ls-files", "-z", "--cached", "--stage")
    entries: list[tuple[str, str]] = []
    for record in listed.split(b"\0"):
        if not record:
            continue
        meta, raw_path = record.split(b"\t", 1)
        mode, sha, _stage = meta.split(b" ")
        if mode == b"160000":  # submodule은 이 저장소의 blob이 아니다.
            continue
        entries.append((sha.decode(), os.fsdecode(raw_path)))
    if not entries:
        return
    batch = _git(
        root,
        "cat-file",
        "--batch",
        stdin=b"".join(f"{sha}\n".encode() for sha, _ in entries),
    )
    # 출력 형식: "<sha> <type> <size>\n<내용>\n"이 입력 순서대로 이어진다.
    pos = 0
    for _sha, path in entries:
        header_end = batch.index(b"\n", pos)
        size = int(batch[pos:header_end].split(b" ")[2])
        start = header_end + 1
        yield path, batch[start : start + size]
        pos = start + size + 1


def scan(
    files: Iterator[tuple[str, bytes]], secrets: Mapping[str, bytes]
) -> list[Finding]:
    return [
        Finding(path, line, rule)
        for path, data in files
        for line, rule in scan_bytes(data, secrets)
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="커밋될 수 있는 파일에서 비밀값을 찾는다."
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="작업 트리 대신 index에 올라간 내용을 본다",
    )
    staged: bool = parser.parse_args(argv).staged

    root = Path(_git(Path.cwd(), "rev-parse", "--show-toplevel").decode().strip())
    files = staged_files(root) if staged else worktree_files(root)
    findings = scan(files, secret_env_values(os.environ))
    if not findings:
        return 0
    for finding in sorted(findings, key=lambda f: (f.path, f.line, f.rule)):
        print(f"{finding.path}:{finding.line}: {finding.rule}", file=sys.stderr)
    print(
        f"비밀값으로 보이는 문자열 {len(findings)}개를 찾았습니다. 값은 출력하지 않습니다.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
