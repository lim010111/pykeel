# AGENTS.md

이 저장소에서 작업하는 AI 협업자(Claude Code, Codex 등)를 위한 규칙이다. 용어는 [GLOSSARY.md](GLOSSARY.md)를 따른다.

핵심 모듈 경로는 AI 협업자가 수정하지 않고 설명·리뷰만 하는 것을 지향하되, 가장 중요한 것은 하네스의 완성도다. 완성도를 위해 핵심 모듈을 고쳐야 한다고 판단되면 먼저 제안하고, 사용자가 요청하면 고친다.

핵심 모듈 경로:

- `src/pykeel/loop/`: 에이전트 루프
- `src/pykeel/llm/`: wire 어댑터, SSE 파서, 스트림 조립, 내부 메시지 모델
- `src/pykeel/tools/`: tool 실행, 취소, 샌드박스 래퍼
- `src/pykeel/session/`: 컨텍스트, Session 관리
- `src/pykeel/trace/`: 실행 기록(trace)
- `tests/<위 모듈 이름>/`: 핵심 모듈의 동작 테스트. 테스트가 곧 명세이므로 핵심 모듈과 같이 취급한다

핵심 모듈 경로 밖은 모두 주변부이고, AI 협업자가 써도 된다. 그중 규칙이 붙은 곳:

- `tests/policy/`: 합의한 규칙(샌드박스 경계, 비밀값 검사)이 지켜지는지 확인하는 테스트. 대상 핵심 모듈의 함수 이름과 시그니처가 정해진 뒤에 쓴다.
- CLI와 설정 읽기: AI 협업자가 구현하고, 사용자는 값만 정한다. 안전 규칙(샌드박스, 비용 상한, 환경 변수 허용 목록)은 핵심 모듈이 지킨다. 주변부에 이 규칙을 끄거나 우회하는 경로를 만들지 않는다.

## Agent skills

### Issue tracker

로컬 마크다운. 티켓은 `.scratch/<feature-slug>/issues/`에 파일로 둔다. `docs/agents/issue-tracker.md` 참고.

### Triage labels

기본 역할 이름 5개를 그대로 쓰고, 핵심 모듈 티켓은 `ready-for-human`이다. `docs/agents/triage-labels.md` 참고.

### Domain docs

단일 컨텍스트. `GLOSSARY.md`, `docs/adr/`, `docs/plan.md`를 읽는다. `docs/agents/domain.md` 참고.
