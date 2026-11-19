# 이슈 트래커: 로컬 마크다운

이 저장소의 이슈와 spec은 `.scratch/` 아래 마크다운 파일이다. `.scratch/`는 git에 커밋한다.

## 규칙

- 작업 묶음 하나에 디렉터리 하나: `.scratch/<feature-slug>/`. 로드맵 단계는 단계 이름을 slug로 쓴다(`.scratch/v0/`).
- 로드맵 단계의 spec은 `docs/plan.md`의 해당 절이다. `.scratch/<feature-slug>/spec.md`는 plan.md에 절이 없는 작업에만 만든다.
- 티켓은 파일 하나에 하나씩 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`로 두고, `01`부터 번호를 붙인다.
- triage 상태는 티켓 위쪽의 `Status:` 줄에 적는다. 값은 [triage-labels.md](triage-labels.md)의 라벨이다.
- 댓글과 대화 기록은 파일 끝의 `## Comments` 아래에 덧붙인다.

## 스킬이 "publish to the issue tracker"라고 할 때

`.scratch/<feature-slug>/` 아래에 새 파일을 만든다. 디렉터리가 없으면 만든다.

## 스킬이 "fetch the relevant ticket"이라고 할 때

해당 경로의 파일을 읽는다. 사용자는 보통 경로나 번호를 직접 준다.

## Wayfinding operations

`/wayfinder`가 쓴다. 맵은 파일 하나이고, 티켓은 자식 파일이다.

- **맵:** `.scratch/<effort>/map.md`(Destination, Notes, Decisions so far, Not yet specified, Out of scope)
- **자식 티켓:** `.scratch/<effort>/issues/NN-<slug>.md`. `01`부터 번호를 붙이고 본문에 질문을 적는다. `Type:` 줄에 종류(`research`/`prototype`/`grilling`/`task`)를, `Status:` 줄에 `claimed`/`resolved`를 적는다.
- **차단:** 위쪽의 `Blocked by: NN, NN` 줄. 나열된 파일이 모두 `resolved`이면 풀린다.
- **프런티어:** 열려 있고, 차단이 풀렸고, 아무도 맡지 않은 파일. 번호가 작은 것부터.
- **맡기:** 작업 전에 `Status: claimed`로 바꾸고 저장한다.
- **해결:** `## Answer` 아래에 답을 덧붙이고 `Status: resolved`로 바꾼 뒤, `map.md`의 Decisions so far에 요지와 링크를 덧붙인다.
- **research 티켓의 결과:** 버리는 `research/<name>` 브랜치 대신 `docs/research/YYYY-MM-DD-<주제>.md`로 써서 main에 병합한다. 티켓에는 그 파일 링크를 남긴다.
- **맵을 마칠 때:** 결정을 `docs/plan.md`와 ADR에 옮긴다. 옮길 곳은 맵의 Destination에 적는다.
