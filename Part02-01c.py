import pandas as pd
import matplotlib.pyplot as plt


# Read in information about suicide statistics and life expectancy. https://ourworldindata.org/life-expectancy
# Feb 29th, 2020
suicstats = pd.read_csv("country_data_2013.csv")
lifexp = pd.read_csv("Life_expectancy_sex.csv")

# Select relevant columns from the life expectancy data.
lifexp = lifexp[["Entity", "Year", "Life expectancy of men (years)", "Life expectancy of women (years)"]]

# From life expectancy data, select information pertaining to the year 2013. Drop rows with missing values as well as
# the year column. Create a new column which gives the relative life expectancy of men as a share of women's life
# expectancy.
data= lifexp[lifexp["Year"]==2013]
data = data.dropna()
data.drop("Year", axis=1, inplace=True)
data["Relative_LE"] = data["Life expectancy of men (years)"] / data["Life expectancy of women (years)"]

# Create a new table / dataframe that unites the suicide data with the life expectancy data for each country.
data.rename({"Entity":"country"}, axis=1, inplace=True)
new_table= suicstats.merge(data, on="country", how="inner")
new_table=new_table.dropna()

# For each country, select only the information about the male share in suicides and the relative life expectancy of men.
ess_data = new_table[["country","Male_Preponderance","Relative_LE"]]


ess_data.to_csv("ess_data.csv")

plt.scatter(ess_data["Relative_LE"], ess_data["Male_Preponderance"])
plt.title("Relative life expectancy of men vs. male preponderance in suicides")
plt.xlabel("Relative life expectancy of men")
plt.ylabel("Male preponderance in suicides")
plt.show()

#import plotly.express as px
#fig = px.scatter(ess_data, x="Relative_LE", y="Male_Prevalence", trendline="ols",
#                 title="Male prevalence in suicides and relative male life expectancy",
#                 )
#fig.show()



from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

feature_cols = ["Relative_LE"]
X=ess_data[feature_cols]
X=sm.add_constant(X)
model = sm.OLS(ess_data["Male_Preponderance"],X)
results=model.fit()
print(results.summary())
