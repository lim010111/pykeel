# llm 설계 메모

llm 모듈(wire 어댑터, SSE 파서, 스트림 조립, 내부 메시지 모델)의 설계 메모다. 사이클을 돌 때마다 날짜를 붙인 절을 쌓는다([plan.md "보완 2"](../plan.md)).

## 2026-11-19 사이클 1: Responses 비스트리밍

### 실제 데이터

티켓 02에서 `POST /v1/responses`를 curl로 호출해 받은 원본이다. 원본은 [tests/fixtures/responses/](../../tests/fixtures/responses/)에 있다.

- 모델 `gpt-6.2-sol`, `store: false`, function tool `bash` 하나, 비스트리밍
- 대화 상태는 하네스가 들고 매 요청에 이전 item 전체를 보냈다([ADR-0004](../adr/0004-harness-owns-responses-state.md)).

| 픽스처 | effort | `output` item | reasoning_tokens | input_tokens |
|---|---|---|---:|---:|
| `bash-no-reasoning/call1` | low | function_call | 0 | 76 |
| `bash-no-reasoning/call2` | low | message | 0 | 108 |
| `bash-with-reasoning/call1` | high | reasoning, function_call | 209 | 316 |
| `bash-with-reasoning/call2` | high | reasoning, message | 37 | 964 |

#### reasoning item

- 추론을 하지 않으면 reasoning item 자체가 없다. 빈 item이 오지 않는다.
- effort는 상한일 뿐이다. 픽스처로 남기지 않은 시도에서 low는 쉬운 요청(`echo hello`)과 어려운 요청(반례 설계) 모두 0토큰, medium도 쉬운 요청에 0토큰이었다. high에 어려운 요청을 줬을 때 처음 추론했다. 둘 중 무엇이 결정적이었는지는 가르지 못했다.
  - v0 기본 설정(low)에서는 reasoning item이 없는 응답이 흔할 것이다. 두 경우를 모두 다뤄야 한다.
- 키는 `id`(`rs_`), `type`, `content`(`[]`), `encrypted_content`, `summary`(`[]`) 다섯 개다. 다른 item과 달리 `status`가 없다.
- `include` 없이도 `encrypted_content`가 왔다(4,556자, 3,192자). ADR-0004의 전제가 맞았다.
- 받은 item을 바이트 그대로 돌려준 요청(`call2`)의 `input_transformations`는 `[]`였다. 서버가 reasoning item을 버리지 않았다.
- **최종 응답에도 reasoning item이 붙는다**(`reasoning, message`). 루프가 끝나는 턴의 reasoning item도 버리지 않고 Session에 쌓아야 다음 사용자 턴에 돌려줄 수 있다.

#### function_call과 message item

- function_call 키: `id`(`fc_`), `type`, `status`, `arguments`, `call_id`(`call_`), `name`.
  - `arguments`는 JSON 문자열이다. 한 번 더 파싱해야 `command`가 나온다.
  - `id`와 `call_id`가 따로 있다. `function_call_output`은 `call_id`로 잇는다.
- message 키: `id`, `type`, `status`, `content`, `phase`, `role`.
  - `phase`가 `"final_answer"`였다. 조사에 없던 필드다. 다른 값(중간 해설 등)이 있는지는 모른다. 루프의 종료 판단에 쓸 수 있는지 확인할 거리다.
  - `content` 항목 키: `type`(`output_text`), `annotations`, `logprobs`, `text`.
- `parallel_tool_calls`는 기본값 `true`로 돌아왔다. 이번 응답은 모두 function_call이 하나였지만, 여러 개가 오는 경우를 다뤄야 한다.

#### 응답 최상위 필드

- 응답이 요청에 없던 값을 기본값으로 채워 돌려준다.
  - `temperature: 1.0`, `top_p: 1.0`. GPT-6.2는 요청에서 이 둘을 빼라고 한다([조사](../research/2026-11-18-openai.md)). 그러니 응답에 찍힌 값을 샘플링 설정으로 기록하면 틀린다. 샘플링 설정은 요청 쪽에서 남긴다.
  - tool 정의에 `strict: true`와 `output_schema: null`이 붙었다. 보낸 요청에는 `strict`가 없었다. function tool이 기본으로 strict 모드라는 뜻으로 보인다. bash tool의 스키마(`additionalProperties: false`, 모든 속성 required)는 strict 조건에 맞는다. tool 스키마를 넓힐 때 이 조건을 지켜야 한다.
- 조사에 없던 필드: `reasoning.context`(`"all_turns"`), `reasoning.mode`(`"standard"`), `prompt_cache_retention`(`"24h"`), `access_programs`, `billing`, `image`, `tool_usage`, `completed_at`.
- `usage`에 `input_tokens_details.cache_write_tokens`(TTL별)가 있다. 네 응답 모두 `cached_tokens`가 0이었다. 입력이 짧아서(최대 964토큰)일 수 있다. 확인하지 않았다.

#### 백엔드 식별 필드

Responses 응답 본문에는 `system_fingerprint` 같은 백엔드 식별 필드가 없다. `model`도 요청한 별칭(`gpt-6.2-sol`) 그대로이고 날짜 스냅샷이 붙지 않는다. plan.md에 반영했다.

#### 응답 헤더

네 응답의 헤더 이름은 모두 같았다.

| 헤더 | 값의 예 | trace |
|---|---|---|
| `x-request-id` | `req_...` | 허용 목록 후보 |
| `openai-processing-ms` | 1975~12577 | 허용 목록 후보 |
| `x-ratelimit-limit-requests`, `x-ratelimit-limit-tokens` | 10000, 4000000 | 허용 목록 후보 |
| `x-ratelimit-remaining-requests`, `x-ratelimit-remaining-tokens` | 9999, 4000000 | 허용 목록 후보 |
| `x-ratelimit-reset-requests`, `x-ratelimit-reset-tokens` | `6ms`, `0s` | 허용 목록 후보 |
| `openai-version` | `2020-10-01` | 미정 |
| `openai-organization`, `openai-project` | 계정 식별 값 | 제외(픽스처에서 지움) |
| `set-cookie`, `cf-ray` | Cloudflare 쿠키, 요청 추적 ID | 제외(픽스처에서 지움) |
| `date`, `content-type`, `content-length`, `server`, `cf-cache-status`, `strict-transport-security`, `x-content-type-options`, `alt-svc`, `access-control-expose-headers` | | 제외 |

- `openai-processing-ms`는 출력 토큰 수와 비례하지 않았다. 17토큰짜리 최종 답(`bash-no-reasoning/call2`)이 12,577ms였다.
- `access-control-expose-headers`에 `Server-Timing-Total`과 `X-OpenAI-Inference-Capacity-Reason`이 나오지만, 네 응답에는 그 헤더가 없었다. 상황에 따라 붙을 수 있다.
- 허용 목록은 아직 정하지 않았다(티켓 02).
