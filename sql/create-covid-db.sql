/*
-- Create the following database before running this script
CREATE DATABASE covid_cases;
*/

CREATE TABLE public.all_case_data (
	case_month varchar(100) NULL,
	res_state varchar(100) NULL,
	res_county varchar(100) NULL,
	county_fips_code varchar(100) NULL,
	age_group varchar(100) NULL,
	sex varchar(100) NULL,
	race varchar(100) NULL,
	ethnicity varchar(100) NULL,
	case_positive_specimen_interval float4 NULL,
	case_onset_interval float4 NULL,
	process varchar(100) NULL,
	exposure_yn varchar(100) NULL,
	current_status varchar(100) NULL,
	symptom_status varchar(100) NULL,
	hosp_yn varchar(100) NULL,
	icu_yn varchar(100) NULL,
	death_yn varchar(100) NULL,
	underlying_conditions_yn varchar(100) NULL,
	low_income_score float4 NULL,
	perc_tribal_ct float4 NULL,
	perc_rural_ct float4 NULL
);

-- no_null_data has removed all records with a NULL, Unknown, or Missing
-- value in any field
CREATE TABLE public.no_null_data (
	case_month varchar(100) NULL,
	res_state varchar(100) NULL,
	res_county varchar(100) NULL,
	county_fips_code varchar(100) NULL,
	age_group varchar(100) NULL,
	sex varchar(100) NULL,
	race varchar(100) NULL,
	ethnicity varchar(100) NULL,
	case_positive_specimen_interval float4 NULL,
	case_onset_interval float4 NULL,
	process varchar(100) NULL,
	exposure_yn varchar(100) NULL,
	current_status varchar(100) NULL,
	symptom_status varchar(100) NULL,
	hosp_yn varchar(100) NULL,
	icu_yn varchar(100) NULL,
	death_yn varchar(100) NULL,
	underlying_conditions_yn varchar(100) NULL,
	low_income_score float4 NULL,
	perc_tribal_ct float4 NULL,
	perc_rural_ct float4 NULL
);

-- some_null_data has removed all records with a NULL, Unknown, or Missing
-- value in the exposure, ICU, and underlying conditions fields
CREATE TABLE public.some_null_data (
	case_month varchar(100) NULL,
	res_state varchar(100) NULL,
	res_county varchar(100) NULL,
	county_fips_code varchar(100) NULL,
	age_group varchar(100) NULL,
	sex varchar(100) NULL,
	race varchar(100) NULL,
	ethnicity varchar(100) NULL,
	case_positive_specimen_interval float4 NULL,
	case_onset_interval float4 NULL,
	process varchar(100) NULL,
	exposure_yn varchar(100) NULL,
	current_status varchar(100) NULL,
	symptom_status varchar(100) NULL,
	hosp_yn varchar(100) NULL,
	icu_yn varchar(100) NULL,
	death_yn varchar(100) NULL,
	underlying_conditions_yn varchar(100) NULL,
	low_income_score float4 NULL,
	perc_tribal_ct float4 NULL,
	perc_rural_ct float4 NULL
);