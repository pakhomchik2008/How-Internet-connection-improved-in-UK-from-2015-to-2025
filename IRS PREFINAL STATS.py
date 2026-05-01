'''
1️⃣ Graph 1 — Coverage threshold comparison
(использует medata.xlsx)
Показывает разницу между -105 dBm и -95 dBm coverage

📊 Что показывает:
при -105 dBm coverage выше, потому что сигнал слабее допускается.

'''

import pandas as pd
import matplotlib.pyplot as plt

# загрузка файла
data = pd.read_excel("medata.xlsx")

# средние значения
mean_105 = data["4G5G_105_geo_out_all"].mean()
mean_95 = data["4G5G_95_geo_out_all"].mean()

# bar chart
plt.bar(["-105 dBm", "-95 dBm"], [mean_105, mean_95])

plt.title("Average 4G/5G Coverage by Signal Threshold")
plt.ylabel("Coverage (%)")

plt.show()

from scipy.stats import ttest_rel

print("\nT-test for Coverage Thresholds")

print("H0: Mean coverage at -105 dBm is equal to mean coverage at -95 dBm.")
print("H1: Mean coverage at -105 dBm is different from mean coverage at -95 dBm.")

# t-test
t_stat, p_value = ttest_rel(data["4G5G_105_geo_out_all"], data["4G5G_95_geo_out_all"])

print("t-statistic:", round(t_stat,3))
print("p-value:", p_value)

if p_value < 0.05:
    print("Result: Reject H0. The difference between thresholds is statistically significant.")
else:
    print("Result: Fail to reject H0. No significant difference detected.")
# correlation (r value)

from scipy.stats import pearsonr

# correlation test
r_value, p_corr = pearsonr(data["4G5G_105_geo_out_all"], data["4G5G_95_geo_out_all"])

print("\nCorrelation Test")
print("Correlation coefficient (r):", round(r_value,3))
print("p-value:", p_corr)


import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("medata.xlsx")

coverage = data["4G5G_105_geo_out_all"]

plt.hist(coverage, bins=20)

plt.title("Distribution of 4G/5G Coverage")
plt.xlabel("Coverage (%)")
plt.ylabel("Number of Areas")
plt.style.use("ggplot")

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel, pearsonr

# загрузка данных
data = pd.read_excel("medata.xlsx")

# переменные
x = data["4G5G_105_geo_out_all"]
y = data["4G5G_95_geo_out_all"]

from scipy.stats import ttest_rel

print("\nGraph 2 — Distribution of 4G/5G Coverage")

print("H0: Coverage distribution does not differ between signal thresholds.")
print("H1: Coverage distribution differs between thresholds.")

mean_cov = coverage.mean()
std_cov = coverage.std()

print(f"Mean coverage: {mean_cov:.2f}%")
print(f"Standard deviation: {std_cov:.2f}")

# t-test
t_stat, p_value = ttest_rel(
    data["4G5G_105_geo_out_all"],
    data["4G5G_95_geo_out_all"]
)

print("t-statistic:", round(t_stat,3))
print("p-value:", p_value)

# correlation
r = data["4G5G_105_geo_out_all"].corr(data["4G5G_95_geo_out_all"])
print("Correlation coefficient (r):", round(r,3))

print("Result: Histogram shows the spread of coverage values across regions.")
plt.show()


'''
'''
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("myprjct.xlsx")

coverage = data["5G_SA_very_high_confidence_geo_out_1"]

plt.hist(coverage, bins=20)

plt.title("Distribution of 5G Coverage")
plt.xlabel("Coverage (%)")
plt.ylabel("Number of Areas")

print("\nGraph 3 — Distribution of 5G Coverage")

print("H0: 5G coverage is evenly distributed across regions.")
print("H1: 5G coverage is uneven across regions.")

mean_5g = coverage.mean()
std_5g = coverage.std()

print(f"Mean 5G coverage: {mean_5g:.2f}%")
print(f"Standard deviation: {std_5g:.2f}")

print("Result: If the histogram is skewed, it indicates unequal 5G deployment.")


plt.show()
'''
'''

#top 10 worst coverage areas
'''
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("myprjct.xlsx")

worst = data.sort_values("5G_SA_very_high_confidence_geo_out_1").head(10)

plt.figure(figsize=(8,6))

plt.barh(worst["laua_name"], worst["5G_SA_very_high_confidence_geo_out_1"])

plt.title("Top 10 Areas with Lowest 5G Coverage")
plt.xlabel("Coverage (%)")
plt.ylabel("Local Authority")

plt.show()

'''
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("myprjct.xlsx")

x = data["prem_count"]
y = data["5G_SA_very_high_confidence_geo_out_1"]

plt.scatter(x, y)

plt.title("5G Coverage vs Number of Premises")
plt.xlabel("Number of Premises")
plt.ylabel("Coverage (%)")

plt.show()

'''
import pandas as pd
import matplotlib.pyplot as plt
plt.figure(figsize=(7,5))
# загрузить файл
data = pd.read_excel("medata.xlsx")

# выбрать страны UK
countries = ["England", "Scotland", "Wales", "Northern Ireland"]

uk_data = data[data["Location"].isin(countries)]

# взять coverage
coverage = uk_data["4G5G_105_geo_out_all"]

# график
plt.bar(uk_data["Location"], coverage)

plt.title("4G/5G Coverage in UK Nations")
plt.xlabel("Country")
plt.ylabel("Coverage (%)")

plt.show()'''