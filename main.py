import logging
import logging.config
import yaml

"""Running the Xetra ETL application"""


def main():
    """
    Entry point to run the xetra ETL job
    """
    # Parsing YAML file
    config_path = "configs/xetra_report1_config.yml"
    config = yaml.safe_load(open(config_path))
    # configure logging
    log_config = config["Logging"]
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)
    logger.info("This is a test.")


if __name__ == "__main__":
    main()
