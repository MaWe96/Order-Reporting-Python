import logging
import sys
from .configure import ReportConfig
from .logger_config import logger_configure
from .filing import data_loader, data_saver
from .calculations import data_validator, data_cleaner, order_total, data_aggregator, agg_overview, returns_by_category

logger = logging.getLogger("order_report")

def main() -> int:
    logger_configure()
    config = ReportConfig() # dataklassen
    
    logger.info("Påbörjar orderrapport..")
    
    try:
        # läs in och säkra kolumner
        raw_data = data_loader(config.input_path)
        data_validator(raw_data)

        # tvätta och kör kalkyler
        clean = data_cleaner(raw_data)
        calculated = order_total(clean)
        
        # gör aggregat med produktkategori och region
        sales_category = data_aggregator(calculated, 'product_category')
        sales_region = data_aggregator(calculated, 'region')
        overview = agg_overview(calculated)
        returns_category = returns_by_category(calculated)
        
        # skapa output csv
        data_saver(sales_category, config.output_dir, 'sales_by_category.csv')
        data_saver(sales_region, config.output_dir, 'sales_by_region.csv')
        data_saver(overview, config.output_dir, 'overview.csv')
        data_saver(returns_category, config.output_dir, "returns_by_category.csv")
        
        logger.info('Orderrapport genomfördes problemfritt.')
        return 0

    except FileNotFoundError as e:
        logger.error('Program-stopp på grund av ej hittad fil. %s', e)
        return 1
    except ValueError as e:
        logger.error('Program-stopp på grund av fel i data. %s', e)
        return 1
    except Exception as e:
        logger.error('Program-stopp på grund av felet: %s', e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())