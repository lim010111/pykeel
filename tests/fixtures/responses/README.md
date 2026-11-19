# Responses 실제 응답 픽스처

티켓 02에서 OpenAI Responses API(`POST /v1/responses`)를 curl로 호출해 받은 원본이다. llm, trace, loop 테스트가 네트워크 없이 쓴다.

- 받은 날: 2026-11-19
- 모델: `gpt-6.2-sol`
- 공통 요청 설정: `store: false`, bash function tool 하나, 비스트리밍
- 대화 상태는 하네스가 들고 간다([ADR-0004](../../../docs/adr/0004-harness-owns-responses-state.md)). 그래서 `call2.request.json`의 `input`에는 첫 요청의 `input`, `call1.response.json`의 `output` item 전체(받은 그대로), `function_call_output`이 이 순서로 들어 있다.

## 시나리오

| 디렉터리 | effort | 사용자 요청 | 내용 |
|---|---|---|---|
| `bash-no-reasoning/` | low | `echo hello` 실행 | reasoning item 없음(`reasoning_tokens: 0`) |
| `bash-with-reasoning/` | high | 잘못된 최단 부분배열 함수의 반례 설계 | 두 응답 모두 reasoning item(`encrypted_content` 포함)이 있음. `call2`의 `input_transformations`는 `[]` |

`function_call_output`의 `output`은 모델이 요청한 명령을 로컬에서 직접 실행한 결과다. 샌드박스 없이 사람이 내용을 확인한 뒤 실행했다.

## 파일

- `callN.request.json`: 보낸 요청 본문. 요청 헤더(API 키 포함)는 남기지 않았다.
- `callN.response.json`: 받은 응답 본문. 바이트 그대로이고 고친 곳이 없다.
- `callN.response-headers.txt`: curl `-D`로 받은 응답 헤더(CRLF). 아래 헤더는 이름만 남기고 값을 `REDACTED`로 바꿨다. 계정 식별 값이거나 쿠키다.
  - `openai-organization`, `openai-project`, `set-cookie`, `cf-ray`

`.gitattributes`가 이 디렉터리의 줄바꿈 변환을 막는다. 원본을 고치지 말고, 새 원본이 필요하면 새 시나리오 디렉터리를 만든다.
