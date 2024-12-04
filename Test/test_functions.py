"""Test functions for testing_to_test module."""
import pytest
from freezegun import freeze_time
from testing_to_test import even_odd, sum_all, time_of_day, calculate_total_textbook_cost


@pytest.mark.parametrize('input_values, expected',
                         [
                             (2, 'even'),
                             (3, 'odd'),
                             (-4, 'even'),
                             (-5, 'odd'),
                             #boundary case
                             (0, 'even')
                             ])
def test_even_odd_positive(input_values : int, expected : str) -> None:
    """Testing even_odd function positives cases"""
    assert even_odd(input_values) == expected

#negative cases
@pytest.mark.parametrize('input_values',
                         ['string',
                             None]
                         )

def test_even_odd_negative(input_values : str) -> None:
    """Testing even_odd function negative cases"""
    with pytest.raises(TypeError):
        even_odd(input_values)


#Testing sum_all function
#positives cases
@pytest.mark.parametrize('input_values, expected', [
    ([1,2, 3], 6),
    ([-1,-2,-3], -6),
    ([0], 0),
    ([], 0),
    ([1.5,1], 2.5)
    ])
def test_sum_all_positives(input_values: list[float] , expected : float) -> None:
    """Testing sum_all function positives cases"""
    assert sum_all(*input_values) == expected

#negatives cases
@pytest.mark.parametrize('input_values',
    [(None, ),
    (['1', '2','3'], ),
    ({'k1': 0, 'k2':1},),
    ([1, 2, '3', 4.5], )
    ])
def test_sum_all_negatives(input_values : tuple) -> None:
    """Testing sum_all function positives cases"""
    with pytest.raises(TypeError):
        sum_all(*input_values)


#Testing time_of_day
@pytest.mark.parametrize('frozen_time, expected', [
    ('2024-11-28 08:00:00', 'morning'),
    #boundary case
    ('2024-11-28 06:00:00', 'morning'),
    ('2024-11-28 16:00:00', 'afternoon'),
    ('2024-11-28 12:00:00', 'afternoon'),
    ('2024-11-28 23:59:59', 'night'),

    #boundary case
    ('2024-11-28 18:00:00', 'night'),
    ])

def test_time_of_day(frozen_time : str , expected : str) -> None:
    """Testing test_time_of_day"""
    #mocking the date-time
    with freeze_time(frozen_time):
        assert time_of_day()== expected



#Testing calculate_total_textbook_cost
#mocking get_book_price

@pytest.mark.parametrize('book_ids, book_prices, expected', [
    ([1,2,3],[10.0, 20.0, 30.0], 60.0 ), #normal case
    ([4,5,6], [None, None, None], 0.0), #unexisting ids
    ([],[], 0.0),#empty case
    ([1], [10.0], 10.0) #unique book
    ])

def test_calculate_total_textbook_cost(mocker, book_ids : list[int], book_prices : list[float], expected : float) -> None:
    """Testing sum_all function positives cases"""
    #mocking get_book_price
    mocker.patch(
        'testing_to_test.get_book_price', #pointing the function to mock
        side_effect= book_prices #returns the prices for  each call
        )

    # calling the function we want to test
    result = calculate_total_textbook_cost(book_ids)

    # asserting the result
    assert result == expected
