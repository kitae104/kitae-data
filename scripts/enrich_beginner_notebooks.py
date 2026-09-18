"""Add beginner exercises and AI project prompts to three course notebooks."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "강의자료_ipynb"
GENERATED_BY = "enrich_beginner_notebooks_v1"


def _metadata(*tags: str) -> dict:
    return {"generated_by": GENERATED_BY, "tags": list(tags)}


def md(text: str, *tags: str):
    return nbformat.v4.new_markdown_cell(
        dedent(text).strip() + "\n", metadata=_metadata(*tags)
    )


def code(text: str, *tags: str):
    return nbformat.v4.new_code_cell(
        dedent(text).strip() + "\n", metadata=_metadata(*tags)
    )


def exercise(title: str, goal: str, template: str, hint: str, solution: str) -> list:
    return [
        md(
            f"""
            ### {title}

            **목표:** {goal}

            아래 코드 셀의 주석을 보고 먼저 직접 작성해 보세요. 막히면 힌트를 확인하고,
            마지막에 정답 예제를 실행해 결과를 비교합니다.
            """,
            "beginner-practice",
        ),
        code(template, "beginner-practice", "beginner-exercise"),
        md(
            f"""
            <details>
            <summary><strong>힌트 보기</strong></summary>

            {hint}

            </details>

            **정답 예제:** 먼저 직접 시도한 뒤 아래 셀을 실행하세요.
            """,
            "beginner-practice",
        ),
        code(solution, "beginner-practice", "beginner-solution"),
    ]


def pandas_cells() -> list:
    cells = [
        md(
            """
            ## 초보자 필수 보강 실습

            지금까지 배운 판다스 기능을 반도체 공정 데이터에 연결해 봅니다.
            각 실습은 **직접 작성 → 힌트 → 정답 확인** 순서입니다.

            초보자가 꼭 기억할 원칙은 세 가지입니다.

            1. 원본 데이터는 덮어쓰지 않고 `copy()`로 복사해 작업합니다.
            2. 분석 전에 크기, 열 이름, 자료형, 결측값을 먼저 확인합니다.
            3. 계산 결과는 몇 행이라도 직접 확인해 예상과 맞는지 검증합니다.
            """,
            "beginner-practice",
        ),
        md(
            """
            ### 실습 데이터 준비

            작은 공정 이력 표를 직접 만듭니다. `None`은 측정값이 없다는 뜻이며,
            마지막 행은 중복 처리 연습을 위해 의도적으로 한 번 더 넣었습니다.
            """,
            "beginner-practice",
        ),
        code(
            """
            process_data = {
                'lot_id': ['L001', 'L002', 'L003', 'L004', 'L005', 'L005'],
                '공정': ['식각', '증착', '식각', '세정', '증착', '증착'],
                '온도_섭씨': [298.5, 302.1, None, 299.8, 305.2, 305.2],
                '압력_Pa': [101.2, 99.8, 103.1, 100.5, 98.9, 98.9],
                '두께_nm': [100.4, 102.3, 98.7, 101.1, 104.8, 104.8],
                '합격여부': [1, 1, -1, 1, -1, -1]
            }

            process_df = pd.DataFrame(process_data)
            process_df
            """,
            "beginner-practice",
            "beginner-setup",
        ),
    ]

    cells += exercise(
        "실습 1 · 데이터의 전체 모습 점검하기",
        "행·열 크기, 열 이름, 자료형, 결측값 개수를 한 번에 점검합니다.",
        """
        # TODO 1: process_df의 행 수와 열 수를 출력하세요.
        # TODO 2: 열 이름과 각 열의 자료형을 출력하세요.
        # TODO 3: 열별 결측값 개수를 출력하세요.
        """,
        "`shape`, `columns`, `dtypes`, `isna().sum()`을 차례로 사용합니다.",
        """
        print(f'행 수: {process_df.shape[0]}, 열 수: {process_df.shape[1]}')
        print('\\n열 이름:', process_df.columns.tolist())
        print('\\n자료형:')
        print(process_df.dtypes)
        print('\\n열별 결측값:')
        print(process_df.isna().sum())
        """,
    )
    cells += exercise(
        "실습 2 · 필요한 데이터만 선택하기",
        "불합격 데이터와 고온 공정 데이터를 조건식으로 골라냅니다.",
        """
        # TODO 1: 합격여부가 -1인 행에서 lot_id, 공정, 온도_섭씨만 선택하세요.
        # TODO 2: 온도가 300도 이상인 행을 선택하세요.
        # TODO 3: 공정이 '증착'이면서 두께가 103nm 이상인 행을 선택하세요.
        """,
        "조건마다 괄호를 쓰고, 두 조건을 모두 만족시킬 때는 `&`를 사용합니다.",
        """
        failed_lots = process_df.loc[
            process_df['합격여부'] == -1,
            ['lot_id', '공정', '온도_섭씨']
        ]
        high_temperature = process_df[process_df['온도_섭씨'] >= 300]
        deposition_risk = process_df[
            (process_df['공정'] == '증착') & (process_df['두께_nm'] >= 103)
        ]

        print('불합격 Lot:')
        print(failed_lots)
        print('\\n300도 이상 공정:', len(high_temperature), '건')
        print('고두께 증착 공정:', len(deposition_risk), '건')
        """,
    )
    cells += exercise(
        "실습 3 · 결측값과 중복 데이터 정리하기",
        "원본을 보존하면서 결측값을 중앙값으로 채우고 중복 행을 제거합니다.",
        """
        # TODO 1: process_df를 practice_clean으로 복사하세요.
        # TODO 2: 온도_섭씨의 결측값을 해당 열의 중앙값으로 채우세요.
        # TODO 3: 중복 행을 제거하고 인덱스를 다시 0부터 매기세요.
        # TODO 4: 정리 전후 행 수와 남은 결측값 수를 출력하세요.
        """,
        "`copy()`, `median()`, `fillna()`, `drop_duplicates()`, `reset_index()`를 사용합니다.",
        """
        practice_clean = process_df.copy()
        temperature_median = practice_clean['온도_섭씨'].median()
        practice_clean['온도_섭씨'] = practice_clean['온도_섭씨'].fillna(temperature_median)
        before_rows = len(practice_clean)
        practice_clean = practice_clean.drop_duplicates().reset_index(drop=True)

        print(f'정리 전 {before_rows}행 -> 정리 후 {len(practice_clean)}행')
        print(f'남은 결측값: {practice_clean.isna().sum().sum()}개')
        practice_clean
        """,
    )
    cells += exercise(
        "실습 4 · 새 열을 만들고 위험 순서로 정렬하기",
        "기준값에서 얼마나 벗어났는지 계산하고 확인 우선순위를 정합니다.",
        """
        # TODO 1: 두께_nm과 기준값 100의 차이를 절댓값으로 계산해 두께편차_nm 열을 만드세요.
        # TODO 2: 합격여부를 {1: '합격', -1: '불합격'}으로 바꾼 판정 열을 만드세요.
        # TODO 3: 두께편차_nm이 큰 순서로 정렬해 상위 3행을 확인하세요.
        """,
        "절댓값은 `.abs()`, 값 치환은 `.map()`, 정렬은 `sort_values()`를 사용합니다.",
        """
        practice_clean['두께편차_nm'] = (practice_clean['두께_nm'] - 100).abs()
        practice_clean['판정'] = practice_clean['합격여부'].map({1: '합격', -1: '불합격'})

        priority_lots = practice_clean.sort_values(
            '두께편차_nm', ascending=False
        ).head(3)
        priority_lots[['lot_id', '공정', '두께_nm', '두께편차_nm', '판정']]
        """,
    )
    cells += exercise(
        "실습 5 · 공정별 요약표와 그래프 만들기",
        "공정별 평균 온도와 평균 두께를 계산하고 막대그래프로 비교합니다.",
        """
        # TODO 1: 공정별 평균 온도와 평균 두께를 계산해 process_summary에 저장하세요.
        # TODO 2: 평균 두께를 막대그래프로 그리세요.
        # TODO 3: 제목, x축 이름, y축 이름을 추가하세요.
        """,
        "`groupby()[[열 목록]].mean()`으로 요약한 뒤 `plot(kind='bar')`를 사용할 수 있습니다.",
        """
        process_summary = (
            practice_clean.groupby('공정')[['온도_섭씨', '두께_nm']]
            .mean()
            .round(2)
        )
        print(process_summary)

        process_summary['두께_nm'].plot(kind='bar', color='steelblue', figsize=(7, 4))
        plt.title('공정별 평균 두께')
        plt.xlabel('공정')
        plt.ylabel('평균 두께 (nm)')
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.show()
        """,
    )
    cells += ai_prompt_cells(
        "판다스 공정 데이터 점검 도구",
        """
        당신은 초보자를 돕는 파이썬 데이터 분석 강사입니다.

        [역할]
        pandas와 matplotlib만 사용해 반도체 공정 CSV를 점검하는 주피터 노트북 프로그램을 작성하세요.

        [입력 데이터]
        - 파일명: 사용자가 지정하는 CSV 파일
        - 예시 열: lot_id, 공정, 온도_섭씨, 압력_Pa, 두께_nm, 합격여부
        - 실제 열 이름이 다를 수 있으므로 처음에 열 목록을 출력하고 사용자가 열 이름을 설정하게 하세요.

        [구현 요구사항]
        1. CSV를 읽고 행·열 수, 앞 5행, 자료형, 결측값, 중복 행 수를 보여주세요.
        2. 원본을 copy()로 보존한 뒤 숫자 결측값은 중앙값으로 채우고 중복을 제거하세요.
        3. 사용자가 지정한 온도 기준과 두께 기준을 벗어난 행을 필터링하세요.
        4. 공정별 평균 온도·압력·두께와 합격/불합격 건수를 표로 만드세요.
        5. 공정별 평균 두께 막대그래프와 온도-두께 산점도를 그리세요.
        6. 각 코드 블록 앞에 초보자용 설명을 2~3문장으로 작성하세요.
        7. 어려운 클래스, 장식용 함수, 머신러닝은 사용하지 마세요.

        [결과물]
        - 위에서 아래로 순서대로 실행되는 주피터 노트북용 코드
        - 정리된 데이터 미리보기와 공정별 요약표
        - 위험 조건에 해당하는 Lot 목록
        - 그래프 2개

        [검증]
        - 실행 전에 필요한 패키지와 CSV 경로를 먼저 확인하세요.
        - 열 이름이 없을 때 이해하기 쉬운 오류 메시지를 보여주세요.
        - 원본 행 수, 정리 후 행 수, 남은 결측값 수를 출력하세요.
        - 마지막에 초보자가 바꿔 볼 값 3가지를 알려주세요.
        """,
        "파일명과 열 이름, 온도·두께 기준값만 자신의 데이터에 맞게 바꾸면 됩니다. 회사 데이터는 외부 AI 서비스에 직접 업로드하지 말고, 열 이름과 일부 가상 예시만 제공하세요.",
    )
    return cells


def semiconductor_eda_cells() -> list:
    cells = [
        md(
            """
            ## 초보자 필수 보강 실습

            이번에는 `반도체_공정_샘플.csv`를 처음 받았다고 가정하고,
            **점검 → 정리 → 비교 → 이상값 확인 → 보고서 작성** 순서로 반복합니다.

            숫자가 계산되었다는 사실보다, 그 숫자가 어떤 공정 판단에 필요한지 한 문장으로
            설명하는 습관이 중요합니다.
            """,
            "beginner-practice",
        ),
    ]
    cells += exercise(
        "실습 1 · 1분 데이터 건강검진",
        "분석 전에 데이터 크기, 결측률, 중복, 판정 비율을 빠르게 확인합니다.",
        """
        # TODO 1: CSV를 practice_raw로 읽으세요.
        # TODO 2: 행·열 수, 열별 결측률(%), 중복 행 수를 출력하세요.
        # TODO 3: 합격여부의 건수와 비율(%)을 출력하세요.
        """,
        "결측률은 `isna().mean().mul(100)`, 판정 비율은 `value_counts(normalize=True)`로 구합니다.",
        """
        practice_raw = pd.read_csv('반도체_공정_샘플.csv')

        print(f'데이터 크기: {practice_raw.shape[0]}행 x {practice_raw.shape[1]}열')
        print('\\n결측률 상위 5개 열(%):')
        print(practice_raw.isna().mean().mul(100).sort_values(ascending=False).head().round(2))
        print(f'\\n중복 행: {practice_raw.duplicated().sum()}개')
        print('\\n판정 건수:')
        print(practice_raw['합격여부'].value_counts(dropna=False))
        print('\\n판정 비율(%):')
        print(practice_raw['합격여부'].value_counts(normalize=True, dropna=False).mul(100).round(2))
        """,
    )
    cells += exercise(
        "실습 2 · 재현 가능한 데이터 정리",
        "숫자 결측값을 중앙값으로 채우고 중복을 제거한 분석용 데이터를 만듭니다.",
        """
        # TODO 1: practice_raw를 practice_clean으로 복사하세요.
        # TODO 2: 숫자 열을 자동으로 찾으세요.
        # TODO 3: 각 숫자 열의 결측값을 중앙값으로 채우세요.
        # TODO 4: 중복 행을 제거하고 인덱스를 다시 매기세요.
        """,
        "`select_dtypes(include='number')`로 숫자 열을 자동 선택할 수 있습니다.",
        """
        practice_clean = practice_raw.copy()
        practice_numeric = practice_clean.select_dtypes(include='number').columns
        practice_clean[practice_numeric] = practice_clean[practice_numeric].fillna(
            practice_clean[practice_numeric].median()
        )
        practice_clean = practice_clean.drop_duplicates().reset_index(drop=True)
        practice_clean['판정'] = practice_clean['합격여부'].map({1: '합격', -1: '불합격'})

        print(f'정리 후 크기: {practice_clean.shape}')
        print(f'남은 결측값: {practice_clean.isna().sum().sum()}개')
        """,
    )
    cells += exercise(
        "실습 3 · IQR로 이상값 후보 찾기",
        "온도 분포에서 일반 범위를 크게 벗어난 측정값을 점검 대상으로 표시합니다.",
        """
        # TODO 1: 온도_섭씨의 Q1(25%)과 Q3(75%)를 구하세요.
        # TODO 2: IQR = Q3 - Q1을 계산하세요.
        # TODO 3: Q1 - 1.5*IQR 미만 또는 Q3 + 1.5*IQR 초과 행을 찾으세요.
        # 주의: 이상값 후보가 반드시 오류나 불량이라는 뜻은 아닙니다.
        """,
        "`quantile(0.25)`와 `quantile(0.75)`를 사용하고 두 조건은 `|`로 연결합니다.",
        """
        q1 = practice_clean['온도_섭씨'].quantile(0.25)
        q3 = practice_clean['온도_섭씨'].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        temperature_outliers = practice_clean[
            (practice_clean['온도_섭씨'] < lower) |
            (practice_clean['온도_섭씨'] > upper)
        ]

        print(f'온도 일반 범위: {lower:.2f} ~ {upper:.2f} °C')
        print(f'이상값 후보: {len(temperature_outliers)}건')
        temperature_outliers[['온도_섭씨', '압력_Pa', '두께_nm', '판정']].head()
        """,
    )
    cells += exercise(
        "실습 4 · 합격과 불합격의 평균 차이 찾기",
        "두 판정 그룹의 평균 차이가 큰 센서를 우선 확인합니다.",
        """
        # TODO 1: 판정별 숫자 열 평균을 계산하세요.
        # TODO 2: 합격 평균과 불합격 평균의 차이 절댓값을 계산하세요.
        # TODO 3: 평균 차이가 큰 상위 5개 열을 출력하세요.
        """,
        "판정별 평균표를 만든 뒤 두 행을 빼고 `.abs().sort_values(ascending=False)`를 사용합니다.",
        """
        compare_cols = [col for col in numeric_cols if col in practice_clean.columns]
        result_means = practice_clean.groupby('판정')[compare_cols].mean()
        mean_gap = (
            result_means.loc['불합격'] - result_means.loc['합격']
        ).abs().sort_values(ascending=False)

        print('합격/불합격 평균 차이 상위 5개 변수:')
        print(mean_gap.head(5).round(3))
        """,
    )
    cells += exercise(
        "실습 5 · 핵심 그래프와 한 줄 결론 만들기",
        "판정 건수와 평균 차이가 가장 큰 변수의 분포를 함께 보고 간단히 해석합니다.",
        """
        # TODO 1: 평균 차이가 가장 큰 변수 이름을 top_gap_col에 저장하세요.
        # TODO 2: 왼쪽에는 판정별 건수, 오른쪽에는 해당 변수의 박스플롯을 그리세요.
        # TODO 3: 합격/불합격 평균과 차이를 한 문장으로 출력하세요.
        """,
        "`mean_gap.index[0]`으로 변수명을 얻고 `plt.subplots(1, 2)`로 그래프 영역을 만듭니다.",
        """
        top_gap_col = mean_gap.index[0]
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        sns.countplot(data=practice_clean, x='판정', hue='판정', legend=False, ax=axes[0])
        axes[0].set_title('판정별 건수')

        sns.boxplot(data=practice_clean, x='판정', y=top_gap_col,
                    hue='판정', legend=False, ax=axes[1])
        axes[1].set_title(f'판정별 {top_gap_col} 분포')
        plt.tight_layout()
        plt.show()

        pass_mean = result_means.loc['합격', top_gap_col]
        fail_mean = result_means.loc['불합격', top_gap_col]
        print(
            f'{top_gap_col}: 합격 평균 {pass_mean:.2f}, '
            f'불합격 평균 {fail_mean:.2f}, 차이 {abs(fail_mean - pass_mean):.2f}'
        )
        print('이 차이는 원인 확정이 아니라 추가 점검이 필요한 단서입니다.')
        """,
    )
    cells += ai_prompt_cells(
        "반도체 공정 품질 EDA 리포트",
        """
        당신은 반도체 공정 데이터를 처음 배우는 사람을 돕는 데이터 분석가입니다.

        [역할]
        pandas, matplotlib, seaborn을 사용해 공정 품질을 점검하는 주피터 노트북 프로그램을 작성하세요.

        [입력 데이터]
        - 파일명: 반도체_공정_샘플.csv
        - 타겟 열: 합격여부 (1=합격, -1=불합격)
        - 주요 숫자 열: 온도_섭씨, 압력_Pa, 가스유량_slm, 전력_W, 진공도_mTorr,
          두께_nm, 습도_pct, 진동_mm_s, 처리시간_sec, 냉각수온도_섭씨

        [구현 요구사항]
        1. 데이터 크기, 자료형, 결측률, 중복 수, 합격/불합격 비율을 점검하세요.
        2. 원본을 보존하고 숫자 결측값은 중앙값으로 채운 뒤 중복을 제거하세요.
        3. 각 숫자 열에서 IQR 방식으로 이상값 후보 수와 비율을 계산하세요.
        4. 합격/불합격별 평균표와 평균 차이가 큰 상위 5개 변수를 만드세요.
        5. 판정 건수 그래프, 상위 변수 박스플롯, 상관관계 히트맵을 그리세요.
        6. 분석 결과를 근거 숫자와 함께 3개의 짧은 문장으로 요약하세요.
        7. 상관관계를 원인이라고 표현하지 말고 '추가 점검 단서'라고 설명하세요.
        8. 머신러닝 모델은 만들지 마세요.

        [결과물]
        - 위에서 아래로 실행 가능한 주피터 노트북 코드
        - data_quality_summary.csv: 결측률과 이상값 후보 비율
        - result_comparison.csv: 판정별 평균과 평균 차이
        - 그래프 3개와 초보자용 해석

        [검증]
        - 처리 전후 행 수와 결측값 수를 출력하세요.
        - 타겟 값이 1과 -1 이외 값을 포함하면 경고하세요.
        - 그래프에 사용한 열이 실제 데이터에 존재하는지 먼저 확인하세요.
        - 마지막 셀에 분석의 한계와 다음 확인 사항을 출력하세요.
        """,
        "이 프롬프트는 '숫자를 계산하는 코드'와 '현업에서 과장하지 않는 해석'을 함께 요청합니다. AI가 만든 코드는 셀 단위로 실행하고, 저장되는 CSV의 행·열과 원본 보존 여부를 반드시 확인하세요.",
    )
    return cells


def semiconductor_ml_cells() -> list:
    cells = [
        md(
            """
            ## 초보자 필수 보강 실습

            모델을 만드는 것보다 중요한 것은 **무엇을 맞혀야 하는지**, **어떤 실수를 줄여야 하는지**를
            이해하는 일입니다. 반도체 불량 탐지에서는 불량을 정상으로 놓치는 `False Negative`와
            불량 재현율(`Recall`)을 특히 주의해서 봅니다.
            """,
            "beginner-practice",
        ),
    ]
    cells += exercise(
        "실습 1 · 클래스 불균형과 기준 모델 이해하기",
        "항상 정상이라고 예측하는 단순 모델과 비교해 정확도의 함정을 확인합니다.",
        """
        # TODO 1: y_test의 정상/불량 건수와 비율을 출력하세요.
        # TODO 2: 항상 정상(0)만 예측하는 배열을 만드세요.
        # TODO 3: 이 기준 모델의 정확도와 불량 Recall을 계산하세요.
        """,
        "`value_counts(normalize=True)`와 `accuracy_score`, `recall_score`를 사용합니다.",
        """
        from sklearn.metrics import accuracy_score, recall_score

        print('테스트 판정 건수:')
        print(y_test.value_counts().sort_index())
        print('\\n테스트 판정 비율(%):')
        print(y_test.value_counts(normalize=True).sort_index().mul(100).round(2))

        always_normal = np.zeros(len(y_test), dtype=int)
        baseline_accuracy = accuracy_score(y_test, always_normal)
        baseline_recall = recall_score(y_test, always_normal, zero_division=0)
        print(f'항상 정상 모델 정확도: {baseline_accuracy:.3f}')
        print(f'항상 정상 모델 불량 Recall: {baseline_recall:.3f}')
        print('정확도가 높아도 불량 Recall이 0이면 불량 탐지 모델로 쓸 수 없습니다.')
        """,
    )
    cells += exercise(
        "실습 2 · 혼동행렬을 숫자로 읽기",
        "정상/불량 예측의 네 가지 경우와 놓친 불량 수를 직접 확인합니다.",
        """
        # TODO 1: 랜덤 포레스트 예측 결과로 혼동행렬을 만드세요.
        # TODO 2: tn, fp, fn, tp 네 값으로 나누어 저장하세요.
        # TODO 3: 불량 Recall = tp / (tp + fn)을 직접 계산하세요.
        """,
        "2x2 혼동행렬에는 `ravel()`을 적용할 수 있습니다. 분모가 0인지도 확인하세요.",
        """
        rf_predictions = rf_model.predict(X_test_scaled)
        tn, fp, fn, tp = confusion_matrix(y_test, rf_predictions).ravel()
        manual_recall = tp / (tp + fn) if (tp + fn) else 0

        print(f'TN(정상을 정상): {tn}')
        print(f'FP(정상을 불량): {fp}')
        print(f'FN(불량을 정상으로 놓침): {fn}')
        print(f'TP(불량을 불량): {tp}')
        print(f'불량 Recall: {manual_recall:.3f}')
        """,
    )
    cells += exercise(
        "실습 3 · 예측 임계값과 Recall의 관계",
        "불량 판정 기준을 바꿀 때 Recall과 Precision이 어떻게 달라지는지 비교합니다.",
        """
        # TODO 1: 랜덤 포레스트의 불량 확률을 구하세요.
        # TODO 2: 임계값 0.3, 0.5, 0.7마다 예측값을 만드세요.
        # TODO 3: 각 임계값의 Precision과 Recall을 표로 정리하세요.
        """,
        "확률이 임계값 이상이면 1로 바꾸고 `precision_score`, `recall_score`를 계산합니다.",
        """
        from sklearn.metrics import precision_score, recall_score

        rf_probabilities = rf_model.predict_proba(X_test_scaled)[:, 1]
        threshold_rows = []
        for threshold in [0.3, 0.5, 0.7]:
            threshold_prediction = (rf_probabilities >= threshold).astype(int)
            threshold_rows.append({
                '임계값': threshold,
                'Precision': precision_score(y_test, threshold_prediction, zero_division=0),
                'Recall': recall_score(y_test, threshold_prediction, zero_division=0),
                '불량예측수': int(threshold_prediction.sum())
            })

        threshold_table = pd.DataFrame(threshold_rows).round(3)
        threshold_table
        """,
    )
    cells += exercise(
        "실습 4 · 두 모델을 같은 기준으로 비교하기",
        "정확도만 보지 않고 불량 Precision, Recall, F1을 한 표에서 비교합니다.",
        """
        # TODO 1: 로지스틱 회귀와 랜덤 포레스트의 예측값을 만드세요.
        # TODO 2: 각 모델의 Accuracy, Precision, Recall, F1을 계산하세요.
        # TODO 3: Recall이 높은 순서로 정렬하세요.
        """,
        "여러 모델을 리스트에 담아 반복하면 같은 계산 기준을 적용할 수 있습니다.",
        """
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

        comparison_rows = []
        for model_name, model in [
            ('로지스틱 회귀', lr_model),
            ('랜덤 포레스트', rf_model)
        ]:
            prediction = model.predict(X_test_scaled)
            comparison_rows.append({
                '모델': model_name,
                'Accuracy': accuracy_score(y_test, prediction),
                'Precision_불량': precision_score(y_test, prediction, zero_division=0),
                'Recall_불량': recall_score(y_test, prediction, zero_division=0),
                'F1_불량': f1_score(y_test, prediction, zero_division=0)
            })

        model_comparison = (
            pd.DataFrame(comparison_rows)
            .sort_values('Recall_불량', ascending=False)
            .round(3)
        )
        model_comparison
        """,
    )
    cells += exercise(
        "실습 5 · 놓친 불량 사례 살펴보기",
        "False Negative 행을 찾아 어떤 센서값을 추가로 점검할지 준비합니다.",
        """
        # TODO 1: y_test가 1이면서 랜덤 포레스트 예측이 0인 위치를 찾으세요.
        # TODO 2: 원래 X_test에서 해당 행을 선택하세요.
        # TODO 3: 놓친 불량 수와 센서값 일부를 출력하세요.
        """,
        "`(y_test == 1) & (예측 == 0)` 조건을 만들고 불리언 배열의 위치로 `X_test`를 선택합니다.",
        """
        false_negative_mask = (y_test.to_numpy() == 1) & (rf_predictions == 0)
        false_negative_cases = X_test.loc[false_negative_mask].copy()

        print(f'랜덤 포레스트가 놓친 불량: {len(false_negative_cases)}건')
        display_cols = top_k_cols[:5]
        if len(false_negative_cases) > 0:
            display(false_negative_cases[display_cols].head())
            print('이 행들은 원인 확정 대상이 아니라 추가 공정 점검 대상입니다.')
        else:
            print('현재 테스트 데이터에서는 놓친 불량이 없습니다.')
        """,
    )
    cells += [
        md(
            """
            ### 꼭 알아둘 데이터 누수

            실제 프로젝트에서는 **데이터를 학습용과 평가용으로 먼저 분리한 뒤** 다음 작업을
            학습 데이터에만 맞춰야 합니다.

            - 결측값을 채울 중앙값 계산
            - 중요한 센서 선택
            - 표준화 평균과 표준편차 계산

            평가 데이터의 정보를 미리 사용하면 모델 성능이 실제보다 좋아 보일 수 있습니다.
            AI에게 프로그램을 요청할 때도 이 순서를 명확히 적어 주는 것이 좋습니다.
            """,
            "beginner-practice",
        )
    ]
    cells += ai_prompt_cells(
        "불량 탐지 모델과 평가 리포트",
        """
        당신은 초보자에게 코드의 이유를 설명하는 반도체 데이터 분석가입니다.

        [역할]
        fab.csv로 정상/불량을 분류하고 불량을 놓치지 않는 데 초점을 둔 주피터 노트북 프로그램을 작성하세요.

        [입력 데이터]
        - 파일명: fab.csv
        - 타겟 열: Pass_Fail (-1=정상, 1=불량)
        - 나머지 숫자 열은 센서값이며 결측값과 상수 열이 포함될 수 있습니다.

        [구현 요구사항]
        1. 클래스 건수와 비율을 확인하고 정확도만 보면 안 되는 이유를 설명하세요.
        2. 데이터를 학습 80%, 테스트 20%로 stratify 분리하세요.
        3. 결측률 기준 열 제거, 중앙값 채우기, 상수 열 제거, SelectKBest, StandardScaler는
           반드시 학습 데이터에만 fit하고 테스트 데이터에는 transform만 하세요.
        4. 로지스틱 회귀와 랜덤 포레스트에 class_weight='balanced'를 적용하세요.
        5. Accuracy, 불량 Precision, 불량 Recall, 불량 F1, ROC-AUC를 같은 표로 비교하세요.
        6. 혼동행렬을 그리고 False Negative 수를 눈에 띄게 출력하세요.
        7. 기본 임계값 0.5에서 결과를 평가하고, 0.3과 0.7은 학습용 비교표로만 보여주세요.
        8. random_state=42를 사용하고 각 단계 앞에 초보자용 설명을 작성하세요.

        [결과물]
        - 위에서 아래로 실행 가능한 주피터 노트북 코드
        - model_comparison.csv
        - 모델별 혼동행렬과 ROC 곡선
        - 놓친 불량 사례의 상위 센서값 표
        - 어떤 모델을 선택할지 근거가 포함된 3문장 결론

        [검증]
        - 학습/테스트 행 수와 불량 건수를 출력하세요.
        - 전처리 객체가 테스트 데이터에 fit되지 않았음을 코드 주석으로 확인하세요.
        - 예측값 개수가 y_test 행 수와 같은지 assert로 검사하세요.
        - 결과를 '원인 규명'으로 과장하지 말고 추가 공정 검토가 필요하다고 표시하세요.
        """,
        "이 프롬프트의 핵심은 AI에게 모델 종류보다 평가 목적과 데이터 누수 방지 순서를 명확히 알려 주는 것입니다. 생성된 코드는 먼저 작은 셀로 나누어 실행하고, 테스트 데이터가 전처리 학습에 사용되지 않았는지 확인하세요.",
    )
    return cells


def ai_prompt_cells(project_name: str, prompt: str, note: str) -> list:
    prompt_markdown = (
        "### 복사해서 사용할 프롬프트\n\n"
        "```text\n"
        f"{dedent(prompt).strip()}\n"
        "```\n"
    )
    return [
        md(
            f"""
            ## AI와 함께 만드는 미니 프로젝트

            ### 프로젝트: {project_name}

            아래 프롬프트를 AI 도구에 붙여 넣으면 이번 노트북에서 배운 범위로 실제 프로그램을
            만들어 볼 수 있습니다. AI가 만든 코드를 한꺼번에 실행하지 말고, 셀별로 읽고 실행하며
            자신의 데이터 열 이름과 결과를 확인하세요.

            **프롬프트 사용 설명**

            {note}
            """,
            "ai-project",
        ),
        md(prompt_markdown, "ai-project", "ai-project-prompt"),
        md(
            """
            ### 결과 검토 체크리스트

            AI가 프로그램을 작성했다고 해서 결과가 자동으로 맞는 것은 아닙니다.

            - [ ] CSV 파일 경로와 열 이름이 실제 데이터와 같은가?
            - [ ] 원본 데이터를 복사한 뒤 정리했는가?
            - [ ] 처리 전후 행 수와 결측값 수가 설명 가능한가?
            - [ ] 그래프의 축, 단위, 범례가 데이터 의미와 맞는가?
            - [ ] 합격/불합격 숫자의 의미를 반대로 사용하지 않았는가?
            - [ ] 오류 메시지가 나오면 해당 셀만 읽고 원인을 설명할 수 있는가?
            - [ ] 분석 결과를 공정 원인으로 단정하지 않았는가?
            - [ ] 실제 회사 데이터라면 보안 규정을 지켰는가?

            마지막으로 AI에게 다음과 같이 요청해 보세요.

            > 위 코드를 한 셀씩 설명하고, 각 셀에서 초보자가 확인해야 할 출력값을 알려줘.
            """,
            "ai-project",
        ),
    ]


def make_existing_reference_cells_safe(notebook) -> None:
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        source = cell.source
        if source.startswith("# 그래프 그리기 (종류에 맞는 명령어 선택)"):
            cell.source = dedent(
                """
                # 아래는 그래프 명령어를 고를 때 보는 참고용 코드입니다.
                # 실제로 사용할 때 x, y, 값, 항목, 데이터 자리에 자신의 변수를 넣으세요.
                # plt.scatter(x, y)                 # 산점도
                # plt.plot(x, y)                    # 선 그래프
                # plt.bar(x, y)                     # 막대 그래프
                # plt.pie(값, labels=항목)          # 파이 차트
                # plt.boxplot([데이터])             # 박스 플롯
                # plt.title('제목')
                # plt.xlabel('x축 이름')
                # plt.ylabel('y축 이름')
                # plt.grid(True)
                # plt.show()

                print('그래프 명령어 요약: scatter, plot, bar, pie, boxplot')
                """
            ).strip() + "\n"

        if "fontprop = fm.FontProperties(fname='malgun.ttf')" in source:
            cell.source = source.replace(
                "fontprop = fm.FontProperties(fname='malgun.ttf')",
                "fontprop = fm.FontProperties(family='Malgun Gothic')",
            )


def insert_generated_cells(path: Path, generated_cells: list) -> None:
    notebook = nbformat.read(path, as_version=4)
    notebook.cells = [
        cell
        for cell in notebook.cells
        if cell.metadata.get("generated_by") != GENERATED_BY
    ]
    make_existing_reference_cells_safe(notebook)

    insert_at = len(notebook.cells)
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type == "markdown" and cell.source.strip().startswith("## 마무리"):
            insert_at = index
            break

    notebook.cells[insert_at:insert_at] = generated_cells
    nbformat.write(notebook, path)
    print(f"UPDATED {path.name}: {len(notebook.cells)} cells")


def main() -> None:
    targets = {
        "01_판다스_수업자료.ipynb": pandas_cells(),
        "05_반도체_공정_데이터분석.ipynb": semiconductor_eda_cells(),
        "06_실전_반도체_공정_데이터분석_강의자료.ipynb": semiconductor_ml_cells(),
    }
    for filename, cells in targets.items():
        insert_generated_cells(NOTEBOOK_DIR / filename, cells)


if __name__ == "__main__":
    main()
