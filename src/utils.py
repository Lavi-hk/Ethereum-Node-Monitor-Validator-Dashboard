"""
utils.py
Helper functions for formatting data in the dashboard.
"""

from datetime import datetime


def format_wei_to_gwei(wei: int) -> float:
    return round(wei / 1e9, 2)


def format_large_number(n: int) -> str:
    """Format large integers with commas: 21850000 → 21,850,000"""
    return f"{n:,}"


def time_ago(dt: datetime) -> str:
    """Return human-readable relative time: '12s ago', '3m ago'"""
    delta = datetime.now() - dt
    seconds = int(delta.total_seconds())

    if seconds < 60:
        return f"{seconds}s ago"
    elif seconds < 3600:
        return f"{seconds // 60}m ago"
    elif seconds < 86400:
        return f"{seconds // 3600}h ago"
    else:
        return f"{seconds // 86400}d ago"


def format_eth(wei: int) -> str:
    return f"{wei / 1e18:.4f} ETH"


def truncate_address(address: str, chars: int = 6) -> str:
    if len(address) <= chars * 2 + 2:
        return address
    return f"{address[:chars+2]}...{address[-chars:]}"
