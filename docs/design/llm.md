# llm 설계 메모

llm 모듈(wire 어댑터, SSE 파서, 스트림 조립, 내부 메시지 모델)의 설계 메모다. 사이클을 돌 때마다 날짜를 붙인 절을 쌓는다([plan.md "보완 2"](../plan.md)).

## 2026-11-19 사이클 1: Responses 비스트리밍

### 실제 데이터

티켓 02에서 `POST /v1/responses`를 curl로 호출해 받은 원본이다. 원본은 [tests/fixtures/responses/](../../tests/fixtures/responses/)에 있다.

- 모델 `gpt-6.2-sol`, `store: false`, function tool `bash` 하나, 비스트리밍
- 대화 상태는 하네스가 들고 매 요청에 이전 item 전체를 보냈다([ADR-0004](../adr/0004-harness-owns-responses-state.md)).

| 픽스처 | effort | `output` item | output_tokens (reasoning) | input_tokens | `openai-processing-ms` |
|---|---|---|---:|---:|---:|
| `bash-no-reasoning/call1` | low | function_call | 19 (0) | 76 | 2,139 |
| `bash-no-reasoning/call2` | low | message | 17 (0) | 108 | 1,975 |
| `bash-with-reasoning/call1` | high | reasoning, function_call | 595 (209) | 316 | 11,479 |
| `bash-with-reasoning/call2` | high | reasoning, message | 749 (37) | 964 | 12,577 |

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
  - `phase`가 `"final_answer"`였다. 조사에 없던 필드이고, 다른 값이 무엇인지는 확인하지 못했다.
  - `content`는 배열이다. 이번에는 `output_text` 하나였고, 항목 키는 `type`, `annotations`, `logprobs`, `text`였다.
- `parallel_tool_calls`는 기본값 `true`로 돌아왔다. 이번 응답은 모두 function_call이 하나였지만, 여러 개가 오는 경우를 다뤄야 한다.
- 그대로 돌려줘야 하는 것은 reasoning item만이 아니다. 이번 `call2` 요청은 function_call도 `id`, `status`를 포함해 받은 그대로 보냈다. GPT-6.2는 대화 앞부분이 바뀌면 reasoning item을 버리므로([조사](../research/2026-11-18-openai.md)), message와 function_call의 필드(`id`, `status`, `phase` 등)를 고쳐 보내면 그 뒤의 reasoning이 버려질 수 있다. 내부 메시지 모델은 모든 output item의 원형을 보관해야 한다.
- "output에 message가 있으면 종료"는 종료 조건이 될 수 없다. message와 function_call이 한 응답에 같이 올 수 있는지는 확인하지 못했지만, 막는 규칙도 없다. 종료 판단은 아래 최상위 `status`와 tool 호출 유무로 한다.

#### 응답 최상위 필드

- **종료 상태:** 응답 본문에 Chat Completions의 `finish_reason`은 없다. 대신 최상위 `status`, `error`, `incomplete_details`가 있다. 네 응답 모두 `"completed"`, `null`, `null`이었다.
  - 출력이 잘리면 `status`가 `"completed"`가 아닐 것이다. 이 셋을 보지 않고 "function_call이 없으면 정상 종료"로 판단하면, 잘린 응답을 정상 종료로 잘못 분류한다. 어댑터는 이 셋을 반드시 읽는다.
  - 잘린 응답과 오류 응답의 실제 모양은 아직 보지 못했다(아래 "미확인").
- **응답이 채워 돌려주는 기본값:** 요청에 없던 값이 응답에 찍힌다.
  - `temperature: 1.0`, `top_p: 1.0`. GPT-6.2는 요청에서 이 둘을 빼라고 한다([조사](../research/2026-11-18-openai.md)). 그러니 응답에 찍힌 값을 샘플링 설정으로 기록하면 틀린다. 샘플링 설정은 요청 쪽에서 남긴다.
  - `service_tier: "default"`. 실제로 처리된 tier이고 요청값과 다를 수 있다([조사](../research/2026-11-18-openai.md)). 비용 분석의 기준이 된다.
  - tool 정의에 `strict: true`와 `output_schema: null`이 붙었다. 보낸 요청에는 `strict`가 없었다. 조사에 따르면 Responses는 `strict`를 생략하면 스키마를 strict 모드로 맞춰 보고, 안 되면 non-strict로 넘어간다. Chat Completions는 생략하면 non-strict다. 이번에는 bash tool의 스키마(`additionalProperties: false`, 모든 속성 required)가 strict 조건에 맞아 strict가 됐다.
    - 같은 tool 정의를 Responses와 Chat Completions(C0)에 보낼 때 `strict`를 생략하면 두 wire API의 동작이 조용히 갈라진다. 어댑터가 `strict`를 항상 명시할지는 05의 골격에서 정한다.
- `reasoning.context`와 `reasoning.mode`는 조사에 있던 필드다. gpt-6.2-sol의 기본값이 `"all_turns"`와 `"standard"`라는 것을 이번에 확인했다.
- 조사에 없던 필드: `prompt_cache_retention`(`"24h"`), `access_programs`, `billing`, `image`, `tool_usage`, `completed_at`.

#### usage와 토큰 산술

- 캐시 필드는 `usage.input_tokens_details` 아래에 셋이다. `cached_tokens`, `cache_write_tokens`(숫자), `cache_write_tokens_details`(`ttl_12h_tokens`, `ttl_30m_tokens`)다. 네 응답 모두 0이었다. GPT-5.6 이후 최소 캐시 길이가 1,024토큰인데([조사](../research/2026-11-18-openai.md)), 이번 입력은 최대 964토큰이었다.
- 네 응답 모두 `total_tokens = input_tokens + output_tokens`였다.
- `reasoning_tokens`는 `output_tokens` 안에 이미 들어 있다(`call1`: 595 중 209). 따로 더하면 두 번 센다.
- 이전 호출의 출력은 다음 호출의 입력으로 다시 계산된다. `bash-with-reasoning`의 `call1` 입력과 출력의 합이 911이고, `call2` 입력이 964다. 차이 53토큰은 `function_call_output`과 형식 토큰이다. reasoning 토큰(209)도 다음 입력에 다시 들어간다.
  - 두 호출은 같은 사용자 턴 안의 호출이다. `reasoning.context`가 `current_turn`이어도 같은 턴 안의 reasoning은 이어지므로, 이 숫자는 `all_turns`의 근거가 아니다.
  - 매 호출의 `input_tokens`를 더하면 대화가 길어질수록 누적이 빠르게 커진다. loop의 토큰 상한이 무엇을 셀지(plan.md "설계 메모에서 다룰 것")의 근거로 쓴다.

#### 백엔드 식별 필드

Responses 응답 본문에는 `system_fingerprint` 같은 백엔드 식별 필드가 없다. `model`도 요청한 별칭(`gpt-6.2-sol`) 그대로이고 날짜 스냅샷이 붙지 않는다. plan.md에 반영했다.

#### 응답 헤더와 trace 허용 목록

네 응답의 헤더 이름은 모두 같았다. HTTP/2라 이름은 모두 소문자였다.

trace에 남길 응답 헤더 허용 목록은 아래로 정했다(2026-11-19). 이번 응답에 없던 헤더는 실패 응답이나 특정 조건에서만 붙는다고 [조사](../research/2026-11-18-openai.md)에 나온 헤더다.

| 헤더 | 이번 응답 | trace |
|---|---|---|
| `x-request-id` | `req_...` | 허용 |
| `openai-processing-ms` | 1,975~12,577 | 허용 |
| `openai-version` | `2020-10-01` | 허용 |
| `x-ratelimit-{limit,remaining,reset}-{requests,tokens}` (6종) | 있음 | 허용 |
| `x-ratelimit-{limit,remaining,reset}-project-tokens` (3종) | 없음 | 허용. 프로젝트 단위 토큰 한도가 걸릴 때 붙는다 |
| `retry-after` | 없음 | 허용. 일시적인 429와 503에 붙는다. 재시도를 기록하려면 필요하다 |
| `server-timing-total`, `x-openai-inference-capacity-reason` | 없음 | 허용. `access-control-expose-headers`에만 이름이 나왔다 |
| `openai-organization`, `openai-project` | 계정 식별 값 | 제외(픽스처에서 지움) |
| `set-cookie`, `cf-ray` | Cloudflare 쿠키, 요청 추적 ID | 제외(픽스처에서 지움) |
| 그 밖의 헤더 | | 제외 |

- `openai-processing-ms`는 출력 토큰 수와 함께 커졌다(맨 위 표).
- `openai-project`는 조사 당시 문서의 응답 헤더 목록에 없어 "확인하지 못한 것"으로 남았던 헤더다. 실제로 왔다. 문서에 없는 계정 식별 헤더가 올 수 있으니 trace는 제외 목록이 아니라 허용 목록으로 걸러야 한다.
- `access-control-expose-headers`는 한 응답에 세 번 왔다. trace는 헤더 이름을 대소문자 구분 없이 맞추고, 같은 이름이 여러 번 오면 모두 남긴다.

#### 미확인

이번 픽스처는 모두 사용자 턴 하나, 호출 두 번, HTTP 200, 시스템 프롬프트 없음, 응답마다 function_call 하나다. 아래는 보지 못했다.

- 시스템 프롬프트의 위치. GPT-6.2는 top-level `instructions`를 캐시에 맞아도 캐시되지 않은 단가로 과금한다(plan.md). `input` 맨 앞에 developer 메시지를 넣었을 때의 요청과 응답 모양.
- 오류 응답(400, 429, 5xx)의 본문과 `status`가 `"completed"`가 아닌 응답의 모양. 05의 오류 분류와 재시도의 입력이다.
- 한 응답에 item이 여럿인 경우. function_call 여러 개, message와 function_call이 같이 오는 경우, `arguments`가 유효한 JSON이 아닌 경우.
- 다음 사용자 턴. 최종 message와 그 앞의 reasoning item을 돌려줬을 때도 `input_transformations`가 `[]`인지.
- `message.phase`가 가질 수 있는 값.
