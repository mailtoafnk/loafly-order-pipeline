"""extract.py - read the raw order rows from the CSV file."""
import csv
import logging

logger = logging.getLogger(__name__)


def read_rows(path):
    """Return every row of the CSV as a list of dicts."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    logger.info("Read %d rows from %s", len(rows), path)
    return rows