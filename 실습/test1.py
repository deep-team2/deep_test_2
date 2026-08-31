import pandas as pd
import numpy as np

def 평균(xs):
    return sum(xs) / len(xs)

def 분산(xs):
    m = 평균(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)

def 표준편차(xs):
    return 분산(xs) ** 0.5

df = pd.read_csv("13_제조센서_전처리.csv", encoding="utf-8-sig")

vib = df["vib"].dropna().tolist()

vib_avg = round(평균(vib), 4)
vib_var = round(분산(vib), 4)
vib_std = round(표준편차(vib), 4)

print("vib 직접:", vib_avg, vib_var, vib_std)
print("vib numpy:", round(np.mean(vib), 4), round(np.var(vib), 4), round(np.std(vib), 4))
print("vib 일치:", abs(평균(vib) - np.mean(vib)) < 1e-9)

press = df["press"].dropna().tolist()
press_avg = round(평균(press), 4)
press_var = round(분산(press), 4)
press_std = round(표준편차(press), 4)

print("press 직접:", press_avg, press_var, press_std)
print("press numpy:", round(np.mean(press), 4), round(np.var(press), 4), round(np.std(press), 4))
print("press 일치:", abs(표준편차(press) - np.std(press)) < 1e-9)
