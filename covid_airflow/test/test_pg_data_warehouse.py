import pytest
from src.pg_data_warehouse import PG_Warehouse
from test.test_data import duplicated_null_countries_df, duplicated_null_covid_df

@pytest.fixture
def pg_warehouse():
    """Fixture that returns an instance of the PG_Warehouse class"""
    return PG_Warehouse()


def test_clean_countries_removes_duplicates_and_nulls(pg_warehouse):
    """
    Test that the `clean_countries` method:
    - Removes duplicate rows based on partition and full duplication.
    - Keeps only the most recent record per country using windowing logic.
    - Drops rows with null values in relevant columns.
    - Returns exactly three unique and complete country records.
    """

    cleaned_df = pg_warehouse.clean_countries(duplicated_null_countries_df)
    result = cleaned_df.collect()
    country_ids = [row["country_id"] for row in result]

    assert len(result) == 3
    assert set(country_ids) == {"ABW", "AFE", "AFG"}
    assert all(row["country_name"] is not None for row in result)


def test_clean_covid_removes_duplicates_and_nulls(pg_warehouse):
    """
    Test that the `clean_covid` method:
    - Removes duplicate rows based on partition and full duplication.
    - Keeps only the most recent record per country using windowing logic.
    - Drops rows with null values in relevant columns such as `active_cases`.
    - Returns exactly two unique and complete COVID records.
    """
   
    cleaned_df = pg_warehouse.clean_covid(duplicated_null_covid_df)
    result = cleaned_df.collect()
    country_names = [row["country_name"] for row in result]

    assert len(result) == 2
    assert set(country_names) == {"USA", "Belgium"}
    assert all(row["active_cases"] is not None for row in result)
