"""transform.py - clean prices and turn raw rows into Order objects."""
import logging

from loafly.models import Order

logger = logging.getLogger(__name__)


def clean_price(text):
    """Turn a messy price string like ' 1,250' into a float 1250.0."""
    return float(text.strip().replace(",", ""))


def apply_discount(price, percent):
    """Return the price after taking `percent` % off."""
    return price - price * percent / 100


def build_orders(rows):
    """Group item rows into Order objects, one per order_id.

    An item whose price is missing or unreadable is skipped with a
    warning, so one bad row never stops the whole run.
    """
    orders = {}
    checked = 0
    skipped = 0
    for row in rows:
        oid = row["order_id"]
        if oid not in orders:
            orders[oid] = Order(oid, row["customer"])
        try:
            price = clean_price(row["item_price"])
        except (ValueError, TypeError, AttributeError):
            # ValueError: blank or non-numeric text, e.g. float("")
            # TypeError/AttributeError: the value is None or not a string
            skipped += 1
            logger.warning("Order %s: skipping '%s' - missing or bad price %r",
                           oid, row["item_name"], row["item_price"])
            continue
        else:
            orders[oid].add_item(row["item_name"], price)
        finally:
            checked += 1        # runs for every row, good or bad

    logger.info("Checked %d items, skipped %d, built %d orders",
                checked, skipped, len(orders))
    return list(orders.values())