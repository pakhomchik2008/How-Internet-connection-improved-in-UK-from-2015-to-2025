'''import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# загрузка данных
data = pd.read_excel("medata.xlsx")

# выбираем переменные
x = data["4G5G_105_geo_out_all"]
y = data["4G5G_95_geo_out_all"]

# mean
mean_x = x.mean()
mean_y = y.mean()

# standard deviation
sd_x = x.std()
sd_y = y.std()

# t-test
t_stat, p_value = stats.ttest_rel(x, y)

# вывод результатов
print("----- Descriptive Statistics -----")
print(f"Mean 105 dBm: {mean_x:.2f}")
print(f"Mean 95 dBm: {mean_y:.2f}")

print(f"SD 105 dBm: {sd_x:.2f}")
print(f"SD 95 dBm: {sd_y:.2f}")

print("\n----- T-test -----")
print(f"T-statistic: {t_stat:.2f}")
print(f"P-value: {p_value:.5f}")

if p_value < 0.05:
    print("Result: statistically significant difference")
else:
    print("Result: no significant difference")

# boxplot
plt.boxplot([x, y], labels=["105 dBm", "95 dBm"])

plt.title("4G/5G Coverage Comparison")
plt.ylabel("Coverage (%)")

plt.show()'''

'''
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("medata.xlsx")

nations = data[data["Level"] == "Nation"]

plt.bar(nations["Location"], nations["4G5G_105_geo_out_all"])

plt.title("4G/5G Coverage by Nation")
plt.xlabel("Nation")
plt.ylabel("Coverage %")

plt.show()'''

'''
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("medata.xlsx")

nations = data[data["Level"] == "Nation"]

x = nations["Location"]

y1 = nations["4G5G_105_geo_out_all"]
y2 = nations["4G5G_95_geo_out_all"]

plt.plot(x, y1, marker='o', label="105 dBm")
plt.plot(x, y2, marker='o', label="95 dBm")

plt.title("4G/5G Coverage Comparison")
plt.xlabel("Nation")
plt.ylabel("Coverage (%)")

plt.legend()

plt.show()'''


'''
import pandas as pd
import matplotlib.pyplot as plt

# загрузка данных
data = pd.read_excel("medata.xlsx")

# берем только nations
nations = data[data["Level"] == "Nation"]

x = nations["Location"]
y1 = nations["4G5G_105_geo_out_all"]
y2 = nations["4G5G_95_geo_out_all"]

# -------- BAR CHART --------
plt.figure()

plt.bar(x, y1)

plt.title("4G/5G Coverage (105 dBm) by Nation")
plt.xlabel("Nation")
plt.ylabel("Coverage (%)")

plt.show()

# -------- LINE GRAPH --------
plt.figure()

plt.plot(x, y1, marker="o", label="105 dBm")
plt.plot(x, y2, marker="o", label="95 dBm")

plt.title("Coverage Comparison")
plt.xlabel("Nation")
plt.ylabel("Coverage (%)")

plt.legend()

plt.show()

# -------- SCATTER PLOT --------
plt.figure()

plt.scatter(y1, y2)

plt.title("Coverage Relationship")
plt.xlabel("105 dBm Coverage")
plt.ylabel("95 dBm Coverage")

plt.show()'''


import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

data = pd.read_excel("myprjct.xlsx")

# посмотреть названия колонок
print(data.columns)

# выбрать только числовые
numeric_data = data.select_dtypes(include="number")

print(numeric_data.head())

# берем первые две числовые колонки
x = numeric_data.iloc[:,0]
y = numeric_data.iloc[:,1]

# mean
print("Mean X:", x.mean())
print("Mean Y:", y.mean())

# SD
print("SD X:", x.std())
print("SD Y:", y.std())

# t-test
t_stat, p_value = stats.ttest_rel(x, y)

print("t statistic:", t_stat)
print("p value:", p_value)

import matplotlib.pyplot as plt

means = [x.mean(), y.mean()]
labels = ["Variable X", "Variable Y"]

plt.bar(labels, means)

plt.title("Mean Comparison")
plt.ylabel("Mean Value")

plt.show()