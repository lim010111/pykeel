# Chat Completions와 Responses 두 wire API를 모두 구현한다

연구 질문의 실험 축인 EXAONE은 OpenAI 호환 Chat Completions만 지원합니다. 반면 OpenAI는 새 프로젝트와 추론 모델에 Responses를 권하고, 일부 모델은 Responses에서만 쓸 수 있습니다. 그래서 두 API를 모두 구현합니다. 실험에서는 GPT를 Responses로, EXAONE을 Chat Completions로 붙입니다.

두 모델이 쓰는 API가 달라도 결론에는 영향이 없습니다. 핵심 비교는 같은 모델 안에서 인터페이스만 바꾸는 것이기 때문입니다. 대신 같은 InterfaceSpec은 두 API 어느 쪽으로 보내든 같은 내용이 전달되도록 옮겨야 합니다.

## Considered Options

- **Chat Completions만:** OpenAI도 아직 지원합니다. 하지만 Responses 전용 모델을 쓸 수 없습니다. reasoning item을 다음 턴에 돌려주는 흐름도 다룰 수 없습니다.
- **Responses만:** EXAONE을 붙일 수 없습니다.

## Consequences

- 내부 메시지 모델이 어느 wire API에도 종속되면 안 됩니다. 내부 메시지 모델 설계는 지금은 임시로 두고, R0 이후에 별도 ADR로 남깁니다.
- Anthropic Messages와 Gemini도 나중에 같은 방식으로 붙입니다. 어댑터를 하나씩 추가하는 방식입니다.
