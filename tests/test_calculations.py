import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from order_report.calculations import order_total, data_cleaner, data_aggregator


def test_order_total_calculations():
    df = pd.DataFrame({
        "quantity": [3.0, 10.0],
        "unit_price": [110.0, 10.0],
        "discount": [0.1, 0.2]
    })
    
    result = order_total(df)
    assert result["discounted_ordertotal"].tolist() == pytest.approx([297.0, 80.0])


def test_data_cleaner_formatting():
    df = pd.DataFrame({
        "region": [" NORTH ", " west "],
        "product_category": [" Bikes", "tools "],
        "unit_price": ["75", "30"],
        "quantity": [10, 3],
        "discount": [0, 0],
        "returned": ["true", "false"]
    })
    
    expected = pd.DataFrame({
        "region": ["North", "West"],
        "product_category": ["Bikes", "Tools"],
        "unit_price": [75.0, 30.0],
        "quantity": [10.0, 3.0],
        "discount": [0.0, 0.0],
        "returned": [True, False]
    })
    
    result = data_cleaner(df)
    assert_frame_equal(result, expected)


def test_data_aggregator():
    data = pd.DataFrame({
        "order_id": ["O1", "O2"],
        "product_category": ["bikes", "bikes"],
        "discounted_ordertotal": [100.0, 200.0],
        "returned": [False, True]
    })

    result = data_aggregator(data, "product_category")
    assert result.loc[0, "order_count"] == 2
    assert result.loc[0, "total_sales"] == 300.0
    assert result.loc[0, "returns"] == 1