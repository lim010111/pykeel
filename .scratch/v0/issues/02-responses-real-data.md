# 02: Responses 실제 응답을 받아 픽스처로 남긴다

**What to build:** llm 모듈 사이클 1단계(실제 데이터 보기)다. 이 티켓에서 처음으로 OpenAI API를 호출하므로, 그 전에 pykeel 전용 OpenAI 프로젝트를 만들어 월 hard spend limit을 걸고 그 프로젝트의 키만 쓴다. 그다음 bash function tool을 붙인 Responses 요청으로 왕복 한 번(모델의 function_call → function_call_output을 돌려줌 → 최종 답)을 curl로 받아 원본을 저장한다. 대화 상태는 ADR-0004대로 하네스가 들고 간다(`store: false`, 매 요청에 이전 item 전체). 저장한 원본은 비밀값과 계정 식별 헤더를 지운 뒤 테스트 픽스처로 커밋한다. 05와 09가 이 픽스처로 네트워크 없이 검증한다.

**Blocked by:** 01 비밀값 검사

**Status:** ready-for-human

- [x] pykeel 전용 OpenAI 프로젝트에 월 hard spend limit이 걸려 있고, 그 프로젝트의 키만 쓴다
- [x] bash function tool을 붙인 요청과 응답의 원본이 왕복 한 번 전체로 남아 있다(function_call, function_call_output, 최종 답)
- [x] `store: false`일 때 오는 reasoning item(암호화된 추론 내용 포함)을 다음 요청에 그대로 돌려준 기록이 있다
- [x] 실제 응답 헤더를 보고 trace 허용 목록(요청 ID, 처리 시간, 속도 제한)에 넣을 헤더 이름을 정한다
- [x] Responses 응답에 백엔드 식별 필드가 있는지 확인하고, 결과를 plan.md에 반영한다
- [x] 비밀값과 계정 식별 헤더를 지운 원본이 픽스처로 커밋되고, 비밀값 검사를 통과한다
- [x] llm 설계 메모에 이번 사이클의 실제 데이터 절을 쓴다

## Comments

- 2026-11-19: 키를 처음 넣을 때 챙길 것(01 비밀값 검사 쪽 사정).
  - `.env.example`을 `.env`로 복사해 채운다. 환경 변수 이름은 `_API_KEY`, `_TOKEN`, `_SECRET`, `_PASSWORD` 중 하나로 끝나야 검사기가 실제 값을 찾는다(`scripts/secret_scan.py`의 `SECRET_ENV_NAME`). 이름을 바꿀 때도 이 규칙을 지킨다.
  - pytest는 `.env`를 알아서 읽지 않는다. 실제 값까지 검사하려면 `uv run --env-file .env pytest`로 돌린다. pre-commit hook은 `.env`가 있으면 읽는다.
  - `.env`를 만든 직후 `uv run --env-file .env pytest tests/policy`가 통과하는지 한 번 본다. 픽스처를 커밋하기 전에도 같은 명령을 돌린다.
- 2026-11-19: 진행 상황.
  - 왕복 두 벌을 `tests/fixtures/responses/`에 픽스처로 넣었다. `bash-no-reasoning`(low)과 `bash-with-reasoning`(high)이다. 응답 헤더에서 `openai-organization`, `openai-project`, `set-cookie`, `cf-ray`의 값을 지웠고, `uv run --env-file .env pytest tests/policy`가 통과했다.
  - low와 medium에서는 reasoning item이 오지 않아 high로 받았다. 관찰 내용은 `docs/design/llm.md` "실제 데이터"에 있다.
  - 남은 것: spend limit 확인(사용자가 콘솔에서), trace 헤더 허용 목록 결정(후보는 설계 메모의 헤더 표).
- 2026-11-19: 외부 리뷰(Gemini)를 반영해 설계 메모를 고쳤다.
  - `openai-processing-ms`를 잘못 짝지었던 서술을 바로잡았다. 처리 시간은 출력 토큰 수와 함께 커졌다.
  - 최상위 종료 상태(`status`, `error`, `incomplete_details`), 토큰 산술, 미확인 목록을 보충했다.
  - trace 헤더 허용 목록을 정했다: `x-request-id`, `openai-processing-ms`, `openai-version`, `retry-after`, `x-ratelimit-*` 9종(project-tokens 3종 포함), `server-timing-total`, `x-openai-inference-capacity-reason`. 근거는 설계 메모의 헤더 표에 있다.
- 2026-11-19: 사용자가 전용 프로젝트에 월 hard spend limit이 걸려 있는 것을 콘솔에서 확인했다. 모든 항목을 마쳤다.
