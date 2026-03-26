def format_currency(amount: float) -> str:
    """Format a float as Indian Rupee currency string."""
    # Indian number formatting: 1,00,000 style
    amount = round(amount, 2)
    s = f"{amount:.2f}"
    integer_part, decimal_part = s.split(".")
    # Apply Indian grouping: last 3 digits, then groups of 2
    if len(integer_part) > 3:
        last3 = integer_part[-3:]
        rest = integer_part[:-3]
        groups = []
        while len(rest) > 2:
            groups.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.append(rest)
        groups.reverse()
        integer_part = ",".join(groups) + "," + last3
    return f"₹{integer_part}.{decimal_part}"


def stock_label(stock: int) -> str:
    """Return a human-readable stock status label."""
    if stock == 0:
        return "❌ Out of stock"
    elif stock <= 5:
        return f"🔥 Only {stock} left!"
    elif stock <= 20:
        return f"⚠️ Low stock ({stock})"
    return f"✅ In stock ({stock})"


def truncate(text: str, max_len: int = 40) -> str:
    """Truncate a string to max_len characters."""
    return text if len(text) <= max_len else text[:max_len - 3] + "..."
