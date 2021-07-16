# Predicting COVID-19 Deaths from Publicly Available Data

<p align="center">
  <a href="https://docs.google.com/presentation/d/1ZuryGxy18rZlF7Ga8g-YR7_lhyIDFDDxJe-eabr94FM/edit?usp=sharing">Presentation</a>
</p>

## Table of Contents
- [Background](#background)
- [Reproducing the Project](#reproducing-the-project)
- [Data](#data)
- [Exploratory-Data-Analysis](#exploratory-data-analysis)

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
