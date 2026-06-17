# -*- coding: utf-8 -*-
"""
반도체_공정_샘플.csv 와 유사한 실습용 데이터 생성기.
- 대표 공정 컬럼 6개 + 측정시간(시간축) + 합격여부(타겟)
- 100행, 합격(1) 다수 / 불합격(0) 소수 (불균형)
- 결측값(빈 칸)과 중복 행을 일부 포함 → 강의의 3단계(결측·중복 처리) 실습 가능
"""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

N = 100               # 전체 행 수
FAIL_RATIO = 0.13     # 불합격 비율 (약 13%)

# (정상 평균, 정상 표준편차, 소수점 자리)
NORMAL = {
    "온도_섭씨":     (300.0, 4.0, 4),
    "압력_Pa":       (1014.0, 9.0, 4),
    "가스유량_slm":  (50.0, 2.0, 4),
    "전력_W":        (2000.0, 30.0, 4),
    "진공도_mTorr":  (5.0, 0.3, 4),
    "두께_nm":       (100.0, 2.0, 4),
}
COLS = list(NORMAL.keys())

# 불합격을 가르는 "핵심 판별 변수" — 원본 샘플처럼 불합격에서 값이 위로 치솟는다.
# (방향: +1 = 위로 이탈) 입문자가 EDA로 차이를 눈으로 확인할 수 있게 신호를 키운다.
KEY_FAIL = {"진공도_mTorr": +1, "두께_nm": +1, "전력_W": +1}

def gen_row(is_fail):
    """한 행의 센서값 생성. 불합격이면 핵심 변수를 정상 범위 밖으로 끌어올린다."""
    row = {}
    if is_fail:
        # 핵심 변수 중 2개 이상을 비정상으로 (뚜렷한 신호) + 가끔 일반 변수도 흔듦
        keys = list(KEY_FAIL)
        abnormal = set(random.sample(keys, random.randint(2, 3)))
        if random.random() < 0.4:
            abnormal |= {random.choice(COLS)}
    else:
        abnormal = set()
    for c in COLS:
        mu, sd, nd = NORMAL[c]
        if c in abnormal:
            mag = random.uniform(3.5, 6.5) * sd            # 3.5~6.5 표준편차 이탈
            direction = KEY_FAIL.get(c, random.choice([-1, 1]))
            val = mu + mag * direction + random.gauss(0, sd)
        else:
            val = random.gauss(mu, sd)
        row[c] = round(val, nd)
    return row

# 합격/불합격 라벨 배치 (합격=1, 불합격=0)
n_fail = round(N * FAIL_RATIO)
labels = [1] * (N - n_fail) + [0] * n_fail
random.shuffle(labels)

# 측정시간: 2024-05-01 부터 평균 6시간 간격으로 증가
t = datetime(2024, 5, 1, 8, 0)
rows = []
for lab in labels:
    t += timedelta(hours=random.randint(1, 11))
    r = {"측정시간": t.strftime("%Y-%m-%d %H:%M")}
    r.update(gen_row(lab == 0))
    r["합격여부"] = lab
    rows.append(r)

# 중복 행 3개 삽입 (강의의 중복 제거 실습용) — 합격 행을 복제해 무작위 위치에 끼워넣음
pass_idx = [i for i, r in enumerate(rows) if r["합격여부"] == 1]
for src in random.sample(pass_idx, 3):
    dup = dict(rows[src])
    rows.insert(random.randint(0, len(rows)), dup)

# 결측값 삽입: 센서 6개 컬럼에 한해 무작위로 약 4% 칸을 비움 (합격여부/측정시간 제외)
total_cells = len(rows) * len(COLS)
n_missing = int(total_cells * 0.04)
for _ in range(n_missing):
    ri = random.randrange(len(rows))
    ci = random.choice(COLS)
    rows[ri][ci] = ""   # 빈 칸 = 결측값(NaN)

# CSV 저장 (Excel/pandas 한글 호환을 위해 utf-8-sig)
header = ["측정시간"] + COLS + ["합격여부"]
out = r"D:\Githubs\DataAnaysis_WS\kitae-data\Web\반도체_공정_샘플_미니.csv"
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=header)
    w.writeheader()
    for r in rows:
        w.writerow(r)

print(f"생성 완료: {out}")
print(f"  행 수(헤더 제외): {len(rows)}")
print(f"  합격(1): {sum(1 for r in rows if r['합격여부']==1)} / 불합격(0): {sum(1 for r in rows if r['합격여부']==0)}")
print(f"  결측 셀 삽입: {n_missing} / 중복 행 삽입: 3")
print(f"  컬럼: {header}")
