--create_load_data_task
DROP TABLE IF EXISTS dw_data_schema.joined_table;

CREATE TABLE dw_data_schema.joined_table AS
SELECT 
    f.country_id,
    c.country_name,
    c.active_cases,
    c.new_cases,
    c.new_deaths,
    c.total_cases,
    c.total_deaths,
    c.total_recovered,
    c.last_update,
    f.income_level
FROM dw_data_schema.covid_table c
JOIN dw_data_schema.countries_table f 
    ON c.country_name = f.country_name;
