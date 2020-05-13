import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import numpy as np

new_df = pd.read_csv("new_df")
gni= pd.read_csv("gross-national-income-per-capita.csv")


print(gni.columns)





gni2013=gni[gni["Year"]==2013]
gni2013=gni2013.drop(columns=["Code", "Year"], axis=1)
gni2013=gni2013.rename(columns={"Entity":"country",
                                'GNI per capita, PPP (constant 2011 international $) (Rate)' : "GNI" })


new_df=new_df.merge(gni2013, on="country", how="inner")

plt.scatter(new_df["GNI"], new_df["Male Preponderance in Suicides"])
plt.xlabel("Gross National Income (per capita)")
plt.ylabel("Male Preponderance in Suicides")
plt.title("GNI and male preponderance in suicides")
plt.show()



cmatrixcols=["Male Preponderance in Suicides","Female Preponderance in Depression","Male Depression Incidence",
             "Male Relative Life Expectancy", "GNI"]

corr_matrix = new_df[cmatrixcols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=np.bool))
sns.heatmap(corr_matrix, annot=True, xticklabels=["MPS", "FPD", "MRLE", "MDI", "GNI"],mask=mask).figure.tight_layout()
plt.title("Heatmap of the correlation matrix")
plt.show()



#feature_cols = ["Male Relative Life Expectancy", "Female Prevalence in Depression", "Male Depression Incidence","GNI"]
#feature_cols = ["Male Relative Life Expectancy", "Male Depression Incidence"]
feature_cols = ["Female Preponderance in Depression", "Male Relative Life Expectancy"]
X=new_df[feature_cols]
X=sm.add_constant(X)
model = sm.OLS(new_df["Male Preponderance in Suicides"],X)
results=model.fit()
print(results.summary())







