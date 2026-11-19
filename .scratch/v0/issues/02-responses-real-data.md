# 02: Responses 실제 응답을 받아 픽스처로 남긴다

**What to build:** llm 모듈 사이클 1단계(실제 데이터 보기)다. 이 티켓에서 처음으로 OpenAI API를 호출하므로, 그 전에 pykeel 전용 OpenAI 프로젝트를 만들어 월 hard spend limit을 걸고 그 프로젝트의 키만 쓴다. 그다음 bash function tool을 붙인 Responses 요청으로 왕복 한 번(모델의 function_call → function_call_output을 돌려줌 → 최종 답)을 curl로 받아 원본을 저장한다. 대화 상태는 ADR-0004대로 하네스가 들고 간다(`store: false`, 매 요청에 이전 item 전체). 저장한 원본은 비밀값과 계정 식별 헤더를 지운 뒤 테스트 픽스처로 커밋한다. 05와 09가 이 픽스처로 네트워크 없이 검증한다.

**Blocked by:** 01 비밀값 검사

**Status:** ready-for-human

- [ ] pykeel 전용 OpenAI 프로젝트에 월 hard spend limit이 걸려 있고, 그 프로젝트의 키만 쓴다
- [ ] bash function tool을 붙인 요청과 응답의 원본이 왕복 한 번 전체로 남아 있다(function_call, function_call_output, 최종 답)
- [ ] `store: false`일 때 오는 reasoning item(암호화된 추론 내용 포함)을 다음 요청에 그대로 돌려준 기록이 있다
- [ ] 실제 응답 헤더를 보고 trace 허용 목록(요청 ID, 처리 시간, 속도 제한)에 넣을 헤더 이름을 정한다
- [ ] Responses 응답에 백엔드 식별 필드가 있는지 확인하고, 결과를 plan.md에 반영한다
- [ ] 비밀값과 계정 식별 헤더를 지운 원본이 픽스처로 커밋되고, 비밀값 검사를 통과한다
- [ ] llm 설계 메모에 이번 사이클의 실제 데이터 절을 쓴다
