# Analysis of Suicide Data

## Content

I provide an analysis of data about suicides, life expectancy, and mental health, as well as Gross National Income across various countries. The analysis focuses on the factor by which suicides by men outnumber those by women ("male preponderance in suicides").

Annual data is available across different countries for the time period from 1985 to 2015. A first exploration suggests that both the size of male preponderance in suicides as well as changes over time differ widely across the various countries considered. Hence, instead of focusing on developments over time, I focus on the 2013 data: Choosing that particular year is compromise between having data that is complete and also fairly recent. For many countries in the dataset, more recent numbers are missing.

I create a map of the world which visualizes cross-country differences in the male preponderance in suicides. Inspecting this visualization yields some first clues: For instance, one observation is that male preponderance in suicides is particularly pronounced in some Central and Eastern European countries which are often said to have a particularly low (male) life expectancy. Another observation is that some countries that are known for having a particularly high Human Development Index (Scandinavian countries, Japan) score low on male preponderance in suicides. 

Starting from such observations, I dig deeper by combining suicide data with data on life expectancy, mental health, and Gross National Income. I visualize correlations between all these variables in a heatmap and perform linear regression. The following conclusions emerge:

1. Countries with high male preponderance in suicides tend to be countries in which the life expectancy of men relative to that of women is low. This finding is consistent with the idea that suicide and early death are driven by a common factors: For instance, a tendency to commit suicide could be related to a tendency towards other "slower" methods of self-destruction (drug use, alcohol). 

2. Male preponderance in suicides is associated with more freqent diagnoses of depression in men. This is consistent with the idea that suitable access to treatment for depression is effective against suicides.

3. Countries with higher Gross National Income tend to have lower male preponderance in suicides. This is consistent with the initial observation that male preponderance in suicides tends to be low in countries that are known for their high level of human development. (I use Gross National Income instead of Human Development Index here because life expectancy data is also used as an explanatory variable, but it is also one of the factors that make up the Human Development Index.)

4. Somewhat surprisingly, the regression analysis reveals that male preponderance in suicides is more closely associated with male relative life expectancy than it is with the data on depression. 


## Acknowledgment of Data Sources

Four datasets are used for this project:

1) Data on suicides is available from Kaggle: https://www.kaggle.com/szamil/who-suicide-statistics The underlying information was compiled by Kaggle user Szamil on the basis of data obtained from the World Health Organization's Mortality Database, see https://apps.who.int/healthinfo/statistics/mortality/whodpms/.

2) Data on Life Expectancy is obtained from the website OurWorldInData.org. The website lists as its original source of information:
James C. Riley (2005) – Estimates of Regional and Global Life Expectancy, 1800–2001. Issue Population and Development Review. Population and Development Review. Volume 31, Issue 3, pages 537–543, September 2005., Zijdeman, Richard; Ribeira da Silva, Filipa, 2015, "Life Expectancy at Birth (Total)", http://hdl.handle.net/10622/LKYT53, IISH Dataverse, V1, and UN Population Division (2019)

3) Data on Mental Health is also obtained from OurWorldInData.org. It gives the original source:
Global Burden of Disease Collaborative Network. Global Burden of Disease Study 2017 (GBD 2017) Results. Seattle, United States: Institute for Health Metrics and Evaluation (IHME), 2018.

4) Finally, data on the Human Development Index comes from OurWorldInData.org, which in turn gives the United Nations Development Program (UNDP) as their source. 
