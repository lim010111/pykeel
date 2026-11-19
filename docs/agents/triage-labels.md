# Triage 라벨

스킬은 다섯 가지 triage 역할로 말한다. 이 저장소는 역할 이름을 그대로 라벨로 쓰고, 티켓의 `Status:` 줄에 적는다.

| 스킬의 역할 | 이 저장소의 라벨 | 뜻 |
|---|---|---|
| `needs-triage` | `needs-triage` | 사용자가 검토해야 함 |
| `needs-info` | `needs-info` | 정보를 더 기다림 |
| `ready-for-agent` | `ready-for-agent` | 명세가 끝나 AI 협업자가 혼자 구현할 수 있음 |
| `ready-for-human` | `ready-for-human` | 사용자가 구현해야 함 |
| `wontfix` | `wontfix` | 처리하지 않음 |

## 핵심 모듈 티켓

[AGENTS.md](../../AGENTS.md)의 핵심 모듈 경로를 고치는 티켓의 라벨은 AGENTS.md가 가리키는 로컬 규칙 파일을 따른다. 그 파일이 없으면 `ready-for-human`이다. 주변부만 고치는 티켓은 `ready-for-agent`일 수 있다.

티켓 하나에 핵심 모듈과 주변부가 섞이면 둘로 나눈다. 주변부 티켓은 핵심 모듈의 함수 이름과 시그니처에 기대므로, 그 시그니처를 만드는 핵심 모듈 티켓을 `Blocked by`로 잇는다.
