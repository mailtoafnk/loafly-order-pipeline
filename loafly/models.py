"""models.py - the data model: one customer order."""


class Order:
    """One customer order: who ordered, and which items at what price."""

    def __init__(self, order_id, customer):
        self.order_id = order_id
        self.customer = customer
        self.items = []                      # list of (name, price) tuples

    def add_item(self, name, price):
        """Add one item with an already-cleaned numeric price."""
        self.items.append((name, price))

    def total(self):
        """Sum of all item prices (before discount)."""
        return sum(price for name, price in self.items)

    def __repr__(self):
        return f"Order({self.order_id}, {self.customer}, {len(self.items)} items)"