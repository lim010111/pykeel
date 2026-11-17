# AGENTS.md

핵심 모듈 경로는 에이전트가 수정하지 않고 설명·리뷰만 한다.

핵심 모듈 경로:

- `src/pykeel/loop/`: 에이전트 루프
- `src/pykeel/llm/`: wire 어댑터, SSE 파서, 스트림 조립, 내부 메시지 모델
- `src/pykeel/tools/`: tool 실행, 취소, 샌드박스 래퍼
- `src/pykeel/session/`: 컨텍스트, Session 관리
