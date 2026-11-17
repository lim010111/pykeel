# 하네스와 실험 코드를 모두 Python으로 쓴다

참고하는 하네스 상당수(Claude Code, pi)가 TypeScript인데도, 이 프로젝트는 하네스와 실험·분석 코드를 모두 Python으로 씁니다. 연구 실험은 InterfaceSpec을 바꿔 끼우면서 하네스를 수백 번 돌려야 합니다. 같은 언어라면 한 프로세스 안에서 객체만 바꿔 끼우면 됩니다. 언어가 다르면 하네스를 별도 프로그램으로 띄우고 결과를 파일로 주고받아야 합니다. 분석 도구(DuckDB, pandas, statsmodels)도 Python에 있습니다. 작성자에게도 TypeScript보다 Python이 익숙합니다.

## Considered Options

- **TypeScript 하네스 + Python 분석:** 참고 하네스와 언어가 같아서 비교해 읽기는 쉽습니다. 하지만 실험할 때마다 프로세스 경계를 넘어야 합니다.
- **전부 TypeScript:** 통계·분석 생태계가 약합니다.

TypeScript는 나중에 웹 trace 뷰어 같은 주변부에만 쓸 수 있습니다.
