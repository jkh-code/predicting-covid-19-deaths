import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from os import environ

from typing import Union, Type, List, Dict
from sqlalchemy.engine.base import Engine


def make_alchemy_engine(
        dbname: str='postgres', port: int=5432) -> Engine:
    username = environ['PG_USER']
    password = environ['PG_PASSWORD']
    host = environ['PG_HOST']
    string = f'postgresql://{username}:{password}@{host}:{port}/{dbname}'
    return create_engine(string)


if __name__ == '__main__':
    print('Starting pipeline...')

    # Loading cases data
    print('Loading cases data...')
    covid_cases_path = ('./data/' 
        + 'COVID-19_Case_Surveillance_Public_Use_Data_with_Geography.csv')
    df_cases = pd.read_csv(
        covid_cases_path, dtype='string')

    df_cases = df_cases.drop(columns=['state_fips_code'])

    df_cases['case_positive_specimen_interval'] = pd.to_numeric(
        df_cases['case_positive_specimen_interval'])
    df_cases['case_onset_interval'] = pd.to_numeric(
        df_cases['case_onset_interval'])

    # Loading counties data
    print('Loading counties data...')
    use_columns = ['STATE', 'COUNTY', 'County FIPS', 
        'Low Income Area (LIA) County SAIPE- Score', 
        'Tribal Community\n(1 if yes)', 'Rural']
    column_names = ['state', 'county', 'county_fips', 'low_income_score', 
        'tribal', 'rural']

    counties_path = ('./data/' 
        + 'COVID-19_Community_Vulnerability_Crosswalk_-_'
        + 'Crosswalk_by_Census_Tract.csv')
    df_counties = pd.read_csv(
        counties_path, usecols=use_columns, dtype='string')
    df_counties.columns = column_names

    df_counties = df_counties.astype({'low_income_score': 'int64', 'rural': 'int64'})

    df_counties['tribal'] = np.where(df_counties['tribal'] == 'Non-Tribal', 0, 1)
    df_counties['ctract_count'] = 1

    df_counties = df_counties.groupby(['state', 'county', 'county_fips']).agg(
        {'low_income_score': 'mean', 'tribal': 'sum', 'rural': 'sum', 
        'ctract_count': 'sum'}).reset_index()

    df_counties['perc_tribal_ct'] = (df_counties['tribal'] 
        / df_counties['ctract_count'])
    df_counties['perc_rural_ct'] = (df_counties['rural'] 
        / df_counties['ctract_count'])
    df_counties = df_counties.drop(columns=['state', 'county', 'tribal', 
        'rural', 'ctract_count'])

    # Joining
    print('Joining data...')
    df = df_cases.merge(
        df_counties, how='left', left_on='county_fips_code', 
        right_on='county_fips')
    df = df.drop(columns=['county_fips'])
    df['res_county'] = df['res_county'] + ', ' + df['res_state']
    
    del df_cases
    del df_counties

    # Limiting to yes/no in death_yn column
    print('Keeping data yes/no data in death_yn column...')
    df_keep = df[~df['death_yn'].isna()]
    df_keep = df_keep[
        (df_keep['death_yn']=='Yes') | (df_keep['death_yn']=='No')]
    df_keep.reset_index(drop=True, inplace=True)
    del df

    # Saving df_keep to database
    alchemy_engine = make_alchemy_engine('covid_cases')
    
    print('Saving all case data to PostgreSQL...')
    # df_keep.to_sql(
    #     'all_case_data', alchemy_engine, index=False, if_exists='replace')
    

    alchemy_engine.dispose()