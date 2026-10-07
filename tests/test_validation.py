import pytest
import pandas as pd
from order_report.calculations import data_validator


def test_validator_error_miss_col():
    df_return_miss_returned = pd.DataFrame({
        "order_id": ["O1"],
        "order_date": ["2025-06-01"],
        "customer_id": ["C1"],
        "region": ["North"],
        "product_category": ["Bikes"],
        "quantity": [1],
        "unit_price": [75],
        "discount": [0]
    })
    
    with pytest.raises(ValueError, match="returned fanns inte med."):
        data_validator(df_return_miss_returned)


def test_validator_error_empty_file():
    empty_df = pd.DataFrame()
    
    with pytest.raises(ValueError, match="Det fanns inga rader i filen."):
        data_validator(empty_df)