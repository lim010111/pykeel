"""비밀값 검사(scripts/secret_scan.py)가 docs/plan.md "원칙 > 비밀값" 절대로 동작하는지 본다.

첫 테스트는 이 저장소 자체를 검사한다. `uv run --env-file .env pytest`로 돌리면
.env의 실제 키 값이 커밋될 수 있는 파일에 들어 있는지도 함께 본다.

나머지는 임시 git 저장소에서 검사기의 동작을 확인한다. 이 파일이 검사기에 걸리지 않도록
키 모양 문자열은 모두 실행할 때 조립한다.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCANNER = REPO_ROOT / "scripts" / "secret_scan.py"

FAKE_OPENAI_KEY = "sk-" + "proj-" + "Ab3" * 15
FAKE_BEARER = "Bearer " + "eyJ" + "x9" * 15
FAKE_GITHUB_TOKEN = "ghp" + "_" + "Z7" * 18
FAKE_PRIVATE_KEY = "-----BEGIN " + "OPENSSH PRIVATE KEY-----"
# 키 모양 규칙에는 맞지 않는 값. 실제 값 검사로만 잡혀야 한다.
FAKE_EXAONE_KEY = "exa" + "0123456789abcdef" * 2


def run_scan(
    repo: Path, *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-I", str(SCANNER), *args],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def isolated_env(tmp_path: Path, **extra: str) -> dict[str, str]:
    # 사용자의 git 설정과 셸의 실제 키 값이 결과에 끼어들지 않게 한다.
    return {
        "PATH": os.environ["PATH"],
        "HOME": str(tmp_path / "home"),
        "GIT_CONFIG_NOSYSTEM": "1",
        **extra,
    }


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    path = tmp_path / "repo"
    path.mkdir()
    (tmp_path / "home").mkdir()
    subprocess.run(
        ["git", "init", "-q", "-b", "main", str(path)],
        env=isolated_env(tmp_path),
        check=True,
    )
    return path


def git_add(repo: Path, tmp_path: Path, *paths: str) -> None:
    subprocess.run(
        ["git", "add", *paths], cwd=repo, env=isolated_env(tmp_path), check=True
    )


def test_repository_has_no_secrets() -> None:
    result = run_scan(REPO_ROOT, env=dict(os.environ))
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    ("content", "rule"),
    [
        (f"OPENAI_API_KEY={FAKE_OPENAI_KEY}\n", "openai-key"),
        (f"curl -H 'Authorization: {FAKE_BEARER}'\n", "bearer-token"),
        (f"token: {FAKE_GITHUB_TOKEN}\n", "github-token"),
        (f"{FAKE_PRIVATE_KEY}\n", "private-key"),
    ],
)
def test_detects_key_shaped_string(
    repo: Path, tmp_path: Path, content: str, rule: str
) -> None:
    (repo / "notes.md").write_text("first line\n" + content)
    git_add(repo, tmp_path, "notes.md")

    result = run_scan(repo, env=isolated_env(tmp_path))

    assert result.returncode == 1
    assert f"notes.md:2: {rule}" in result.stderr


@pytest.mark.parametrize(
    "content",
    [
        "Authorization: Bearer <key>\n",
        'curl -H "Authorization: Bearer $OPENAI_API_KEY"\n',
        "scikit-learn and sk-short\n",
    ],
)
def test_ignores_placeholders(repo: Path, tmp_path: Path, content: str) -> None:
    (repo / "README.md").write_text(content)
    git_add(repo, tmp_path, "README.md")

    result = run_scan(repo, env=isolated_env(tmp_path))

    assert result.returncode == 0, result.stderr


def test_scans_untracked_file_that_could_be_committed(
    repo: Path, tmp_path: Path
) -> None:
    (repo / "response.json").write_text(f'{{"key": "{FAKE_OPENAI_KEY}"}}\n')

    result = run_scan(repo, env=isolated_env(tmp_path))

    assert result.returncode == 1
    assert "response.json:1: openai-key" in result.stderr


def test_skips_gitignored_file(repo: Path, tmp_path: Path) -> None:
    (repo / ".gitignore").write_text(".env\n")
    (repo / ".env").write_text(f"OPENAI_API_KEY={FAKE_OPENAI_KEY}\n")

    result = run_scan(repo, env=isolated_env(tmp_path))

    assert result.returncode == 0, result.stderr


def test_detects_actual_value_of_secret_env_var(repo: Path, tmp_path: Path) -> None:
    (repo / "fixture.json").write_text(f'{{"echo": "{FAKE_EXAONE_KEY}"}}\n')
    git_add(repo, tmp_path, "fixture.json")

    without_env = run_scan(repo, env=isolated_env(tmp_path))
    with_env = run_scan(
        repo, env=isolated_env(tmp_path, EXAONE_API_KEY=FAKE_EXAONE_KEY)
    )

    assert without_env.returncode == 0, without_env.stderr
    assert with_env.returncode == 1
    assert "fixture.json:1: env:EXAONE_API_KEY" in with_env.stderr


def test_ignores_short_or_unrelated_env_values(repo: Path, tmp_path: Path) -> None:
    (repo / "notes.md").write_text("main\nshort\n" + FAKE_EXAONE_KEY + "\n")
    git_add(repo, tmp_path, "notes.md")

    env = isolated_env(tmp_path, GH_TOKEN="short", EXAONE_MODEL=FAKE_EXAONE_KEY)
    result = run_scan(repo, env=env)

    assert result.returncode == 0, result.stderr


def test_staged_mode_reads_index_not_worktree(repo: Path, tmp_path: Path) -> None:
    # 키가 든 내용을 add한 뒤 작업 트리에서만 지우면, 키는 그대로 커밋된다.
    (repo / "capture.txt").write_text(FAKE_OPENAI_KEY + "\n")
    git_add(repo, tmp_path, "capture.txt")
    (repo / "capture.txt").write_text("redacted\n")

    worktree = run_scan(repo, env=isolated_env(tmp_path))
    staged = run_scan(repo, "--staged", env=isolated_env(tmp_path))

    assert worktree.returncode == 0, worktree.stderr
    assert staged.returncode == 1
    assert "capture.txt:1: openai-key" in staged.stderr


def test_staged_mode_skips_unstaged_new_file(repo: Path, tmp_path: Path) -> None:
    (repo / "clean.txt").write_text("nothing here\n")
    git_add(repo, tmp_path, "clean.txt")
    (repo / "later.txt").write_text(FAKE_OPENAI_KEY + "\n")

    result = run_scan(repo, "--staged", env=isolated_env(tmp_path))

    assert result.returncode == 0, result.stderr


def test_output_never_contains_secret_values(repo: Path, tmp_path: Path) -> None:
    (repo / "dump.txt").write_text(f"{FAKE_OPENAI_KEY}\n{FAKE_EXAONE_KEY}\n")
    git_add(repo, tmp_path, "dump.txt")

    env = isolated_env(tmp_path, EXAONE_API_KEY=FAKE_EXAONE_KEY)
    results = [run_scan(repo, env=env), run_scan(repo, "--staged", env=env)]

    for result in results:
        assert result.returncode == 1
        output = result.stdout + result.stderr
        assert FAKE_OPENAI_KEY not in output
        assert FAKE_EXAONE_KEY not in output
