# 03: EXAONE이 tool_calls를 돌려주는지 확인한다

**What to build:** EXAONE 전제를 일찍 확인하는 관문이다. tools를 붙인 Chat Completions 요청을 EXAONE에 curl로 보내 원본을 저장하고, tool_calls가 실제로 오는지, `reasoning_content`를 다음 요청에 어떻게 돌려줘야 하는지 본다. tool_calls가 오지 않으면 E0까지 기다리지 않고 plan.md에서 EXAONE 전제를 다시 연다. 바닥 효과(plan.md 위험 절)도 여기서 처음 엿본다. 무료 구간은 하루 100회이고, 입력과 출력이 기본적으로 모델 학습에 쓰이므로(거부 가능) 보낼 내용에 주의한다. v0의 다른 티켓은 이 결과를 기다리지 않는다.

**Blocked by:** 01 비밀값 검사

**Status:** ready-for-human

- [ ] tools를 붙인 요청과 응답의 원본이 남아 있다
- [ ] tool_calls가 오는지 확인하고, 왔다면 tool 결과를 돌려준 다음 응답까지 받아 본다
- [ ] `reasoning_content`를 다음 요청에 돌려줘야 하는지, 돌려준다면 어떤 모양인지 확인한다
- [ ] 응답에 백엔드 식별 필드(`metadata.weight_version`)가 있는지 확인한다
- [ ] 비밀값을 지운 원본이 픽스처로 커밋되고, 비밀값 검사를 통과한다
- [ ] 결과를 llm 설계 메모의 실제 데이터 절과 plan.md에 남긴다. tool_calls가 오지 않으면 EXAONE 전제를 다시 연다
