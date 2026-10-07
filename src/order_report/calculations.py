import pandas as pd, numpy as np
import logging

logger = logging.getLogger(__name__)

REQ_CSV_COLS = [
    'order_id', 'order_date', 'customer_id', 'region', 
    'product_category', 'quantity', 'unit_price', 'discount', 'returned'
]


def data_validator(df: pd.DataFrame):
    """Funktion för att kontrollera om behövda kolumner finns med i csv-filen."""

    if len(df) == 0:
        raise ValueError('Det fanns inga rader i filen.')

    for col in REQ_CSV_COLS:
        if col not in df.columns:
            logger.error('%s fanns inte med.', col)
            raise ValueError(f'{col} fanns inte med.')
        
    logger.info('Success: Behövda kolumner fanns med i csv-filen.')


def data_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    """Funktion som gör trim och lower (string), bool, samt säkrar datatyp och NaN hantering på csv-filens kolumner."""
    df = df.copy()
    
    # coerce datatyper och gör NaN till 0 (styckpris och rabatt) eller 1 (kvantitet)
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median()).astype(float)
    df['discount'] = pd.to_numeric(df['discount'], errors='coerce').fillna(0).astype(float)
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1).astype(float)

    # string columns
    for col in ['product_category', 'region']:
        fixed = df[col].fillna("unknown").astype(str)
        fixed = fixed.str.strip().str.title()
        df[col] = fixed

    # boolean
    df['returned'] = df['returned'].astype(str).str.lower().isin(['true','yes'])

    nonvalid_price = pd.to_numeric(df['unit_price'], errors='coerce').isna().sum()

    if nonvalid_price > 0:
        logger.warning('%d iligitimt värde fanns i unit_price vilket ersätts med medianen.', nonvalid_price)

    return df


def order_total(df: pd.DataFrame) -> pd.DataFrame:
    """Beräknar ordervärde per rad."""

    # total utan discount:
    df['order_total'] = df['quantity'] * df['unit_price']

    # total med discount:
    df['discounted_ordertotal'] = df['order_total'] * (1 - df['discount'])
    return df


def data_aggregator(df: pd.DataFrame, groupby_col: str) -> pd.DataFrame:
    """Grupperar summan försäljning & returer samt antalet ordrar."""
    
    # aggregering
    summary = df.groupby(groupby_col, as_index=False).agg(
        order_count=('order_id', 'nunique'),
        total_sales=('discounted_ordertotal', 'sum'),
        returns=('returned', 'sum'),
    )

    # runda av total_sales och lägg till kolumn return_rate
    summary['total_sales'] = np.round(summary['total_sales'],2)
    summary['return_rate'] = np.round((summary['returns'] / summary['order_count']),3)

    # return med fallande total_sales
    return (
        summary.sort_values('total_sales', ascending=False)
        .reset_index(drop=True)
    )


def agg_overview(df: pd.DataFrame) -> pd.DataFrame:
    total_sales = np.round(df['discounted_ordertotal'].sum(), 2)
    order_count = df['order_id'].nunique()
    return_count = np.round(df['returned'].sum(),0)

    return pd.DataFrame({
        'metric': ['total_sales', 'order_count', 'return_count'],
        'value': [total_sales, order_count, return_count]
    })


def returns_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Grupperar summan från returer över produkt-kategorierna."""

    summary = df.groupby('product_category', as_index=False).agg(
        order_count=('order_id', 'nunique'),
        returns=('returned', 'sum')
    )
    summary['return_rate'] = np.round(summary['returns'] / summary['order_count'],3)

    return summary.sort_values('return_rate', ascending=False).reset_index(drop=True)