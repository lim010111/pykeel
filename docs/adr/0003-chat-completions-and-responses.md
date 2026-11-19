# Chat Completions와 Responses 두 wire API를 모두 구현한다

지금 실험에 쓰는 EXAONE은 OpenAI 호환 Chat Completions만 지원합니다. 반면 OpenAI는 새 프로젝트와 추론 모델에 Responses를 권합니다. 2026-11 기준으로 GPT-6.x 주력 모델은 tool 호출에 Responses가 필요하고, GPT-5.4 이후 모델은 Chat Completions에서 추론과 tool을 함께 쓸 수 없습니다([조사](../research/2026-11-18-openai.md)). 그래서 두 API를 모두 구현합니다. 지금 실험에서는 GPT를 Responses로, EXAONE을 Chat Completions로 붙입니다.

모델마다 쓰는 API가 달라도 결론에는 영향이 없습니다. 핵심 비교는 같은 모델 안에서 인터페이스만 바꾸는 것이기 때문입니다. 대신 같은 InterfaceSpec은 어느 wire API로 보내든 같은 내용이 전달되도록 옮겨야 합니다. 한쪽 wire API에만 있는 요소(예: Responses 전용 내장 tool)를 어떻게 다룰지는 [plan.md](../plan.md)의 열린 질문입니다.

## Considered Options

- **Chat Completions만:** OpenAI도 아직 지원합니다. 하지만 Responses 전용 모델을 쓸 수 없습니다. reasoning item을 다음 턴에 돌려주는 흐름도 다룰 수 없습니다.
- **Responses만:** EXAONE을 붙일 수 없습니다.

## Consequences

- 내부 메시지 모델이 어느 wire API에도 종속되면 안 됩니다. 내부 메시지 모델 설계는 지금은 임시로 두고, C0(Chat Completions 어댑터) 이후에 별도 ADR로 남깁니다.
- Responses의 대화 상태는 OpenAI 서버에 맡기지 않고 하네스가 관리합니다([ADR-0004](0004-harness-owns-responses-state.md)).
- Anthropic Messages와 Gemini도 나중에 같은 방식으로 붙입니다. 어댑터를 하나씩 추가하는 방식입니다.
