"""run_pipeline.py - run the Loafly pipeline: extract -> transform -> load."""
import logging

from loafly.config import SETTINGS
from loafly.extract import read_rows
from loafly.transform import build_orders
from loafly.load import save_orders


def setup_logging():
    """Send timestamped log lines to the terminal and to a log file."""
    logging.basicConfig(
        level=SETTINGS["log_level"],
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),                                   # terminal
            logging.FileHandler(SETTINGS["log_file"], encoding="utf-8"),  # file
        ],
    )


def main():
    setup_logging()
    logger = logging.getLogger("loafly")
    logger.info("Pipeline started")
    try:
        rows = read_rows(SETTINGS["input_file"])
    except FileNotFoundError:
        logger.error("Input file not found: %s", SETTINGS["input_file"])
        return
    orders = build_orders(rows)
    save_orders(orders)
    logger.info("Pipeline finished")


if __name__ == "__main__":
    main()