# 12: trace만으로 replay한다

**What to build:** v0 완료 기준 2다. 11의 실행 trace만으로, API를 호출하지 않고 같은 tool 호출 순서를 재현하는 replay 테스트를 만든다. replay가 정확히 무엇을 비교하는지는 여기서 정한다.

**Blocked by:** 11 확인용 저장소 풀기

**Status:** ready-for-human

- [ ] 11의 trace 하나 이상으로 replay 테스트가 API 호출 없이 통과한다
- [ ] replay가 trace와 다른 tool 호출 순서를 내면 테스트가 실패한다
- [ ] replay에 쓰는 trace가 픽스처로 커밋되고, 비밀값 검사를 통과한다
- [ ] 설계 메모(loop, trace): replay가 정확히 무엇을 비교하는지
