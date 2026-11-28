"""Check CSV records that DictReader would otherwise silently truncate."""


def record_width_errors(rows):
    """Return record indices and shape errors for parsed CSV rows."""
    errors = []
    for index, row in enumerate(rows, start=2):
        if None in row:
            errors.append((index, f"{len(row[None])} extra field(s)"))
        missing = [key for key, value in row.items() if key is not None and value is None]
        if missing:
            errors.append((index, "missing field(s): " + ", ".join(missing)))
    return errors
