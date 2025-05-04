import re


def humanize(s: str) -> str:
    """
    Convert a snake_case string to a human-readable format.
    For example, "bulk_import" becomes "Bulk import".
    """
    return re.sub(r"(_)([a-z])", lambda m: f" {m.group(2).upper()}", s).title()


def split_camel_case(s: str) -> str:
    """
    Convert a camelCase string to a human-readable format.
    For example, "bulkImport" becomes "Bulk Import".
    """
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', s)
