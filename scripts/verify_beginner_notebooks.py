"""Verify the beginner practice sections in the generated course notebooks."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "강의자료_ipynb"

EXPECTED = {
    "01_판다스_수업자료.ipynb": {"exercises": 5, "solutions": 5},
    "05_반도체_공정_데이터분석.ipynb": {"exercises": 5, "solutions": 5},
    "06_실전_반도체_공정_데이터분석_강의자료.ipynb": {
        "exercises": 5,
        "solutions": 5,
    },
}


def source_text(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def verify_notebook(path: Path, expected: dict[str, int]) -> None:
    raw = json.loads(path.read_text(encoding="utf-8"))
    notebook = nbformat.from_dict(raw)
    nbformat.validate(notebook)

    cells = notebook.cells
    markdown = "\n".join(
        source_text(cell) for cell in cells if cell.cell_type == "markdown"
    )
    assert "## 초보자 필수 보강 실습" in markdown, f"{path.name}: 보강 실습 제목 없음"
    assert "## AI와 함께 만드는 미니 프로젝트" in markdown, f"{path.name}: AI 프로젝트 없음"
    assert "결과 검토 체크리스트" in markdown, f"{path.name}: AI 결과 검토 안내 없음"

    exercise_cells = []
    solution_cells = []
    prompt_cells = []

    for index, cell in enumerate(cells):
        tags = set(cell.metadata.get("tags", []))
        if "beginner-exercise" in tags:
            exercise_cells.append(cell)
        if "beginner-solution" in tags:
            solution_cells.append(cell)
        if "ai-project-prompt" in tags:
            prompt_cells.append(cell)

        if cell.cell_type == "code":
            ast.parse(source_text(cell), filename=f"{path.name}:cell-{index}")

    assert len(exercise_cells) >= expected["exercises"], (
        f"{path.name}: 연습 셀 {len(exercise_cells)}개, "
        f"최소 {expected['exercises']}개 필요"
    )
    assert len(solution_cells) >= expected["solutions"], (
        f"{path.name}: 정답 셀 {len(solution_cells)}개, "
        f"최소 {expected['solutions']}개 필요"
    )
    assert len(prompt_cells) == 1, f"{path.name}: AI 프롬프트 셀은 1개여야 함"

    prompt = source_text(prompt_cells[0])
    assert "\n```text\n" in prompt, f"{path.name}: AI 프롬프트 코드 블록 형식 오류"
    for heading in ("역할", "입력 데이터", "구현 요구사항", "결과물", "검증"):
        assert heading in prompt, f"{path.name}: AI 프롬프트에 '{heading}' 항목 없음"


def main() -> None:
    for filename, expected in EXPECTED.items():
        path = NOTEBOOK_DIR / filename
        assert path.exists(), f"노트북 없음: {path}"
        verify_notebook(path, expected)
        print(f"OK {filename}")

    for csv_name in ("반도체_공정_샘플.csv", "fab.csv"):
        csv_path = NOTEBOOK_DIR / csv_name
        assert csv_path.exists() and csv_path.stat().st_size > 0, f"데이터 파일 없음: {csv_name}"
        print(f"OK {csv_name}")


if __name__ == "__main__":
    main()
