"""Test module for API_Handler functions."""
import pytest
from unittest.mock import MagicMock, patch
from src.api_get import API_Handler
from test.test_data import covid_api_data, countries_api_data


@pytest.fixture
def covid_api_handler():
    """Fixture that returns an API_Handler instance for the COVID-19 API."""
    return API_Handler('https://mock-covid-19.dataflowkit.com/v1')


@pytest.fixture
def countries_api_handler():
    """Fixture that returns an API_Handler instance for the World Bank countries API."""
    return API_Handler('https://mock-api.worldbank.org/v2/country?format=json')


@patch('src.api_get.requests.get')
def test_extract_data_api_covid(mock_get, covid_api_handler):
    """
    Test API_Handler.extract_data_api with a mocked COVID-19 API response.
    Ensures that the method returns the expected data when the API responds with status 200.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = covid_api_data
    mock_get.return_value = mock_response

    result = covid_api_handler.extract_data_api()
    assert result == covid_api_data


@patch('src.api_get.requests.get')
def test_extract_data_api_countries(mock_get, countries_api_handler):
    """
    Test API_Handler.extract_data_api with a mocked World Bank API response.
    Ensures that the method returns the second element of the response,
    as expected from the World Bank API format.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [None, countries_api_data]
    mock_get.return_value = mock_response

    result = countries_api_handler.extract_data_api()
    assert result == countries_api_data
