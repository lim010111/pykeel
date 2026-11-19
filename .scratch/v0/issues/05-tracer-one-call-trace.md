# 05: 트레이서: 모델 호출 한 번이 trace에 남는다

**What to build:** 루프 없이 llm과 trace만 얇게 잇는 첫 경로다. Responses 어댑터가 요청 하나를 httpx2로 보내고, 응답을 내부 메시지 모델로 읽는다. 그 사이에 일어난 일은 모두 trace에 남는다. 응답 본문을 파싱하기 전에 받은 텍스트 그대로 trace에 넘기는 경계를 여기서 정한다. 02의 픽스처로 네트워크 없이 검증하고, 실제 호출도 한 번 해 본다. 스트리밍과 SSE 파싱은 다루지 않는다(v1). 기록 원칙은 plan.md "원칙 > 기록" 절을 따른다.

**Blocked by:** 02 Responses 실제 응답

**Status:** ready-for-human

- [ ] Responses 요청 하나를 보내고, 응답의 output item(message, function_call, reasoning)을 내부 메시지 모델로 읽는다. reasoning item은 해석하지 않고 받은 그대로 보관한다
- [ ] trace는 덧붙이기만 하는 JSONL이고, 일이 하나 생길 때마다 덧붙이고 flush한다
- [ ] trace에 실행 정보(샘플링 설정, 실행 상한 값, 하네스 커밋과 dirty 여부, 스키마 버전)와 응답에 실제로 찍힌 모델 ID가 남는다
- [ ] 요청 본문 원본과 파싱 전 응답 원문이 남는다. 파싱에 실패한 응답도 남는다
- [ ] 요청 헤더는 남지 않고, 응답 헤더는 허용 목록에 있는 것만 남는다
- [ ] 실패한 시도(HTTP 오류, 타임아웃, 재시도 하나하나)가 각각 남는다
- [ ] 마지막 줄에 하네스가 판단한 종료 이유가 남는다
- [ ] 02의 픽스처로 네트워크 없이 위 항목을 확인하는 동작 테스트가 있다
- [ ] 설계 메모(trace): 필드 이름과 파일 배치, flush와 운영체제 버퍼
- [ ] 설계 메모(llm): 재시도 방침, GPT-6.2 주의점(`instructions` 캐시 과금, reasoning item이 버려지는 조건과 `input_transformations`, `temperature`와 `top_p` 미지원)
- [ ] 두 설계 메모에 예측과 실제 절을 쓴다
