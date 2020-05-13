import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import statsmodels.api as sm

# Read in data.
dep_data=pd.read_csv("prevalence-of-depression-males-vs-females.csv") #https://ourworldindata.org/mental-health
ess_data = pd.read_csv("ess_data.csv")

# From the data on depression, select information for the year 2013, reduce dataframe to the relevant columns,
# and drop missing values.
dep_data2013 = dep_data[dep_data["Year"]==2013]
dep_data2013=dep_data2013.drop(["Year", "Code", "Population"], axis=1)
dep_data2013=dep_data2013.rename(columns={"Entity":"country"})
dep_data2013["Relative_prevalence_females"] = dep_data2013["Prevalence in females (%)"] / dep_data2013["Prevalence in males (%)"]
dep_data2013=dep_data2013.dropna()



# Create a new dataframe which merges information on suicide and life expectancy with than on depression. Rename
# the columns to make them more intuitively understandable.
new_df = ess_data.merge(dep_data2013, on="country", how="inner")
new_df=new_df.rename(columns={"Male_Preponderance": "Male Preponderance in Suicides",
               "Relative_LE" : "Male Relative Life Expectancy",
               "Prevalence in males (%)" : "Male Depression Incidence",
               "Prevalence in females (%)" : "Female Depression Incidence",
               "Relative_prevalence_females" : "Female Preponderance in Depression"}
                     )

# Export this dataframe to a csv file for later use.
new_df.to_csv("new_df")

sns.distplot(new_df["Female Preponderance in Depression"], norm_hist=False, bins=10)
plt.xlabel("Female preponderance in depression")
#plt.ylabel("Density")
plt.yticks([])
plt.axvline(x=1, ymin=0, ymax=1, c="red")
plt.title("Women are more often diagnosed with depression")
plt.show()


plt.scatter(new_df["Female Preponderance in Depression"], new_df["Male Preponderance in Suicides"])
plt.title("Female preponderance in depression vs. male preponderance in suicides")
plt.xlabel("Female Preponderance in Depression")
plt.ylabel("Male Preponderance in Suicides")
plt.show()


#fig = px.scatter(new_df, x="Female Prevalence in Depression", y="Male Prevalence in Suicides", trendline="ols",
#                 title="Male prevalence in suicides and relative male depression incidence",
#                 )
#fig.show()










feature_cols = ["Female Preponderance in Depression","Male Relative Life Expectancy", "Male Depression Incidence"]
X=new_df[feature_cols]
X=sm.add_constant(X)
model = sm.OLS(new_df["Male Preponderance in Suicides"],X)
results=model.fit()
print(results.summary())

