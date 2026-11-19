# Responses의 대화 상태는 OpenAI 서버에 맡기지 않고 하네스가 관리한다

Responses API에서는 이전 응답을 `previous_response_id`로 가리키면 OpenAI 서버가 대화를 이어 붙여 줍니다. 이 하네스는 그 기능을 쓰지 않고 대화 상태를 직접 관리합니다.
- 매 요청에 지금까지의 item을 전부 `input`으로 보냅니다.
- `store: false`로 설정해 대화를 서버에 저장하지 않습니다.
- `store: false`이면 reasoning item에 암호화된 추론 내용(`encrypted_content`)이 기본으로 들어옵니다([조사](../research/2026-11-18-openai.md)). 이 item을 다음 요청에 그대로 돌려줍니다.

이렇게 하는 이유는 두 가지입니다. 첫째, trace의 요청 원본 하나에 그 시점의 대화 전체가 들어 있어야 합니다. 그래야 API를 호출하지 않고 실행을 다시 돌려 볼 수 있고(replay), 그때 모델이 본 인터페이스도 복원할 수 있습니다. 둘째, Chat Completions에는 서버 쪽 상태가 없으므로 두 어댑터가 같은 흐름을 갖게 됩니다.

## Considered Options

- **`previous_response_id`로 서버에 맡기기:** 요청이 작고 클라이언트 코드가 짧습니다. reasoning item을 서버가 직접 이어 주므로, 하네스가 이어 붙이다가 실수할 일도 없습니다. 하지만 요청 원본만으로는 대화를 알 수 없고, 서버 저장 기간이 지나면 다시 돌려 볼 수 없으며, OpenAI에 대화 내용이 남습니다.

## Consequences

- 요청이 대화 길이만큼 커집니다. 앞부분은 프롬프트 캐시로 싸게 과금되므로 부담이 줄어듭니다.
- 이전 item, 특히 reasoning item은 받은 그대로 돌려줘야 합니다. GPT-6.2부터는 대화 앞부분이 바뀌면 reasoning item이 버려지고, 그 사실이 응답의 `input_transformations`에 기록됩니다([조사](../research/2026-11-18-openai.md)).
- 서버 저장을 전제로 하는 Responses 기능은 쓰지 않습니다.
