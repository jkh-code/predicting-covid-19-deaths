# Predicting COVID-19 Deaths from Publicly Available Data

<p align="center">
  <a href="https://docs.google.com/presentation/d/1ZuryGxy18rZlF7Ga8g-YR7_lhyIDFDDxJe-eabr94FM/edit?usp=sharing">Presentation</a>
</p>

## Table of Contents
- [Background](#background)
- [Reproducing the Project](#reproducing-the-project)
- [Data](#data)
- [Exploratory-Data-Analysis](#exploratory-data-analysis)
- [Predictive Modeling](#predictive-modeling)
- [Next Steps](#next-steps)

## Background
The COVID-19 pandemic flooded hospitals with a torrent of patients during case surges and overwhelmed the medical industry. At this time, vaccination rates are rising, but the possibility of local surges due to the Delta variant and vaccine hesitancy means hospitals may continue to face surges. During these surges staff are overwhelmed and may need a tool to help diagnose if a patient may die from their COVID-19 infection. By predicting that a patient may die from their infection, hospital staff have time to change treatment, provide targeted increased care, or can suggest experimental treatments in an effort to save a patient's life. The goal of this project is to develop a predictive model from publicly available data to determine if a COVID-19 infected patient will die from their infection with the hope this information will change treatment for the patient and save their life.

## Reproducing the Project
Install a local instance of [PostgreSQL](https://www.postgresql.org/download/) or use an existing instance. Create a database in the instance named `covid_cases` and then run the [`create-covid-db.sql`](https://github.com/jkh-code/predicting-covid-19-deaths/blob/main/sql/create-covid-db.sql) script from the command line to add tables to the database.

Add the following environment variables to use the `make_postgres_conn()` and `make_alchemy_engine()` functions:

```sh
export PG_HOST="my host"
export PG_USER="my user"
export PG_PASSWORD="my password"
```

Add the following path to your Python paths to allow for importing the `make_postgres_conn()` and `make_alchemy_engine()` functions from the *src* folder.

```sh
export PYTHONPATH=$PYTHONPATH:$/my/path/to/predicting-covid-19-deaths/src/
```

## Data
The main dataset for this project comes from the CDC's [COVID-19 Case Surveillance Public Use Data with Geography](https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data-with-Ge/n8mc-b4w4) dataset. This dataset contains 19 columns, each row is a deidentified patient, and, as of July 12, 2021, this dataset contains 27.1 million rows. Below is a description of the data.

| Field  | Description |
| ------------- | ------------- |
| case_month | Date related to illness received by the CDC. |
| res_state | State of residence of the patient. |
| state_fips_code | State FIPS code. |
| res_county | County of residence of the patient. |
| county_fips_code | County FIPS code. |
| age_group | Age group of the patient. |
| sex | Sex of the patient. |
| race | Race of the patient. |
| ethnicity | Ethnicity of the patient. |
| case_positive_specimen_interval | Weeks between earliest date and date of first positive specimen collected. |
| case_onset_interval | Weeks between earliest date and date of symptom onset. |
| process | How was this case first identified. |
| exposure_yn | If the patient engage in behavior that led to exposure. |
| current_status | Is this a confirmed or probable case of COVID-19. |
| symptom_status | Is the patient asymptomatic or symptomatic. |
| hosp_yn | Was the patient hospitalized? |
| icu_yn | Was the patient admitted to hte ICU? |
| death_yn | Did the patient die as a result of the illness? |
| underlying_conditions_yn | Did the patient have one or more underlying conditions? |

The fields above can contain one of four missing data values. The table below describes the four types of missing values a field can have. See the [Exploratory Data Analysis](#exploratory-data-analysis) section for a discussion on how these missing values were handled.

| Missing Value  | Description |
| ------------- | ------------- |
| NA | Suppressed due to privacy. |
| Missing | Jurisdiction did not collect. |
| Unknown | Jurisdiction reported field as unknown. |
| Blank | Jurisdiction did not collect. |

The secondary dataset for this project comes from the U.S. Department of Health and Human Services' [COVID-19 Community Vulnerability Crosswalk by Census Tract](https://healthdata.gov/Health/COVID-19-Community-Vulnerability-Crosswalk-Crosswa/x2y5-9muu) dataset. This dataset contains 19 columns, 72.8 thousand rows, and each row is a census tract in the United States. This dataset contains data on how vulnerable a census tract or county is to COVID-19. For the purposes of this project, county-level low income area score, tribal, and rural data will be extracted. Below are the fields used.

| Field  | Description |
| ------------- | ------------- |
| County FIPS  | Unique ID for each county which will be used for aggregation and joining. |
| Low Income Area (LIA) County SAIPE - Score | Score indicating if if there is low, medium, or high poverty in a county. |
| Tribal Community | A flag indicating if a census tract contains tribal land or not. |
| Rural | A flag indicating if a census tract is rural. |

The tribal community and rural fields was combined into a county-level view. To calculate an estimate of how rural or tribal a county is, the number of census tracts per county were calculated and then the number of rural or tribal census tracts per county were aggregated. Next, the number of rural or tribal census tracts were divided by the total number of census tracts to produce the estimate.

After the community crosswalk data was transformed into county-level data, it was joined to the patient data so that features for the the low income score, percent tribal, and percent rural can be used during the predictive analysis and exploratory data analysis phases of this project.

## Exploratory Data Analysis
The patient dataset is 27.1 million rows, however, for exploratory data analysis (EDA), a subset of this dataset was used. Only records without missing values in the `death_yn` field were used for EDA because this is the data that would be used during predictive modeling. A sample of 10 million records was extract from the dataset and only 4.4 million records did not have a missing death value. These 4.4 million record were used for EDA.

The number of cases by state is plotted below. Only two of the top five states with the largest populations are in the top 5 states by number of cases and three states with a population between five and 10 million are also in the top 5 states by number of cases.

![cases by state](images/number-cases-by-state.png)

The two plots below indicate that the majority of cases in the dataset are patients 18 to 49 years old and females are a slightly higher percent of cases.

![percent cases by age group](images/percent-cases-age-group.png)

![percent cases by sex](images/percent-cases-sex.png)

When race is examined, issues with missing and null values start to appear. The majority of cases in the dataset are White, however, the next two largest percent of cases are NaN (equivalent to NA) and Unknown followed by African-American.

![percent cases by race](images/percent-cases-race.png)

The issue of a significant number of NA, Missing, or Unknown values will appear again for exposure behavior, hospitalization, ICU visit, and underlying conditions.

The majority of cases have exposure behavior missing, with about 13% responding "Yes".

![percent exposure behavior](images/percent-cases-exposure-behavior.png)

The majority of cases were not hospitalized and the ICU visit feature has an overwhelming majority of missing or unknown values.

![percent cases hospitalized](images/percent-cases-hospitalization.png)

![percent cases to icu](images/percent-cases-icu-visit.png)

The majority of cases have NA for underlying conditions.

![percent cases underlying conditions](images/percent-cases-underlying-conditions.png)

In the dataset for EDA, only about 1.2% of cases resulted in deaths.

![percent cases with death](images/percent-cases-with-death.png)





## Predictive Modeling


## Next Steps
