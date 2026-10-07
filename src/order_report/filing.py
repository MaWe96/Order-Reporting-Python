import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def data_loader(path: Path) -> pd.DataFrame:
    """Funktion som ger df från en .csv"""
    if not path.exists():
        logger.error('Ingen fil fanns i: %s', path)
        raise FileNotFoundError(f'Ingen fil fanns i: {path}')

    logger.info('Läser in CSV fil: %s', path)
    return pd.read_csv(path)


def data_saver(df: pd.DataFrame, folder: Path, filename: str) -> None:
    """Funktion som skriver df till en .csv"""
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / filename
    df.to_csv(target, index=False)
    logger.info('Sparade rapport: %s', target)