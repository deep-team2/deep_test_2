import numpy as np
import pandas as pd

df = pd.read_csv("설비배치1.csv", encoding="utf-8-sig")
센서 = ["온도", "진동", "회전수", "압력"]


q1 = df["압력"].quantile(0.25)
q3 = df["압력"].quantile(0.75)
iqr = q3 - q1

lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

# print(round(lower, 2), round(upper, 2))
mask = (df["압력"] < lower) | (df["압력"] > upper)

print(round(lower, 2), round(upper, 2))
print(mask.sum())
print(df.loc[mask, ["생산라인", "압력"]])
outliers = df.loc[mask].copy()
# print(mask.sum())
# print(df.loc[mask, "생산라인"].value_counts().to_dict())


# # 문제 8
# before_count = df["생산라인"].value_counts().sort_index().to_dict()
# print(before_count)

# df = df.loc[~mask].reset_index(drop=True)

# after_count = df["생산라인"].value_counts().sort_index().to_dict()
# print(after_count)
# print(df.shape)


# # 문제 9
# sensor_min = df[센서].min()
# sensor_max = df[센서].max()

# scaled = (df[센서] - sensor_min) / (sensor_max - sensor_min)

# print(scaled.min().round(3).to_dict())
# print(scaled.max().round(3).to_dict())
# print(scaled.mean().round(3).to_dict())

# normalized_result = df[["검사일시", "생산라인"]].copy()

# normalized_result[센서] = scaled.round(4)

# normalized_result.to_csv(
#     "정규화_멘티.csv",
#     index=False,
#     encoding="utf-8-sig",
# )

# normalized_check = pd.read_csv(
#     "정규화_멘티.csv",
#     encoding="utf-8-sig",
# )

# print(normalized_check.shape)


# # 문제 10
# line_map = {
#     "A라인": 0,
#     "B라인": 1,
#     "C라인": 2,
# }

# df["라인코드"] = df["생산라인"].map(line_map)

# result_cols = [
#     "검사일시",
#     "생산라인",
#     "라인코드",
#     "온도",
#     "진동",
#     "회전수",
#     "압력",
#     "판정",
# ]

# clean_result = df[result_cols].copy()

# clean_result.to_csv(
#     "정제결과_멘티.csv",
#     index=False,
#     encoding="utf-8-sig",
# )

# clean_check = pd.read_csv(
#     "정제결과_멘티.csv",
#     encoding="utf-8-sig",
# )

# print(
#     clean_check.shape,
#     clean_check.isna().sum().sum(),
#     clean_check.duplicated().sum(),
# )

# print(clean_check.columns.tolist())

import pandas as pd
import numpy as np

raw = pd.read_csv("설비배치1.csv", encoding="utf-8-sig")  # 원본
men = pd.read_csv("정제결과_멘티.csv", encoding="utf-8-sig")  # 멘티 결과
men_norm = pd.read_csv("정규화_멘티.csv", encoding="utf-8-sig")
sensor = ["온도", "진동", "회전수", "압력"]
key = ["검사일시", "생산라인", "설비번호"]

print("=" * 30, "문제 1", "=" * 30)
df = raw.drop_duplicates().reset_index(drop=True)  # 원본에서 완전 중복만 제거
# print(df.shape[0])
print(raw.shape[0], men.shape[0], men_norm.shape[0])  # 세 표의 행 수

a = (
    df["생산라인"].value_counts().sort_index()
)  # 완전 중복 제거한 표에서 생산라인별 행 수
# print(a)
b = men["생산라인"].value_counts().sort_index()  # 멘티 생산라인별 행 수
# print(b)
# mean 은 기본적으로 Null 제거하고 계산
df_mean = df.groupby("생산라인")["온도"].mean()  # 생산라인별 원본 온도 평균
# print(df_mean)

men_mean = men.groupby("생산라인")["온도"].mean()  # 생산라인별 멘티 온도 평균
# print(men_mean)

diff_mean = men_mean - df_mean  # 멘티, 원본 차이
print(diff_mean)

temp = pd.DataFrame({"원본": df_mean, "멘티": men_mean, "차이": diff_mean})  # 표 생성
print(temp.round(2))

print("결과 비교", a.compare(b))  # 원본과 멘티 결과 비교
# 생산라인
# C라인   60.0   57.0 -> C라인 행이 3 감소

comp = ["검사일시", "생산라인"]  # 한 묶음의 비교 기준

df_index = df.set_index(comp)
print("결과 확인", df_index)
men_index = men.set_index(comp)

miss = df_index.loc[
    ~df_index.index.isin(men_index.index)
]  # 원본에 있지만 멘티결과에서 사라진 행이 어느 생산라인의 기록인지 확인

print(miss.reset_index())
print(diff_mean[diff_mean >= 0.5].round(2))
# A 라인이고 0.55 올라감

"""
C라인만 3행이 사라졌는데 그 이유는 IQR 울타리를 초과했기 때문이다.
"""

print(outliers[["생산라인", "압력"]])


print("=" * 30, "문제 2", "=" * 30)

key_du = df.duplicated(subset=key, keep=False)
du = df.loc[key_du, key + ["온도", "압력"]].sort_values(key)
print(du)  # 온도 압력까지 붙여 출력


du_k = df.groupby(key).size()
du_k = du_k[du_k > 1]
print(du_k.shape[0])


result = df.drop_duplicates(subset=key, keep="first").reset_index(
    drop=True
)  # 앞의 것만 남기고 정리
print(
    result.shape, result["생산라인"].value_counts().sort_index().to_dict()
)  # 표 크기, 라인별 행 수

# # 값이 0.03 다르면 컴퓨터는 다른 행으로 보지만 현실에서는 같은 행으로 본다. 같은 시간 같은 설비를 검사했으므로
# # 중복이 발생했다고 할 수 있다, 0.03의 차이가 있었고 그대로 두면 평균이 근소하게 달라진다.

print("=" * 30, "문제 3", "=" * 30)


z_score = abs((result["온도"] - result["온도"].mean()) / result["온도"].std(ddof=0))
print((z_score > 2.5).sum())
a = result.groupby("생산라인")["온도"]
a_mean = a.transform("mean")
a_std = a.transform("std", ddof=0)
z = abs((result["온도"] - a_mean) / a_std)
print((z > 2.5).sum())


error_row = result.loc[
    (z > 2.5),
    ["검사일시", "생산라인", "설비번호", "온도"],
].sort_values(["생산라인"])

print(error_row)


print(result.groupby("생산라인")["온도"].mean().round(2))
# # 온도 73.5도는 평균이 73.35도인 A라인에서는 정상적인 값이지만, 평균이 94.57도인 C라인에서는 이상값으로 본다.
# 라인별로 평균 다름, 라인 세개를 하나로 보고 처리하면 최종 결과 이상해짐

print("=" * 30, "문제 4", "=" * 30)

mwo = result.groupby("생산라인")["온도"].mean()
# 이상값을 제외
moo = result.loc[~(z > 2.5)].groupby("생산라인")["온도"].mean()

mean_compare = pd.DataFrame(
    {
        "이상값 포함": mwo,
        "이상값 제외": moo,
        "차이": abs(mwo - moo),
    }
)

print(mean_compare.round(2))

c = result.copy()
c["진동"] = pd.to_numeric(
    c["진동"],
    errors="coerce",
)
temp_fill = c["생산라인"].map(moo)

c["온도"] = c["온도"].fillna(temp_fill)


for col in ["압력", "진동"]:
    line_median = c.groupby("생산라인")[col].transform("median")
    c[col] = c[col].fillna(line_median)

print(c[센서].isna().sum().sum())

clean_mean = c.groupby("생산라인")["온도"].mean().round(2)
print(clean_mean)

men_mean = men.groupby("생산라인")["온도"].mean().round(2)
print(men_mean)
# 결측 채우기 전 이상값부터 봐야하는 이유는 이상값이 평균 왜곡하고 왜곡된 평균으로 결측값 채우면 이것 또한 왜곡된 데이터
print("=" * 30, "문제 5", "=" * 30)


def find_pressure_outlier(data):
    line_mean = data.groupby("생산라인")["압력"].mean()

    line_std = data.groupby("생산라인")["압력"].std(ddof=0)

    mean_for_row = data["생산라인"].map(line_mean)
    std_for_row = data["생산라인"].map(line_std)

    z = abs((data["압력"] - mean_for_row) / std_for_row)

    return z > 3


def c_std(data):
    c_pressure = data.loc[
        data["생산라인"] == "C라인",
        "압력",
    ]

    return c_pressure.std(ddof=0)


print("1차 처리 전 C라인 표준편차:", round(c_std(c), 3))

mask1 = find_pressure_outlier(c)

print("1차 이상값:", mask1.sum())
print(c.loc[mask1, ["생산라인", "압력"]])

# 현재 라인별 압력 중앙값
line_median = c.groupby("생산라인")["압력"].median()

median_for_row = c["생산라인"].map(line_median)

# 이상값을 해당 라인의 중앙값으로 변경
c.loc[mask1, "압력"] = median_for_row[mask1]

print("1차 처리 후 C라인 표준편차:", round(c_std(c), 3))


mask2 = find_pressure_outlier(c)

print("2차 이상값:", mask2.sum())
print(c.loc[mask2, ["생산라인", "압력"]])

line_median = c.groupby("생산라인")["압력"].median()

median_for_row = c["생산라인"].map(line_median)

c.loc[mask2, "압력"] = median_for_row[mask2]

mask3 = find_pressure_outlier(c)

print("3차 이상값:", mask3.sum())
print(c.loc[mask3, ["생산라인", "압력"]])


print(c["생산라인"].value_counts().sort_index().to_dict())

# 큰 이상값 하나가 표준편차를 부풀려서 작은 이상값을 정상처럼 보이게 할 수 있으니 이상값 처리 후 다시 탐지해야 한다

mentor_scaled = (
    (c[sensor] - c[sensor].min()) / (c[sensor].max() - c[sensor].min())
).round(4)

mentor_norm = c[["검사일시", "생산라인"]].copy()

mentor_norm[sensor] = mentor_scaled
mentor_norm["key"] = mentor_norm["검사일시"].astype(str) + "_" + mentor_norm["생산라인"]

men_norm["key"] = men_norm["검사일시"].astype(str) + "_" + men_norm["생산라인"]
mentee_part = men_norm[["key"] + sensor].rename(
    columns={col: f"{col}_멘티" for col in sensor}
)

mentor_part = mentor_norm[["key", "생산라인"] + sensor].rename(
    columns={col: f"{col}_멘토" for col in sensor}
)

compare = mentee_part.merge(
    mentor_part,
    on="key",
    how="inner",
)
print(compare.shape[0])
for col in sensor:
    compare[f"{col}_차이"] = abs(compare[f"{col}_멘티"] - compare[f"{col}_멘토"])

max_diff = {col: round(compare[f"{col}_차이"].max(), 4) for col in sensor}

print(max_diff)

over_count = {col: int((compare[f"{col}_차이"] > 0.05).sum()) for col in sensor}

print(over_count)

top4 = compare.sort_values(
    "온도_차이",
    ascending=False,
).head(4)

print(top4[["key", "온도_멘티", "온도_멘토", "온도_차이"]])

line_temp_mean = compare.groupby("생산라인")[["온도_멘티", "온도_멘토"]].mean().round(3)

print(line_temp_mean)
# 같은 A라인 기록인데 0.1111이 아니라 0.5363으로 찍힌 이유는 온도 결측값을 A라인 평균이 아닌 전체 데이터 평균으로 채워 라인별 온도 특성이 사라졌기 때문이다.


np.random.seed(6)

order = np.random.permutation(len(c))

shuffled = c.iloc[order].reset_index(drop=True)

n = len(shuffled)

train_end = int(n * 0.6)
valid_end = int(n * 0.8)

train = shuffled.iloc[:train_end].copy()
valid = shuffled.iloc[train_end:valid_end].copy()
test = shuffled.iloc[valid_end:].copy()

print(train.shape, valid.shape, test.shape)


# 학습 데이터 기준
train_base = pd.DataFrame(
    {
        "min": train[센서].min(),
        "max": train[센서].max(),
    }
)
all_base = pd.DataFrame(
    {
        "min": c[센서].min(),
        "max": c[센서].max(),
    }
)

base_compare = pd.concat(
    {
        "학습 기준": train_base,
        "전체 기준": all_base,
    },
    axis=1,
)

print(base_compare)


train_base.to_csv(
    "스케일링기준.csv",
    encoding="utf-8-sig",
)

test_scaled_all = (test[센서] - all_base["min"]) / (all_base["max"] - all_base["min"])

test_scaled_train = (test[센서] - train_base["min"]) / (
    train_base["max"] - train_base["min"]
)

out_all = ((test_scaled_all < 0) | (test_scaled_all > 1)).sum().sum()

out_train = ((test_scaled_train < 0) | (test_scaled_train > 1)).sum().sum()

print(out_all, out_train)

edge_all = ((test_scaled_all == 0) | (test_scaled_all == 1)).sum().sum()

edge_train = ((test_scaled_train == 0) | (test_scaled_train == 1)).sum().sum()

print(edge_all, edge_train)

print(test_scaled_train.max().round(3).to_dict())


import numpy as np
import pandas as pd

센서 = ["온도", "진동", "회전수", "압력"]

base = pd.read_csv(
    "스케일링기준.csv",
    index_col=0,
    encoding="utf-8-sig",
)

batch2 = pd.read_csv(
    "설비배치2.csv",
    encoding="utf-8-sig",
)

batch2[센서] = batch2[센서].apply(
    pd.to_numeric,
    errors="coerce",
)


print(batch2["생산라인"].value_counts().sort_index().to_dict())

known_lines = set(result["생산라인"].unique())

new_line_mask = ~batch2["생산라인"].isin(known_lines)

new_line_names = sorted(batch2.loc[new_line_mask, "생산라인"].unique().tolist())

print(new_line_mask.sum(), new_line_names)


def scale_data(data, base):
    minimum = base["min"]
    maximum = base["max"]

    return (data[센서] - minimum) / (maximum - minimum)


batch2_scaled = scale_data(batch2, base)

temp_scaled = pd.DataFrame(
    {
        "생산라인": batch2["생산라인"],
        "온도": batch2_scaled["온도"],
    }
)

print(temp_scaled.groupby("생산라인")["온도"].agg(["min", "max"]).round(3))


line_map = {
    "A라인": 0,
    "B라인": 1,
    "C라인": 2,
}

batch2["라인코드"] = batch2["생산라인"].map(line_map)

print(batch2["라인코드"].isna().sum())

new_line_data = batch2.loc[new_line_mask].copy()

batch2_known = batch2.loc[~new_line_mask].copy().reset_index(drop=True)

batch2_known_scaled = scale_data(batch2_known, base)


out_mask = (batch2_known_scaled < 0) | (batch2_known_scaled > 1)

print(out_mask.sum().sum())

range_table = pd.DataFrame(
    {
        "min": batch2_known_scaled.min(),
        "max": batch2_known_scaled.max(),
    }
)

print(range_table.round(3))


batch2_known_scaled_again = scale_data(
    batch2_known,
    base,
)

print(batch2_known_scaled.equals(batch2_known_scaled_again))

c.to_csv(
    "정제결과_최종.csv",
    index=False,
    encoding="utf-8-sig",
)

final_check = pd.read_csv(
    "정제결과_최종.csv",
    encoding="utf-8-sig",
)

print(final_check.shape)
print(final_check.isna().sum().sum())

print(final_check["생산라인"].value_counts().sort_index().to_dict())
