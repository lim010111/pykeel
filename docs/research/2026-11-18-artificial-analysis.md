# Artificial Analysis 조사: OpenAI 후보 모델과 EXAONE의 가격·성능 (2026-11-18 조회)

> 2026-11-18 서브에이전트가 조사한 보고서다. 처음에는 임시 폴더에 저장했으나 재부팅으로 사라져, 2026-11-19에 대화에 남아 있던 전문으로 다시 만들었다. 다운로드한 원본 페이지와 파싱 스크립트는 복구하지 못했다.

- **조사 범위**: artificialanalysis.ai만 봤다. 출발 페이지는 https://artificialanalysis.ai/leaderboards/providers 이고, 모델 페이지 19개, 방법론 페이지 4개, 평가 페이지 10개를 받았다.
- **값을 읽은 방법**: 페이지는 서버에서 HTML로 렌더링된다.
  - 표와 FAQ 문장은 HTML 텍스트에서 바로 읽었다.
  - 차트 값(개별 벤치마크, cost to run, 출력 속도, capability index)은 같은 HTML에 들어 있는 Next.js 데이터 페이로드에서 읽었다.
  - 같은 변형이 여러 페이지에 나올 때 값을 서로 대조했고, 5,079건이 모두 일치했다.
  - 지수 정수값, 가격, TTFAT, 과제당 시간, 7:2:1 blended는 FAQ 문장과도 일치한다.

## A. 결론 요약

1. 현재 사이트의 종합 지수는 **Intelligence Index v5.0.1**(2026년 11월부터)이다. "Coding Index"와 "Agentic Index"는 사이트에 없고, 대신 Capability Index 6종이 있다. 코딩은 Intelligence Index의 Coding 카테고리(25%)에 들어 있으며, Terminal-Bench 4.0 10%와 FrontierCode-AA 2.0 15%로 이루어진다.
2. 사용자가 알고 있는 값 **"gpt-6-luna 비추론 = 9"는 맞다.** providers 표와 모델 페이지 FAQ 모두 9이고, 원값은 9.44다. 같은 모델의 low 변형은 10(9.67)으로 거의 같다.
3. v5.0.1 지수가 있는 비추론 변형은 GPT-6 Luna(9)와 GPT-6.1 Terra(31) 둘뿐이다. GPT-6 Sol, GPT-5.6 Sol/Terra/Luna, GPT-5.5, GPT-5.4, GPT-5.4 mini, GPT-5.2의 비추론 변형은 지수가 "N/A"이고, 레거시 개별 점수(τ²-Bench, Terminal-Bench Hard, IFBench 등)만 있다.
4. 지수가 있는 추론 변형의 최고값은 GPT-6.2 Astra 62(xhigh·max), GPT-6.2 Sol 57(max), GPT-6 Astra 57, GPT-6.1 Sol 55, GPT-6.1 Terra 51, GPT-6 Sol 44(max만), GPT-5.6 Terra 32(max만), GPT-6 Luna 28, GPT-5.6 Luna 24(max만)이다.
5. 단가가 같아도 effort에 따라 cost to run이 크게 달라진다. GPT-6.2 Sol($2/$10)은 low $224에서 max $1,108까지, GPT-6.2 Astra($8/$40)는 low $794에서 max $4,530까지 간다. GPT-6 Luna는 low($9.09)가 non-reasoning($53.14)보다 싸다.

## B. 모델 × reasoning 변형 표

읽는 법:
- **Intelligence Index**: v5.0.1 값이다. 사이트에 표시되는 정수를 먼저 쓰고, 괄호 안에 페이로드 원값을 적었다. "없음(N/A)"은 사이트가 N/A로 표시하거나 값을 싣지 않은 경우다.
- **Coding Index / Agentic Index**: 사이트에 해당 지수가 없다(C절 참고). 비슷한 성격의 Capability Index는 B-2 표에 따로 정리했다.
- **개별 점수**는 %다(BC만 Elo). ‖ 왼쪽은 v5.0.1 구성 평가, 오른쪽은 지수 밖의 단독·레거시 평가다. "–"는 사이트에 값이 없다는 뜻이다.
  - TB4 = Terminal-Bench 4.0
  - FC2 = FrontierCode-AA 2.0
  - AB = AutomationBench-AA
  - BC = AA-Briefcase v1.1 Elo
  - TBS = Terminal-Bench-Science 0.1
  - τ² = τ²-Bench Telecom (레거시, v4.1 이전 지수 구성)
  - τ³B = τ³-Banking (v4.3부터 단독)
  - TBH = Terminal-Bench Hard (레거시, v4.1 이전 구성)
  - TB2.1 = Terminal-Bench 2.1 (레거시, v4.2까지 구성)
  - IF = IFBench (v4.1부터 단독)
  - EOG = EnterpriseOps-Gym-AA (MCP tool use, 단독)
  - ITB = ITBench-AA (단독)
- **가격**: USD/1M 토큰이며 "입력 / 출력 (캐시 히트)" 순서다.
  - 7:2:1 = 사이트 기본 blended (캐시 히트 : 입력 : 출력)
  - 3:1 = 입력 : 출력 blended. 사이트가 독점 모델의 가격대를 나눌 때 쓰는 비율이며, 페이로드 필드 `price1mBlended0To3To1`에서 읽었다.
  - [median] = 1st-party가 아닌 제공자 중앙값
- **cost to run**: Intelligence Index 전체를 한 번 돌리는 데 든 USD 비용이다(반복 실행 제외). 괄호 안은 Cost per Task로, 지수 가중치를 적용한 과제당 평균이다.
- **속도**: 출력 tok/s, TTFT/TTFAT, 멀티턴 agentic 워크로드 TTFT, 지수 과제당 시간(분). OpenAI 1st-party API 기준이고 최근 5일 평균이다. OpenAI 엔드포인트는 TTFT와 TTFAT가 모두 같게 나온다.
- **† 표시**: 사이트에서 deprecated로 표시된 모델이다. 측정 주기가 6시간이 아니라 18시간이다.
- **출처**: 모델 페이지 URL을 적었다. "; providers"는 같은 변형이 https://artificialanalysis.ai/leaderboards/providers 표에도 있다는 뜻이고, 그 표의 값과 일치한다.

| 모델 (API id / AA 표기) | 변형 | Intelligence Index v5.0.1 | Coding Index | Agentic Index | tool·에이전트 관련 개별 점수 | 입력/출력/blended 가격 | cost to run (과제당) | 속도 | 출처 |
|---|---|---|---|---|---|---|---|---|---|
| **Chat Completions에서 function tool 사용 시 reasoning_effort="none" 필요(OpenAI 문서)** | | | | | | | | | |
| gpt-6-luna (GPT-6 Luna) | Non-reasoning | 9 (9.44) | 없음 | 없음 | TB4 1.5 · FC2 1.6 · AB 9.1 · BC 903 · TBS 1.0 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $0.100 / $0.500 (캐시히트 $0.010) · 7:2:1 $0.077 · 3:1 $0.200 | $53.14 (과제당 $0.071) | 91 tok/s · TTFT=TTFAT 1.51s · 멀티턴 TTFT 1.04s · 과제당 1.8분 | https://artificialanalysis.ai/models/gpt-6-luna ; providers |
| gpt-6-luna (GPT-6 Luna) | Low | 10 (9.67) | 없음 | 없음 | TB4 0.0 · FC2 2.2 · AB 12.0 · BC 740 · TBS 1.0 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $0.100 / $0.500 (캐시히트 $0.010) · 7:2:1 $0.077 · 3:1 $0.200 | $9.09 (과제당 $0.0051) | 88 tok/s · TTFT=TTFAT 2.49s · 멀티턴 TTFT 1.65s · 과제당 0.6분 | https://artificialanalysis.ai/models/gpt-6-luna ; providers |
| gpt-6-luna (GPT-6 Luna) | Medium | 18 (18.45) | 없음 | 없음 | TB4 2.5 · FC2 12.8 · AB 40.5 · BC 1096 · TBS 1.4 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $0.100 / $0.500 (캐시히트 $0.010) · 7:2:1 $0.077 · 3:1 $0.200 | $39.55 (과제당 $0.042) | 95 tok/s · TTFT=TTFAT 5.28s · 멀티턴 TTFT 3.14s · 과제당 3.5분 | https://artificialanalysis.ai/models/gpt-6-luna ; providers |
| gpt-6-luna (GPT-6 Luna) | High | 21 (21.43) | 없음 | 없음 | TB4 4.5 · FC2 18.6 · AB 47.8 · BC 1187 · TBS 2.9 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $0.100 / $0.500 (캐시히트 $0.010) · 7:2:1 $0.077 · 3:1 $0.200 | $62.58 (과제당 $0.073) | 94 tok/s · TTFT=TTFAT 10.33s · 멀티턴 TTFT 6.05s · 과제당 5.8분 | https://artificialanalysis.ai/models/gpt-6-luna ; providers |
| gpt-6-luna (GPT-6 Luna) | Xhigh | 23 (23.45) | 없음 | 없음 | TB4 8.1 · FC2 18.4 · AB 47.8 · BC 1235 · TBS 5.2 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $0.100 / $0.500 (캐시히트 $0.010) · 7:2:1 $0.077 · 3:1 $0.200 | $85.74 (과제당 $0.104) | 100 tok/s · TTFT=TTFAT 15.64s · 멀티턴 TTFT 8.14s · 과제당 7.3분 | https://artificialanalysis.ai/models/gpt-6-luna ; providers |
| gpt-6-luna (GPT-6 Luna) | Max | 28 (27.86) | 없음 | 없음 | TB4 12.6 · FC2 25.2 · AB 53.2 · BC 1336 · TBS 8.6 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $0.100 / $0.500 (캐시히트 $0.010) · 7:2:1 $0.077 · 3:1 $0.200 | $136.06 (과제당 $0.152) | 103 tok/s · TTFT=TTFAT 67.60s · 멀티턴 TTFT 24.88s · 과제당 12.1분 | https://artificialanalysis.ai/models/gpt-6-luna ; providers |
| gpt-6-sol (GPT-6 Sol) † | Non-reasoning | 없음(N/A) | 없음 | 없음 | TB4 13.1 · FC2 – · AB 34.2 · BC 1106 · TBS 5.7 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $2.00 / $10.00 (캐시히트 $0.200) · 7:2:1 $1.54 · 3:1 $4.00 | 없음 | 101 tok/s · TTFT=TTFAT 1.54s · 멀티턴 TTFT 1.08s | https://artificialanalysis.ai/models/gpt-6-sol |
| gpt-6-sol (GPT-6 Sol) † | Low | 없음(N/A) | 없음 | 없음 | TB4 9.1 · FC2 – · AB 53.9 · BC 886 · TBS 3.3 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $2.00 / $10.00 (캐시히트 $0.200) · 7:2:1 $1.54 · 3:1 $4.00 | 없음 | 94 tok/s · TTFT=TTFAT 2.07s · 멀티턴 TTFT 1.59s | https://artificialanalysis.ai/models/gpt-6-sol |
| gpt-6-sol (GPT-6 Sol) † | Medium | 없음(N/A) | 없음 | 없음 | TB4 18.7 · FC2 – · AB 58.0 · BC 1149 · TBS 8.6 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $2.00 / $10.00 (캐시히트 $0.200) · 7:2:1 $1.54 · 3:1 $4.00 | 없음 | 없음 | https://artificialanalysis.ai/models/gpt-6-sol |
| gpt-6-sol (GPT-6 Sol) † | High | 없음(N/A) | 없음 | 없음 | TB4 26.3 · FC2 – · AB 60.1 · BC 1266 · TBS 17.1 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $2.00 / $10.00 (캐시히트 $0.200) · 7:2:1 $1.54 · 3:1 $4.00 | 없음 | 103 tok/s · TTFT=TTFAT 5.80s · 멀티턴 TTFT 2.79s | https://artificialanalysis.ai/models/gpt-6-sol |
| gpt-6-sol (GPT-6 Sol) † | Xhigh | 없음(N/A) | 없음 | 없음 | TB4 30.3 · FC2 – · AB 61.7 · BC 1359 · TBS 17.6 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $2.00 / $10.00 (캐시히트 $0.200) · 7:2:1 $1.54 · 3:1 $4.00 | 없음 | 103 tok/s · TTFT=TTFAT 14.19s · 멀티턴 TTFT 3.65s | https://artificialanalysis.ai/models/gpt-6-sol |
| gpt-6-sol (GPT-6 Sol) † | Max | 44 (44.16) | 없음 | 없음 | TB4 43.9 · FC2 35.6 · AB 61.6 · BC 1476 · TBS 30.0 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB 49.4 | $2.00 / $10.00 (캐시히트 $0.200) · 7:2:1 $1.54 · 3:1 $4.00 | $1,930.40 (과제당 $2.47) | 117 tok/s · TTFT=TTFAT 36.52s · 멀티턴 TTFT 6.53s · 과제당 7.7분 | https://artificialanalysis.ai/models/gpt-6-sol |
| gpt-5.6-sol (GPT-5.6 Sol) † | Non-reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB 22.7 · BC 1006 · TBS – ‖ τ² – · τ³B 19.6 · TBH – · TB2.1 74.2 · IF – · EOG – · ITB – | $4.00 / $20.00 (캐시히트 $0.400) · 7:2:1 $3.08 · 3:1 $8.00 | 없음 | 91 tok/s · TTFT=TTFAT 2.10s · 멀티턴 TTFT 1.63s | https://artificialanalysis.ai/models/gpt-5-6-sol |
| gpt-5.6-sol (GPT-5.6 Sol) † | Low | 없음(N/A) | 없음 | 없음 | TB4 1.0 · FC2 – · AB 41.0 · BC 1043 · TBS – ‖ τ² 76.0 · τ³B 29.1 · TBH 60.6 · TB2.1 76.8 · IF 66.5 · EOG – · ITB – | $4.00 / $20.00 (캐시히트 $0.400) · 7:2:1 $3.08 · 3:1 $8.00 | 없음 | 89 tok/s · TTFT=TTFAT 3.81s · 멀티턴 TTFT 4.06s | https://artificialanalysis.ai/models/gpt-5-6-sol |
| gpt-5.6-sol (GPT-5.6 Sol) † | Medium | 없음(N/A) | 없음 | 없음 | TB4 14.6 · FC2 – · AB 51.3 · BC 1240 · TBS – ‖ τ² 81.0 · τ³B 36.5 · TBH 62.9 · TB2.1 86.1 · IF 69.6 · EOG – · ITB – | $4.00 / $20.00 (캐시히트 $0.400) · 7:2:1 $3.08 · 3:1 $8.00 | 없음 | 95 tok/s · TTFT=TTFAT 5.59s · 멀티턴 TTFT 3.76s | https://artificialanalysis.ai/models/gpt-5-6-sol |
| gpt-5.6-sol (GPT-5.6 Sol) † | High | 없음(N/A) | 없음 | 없음 | TB4 20.7 · FC2 – · AB 55.3 · BC 1369 · TBS – ‖ τ² 83.3 · τ³B 36.7 · TBH 62.1 · TB2.1 87.3 · IF 69.2 · EOG – · ITB – | $4.00 / $20.00 (캐시히트 $0.400) · 7:2:1 $3.08 · 3:1 $8.00 | 없음 | 94 tok/s · TTFT=TTFAT 9.41s · 멀티턴 TTFT 5.22s | https://artificialanalysis.ai/models/gpt-5-6-sol |
| gpt-5.6-sol (GPT-5.6 Sol) † | Xhigh | 없음(N/A) | 없음 | 없음 | TB4 24.7 · FC2 – · AB 55.3 · BC 1436 · TBS – ‖ τ² 84.8 · τ³B 38.1 · TBH 61.4 · TB2.1 89.5 · IF 71.0 · EOG – · ITB – | $4.00 / $20.00 (캐시히트 $0.400) · 7:2:1 $3.08 · 3:1 $8.00 | 없음 | 105 tok/s · TTFT=TTFAT 15.29s · 멀티턴 TTFT 6.77s | https://artificialanalysis.ai/models/gpt-5-6-sol |
| gpt-5.6-sol (GPT-5.6 Sol) † | Max | 없음(N/A) | 없음 | 없음 | TB4 39.9 · FC2 – · AB 60.1 · BC 1479 · TBS 22.4 ‖ τ² 85.1 · τ³B 44.3 · TBH 65.9 · TB2.1 88.0 · IF 72.7 · EOG 42.9 · ITB 56.2 | $4.00 / $20.00 (캐시히트 $0.400) · 7:2:1 $3.08 · 3:1 $8.00 | 없음 | 98 tok/s · TTFT=TTFAT 35.52s · 멀티턴 TTFT 9.69s | https://artificialanalysis.ai/models/gpt-5-6-sol |
| gpt-5.6-terra (GPT-5.6 Terra) † | Non-reasoning | 없음(N/A) | 없음 | 없음 | TB4 0.5 · FC2 – · AB 12.5 · BC 946 · TBS – ‖ τ² – · τ³B 15.7 · TBH – · TB2.1 56.2 · IF – · EOG – · ITB – | $2.00 / $12.00 (캐시히트 $0.200) · 7:2:1 $1.74 · 3:1 $4.50 | 없음 | 83 tok/s · TTFT=TTFAT 1.66s · 멀티턴 TTFT 1.46s | https://artificialanalysis.ai/models/gpt-5-6-terra |
| gpt-5.6-terra (GPT-5.6 Terra) † | Low | 없음(N/A) | 없음 | 없음 | TB4 1.5 · FC2 – · AB 29.1 · BC 1014 · TBS – ‖ τ² 60.5 · τ³B 18.8 · TBH 43.9 · TB2.1 62.5 · IF 59.7 · EOG – · ITB – | $2.00 / $12.00 (캐시히트 $0.200) · 7:2:1 $1.74 · 3:1 $4.50 | 없음 | 80 tok/s · TTFT=TTFAT 2.61s · 멀티턴 TTFT 2.48s | https://artificialanalysis.ai/models/gpt-5-6-terra |
| gpt-5.6-terra (GPT-5.6 Terra) † | Medium | 없음(N/A) | 없음 | 없음 | TB4 1.0 · FC2 – · AB 33.5 · BC 1039 · TBS – ‖ τ² 72.8 · τ³B 25.6 · TBH – · TB2.1 72.3 · IF 62.2 · EOG – · ITB – | $2.00 / $12.00 (캐시히트 $0.200) · 7:2:1 $1.74 · 3:1 $4.50 | 없음 | 87 tok/s · TTFT=TTFAT 3.00s · 멀티턴 TTFT 3.29s | https://artificialanalysis.ai/models/gpt-5-6-terra |
| gpt-5.6-terra (GPT-5.6 Terra) † | High | 없음(N/A) | 없음 | 없음 | TB4 1.5 · FC2 – · AB 42.0 · BC 1202 · TBS – ‖ τ² 78.4 · τ³B 28.7 · TBH 57.6 · TB2.1 75.7 · IF 64.4 · EOG – · ITB – | $2.00 / $12.00 (캐시히트 $0.200) · 7:2:1 $1.74 · 3:1 $4.50 | 없음 | 88 tok/s · TTFT=TTFAT 6.25s · 멀티턴 TTFT 5.30s | https://artificialanalysis.ai/models/gpt-5-6-terra |
| gpt-5.6-terra (GPT-5.6 Terra) † | Xhigh | 없음(N/A) | 없음 | 없음 | TB4 10.1 · FC2 – · AB 47.1 · BC 1332 · TBS – ‖ τ² 80.4 · τ³B 29.7 · TBH 62.9 · TB2.1 80.1 · IF 66.3 · EOG – · ITB – | $2.00 / $12.00 (캐시히트 $0.200) · 7:2:1 $1.74 · 3:1 $4.50 | 없음 | 87 tok/s · TTFT=TTFAT 16.19s · 멀티턴 TTFT 4.93s | https://artificialanalysis.ai/models/gpt-5-6-terra |
| gpt-5.6-terra (GPT-5.6 Terra) † | Max | 32 (32.34) | 없음 | 없음 | TB4 35.4 · FC2 23.9 · AB 59.6 · BC 1333 · TBS 13.8 ‖ τ² 86.3 · τ³B 40.2 · TBH 57.6 · TB2.1 88.0 · IF 71.2 · EOG 38.5 · ITB 51.0 | $2.00 / $12.00 (캐시히트 $0.200) · 7:2:1 $1.74 · 3:1 $4.50 | $3,250.14 (과제당 $3.73) | 89 tok/s · TTFT=TTFAT 64.08s · 멀티턴 TTFT 13.29s · 과제당 12.4분 | https://artificialanalysis.ai/models/gpt-5-6-terra |
| gpt-5.6-luna (GPT-5.6 Luna) † | Non-reasoning | 없음(N/A) | 없음 | 없음 | TB4 1.0 · FC2 – · AB 5.0 · BC 707 · TBS – ‖ τ² – · τ³B 9.7 · TBH – · TB2.1 39.0 · IF – · EOG – · ITB – | $0.200 / $1.20 (캐시히트 $0.020) · 7:2:1 $0.174 · 3:1 $0.450 | 없음 | 90 tok/s · TTFT=TTFAT 1.47s · 멀티턴 TTFT 1.10s | https://artificialanalysis.ai/models/gpt-5-6-luna |
| gpt-5.6-luna (GPT-5.6 Luna) † | Low | 없음(N/A) | 없음 | 없음 | TB4 0.0 · FC2 – · AB 11.7 · BC 740 · TBS – ‖ τ² – · τ³B 12.8 · TBH – · TB2.1 43.4 · IF – · EOG – · ITB – | $0.200 / $1.20 (캐시히트 $0.020) · 7:2:1 $0.174 · 3:1 $0.450 | 없음 | 95 tok/s · TTFT=TTFAT 2.02s · 멀티턴 TTFT 1.46s | https://artificialanalysis.ai/models/gpt-5-6-luna |
| gpt-5.6-luna (GPT-5.6 Luna) † | Medium | 없음(N/A) | 없음 | 없음 | TB4 0.5 · FC2 – · AB 23.1 · BC 933 · TBS – ‖ τ² – · τ³B 17.7 · TBH – · TB2.1 53.2 · IF – · EOG – · ITB – | $0.200 / $1.20 (캐시히트 $0.020) · 7:2:1 $0.174 · 3:1 $0.450 | 없음 | 96 tok/s · TTFT=TTFAT 2.68s · 멀티턴 TTFT 1.52s | https://artificialanalysis.ai/models/gpt-5-6-luna |
| gpt-5.6-luna (GPT-5.6 Luna) † | High | 없음(N/A) | 없음 | 없음 | TB4 2.5 · FC2 – · AB 35.6 · BC 1169 · TBS – ‖ τ² – · τ³B 25.2 · TBH – · TB2.1 69.7 · IF – · EOG – · ITB – | $0.200 / $1.20 (캐시히트 $0.020) · 7:2:1 $0.174 · 3:1 $0.450 | 없음 | 97 tok/s · TTFT=TTFAT 8.22s · 멀티턴 TTFT 2.99s | https://artificialanalysis.ai/models/gpt-5-6-luna |
| gpt-5.6-luna (GPT-5.6 Luna) † | Xhigh | 없음(N/A) | 없음 | 없음 | TB4 3.5 · FC2 – · AB 42.6 · BC 1267 · TBS – ‖ τ² – · τ³B 28.7 · TBH – · TB2.1 77.9 · IF – · EOG – · ITB – | $0.200 / $1.20 (캐시히트 $0.020) · 7:2:1 $0.174 · 3:1 $0.450 | 없음 | 104 tok/s · TTFT=TTFAT 20.58s · 멀티턴 TTFT 3.00s | https://artificialanalysis.ai/models/gpt-5-6-luna |
| gpt-5.6-luna (GPT-5.6 Luna) † | Max | 24 (23.79) | 없음 | 없음 | TB4 11.6 · FC2 17.6 · AB 50.2 · BC 1339 · TBS 3.3 ‖ τ² – · τ³B 31.1 · TBH – · TB2.1 80.9 · IF – · EOG 40.8 · ITB 40.3 | $0.200 / $1.20 (캐시히트 $0.020) · 7:2:1 $0.174 · 3:1 $0.450 | $334.35 (과제당 $0.331) | 99 tok/s · TTFT=TTFAT 43.99s · 멀티턴 TTFT 6.23s · 과제당 10.0분 | https://artificialanalysis.ai/models/gpt-5-6-luna |
| gpt-5.5 (GPT-5.5) † | Non-reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 69.3 · τ³B 14.8 · TBH 49.2 · TB2.1 61.0 · IF 46.1 · EOG – · ITB – | $5.00 / $30.00 (캐시히트 $0.500) · 7:2:1 $4.35 · 3:1 $11.25 | 없음 | 75 tok/s · TTFT=TTFAT 1.72s · 멀티턴 TTFT 1.29s | https://artificialanalysis.ai/models/gpt-5-5 |
| gpt-5.5 (GPT-5.5) † | Low | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 83.9 · τ³B 24.9 · TBH 52.3 · TB2.1 65.5 · IF 64.4 · EOG – · ITB – | $5.00 / $30.00 (캐시히트 $0.500) · 7:2:1 $4.35 · 3:1 $11.25 | 없음 | 71 tok/s · TTFT=TTFAT 2.03s · 멀티턴 TTFT 1.42s | https://artificialanalysis.ai/models/gpt-5-5 |
| gpt-5.5 (GPT-5.5) † | Medium | 없음(N/A) | 없음 | 없음 | TB4 5.1 · FC2 – · AB 40.1 · BC 1000 · TBS – ‖ τ² 91.8 · τ³B 29.9 · TBH 57.6 · TB2.1 80.5 · IF 71.0 · EOG 44.1 · ITB – | $5.00 / $30.00 (캐시히트 $0.500) · 7:2:1 $4.35 · 3:1 $11.25 | 없음 | 77 tok/s · TTFT=TTFAT 5.31s · 멀티턴 TTFT 3.44s | https://artificialanalysis.ai/models/gpt-5-5 |
| gpt-5.5 (GPT-5.5) † | High | 없음(N/A) | 없음 | 없음 | TB4 9.1 · FC2 – · AB 44.3 · BC 1087 · TBS – ‖ τ² 93.0 · τ³B 36.7 · TBH 59.8 · TB2.1 79.4 · IF 71.6 · EOG – · ITB – | $5.00 / $30.00 (캐시히트 $0.500) · 7:2:1 $4.35 · 3:1 $11.25 | 없음 | 72 tok/s · TTFT=TTFAT 13.84s · 멀티턴 TTFT 5.34s | https://artificialanalysis.ai/models/gpt-5-5 |
| gpt-5.5 (GPT-5.5) † | Xhigh | 없음(N/A) | 없음 | 없음 | TB4 14.6 · FC2 – · AB 47.3 · BC 1135 · TBS – ‖ τ² 93.9 · τ³B 39.0 · TBH 60.6 · TB2.1 84.3 · IF 75.9 · EOG 46.6 · ITB 45.8 | $5.00 / $30.00 (캐시히트 $0.500) · 7:2:1 $4.35 · 3:1 $11.25 | 없음 | 88 tok/s · TTFT=TTFAT 39.29s · 멀티턴 TTFT 28.05s | https://artificialanalysis.ai/models/gpt-5-5 |
| gpt-5.4 (GPT-5.4) † | Non-reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 36.0 · τ³B – · TBH 37.9 · TB2.1 – · IF 48.4 · EOG – · ITB – | $2.50 / $15.00 (캐시히트 $0.250) · 7:2:1 $2.17 · 3:1 $5.62 | 없음 | 52 tok/s · TTFT=TTFAT 1.69s · 멀티턴 TTFT 1.19s | https://artificialanalysis.ai/models/gpt-5-4 |
| gpt-5.4 (GPT-5.4) † | Low | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 74.6 · τ³B – · TBH 43.2 · TB2.1 – · IF 65.9 · EOG – · ITB – | $2.50 / $15.00 (캐시히트 $0.250) · 7:2:1 $2.17 · 3:1 $5.62 | 없음 | 64 tok/s · TTFT=TTFAT 3.26s · 멀티턴 TTFT 2.97s | https://artificialanalysis.ai/models/gpt-5-4 |
| gpt-5.4 (GPT-5.4) † | Xhigh | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 87.1 · τ³B 39.6 · TBH 57.6 · TB2.1 78.3 · IF 73.9 · EOG – · ITB – | $2.50 / $15.00 (캐시히트 $0.250) · 7:2:1 $2.17 · 3:1 $5.62 | 없음 | 70 tok/s · TTFT=TTFAT 98.95s · 멀티턴 TTFT 57.17s | https://artificialanalysis.ai/models/gpt-5-4 |
| gpt-5.4-mini (GPT-5.4 mini) † | Non-reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 23.4 · τ³B – · TBH 18.2 · TB2.1 – · IF 38.8 · EOG – · ITB 18.6 | $0.750 / $4.50 (캐시히트 $0.075) · 7:2:1 $0.653 · 3:1 $1.69 | 없음 | 116 tok/s · TTFT=TTFAT 1.42s · 멀티턴 TTFT 0.85s | https://artificialanalysis.ai/models/gpt-5-4-mini |
| gpt-5.4-mini (GPT-5.4 mini) † | Medium | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 36.5 · τ³B – · TBH 34.1 · TB2.1 – · IF 64.8 · EOG – · ITB – | $0.750 / $4.50 (캐시히트 $0.075) · 7:2:1 $0.653 · 3:1 $1.69 | 없음 | 150 tok/s · TTFT=TTFAT 4.88s · 멀티턴 TTFT 2.52s | https://artificialanalysis.ai/models/gpt-5-4-mini |
| gpt-5.4-mini (GPT-5.4 mini) † | Xhigh | 없음(N/A) | 없음 | 없음 | TB4 2.0 · FC2 – · AB 26.2 · BC 720 · TBS – ‖ τ² 83.3 · τ³B 25.6 · TBH 52.3 · TB2.1 59.2 · IF 73.3 · EOG 34.6 · ITB 35.2 | $0.750 / $4.50 (캐시히트 $0.075) · 7:2:1 $0.653 · 3:1 $1.69 | 없음 | 186 tok/s · TTFT=TTFAT 120.19s · 멀티턴 TTFT 11.75s | https://artificialanalysis.ai/models/gpt-5-4-mini |
| **tool 호출에 Responses API 필요(OpenAI 문서)** | | | | | | | | | |
| gpt-6.2-astra (GPT-6.2 Astra) | Low | 46 (45.65) | 없음 | 없음 | TB4 51.0 · FC2 32.7 · AB 68.6 · BC 1039 · TBS 51.0 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG 21.8 · ITB – | $8.00 / $40.00 (캐시히트 $0.400) · 7:2:1 $5.88 · 3:1 $16.00 | $794.01 (과제당 $0.662) | 53 tok/s · TTFT=TTFAT 2.82s · 멀티턴 TTFT 2.64s · 과제당 1.6분 | https://artificialanalysis.ai/models/gpt-6-2-astra ; providers |
| gpt-6.2-astra (GPT-6.2 Astra) | Medium | 57 (57.00) | 없음 | 없음 | TB4 58.6 · FC2 46.6 · AB 72.8 · BC 1408 · TBS 74.8 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG 22.6 · ITB – | $8.00 / $40.00 (캐시히트 $0.400) · 7:2:1 $5.88 · 3:1 $16.00 | $1,456.80 (과제당 $1.62) | 53 tok/s · TTFT=TTFAT 3.21s · 멀티턴 TTFT 2.93s · 과제당 4.2분 | https://artificialanalysis.ai/models/gpt-6-2-astra ; providers |
| gpt-6.2-astra (GPT-6.2 Astra) | High | 60 (60.09) | 없음 | 없음 | TB4 60.1 · FC2 47.1 · AB 76.0 · BC 1570 · TBS 75.2 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG 25.2 · ITB – | $8.00 / $40.00 (캐시히트 $0.400) · 7:2:1 $5.88 · 3:1 $16.00 | $2,006.78 (과제당 $2.07) | 56 tok/s · TTFT=TTFAT 22.07s · 멀티턴 TTFT 4.95s · 과제당 5.3분 | https://artificialanalysis.ai/models/gpt-6-2-astra ; providers |
| gpt-6.2-astra (GPT-6.2 Astra) | Xhigh | 62 (61.56) | 없음 | 없음 | TB4 64.1 · FC2 49.0 · AB 76.1 · BC 1594 · TBS 78.6 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG 25.3 · ITB – | $8.00 / $40.00 (캐시히트 $0.400) · 7:2:1 $5.88 · 3:1 $16.00 | $2,483.62 (과제당 $2.52) | 54 tok/s · TTFT=TTFAT 52.89s · 멀티턴 TTFT 6.31s · 과제당 6.8분 | https://artificialanalysis.ai/models/gpt-6-2-astra ; providers |
| gpt-6.2-astra (GPT-6.2 Astra) | Max | 62 (62.14) | 없음 | 없음 | TB4 64.1 · FC2 45.4 · AB 77.2 · BC 1644 · TBS 78.1 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG 29.9 · ITB – | $8.00 / $40.00 (캐시히트 $0.400) · 7:2:1 $5.88 · 3:1 $16.00 | $4,530.46 (과제당 $4.00) | 53 tok/s · TTFT=TTFAT 170.99s · 멀티턴 TTFT 11.70s · 과제당 12.9분 | https://artificialanalysis.ai/models/gpt-6-2-astra ; providers |
| gpt-6.2-sol (GPT-6.2 Sol) | Low | 41 (40.55) | 없음 | 없음 | TB4 37.9 · FC2 31.4 · AB 63.2 · BC 1230 · TBS 37.1 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG 19.9 · ITB – | $2.00 / $10.00 (캐시히트 $0.100) · 7:2:1 $1.47 · 3:1 $4.00 | $224.22 (과제당 $0.184) | 70 tok/s · TTFT=TTFAT 2.03s · 멀티턴 TTFT 1.97s · 과제당 1.4분 | https://artificialanalysis.ai/models/gpt-6-2-sol ; providers |
| gpt-6.2-sol (GPT-6.2 Sol) | Medium | 53 (52.68) | 없음 | 없음 | TB4 56.1 · FC2 41.4 · AB 70.3 · BC 1495 · TBS 60.5 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG 21.4 · ITB – | $2.00 / $10.00 (캐시히트 $0.100) · 7:2:1 $1.47 · 3:1 $4.00 | $405.17 (과제당 $0.406) | 73 tok/s · TTFT=TTFAT 3.03s · 멀티턴 TTFT 2.21s · 과제당 3.1분 | https://artificialanalysis.ai/models/gpt-6-2-sol ; providers |
| gpt-6.2-sol (GPT-6.2 Sol) | High | 55 (54.89) | 없음 | 없음 | TB4 58.6 · FC2 40.2 · AB 69.9 · BC 1541 · TBS 67.6 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG 23.4 · ITB – | $2.00 / $10.00 (캐시히트 $0.100) · 7:2:1 $1.47 · 3:1 $4.00 | $552.68 (과제당 $0.564) | 78 tok/s · TTFT=TTFAT 9.63s · 멀티턴 TTFT 4.23s · 과제당 4.3분 | https://artificialanalysis.ai/models/gpt-6-2-sol ; providers |
| gpt-6.2-sol (GPT-6.2 Sol) | Xhigh | 56 (55.74) | 없음 | 없음 | TB4 56.1 · FC2 42.8 · AB 70.6 · BC 1580 · TBS 66.7 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG 26.3 · ITB – | $2.00 / $10.00 (캐시히트 $0.100) · 7:2:1 $1.47 · 3:1 $4.00 | $698.10 (과제당 $0.648) | 81 tok/s · TTFT=TTFAT 26.63s · 멀티턴 TTFT 5.25s · 과제당 5.0분 | https://artificialanalysis.ai/models/gpt-6-2-sol ; providers |
| gpt-6.2-sol (GPT-6.2 Sol) | Max | 57 (57.26) | 없음 | 없음 | TB4 60.1 · FC2 44.4 · AB 71.3 · BC 1612 · TBS 67.6 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG 28.9 · ITB – | $2.00 / $10.00 (캐시히트 $0.100) · 7:2:1 $1.47 · 3:1 $4.00 | $1,108.28 (과제당 $1.01) | 85 tok/s · TTFT=TTFAT 66.70s · 멀티턴 TTFT 10.75s · 과제당 8.0분 | https://artificialanalysis.ai/models/gpt-6-2-sol ; providers |
| gpt-6.1-terra (GPT-6.1 Terra) | Non-reasoning | 31 (30.52) | 없음 | 없음 | TB4 26.8 · FC2 33.4 · AB 51.0 · BC 1226 · TBS 24.3 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $1.00 / $5.00 (캐시히트 $0.050) · 7:2:1 $0.735 · 3:1 $2.00 | $213.33 (과제당 $0.226) | 63 tok/s · TTFT=TTFAT 2.61s · 멀티턴 TTFT 2.89s · 과제당 2.5분 | https://artificialanalysis.ai/models/gpt-6-1-terra ; providers |
| gpt-6.1-terra (GPT-6.1 Terra) | Low | 29 (29.42) | 없음 | 없음 | TB4 15.2 · FC2 24.5 · AB 56.2 · BC 1032 · TBS 7.6 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $1.00 / $5.00 (캐시히트 $0.050) · 7:2:1 $0.735 · 3:1 $2.00 | $111.16 (과제당 $0.071) | 60 tok/s · TTFT=TTFAT 2.97s · 멀티턴 TTFT 2.87s · 과제당 1.2분 | https://artificialanalysis.ai/models/gpt-6-1-terra ; providers |
| gpt-6.1-terra (GPT-6.1 Terra) | Medium | 38 (38.17) | 없음 | 없음 | TB4 32.3 · FC2 34.5 · AB 57.8 · BC 1191 · TBS 24.8 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $1.00 / $5.00 (캐시히트 $0.050) · 7:2:1 $0.735 · 3:1 $2.00 | $190.36 (과제당 $0.169) | 63 tok/s · TTFT=TTFAT 4.64s · 멀티턴 TTFT 4.29s · 과제당 2.9분 | https://artificialanalysis.ai/models/gpt-6-1-terra ; providers |
| gpt-6.1-terra (GPT-6.1 Terra) | High | 42 (42.43) | 없음 | 없음 | TB4 41.9 · FC2 37.5 · AB 58.5 · BC 1265 · TBS 33.3 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $1.00 / $5.00 (캐시히트 $0.050) · 7:2:1 $0.735 · 3:1 $2.00 | $266.79 (과제당 $0.259) | 65 tok/s · TTFT=TTFAT 10.50s · 멀티턴 TTFT 5.26s · 과제당 4.3분 | https://artificialanalysis.ai/models/gpt-6-1-terra ; providers |
| gpt-6.1-terra (GPT-6.1 Terra) | Xhigh | 45 (45.25) | 없음 | 없음 | TB4 46.5 · FC2 36.9 · AB 59.9 · BC 1334 · TBS 41.9 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $1.00 / $5.00 (캐시히트 $0.050) · 7:2:1 $0.735 · 3:1 $2.00 | $400.18 (과제당 $0.401) | 65 tok/s · TTFT=TTFAT 30.33s · 멀티턴 TTFT 7.27s · 과제당 6.7분 | https://artificialanalysis.ai/models/gpt-6-1-terra ; providers |
| gpt-6.1-terra (GPT-6.1 Terra) | Max | 51 (51.33) | 없음 | 없음 | TB4 55.6 · FC2 42.3 · AB 60.2 · BC 1399 · TBS 57.6 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $1.00 / $5.00 (캐시히트 $0.050) · 7:2:1 $0.735 · 3:1 $2.00 | $972.34 (과제당 $0.961) | 69 tok/s · TTFT=TTFAT 146.49s · 멀티턴 TTFT 18.93s · 과제당 14.5분 | https://artificialanalysis.ai/models/gpt-6-1-terra ; providers |
| gpt-6-astra (GPT-6 Astra) † | Low | 43 (43.33) | 없음 | 없음 | TB4 41.9 · FC2 26.2 · AB 59.1 · BC 1256 · TBS 37.1 ‖ τ² – · τ³B 32.0 · TBH – · TB2.1 88.0 · IF – · EOG – · ITB – | $10.00 / $50.00 (캐시히트 $1.00) · 7:2:1 $7.70 · 3:1 $20.00 | $1,650.75 (과제당 $1.42) | 46 tok/s · TTFT=TTFAT 3.38s · 멀티턴 TTFT 2.77s · 과제당 3.3분 | https://artificialanalysis.ai/models/gpt-6-astra |
| gpt-6-astra (GPT-6 Astra) † | Medium | 52 (51.55) | 없음 | 없음 | TB4 49.5 · FC2 36.6 · AB 64.6 · BC 1462 · TBS 53.3 ‖ τ² – · τ³B 35.5 · TBH – · TB2.1 89.5 · IF – · EOG – · ITB – | $10.00 / $50.00 (캐시히트 $1.00) · 7:2:1 $7.70 · 3:1 $20.00 | $2,638.29 (과제당 $2.73) | 46 tok/s · TTFT=TTFAT 5.96s · 멀티턴 TTFT 4.23s · 과제당 6.5분 | https://artificialanalysis.ai/models/gpt-6-astra |
| gpt-6-astra (GPT-6 Astra) † | High | 55 (54.85) | 없음 | 없음 | TB4 54.0 · FC2 40.1 · AB 66.6 · BC 1503 · TBS 59.5 ‖ τ² – · τ³B 40.0 · TBH – · TB2.1 89.9 · IF – · EOG – · ITB – | $10.00 / $50.00 (캐시히트 $1.00) · 7:2:1 $7.70 · 3:1 $20.00 | $3,204.00 (과제당 $3.24) | 44 tok/s · TTFT=TTFAT 40.21s · 멀티턴 TTFT 7.73s · 과제당 8.8분 | https://artificialanalysis.ai/models/gpt-6-astra |
| gpt-6-astra (GPT-6 Astra) † | Xhigh | 55 (55.31) | 없음 | 없음 | TB4 59.6 · FC2 41.4 · AB 67.2 · BC 1544 · TBS 54.8 ‖ τ² – · τ³B 43.1 · TBH – · TB2.1 89.1 · IF – · EOG – · ITB – | $10.00 / $50.00 (캐시히트 $1.00) · 7:2:1 $7.70 · 3:1 $20.00 | $3,746.22 (과제당 $3.66) | 44 tok/s · TTFT=TTFAT 83.77s · 멀티턴 TTFT 12.09s · 과제당 10.2분 | https://artificialanalysis.ai/models/gpt-6-astra |
| gpt-6-astra (GPT-6 Astra) † | Max | 57 (56.85) | 없음 | 없음 | TB4 59.1 · FC2 42.4 · AB 68.5 · BC 1569 · TBS 63.3 ‖ τ² – · τ³B 41.4 · TBH – · TB2.1 88.4 · IF – · EOG – · ITB 48.6 | $10.00 / $50.00 (캐시히트 $1.00) · 7:2:1 $7.70 · 3:1 $20.00 | $5,661.18 (과제당 $6.24) | 43 tok/s · TTFT=TTFAT 187.26s · 멀티턴 TTFT 27.60s · 과제당 20.0분 | https://artificialanalysis.ai/models/gpt-6-astra |
| gpt-6.1-sol (GPT-6.1 Sol) † | Low | 35 (34.80) | 없음 | 없음 | TB4 30.8 · FC2 20.2 · AB 52.6 · BC 1115 · TBS 11.0 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $2.00 / $10.00 (캐시히트 $0.100) · 7:2:1 $1.47 · 3:1 $4.00 | $237.91 (과제당 $0.161) | 51 tok/s · TTFT=TTFAT 2.95s · 멀티턴 TTFT 2.27s · 과제당 1.9분 | https://artificialanalysis.ai/models/gpt-6-1-sol |
| gpt-6.1-sol (GPT-6.1 Sol) † | Medium | 46 (46.35) | 없음 | 없음 | TB4 48.0 · FC2 33.4 · AB 62.6 · BC 1361 · TBS 37.1 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $2.00 / $10.00 (캐시히트 $0.100) · 7:2:1 $1.47 · 3:1 $4.00 | $388.57 (과제당 $0.359) | 52 tok/s · TTFT=TTFAT 4.77s · 멀티턴 TTFT 3.42s · 과제당 4.3분 | https://artificialanalysis.ai/models/gpt-6-1-sol |
| gpt-6.1-sol (GPT-6.1 Sol) † | High | 50 (50.33) | 없음 | 없음 | TB4 51.5 · FC2 36.7 · AB 64.5 · BC 1469 · TBS 46.2 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $2.00 / $10.00 (캐시히트 $0.100) · 7:2:1 $1.47 · 3:1 $4.00 | $573.17 (과제당 $0.591) | 51 tok/s · TTFT=TTFAT 25.90s · 멀티턴 TTFT 7.13s · 과제당 7.5분 | https://artificialanalysis.ai/models/gpt-6-1-sol |
| gpt-6.1-sol (GPT-6.1 Sol) † | Xhigh | 52 (52.46) | 없음 | 없음 | TB4 54.0 · FC2 38.5 · AB 66.6 · BC 1504 · TBS 50.5 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $2.00 / $10.00 (캐시히트 $0.100) · 7:2:1 $1.47 · 3:1 $4.00 | $717.71 (과제당 $0.764) | 54 tok/s · TTFT=TTFAT 59.52s · 멀티턴 TTFT 9.73s · 과제당 9.4분 | https://artificialanalysis.ai/models/gpt-6-1-sol |
| gpt-6.1-sol (GPT-6.1 Sol) † | Max | 55 (54.61) | 없음 | 없음 | TB4 56.1 · FC2 40.6 · AB 64.9 · BC 1557 · TBS 58.1 ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | $2.00 / $10.00 (캐시히트 $0.100) · 7:2:1 $1.47 · 3:1 $4.00 | $1,123.97 (과제당 $1.27) | 48 tok/s · TTFT=TTFAT 143.29s · 멀티턴 TTFT 21.16s · 과제당 23.4분 | https://artificialanalysis.ai/models/gpt-6-1-sol |
| **OpenAI 문서에 명시 없음** | | | | | | | | | |
| gpt-5.2 (GPT-5.2) † | Non-reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 46.5 · τ³B 11.1 · TBH 31.8 · TB2.1 – · IF 47.4 · EOG – · ITB – | $1.75 / $14.00 (캐시히트 $0.175) · 7:2:1 $1.87 · 3:1 $4.81 | 없음 | 60 tok/s · TTFT=TTFAT 2.06s · 멀티턴 TTFT 1.04s | https://artificialanalysis.ai/models/gpt-5-2 |
| gpt-5.2 (GPT-5.2) † | Medium | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 74.3 · τ³B – · TBH 43.2 · TB2.1 – · IF 65.2 · EOG – · ITB – | $1.75 / $14.00 (캐시히트 $0.175) · 7:2:1 $1.87 · 3:1 $4.81 [median] | 없음 | 69 tok/s · TTFT=TTFAT 6.18s · 멀티턴 TTFT 6.81s [median] | https://artificialanalysis.ai/models/gpt-5-2 |
| gpt-5.2 (GPT-5.2) † | Xhigh | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 84.8 · τ³B – · TBH 47.0 · TB2.1 – · IF 75.4 · EOG – · ITB – | $1.75 / $14.00 (캐시히트 $0.175) · 7:2:1 $1.87 · 3:1 $4.81 | 없음 | 74 tok/s · TTFT=TTFAT 91.14s · 멀티턴 TTFT 41.48s | https://artificialanalysis.ai/models/gpt-5-2 |
| **LG AI Research EXAONE 계열** | | | | | | | | | |
| K-EXAONE 2.0 | (단일) | 8 (7.56) | 없음 | 없음 | TB4 0.0 · FC2 0.8 · AB 3.9 · BC 652 · TBS 0.0 ‖ τ² – · τ³B 11.5 · TBH – · TB2.1 40.4 · IF – · EOG – · ITB – | 없음 | 없음 | 없음 | https://artificialanalysis.ai/models/k-exaone-2-0 |
| EXAONE 4.5 33B | Non-reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² – · τ³B – · TBH – · TB2.1 – · IF – · EOG – · ITB – | 없음 | 없음 | 없음 | https://artificialanalysis.ai/models/exaone-4-5-33b |
| EXAONE 4.5 33B | Reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 78.1 · τ³B – · TBH 20.5 · TB2.1 21.3 · IF 58.0 · EOG – · ITB – | 없음 | 없음 | 없음 | https://artificialanalysis.ai/models/exaone-4-5-33b |
| K-EXAONE † | Non-reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 59.1 · τ³B – · TBH 6.8 · TB2.1 – · IF 39.6 · EOG – · ITB – | 없음 | 없음 | 없음 | https://artificialanalysis.ai/models/k-exaone |
| K-EXAONE † | Reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 74.3 · τ³B – · TBH 22.7 · TB2.1 30.3 · IF 64.7 · EOG – · ITB – | 없음 | 없음 | 없음 | https://artificialanalysis.ai/models/k-exaone |
| EXAONE 4.0 32B † | Non-reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 4.1 · τ³B – · TBH 1.5 · TB2.1 – · IF 33.5 · EOG – · ITB – | 없음 | 없음 | 없음 | https://artificialanalysis.ai/models/exaone-4-0-32b |
| EXAONE 4.0 32B † | Reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 17.3 · τ³B – · TBH 3.8 · TB2.1 – · IF 36.3 · EOG – · ITB – | 없음 | 없음 | 없음 | https://artificialanalysis.ai/models/exaone-4-0-32b |
| Exaone 4.0 1.2B | Non-reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 20.5 · τ³B – · TBH 0.0 · TB2.1 – · IF 25.3 · EOG – · ITB – | 없음 | 없음 | 없음 | https://artificialanalysis.ai/models/exaone-4-0-1-2b |
| Exaone 4.0 1.2B | Reasoning | 없음(N/A) | 없음 | 없음 | TB4 – · FC2 – · AB – · BC – · TBS – ‖ τ² 16.4 · τ³B – · TBH 0.0 · TB2.1 – · IF 23.0 · EOG – · ITB – | 없음 | 없음 | 없음 | https://artificialanalysis.ai/models/exaone-4-0-1-2b |

표에 대한 보충:
- **출시일·상태** (모델 페이지 페이로드 기준):
  - gpt-6.2-astra, gpt-6.2-sol: 2026-11-17 출시, current
  - gpt-6.1-terra: 2026-10-26, current
  - gpt-6-luna: 2026-09-22, current
  - gpt-6.1-sol: 2026-09-29, deprecated → 6.2 Sol
  - gpt-6-sol: 2026-09-22, deprecated → 6.1 Sol
  - gpt-6-astra: 2026-09-03, deprecated → 6.2 Astra
  - gpt-5.6-sol/terra/luna: 2026-07-09, deprecated
  - gpt-5.5: 2026-04-23, deprecated
  - gpt-5.4: 2026-03-05, deprecated
  - gpt-5.4-mini: 2026-03-17, deprecated
  - gpt-5.2: 2025-12-11, deprecated
- **providers 페이지의 기본 필터**: "Status: Current"다. 그래서 deprecated 모델은 그 표에 나오지 않고, 모델 페이지에서 읽었다.
- **GPT-6 Luna의 다른 엔드포인트**: providers 표에는 Microsoft Azure 엔드포인트와 OpenAI Flex 엔드포인트도 있다.
  - Azure: non-reasoning 과제당 $0.077, TTFAT 1.15s. max 과제당 $0.16.
  - OpenAI max (Flex): 과제당 $0.076, TTFAT 144.70s, 오류율 14.6%.
- **GPT-6 Sol Medium**: 속도·지연 값이 사이트에 없다. FAQ에도 medium만 빠져 있다.
- **GPT-5.2 Medium**: 가격과 속도가 "median across providers"다. FAQ 문장에 그렇게 적혀 있다.

### B-2. Capability Index (사이트의 다른 종합 지수, 페이로드 값)

출처는 B 표와 같은 모델 페이지다. 각 지수 구성은 https://artificialanalysis.ai/methodology/capability-indexes 에 있다. 지수 값이 없는 모델·변형은 표에서 뺐다. GPT-5.6 Terra의 non-reasoning부터 xhigh까지는 Intelligence Index가 N/A인데도 Engineering을 뺀 Capability Index 값은 페이로드에 있다.

| 모델 | 변형 | Engineering | Strategy & Ops | Finance & Accounting | Legal | Healthcare & Medical | Economics |
|---|---|---|---|---|---|---|---|
| GPT-6 Luna | Non-reasoning | 16.6 | 17.0 | 19.0 | 16.6 | 15.7 | 19.3 |
| GPT-6 Luna | Low | 18.7 | 16.8 | 17.2 | 16.3 | 16.2 | 18.6 |
| GPT-6 Luna | Medium | 24.9 | 33.8 | 26.3 | 24.5 | 27.4 | 26.7 |
| GPT-6 Luna | High | 27.3 | 37.8 | 29.3 | 26.7 | 29.2 | 29.0 |
| GPT-6 Luna | Xhigh | 29.0 | 39.4 | 30.6 | 28.4 | 30.5 | 31.2 |
| GPT-6 Luna | Max | 33.3 | 43.2 | 33.9 | 32.2 | 34.8 | 34.5 |
| GPT-6 Sol | Max | 48.9 | 52.1 | 47.5 | 46.3 | 45.1 | 47.7 |
| GPT-5.6 Terra | Non-reasoning | – | 19.0 | 16.2 | 15.2 | 17.4 | 18.2 |
| GPT-5.6 Terra | Low | – | 28.1 | 22.8 | 22.3 | 24.1 | 24.8 |
| GPT-5.6 Terra | Medium | – | 29.9 | 23.1 | 24.3 | 26.3 | 25.2 |
| GPT-5.6 Terra | High | – | 35.9 | 28.7 | 27.5 | 30.0 | 30.3 |
| GPT-5.6 Terra | Xhigh | – | 39.8 | 31.4 | 30.5 | 33.0 | 33.5 |
| GPT-5.6 Terra | Max | 36.6 | 45.1 | 34.6 | 32.0 | 37.0 | 35.7 |
| GPT-5.6 Luna | Max | 29.4 | 40.7 | 31.8 | 27.7 | 32.4 | 32.8 |
| GPT-6.2 Astra | Low | 50.5 | 48.6 | 45.1 | 45.6 | 41.9 | 43.6 |
| GPT-6.2 Astra | Medium | 59.9 | 57.3 | 54.5 | 52.7 | 50.2 | 52.8 |
| GPT-6.2 Astra | High | 63.6 | 61.6 | 59.0 | 56.1 | 54.1 | 58.1 |
| GPT-6.2 Astra | Xhigh | 65.1 | 62.0 | 60.2 | 56.9 | 54.9 | 59.0 |
| GPT-6.2 Astra | Max | 66.6 | 63.3 | 60.9 | 58.7 | 57.0 | 61.1 |
| GPT-6.2 Sol | Low | 44.4 | 48.4 | 42.3 | 40.2 | 41.0 | 41.5 |
| GPT-6.2 Sol | Medium | 56.2 | 56.3 | 51.6 | 48.8 | 48.0 | 51.1 |
| GPT-6.2 Sol | High | 58.7 | 58.0 | 54.8 | 51.4 | 51.2 | 54.7 |
| GPT-6.2 Sol | Xhigh | 59.9 | 57.9 | 55.5 | 52.8 | 52.1 | 55.4 |
| GPT-6.2 Sol | Max | 61.2 | 59.4 | 57.2 | 55.0 | 53.3 | 57.4 |
| GPT-6.1 Terra | Non-reasoning | 32.8 | 40.0 | 33.5 | 28.2 | – | 31.9 |
| GPT-6.1 Terra | Low | 35.2 | 42.2 | 37.9 | 37.3 | – | 36.0 |
| GPT-6.1 Terra | Medium | 42.6 | 45.4 | 42.5 | 40.5 | – | 40.8 |
| GPT-6.1 Terra | High | 46.4 | 47.4 | 44.2 | 42.5 | – | 43.1 |
| GPT-6.1 Terra | Xhigh | 49.4 | 48.7 | 47.6 | 43.8 | – | 46.0 |
| GPT-6.1 Terra | Max | 54.7 | 50.0 | 49.0 | 46.4 | 44.7 | 48.5 |
| GPT-6 Astra | Low | 49.8 | 49.9 | 48.1 | 47.7 | 45.0 | 47.4 |
| GPT-6 Astra | Medium | 56.8 | 55.7 | 53.7 | 51.8 | 49.6 | 53.0 |
| GPT-6 Astra | High | 60.0 | 57.2 | 56.1 | 55.1 | 51.6 | 55.7 |
| GPT-6 Astra | Xhigh | 60.4 | 57.9 | 56.8 | 55.7 | 52.7 | 56.8 |
| GPT-6 Astra | Max | 61.8 | 58.0 | 57.4 | 55.6 | 53.7 | 57.2 |
| GPT-6.1 Sol | Low | 42.6 | 45.6 | 44.3 | 42.9 | 39.7 | 43.2 |
| GPT-6.1 Sol | Medium | 52.1 | 53.3 | 50.6 | 49.0 | 45.8 | 49.6 |
| GPT-6.1 Sol | High | 55.4 | 55.4 | 53.2 | 51.8 | 48.8 | 52.8 |
| GPT-6.1 Sol | Xhigh | 57.5 | 57.2 | 55.2 | 53.7 | 50.8 | 54.8 |
| GPT-6.1 Sol | Max | 59.4 | 57.6 | 56.2 | 53.7 | 52.0 | 56.3 |
| K-EXAONE 2.0 | (단일) | 18.2 | 10.9 | 18.5 | 17.1 | – | 18.4 |

## C. 지수 구성(방법론)과 버전

출처: https://artificialanalysis.ai/methodology/intelligence-benchmarking (Version History 포함), https://artificialanalysis.ai/methodology , https://artificialanalysis.ai/methodology/capability-indexes , https://artificialanalysis.ai/methodology/performance-benchmarking

**Artificial Analysis Intelligence Index v5.0.1** ("November 2026 to current")는 9개 평가로 이루어진다. 4개 카테고리가 각 25%씩이다.

| 카테고리 | 평가 | 가중치 | Tool 사용 | 비공개 |
|---|---|---|---|---|
| Knowledge Work 25% | AA-Briefcase v1.1 (에이전트형 지식노동, Stirrup 하네스, 최대 500턴) | 15% | ✓ | ✓ |
| | AutomationBench-AA (Zapier, REST API tool로 SaaS 워크플로, 50턴 상한, guardrail 위반 시 0점) | 5% | ✓ | ✓ |
| | GDP.pdf (긴 PDF 추론, 단일 턴, 도구 없음) | 5% | ✗ | ✗ |
| Coding 25% | FrontierCode-AA 2.0 (Cognition, 실제 OSS 저장소 변경, 132과제×3회, Stirrup 하네스, 500턴) | 15% | ✓ | ✓ |
| | Terminal-Bench 4.0 (66과제×3회, mini-swe-agent 하네스, 500스텝) | 10% | ✓ | ✗ |
| Science 25% | Terminal-Bench-Science 0.1 (70과제, mini-swe-agent, 1,000스텝) | 15% | ✓ | ✗ |
| | CritPt v2 (Hard Subset, 40문항) | 10% | ✓ | ✓ |
| General 25% | AA-Omniscience v1.1 (정확도 10% + 1−환각률 5%) | 15% | ✗ | ✓ |
| | HLE-Diamond (1,000문항, 도구 없음) | 10% | ✗ | ✗ |

- **공통 조건**: 온도는 비추론 0, 추론 0.6이다. 최대 출력은 비추론 16,384토큰, 추론은 제작사가 공개한 최대값이다. 채점은 pass@1이다. 에이전트형 벤치마크의 샌드박스는 e2b를 쓴다. 비용은 제공자 API가 보고한 토큰 수에 실측 캐시 히트율을 곱해 계산한다.
- **Coding Index / Agentic Index**: 방법론 페이지, 버전 이력, 모델 페이지 어디에도 같은 이름의 지수가 없다.
  - v4.0~v4.3.2에는 Intelligence Index 안에 "Agents" 카테고리가 있었다. v5.0에서 이름이 Knowledge Work로 바뀌었다.
  - 별도의 "Coding Agent Index"는 있다. 이것은 코딩 에이전트 제품을 평가하는 지수이고 FrontierCode-AA 2.0을 별도로 실행해 쓴다. 다른 하네스는 조사 범위 밖이라 열어보지 않았다.
- **Capability Index 6종**: Finance & Accounting, Strategy & Ops, Legal, Healthcare & Medical, Engineering, Economics. 에이전트·코딩과 관련된 것은 두 가지다.
  - Engineering: Agentic Coding(TB4.0+FC2) 15%, Agentic Knowledge Work(Briefcase) 15%, Science 20%, Reasoning(HLE-Diamond) 20%, Engineering Knowledge(Omniscience) 30%.
  - Strategy & Ops: Agentic Tool Use(AutomationBench) 35%, Agentic Knowledge Work(Briefcase) 30%, Business Knowledge 25%, Long-Context 5%, Non-Hallucination 5%.
- **사용자가 예로 든 벤치마크의 현재 지위** (모두 방법론 페이지 기준):
  - τ²-Bench Telecom: v4.1에서 τ³-Banking으로 대체됐다(레거시).
  - τ³-Banking: v4.3에서 지수에서 빠졌다. 새 모델에는 계속 실행한다.
  - Terminal-Bench Hard: v4.1에서 Terminal-Bench 2.1로 대체됐다.
  - Terminal-Bench 2.1: v4.3에서 Terminal-Bench 4.0으로 대체됐다.
  - IFBench: v4.1에서 지수에서 빠졌다. 새 모델에는 계속 실행한다.
  - 그 결과 최근 모델(GPT-6.x)에는 τ², TBH, IF 값이 없고, 예전 모델(GPT-5.x)에는 TB4, FC2 값이 대부분 없다.
- **버전 이력 요약**:

| 버전 | 기간 | 주요 변경 |
|---|---|---|
| v5.0.1 | 2026-11~현재 | CritPt v2 재채점 |
| v5.0 | 2026-10~11 | HLE-Diamond, TB-Science, FrontierCode-AA 2.0 추가. GDPval-AA, SciCode, AA-LCR, HLE 제외. 카테고리 25%×4로 재조정 |
| v4.3.2 | 2026-09~10 | |
| v4.3 | 2026-09 | AutomationBench-AA, TB4.0 도입 |
| v4.2 | 2026-09 | |
| v4.1 | 2026-06~08 | τ³-Banking, TB2.1 도입. IFBench 제외. 비용 지표에 캐시 반영 |
| v4.0 | 2026-01~06 | |
| v3.0 | 2025-09~12 | TBH, τ² 추가 |

  - 버전이 다르면 점수를 직접 비교할 수 없다. 이 조사의 지수 값은 모두 v5.0.1이다.
- **가격·비용 정의** (https://artificialanalysis.ai/methodology 의 Definitions):
  - Blended: "7:2:1 ratio of cache hit, input, and output tokens".
  - 모델 페이지의 "Technical specifications"는 독점 모델의 가격대를 나눌 때 "blended 3:1 input/output price ratio"를 쓴다고 적는다.
  - Cost per Task: 지수 가중치를 적용한 과제당 평균 비용. 추론 토큰을 많이 쓸수록 커진다고 명시돼 있다.
  - Cost to Run: 지수 평가 전체 비용(반복 제외). 입력, 캐시 히트, 캐시 쓰기, 추론, 답변 토큰 단가를 모두 반영한다.
- **속도 정의** (Performance 방법론 v3.0.0, 2026-11-03 변경):
  - 헤드라인 값은 1k, 10k, 100k 입력 워크로드와 멀티턴 agentic 워크로드(tool 호출 포함)를 같은 비중으로 평균한 것이다. 최근 5일 평균이고, 6시간마다 측정한다. 측정 위치는 Google Cloud us-central1이다.
  - 출력 속도는 TTFT를 포함한 전체 요청 시간 기준이다.
  - TTFAT는 추론 시간을 포함해 첫 답변 토큰까지 걸린 시간이다.
  - 과제당 시간은 실측이 아니라 "출력 토큰 ÷ 출력 속도"로 추정한 값이다.

## D. EXAONE 항목

| 모델 | 변형 | 상태·출시 | Intelligence Index v5.0.1 | 개별 점수(%) | 가격·cost to run·속도 | 출처 |
|---|---|---|---|---|---|---|
| K-EXAONE 2.0 (750B, 활성 37B, Apache 2.0) | 단일(추론 모델) | current, 2026-08-12 | **8 (7.56)**. 같은 크기 오픈웨이트 중앙값은 23 | TB4 0.0, FC2 0.8, AB 3.9, Briefcase Elo 652, TBS 0.0, τ³B 11.5, TB2.1 40.4, GPQA 82.9, HLE 18.6. 지수 산출 출력 토큰 63.1M | 가격·속도 없음(페이지에 "In - Out -", N/A). cost to run 없음 | https://artificialanalysis.ai/models/k-exaone-2-0 ; 지수 8은 https://artificialanalysis.ai/leaderboards/models 표에도 있음 |
| EXAONE 4.5 33B (비상업 라이선스) | Reasoning | current, 2026-04-09 | 없음(N/A) | τ² 78.1, TBH 20.5, TB2.1 21.3, IFBench 58.0, GDPval Elo 474 | 없음 | https://artificialanalysis.ai/models/exaone-4-5-33b |
| EXAONE 4.5 33B | Non-reasoning | current | 없음(N/A) | 사이트에 값 없음 | 없음 | 같은 페이지 |
| K-EXAONE (236B, 활성 23B) | Reasoning | deprecated → K-EXAONE 2.0, 2025-12-31 | 없음(N/A) | τ² 74.3, TBH 22.7, TB2.1 30.3, IFBench 64.7 | 없음 | https://artificialanalysis.ai/models/k-exaone |
| K-EXAONE | Non-reasoning | deprecated | 없음(N/A) | τ² 59.1, TBH 6.8, IFBench 39.6 | 없음 | 같은 페이지 |
| EXAONE 4.0 32B | Reasoning / Non-reasoning | deprecated → 4.5 33B, 2025-07-15 | 없음(N/A) | 추론: τ² 17.3, TBH 3.8, IF 36.3. 비추론: τ² 4.1, TBH 1.5, IF 33.5 | 없음 | https://artificialanalysis.ai/models/exaone-4-0-32b |
| Exaone 4.0 1.2B | Reasoning / Non-reasoning | current, 2025-07-15 | 없음(N/A) | 추론: τ² 16.4, TBH 0.0, IF 23.0. 비추론: τ² 20.5, TBH 0.0, IF 25.3 | 없음 | https://artificialanalysis.ai/models/exaone-4-0-1-2b |
| **K-EXAONE 2.5** | – | – | **확인 못 함** | – | – | /models/k-exaone-2-5 는 404다. 사이트 모델 카탈로그(providers 페이지 페이로드의 전체 모델 목록)에도 이름이 없다. |

EXAONE 모델은 providers 표에 API 엔드포인트가 하나도 없다. 그래서 가격, 속도, cost to run이 모두 비어 있다.

## E. 확인하지 못한 것

1. **Coding Index와 Agentic Index**: 현재 사이트(v5.0.1)에서 찾지 못했다. 과거 버전에 그런 이름의 지수가 있었는지도 버전 이력에 언급이 없어 확인하지 못했다.
2. **deprecated 모델의 지수**: GPT-5.6 Sol 전체, GPT-5.5, GPT-5.4, GPT-5.4 mini, GPT-5.2 전 변형, GPT-6 Sol·GPT-5.6 Terra·GPT-5.6 Luna의 max 외 변형은 v5.0.1 지수, cost to run, 과제당 시간이 사이트에 없다(N/A). 이 모델들의 과거 버전(v4.x) 지수도 사이트에 남아 있지 않아 확인하지 못했다.
3. **K-EXAONE 2.5**: 사이트에 없다(위 D 참고).
4. **EXAONE 계열의 가격·속도·cost to run**: 엔드포인트가 없어 값이 없다.
5. **GPT-6 Sol Medium의 출력 속도와 지연**: 값이 없다.
6. **"Non-reasoning" 변형과 API 파라미터의 관계**: 사이트의 "Non-reasoning"이 OpenAI API의 `reasoning_effort="none"`과 같은 설정인지 명시돼 있지 않다. 평가에 Chat Completions를 썼는지 Responses API를 썼는지도 방법론 페이지에 적혀 있지 않다. 방법론에는 "OpenAI 호환 제공자는 공식 OpenAI Python 라이브러리 사용"이라는 문장만 있다.
7. **"minimal" 변형**: 대상 OpenAI 모델 가운데 사이트에 minimal 변형이 실린 모델은 없다. 사이트가 싣는 effort는 non-reasoning, low, medium, high, xhigh, max다. GPT-5.4는 non-reasoning·low·xhigh, GPT-5.4 mini와 GPT-5.2는 non-reasoning·medium·xhigh만 실려 있다.
8. **값별 측정 날짜**: 개별 값마다 측정일이 표시돼 있지 않다. 확인할 수 있는 것은 지수 버전(v5.0.1, 2026년 11월부터), 속도 집계 기간(최근 5일), 측정 주기(6시간, deprecated는 18시간)뿐이다.
9. **값의 출처 성격**: 개별 벤치마크 점수, cost to run, 출력 속도, 멀티턴 TTFT, Capability Index는 화면 차트로 그려진 것을 본 것이 아니다. 같은 HTML 안의 차트 데이터에서 읽었다. 정수 지수, 가격, TTFAT, 과제당 시간, blended 7:2:1은 화면 텍스트(FAQ·표)와 대조해 일치를 확인했다.
