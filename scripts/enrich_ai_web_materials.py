"""Add service-neutral AI learning sections to the three web lessons."""

from __future__ import annotations

from html import escape
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "Web"
START = "<!-- AI_EXTENSION_START -->"
END = "<!-- AI_EXTENSION_END -->"


COURSES = {
    "판다스_수업자료.html": {
        "accent": "var(--primary)",
        "improve_accent": "var(--accent)",
        "project_accent": "var(--primary-light)",
        "surface": "var(--surface)",
        "muted_surface": "var(--surface2)",
        "learning": """
            나는 pandas를 처음 배우는 학습자입니다. DataFrame 구조 확인, 열과 행 선택,
            조건 필터링, 결측값·중복 처리, groupby와 기본 그래프에서 확인 문제를 5개 내주세요.
            한 번에 한 문제만 내고 내가 답할 때까지 정답을 공개하지 마세요.
            답을 평가한 뒤 쉬운 설명, 5행 이하 예제, 다음 문제를 제공하세요.
            반도체 공정의 온도, 압력, 두께, 합격여부 예시를 사용하고 마지막에 취약 개념을 정리하세요.
        """,
        "improvement": """
            아래 pandas 코드를 초보자 관점에서 검토하세요.
            CSV 경로와 필수 열, 원본 보존, 결측·중복 처리, 조건식 괄호,
            변수 이름, 중복 코드, 그래프 축과 단위를 확인하세요.
            pandas와 matplotlib 범위를 벗어나는 머신러닝이나 복잡한 클래스는 추가하지 마세요.
            문제 목록, 최소 수정 코드, 변경 이유, 작은 가상 데이터 검증 코드 순서로 답하세요.

            [검토할 코드]
            여기에 코드를 붙여 넣으세요.
        """,
        "projects": [
            (
                "Lot 검색·정렬 도구",
                """
                    pandas로 반도체 Lot 검색 도구를 만들어 주세요.
                    공정명, 최소·최대 온도, 정렬 기준을 변수로 설정하고 조건에 맞는 행을 선택하세요.
                    두께편차가 큰 순서의 상위 10개 Lot와 공정별 건수를 출력하고
                    lot_search_result.csv로 저장하세요. 필수 열 확인과 테스트 3개도 포함하세요.
                """,
            ),
            (
                "공정 기준 이탈 알림표",
                """
                    pandas와 matplotlib로 온도·압력·두께 기준 이탈 알림표를 만들어 주세요.
                    사용자가 하한과 상한을 지정하면 이탈 여부와 이탈 사유 열을 추가하세요.
                    이탈 Lot 목록, 변수별 이탈 건수, 공정별 이탈률과 막대그래프를 만들고
                    process_alerts.csv로 저장하세요. 원본은 copy()로 보존하세요.
                """,
            ),
        ],
    },
    "반도체_공정_데이터분석.html": {
        "accent": "var(--blue)",
        "improve_accent": "var(--orange)",
        "project_accent": "var(--green)",
        "surface": "var(--bg)",
        "muted_surface": "var(--bg2)",
        "learning": """
            나는 반도체 공정 EDA를 복습하고 있습니다. 결측률, 중복, IQR 이상값 후보,
            groupby 비교, 상관관계, 히스토그램·박스플롯·히트맵에서 문제를 6개 내주세요.
            한 번에 한 문제만 내고 답을 먼저 공개하지 마세요.
            내 답의 코드와 해석을 함께 평가하고, 상관관계와 원인을 구분하도록 질문하세요.
            틀린 답에는 수정 코드, 예상 출력 형태, 안전한 공정 해석을 제공하세요.
        """,
        "improvement": """
            아래 반도체 공정 EDA 코드를 검토해 최소한으로 개선하세요.
            원본 보존, 결측·중복 처리, 숫자 열 선택, IQR 후보 처리,
            합격/불합격 라벨, groupby 비교, 그래프 축·단위, 과장된 인과 해석을 확인하세요.
            머신러닝은 추가하지 말고 문제 목록, 수정 코드, 변경 이유,
            처리 전후 행 수·결측값·타겟 분포 검증 코드 순서로 답하세요.

            [검토할 코드]
            여기에 코드를 붙여 넣으세요.
        """,
        "projects": [
            (
                "센서별 이상값 후보 보고서",
                """
                    반도체_공정_샘플.csv의 숫자 센서별 Q1, Q3, IQR, 하한, 상한,
                    이상값 후보 건수와 비율을 표로 만드세요. 후보 비율 상위 5개를 출력하고
                    상위 3개 센서의 박스플롯을 그린 뒤 sensor_outlier_summary.csv로 저장하세요.
                    이상값을 자동 삭제하지 않는 이유와 직접 계산 검증도 포함하세요.
                """,
            ),
            (
                "합격·불합격 비교 리포트",
                """
                    반도체_공정_샘플.csv에서 판정별 평균·중앙값·표준편차와 표본 수를 계산하세요.
                    평균 차이가 큰 상위 5개 센서를 표와 박스플롯으로 보여주고
                    pass_fail_comparison.csv로 저장하세요. 차이를 공정 원인으로 단정하지 않는
                    3문장 결론과 다음 점검 사항을 작성하세요.
                """,
            ),
        ],
    },
    "실전_반도체_공정_데이터분석_강의자료.html": {
        "accent": "var(--purple)",
        "improve_accent": "var(--orange)",
        "project_accent": "var(--green)",
        "surface": "var(--bg)",
        "muted_surface": "var(--bg2)",
        "learning": """
            나는 반도체 불량 분류를 복습하고 있습니다. 클래스 불균형, stratify,
            fit과 transform, 데이터 누수, 혼동행렬, 불량 Precision·Recall,
            예측 임계값에서 확인 문제를 6개 내주세요.
            한 번에 한 문제만 내고 답을 먼저 공개하지 마세요.
            작은 혼동행렬이나 10줄 이하 코드를 사용하고 False Negative 관점에서 설명하세요.
        """,
        "improvement": """
            아래 불량 분류 코드를 데이터 누수와 평가 오류 중심으로 검토하세요.
            Pass_Fail 매핑, stratify 분할, 전처리 fit 범위, class_weight,
            random_state, 불량 Precision·Recall·F1·ROC-AUC, False Negative를 확인하세요.
            고급 모델이나 복잡한 튜닝은 추가하지 말고 심각도별 문제,
            최소 수정 코드, 처리 순서 비교, assert 검증 코드 순서로 답하세요.

            [검토할 코드]
            여기에 코드를 붙여 넣으세요.
        """,
        "projects": [
            (
                "불량 판정 임계값 비교 도구",
                """
                    y_valid와 y_valid_prob를 사용해 임계값 0.2부터 0.8까지 비교하세요.
                    각 임계값의 Precision, Recall, F1, FP, FN, 불량 예측 수를 표로 만들고
                    Precision과 Recall 선 그래프를 그리세요. 임계값은 테스트가 아닌 검증 데이터에서
                    선택해야 한다는 설명과 결과 검증 코드를 포함하세요.
                """,
            ),
            (
                "놓친 불량 사례 점검 도구",
                """
                    X_test, y_test, y_pred로 False Negative 사례를 찾으세요.
                    놓친 불량, 탐지한 불량, 정상 데이터의 센서 중앙값을 비교하고 차이가 큰 센서
                    상위 10개를 표로 만드세요. 놓친 사례를 CSV로 저장하고 표본이 0일 때도
                    오류 없이 안내하며 결과를 원인으로 단정하지 마세요.
                """,
            ),
        ],
    },
}


def prompt_box(title: str, prompt: str) -> str:
    prompt_text = escape(dedent(prompt).strip())
    return f"""
      <div class="code-wrap" style="margin-top:14px;">
        <div class="code-header">
          <span class="code-title">{escape(title)}</span>
          <button class="copy-btn" onclick="copyCode(this)">복사</button>
        </div>
        <pre><code>{prompt_text}</code></pre>
      </div>
    """


def make_snippet(course: dict) -> str:
    projects = course["projects"]
    project_boxes = "\n".join(
        prompt_box(f"추가 프로젝트 {number} · {title}", prompt)
        for number, (title, prompt) in enumerate(projects, 1)
    )
    return dedent(
        f"""
        {START}
        <section id="ai-learning-check" style="margin:28px 0; padding:24px; border:1px solid var(--border); border-left:4px solid {course['accent']}; border-radius:10px; background:{course['surface']};">
          <div class="section-title">AI로 학습 내용 확인하기</div>
          <div class="section-desc">정답을 바로 받기보다 AI가 한 문제씩 질문하게 해서 이해도를 확인합니다.</div>
          {prompt_box('AI 튜터 프롬프트', course['learning'])}
          <div style="margin-top:14px; padding:14px; border-radius:8px; background:{course['muted_surface']}; font-size:13px; line-height:1.7;">
            <strong>확인 방법</strong><br>
            강의 노트를 보지 않고 먼저 답한 뒤 원래 예제와 비교하세요. AI가 제시한 코드는 작은 가상 데이터로 직접 실행하고, 함수·열 이름·라벨 의미가 맞는지 확인합니다.
          </div>
        </section>

        <section id="ai-code-improvement" style="margin:28px 0; padding:24px; border:1px solid var(--border); border-left:4px solid {course['improve_accent']}; border-radius:10px; background:{course['surface']};">
          <div class="section-title">AI로 작성한 프로그램 개선하기</div>
          <div class="section-desc">현재 강의 범위 안에서 오류와 가독성을 점검하고, 수정 이유와 검증 코드까지 요청합니다.</div>
          {prompt_box('프로그램 개선 프롬프트', course['improvement'])}
          <ol style="margin:14px 0 0 20px; line-height:1.8; font-size:13px;">
            <li>원본 코드를 남기고 복사본에서 수정 코드를 실행합니다.</li>
            <li>AI가 바꾼 줄과 이유를 먼저 읽습니다.</li>
            <li>행 수, 결측값 수, 타겟 분포처럼 유지되어야 할 값을 비교합니다.</li>
            <li>이해하지 못한 고급 문법은 현재 강의 수준으로 다시 작성해 달라고 요청합니다.</li>
          </ol>
        </section>

        <section id="ai-extra-projects" style="margin:28px 0; padding:24px; border:1px solid var(--border); border-left:4px solid {course['project_accent']}; border-radius:10px; background:{course['surface']};">
          <div class="section-title">AI 프롬프트로 도전하는 추가 미니 프로젝트</div>
          <div class="section-desc">현재 강의에서 배운 기능을 새로운 반도체 데이터 문제에 조합해 봅니다.</div>
          {project_boxes}
          <div style="margin-top:16px; padding:15px; border:1px solid rgba(188,76,0,.35); border-radius:8px; background:rgba(188,76,0,.06); font-size:13px; line-height:1.75;">
            <strong>AI 결과 검증과 보안</strong><br>
            가상·비식별 데이터로 먼저 실행하고 원본 파일을 보존하세요. 처리 전후 행 수, 결측값 수, 라벨 분포를 비교하고 상관관계나 모델 중요도를 공정 원인으로 단정하지 않습니다. 회사의 장비명, 레시피값, Lot 식별자는 외부 AI 서비스에 입력하지 않습니다.
          </div>
        </section>
        {END}
        """
    ).strip()


def upsert(path: Path, snippet: str, anchor: str) -> None:
    text = path.read_text(encoding="utf-8")
    if START in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        text = before.rstrip() + "\n\n" + after.lstrip()

    position = text.rfind(anchor)
    if position < 0:
        raise ValueError(f"삽입 위치를 찾을 수 없습니다: {path.name} / {anchor}")

    updated = text[:position].rstrip() + "\n\n" + snippet + "\n\n" + text[position:]
    path.write_text(updated, encoding="utf-8")
    print(f"UPDATED {path.name}")


def main() -> None:
    for filename, course in COURSES.items():
        anchor = "</main>" if filename == "판다스_수업자료.html" else "</div><!-- /content -->"
        upsert(WEB_DIR / filename, make_snippet(course), anchor)


if __name__ == "__main__":
    main()
