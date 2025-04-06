from backend import db_helper
import pytest


def test_fetch_expenses_for_date_aug_15():
    expenses = db_helper.fetch_expenses_for_date("2024-08-15")

    assert len(expenses) == 1
    
    assert expenses[0]['amount'] == 10
    assert expenses[0]['category'] == 'Shopping'
    assert expenses[0]['notes'] == 'Bought potatoes'

def test_fetch_expenses_for_date_invalid_date():
    expenses = db_helper.fetch_expenses_for_date("9999-08-15")

    assert len(expenses) == 1
    
    assert expenses[0]['amount'] == 0
    
def test_fetch_expenses_summary_invalid_range():
    summary = db_helper.fetch_expenses_summary("9999-08-15", "9999-08-16")

    assert len(summary) == 1
    
    assert len(summary) == 0
    
    


    