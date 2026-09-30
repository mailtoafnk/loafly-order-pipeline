"""load.py - save each finished order to the orders API, with retry."""
import logging
import time

from gateway import save_to_orders_api
from loafly.config import SETTINGS, API_KEY
from loafly.transform import apply_discount

logger = logging.getLogger(__name__)


def save_with_retry(order_id, total):
    """Try to save one order, retrying on ConnectionError.

    Returns True if saved, False if every attempt failed.
    """
    retries = SETTINGS["max_retries"]
    wait = SETTINGS["retry_wait_seconds"]
    for attempt in range(1, retries + 1):
        try:
            save_to_orders_api(order_id, total)
            logger.info("Order %s saved (attempt %d/%d)", order_id, attempt, retries)
            return True
        except ConnectionError as err:
            logger.warning("Order %s: attempt %d/%d failed - %s",
                           order_id, attempt, retries, err)
            if attempt < retries:
                time.sleep(wait)
    logger.error("Order %s: giving up after %d attempts", order_id, retries)
    return False


def save_orders(orders):
    """Apply the discount and save every order. Returns (saved, failed)."""
    if API_KEY == "demo-key":
        logger.warning("LOAFLY_API_KEY not set - using demo key")
    else:
        logger.info("API key loaded from environment (ends ...%s)", API_KEY[-4:])

    saved, failed = 0, 0
    for order in orders:
        total = round(apply_discount(order.total(), SETTINGS["discount_percent"]), 2)
        logger.info("Saving order %s for %s, total %.2f %s",
                    order.order_id, order.customer, total, SETTINGS["currency"])
        if save_with_retry(order.order_id, total):
            saved += 1
        else:
            failed += 1

    logger.info("Saved %d orders, failed %d", saved, failed)
    return saved, failed