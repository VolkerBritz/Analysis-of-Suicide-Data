import pandas as pd
import pycountry_convert as pycc
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Read in file and check for missing values. Those occur only in one column (the Human Development Index), and there,
# the value is missing for most of the rows. Hence, drop this column.
# Also drop a column which merely duplicates information contained in other columns.
suicides= pd.read_csv("Suicide Data.csv")
print(suicides.shape)
print(suicides.isnull().sum())
suicides.drop(["HDI for year", "country-year"], axis=1, inplace=True)

# We are interested in the number of suicides per 100,000 people in various countries, year, and demographic groups.
# For this number to be meaningful, the groups considered should not be too small. Drop groups in which not a single
# suicide occurred. Also, drop groups whose size is below some threshold. Check how much data remains.
suicides = suicides[suicides["population"]>=50000]
suicides = suicides[suicides["suicides_no"]>0]


# In order to compare suicides in men vs. women for a given country, year, and age group, create a suitably merged
# dataframe. Use an inner join to make sure that we focus on groups, countries, and years where information
# is available for both men and women.
suicides["combi"] = suicides["country"].astype("str")+"--"+suicides["year"].astype("str")+"--"+suicides["age"].astype("str")
male_suicides = suicides[suicides["sex"]=="male"]
female_suicides = suicides[suicides["sex"]=="female"]
joint_table = male_suicides.merge(female_suicides, on="combi", how="inner", suffixes=("","_f"))

# Remove duplicate information from the merged dataframe, and make column names more intuitive.
joint_table = male_suicides.merge(female_suicides, on="combi", how="inner", suffixes=("","_f"))
joint_table.drop(["country_f","year_f","sex_f","age_f","gdp_per_capita ($)_f","generation_f","sex"],
                 axis=1, inplace=True)
rename_dict = {"suicides_no" : "suicides_no_m", "population":"population_m", "suicides/100k pop":"suicides/100k pop_m",
               }
joint_table.rename(rename_dict, axis=1, inplace=True)

# Create a reduced dataframe with only those columns that can be summed over different demographic groups
# in a meaningful way.
data=joint_table.drop(["age", " gdp_for_year ($) ", "gdp_per_capita ($)", "generation", "combi"], axis=1)

# Now group this data by country and year, and include columns for total suicides and for the "male prevalence"
# in suicides.
grouped_data=data.groupby(["country", "year"]).sum()
grouped_data["Total_suicides"] = grouped_data["suicides_no_m"]+grouped_data["suicides_no_f"]
grouped_data["Total_population"] = grouped_data["population_m"]+grouped_data["population_f"]
grouped_data["Suicides per 100k"] = grouped_data["Total_suicides"]/(grouped_data["Total_population"]/100000)
grouped_data["Male_Preponderance"] = grouped_data["suicides/100k pop_m"]/grouped_data["suicides/100k pop_f"]

grouped_data.to_csv("grouped_data.csv")



# In order to get a first rough impression of the frequency of suicides: Take all the country/year-pairs and plot
# a histogram of all the values of suicides per 100k people.
sns.distplot(grouped_data["Suicides per 100k"], norm_hist=True)
plt.xlabel("Suicides per 100k people")
#plt.ylabel("Density")
plt.yticks([])
plt.title("Distribution of suicide frequency over country-year pairs")
plt.xlim(0,60)
plt.ylim(0,)
plt.show()






print(grouped_data["Suicides per 100k"].describe())

# Use a scatter-plot to visualize male and female suicides. Each dot represents a country-year pair. Clearly,
# suicides by men and women seem to be strongly positively correlated, but male suicides consistently outnumber
# female suicides.
plt.scatter(grouped_data["suicides/100k pop_m"], grouped_data["suicides/100k pop_f"], s=1)
plt.xlim(0,100)
plt.ylim(0,100)
plt.xlabel("Suicides per 100,000 men")
plt.ylabel("Suicides per 100,000 women")
plt.title("Scatterplot of Suicides by Men vs. Women")
plt.show()

# Make a histogram of the male preponderance across country-year pairs.
sns.distplot(grouped_data["Male_Preponderance"], norm_hist=True)
plt.xlabel("Male preponderance")
#plt.ylabel("Density")
plt.yticks([])
plt.title("Distribution of male preponderance in suicides over country-year pairs")
plt.axvline(x=1, ymin=0, ymax=1, c="red", label="Equal suicide rate for men and women")
plt.legend()
plt.xlim(0,)
plt.show()
print(grouped_data["Male_Preponderance"].describe())






# Next, look at the male preponderance over time in different countries.
countries = ["Germany", "United States", "France", "Canada", "Japan", "Poland"]
sns.set(rc={'axes.facecolor':'lavenderblush'})
#fig, ax = plt.subplots(nrows=3, ncols=2, constrained_layout=True)


# Plot male preponderance over time for various countries in one figure.
for country in countries:
    plt.plot(grouped_data.loc[country].index, grouped_data.loc[country]["Male_Preponderance"], label=country)
plt.title("Male preponderance in suicides over time")
plt.xlabel("Year")
plt.ylim(1.0, 8)
plt.ylabel("Male Preponderance in Suicides")
plt.legend(countries)
plt.legend(loc='upper center', bbox_to_anchor=(0.3, 1.0), shadow=True, ncol=2)
plt.show()

# It may be useful to look at cross-country differences in the male share of suicides.
# To do so for a specific year, select only the data corresponding to 2013 and group by country.
grouped_data_y=data.groupby(["year", "country"]).sum()
grouped_data_y["Total_suicides"] = grouped_data_y["suicides_no_m"]+grouped_data_y["suicides_no_f"]
grouped_data_y["Total_population"] = grouped_data_y["population_m"]+grouped_data_y["population_f"]
grouped_data_y["Suicides per 100k"] = grouped_data_y["Total_suicides"]/(grouped_data_y["Total_population"]/100000)
grouped_data_y["Male_Preponderance"] = grouped_data_y["suicides/100k pop_m"]/grouped_data_y["suicides/100k pop_f"]
country_data_2013 = grouped_data_y.loc[2013]

# For later use, export 2013 data on suicides to a csv file.
country_data_2013.to_csv("country_data_2013.csv")


# Map country names to ISO codes. Manually clean up the entry for Korea, which reads "Republic of Korea" but should
# be "Korea, Republic of"
new_column = []
for i in range(len(country_data_2013.index)):
    country_name = country_data_2013.index[i]
    try:
        country_code = pycc.country_name_to_country_alpha3(country_name, cn_name_format="default")
    except KeyError:
        if country_name=="Republic of Korea":
            country_code="KOR"
        else:
            country_code="ERROR"
    new_column.append(country_code)

# Add ISO codes to the data as a new column.
country_data_2013.insert(0, "ISO_code", new_column, True)

# Now create the world map with different colors indicating the male share of suicides per country.
figure = px.choropleth(country_data_2013, locations="ISO_code",
                    color="Male_Preponderance",
                    hover_name=country_data_2013.index,
                    color_continuous_scale=px.colors.sequential.Plasma)

figure.update_layout(title_text = "Male preponderance in suicides throughout the world (2013)")
figure.show()