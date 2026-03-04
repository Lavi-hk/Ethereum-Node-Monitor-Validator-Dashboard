"""
metrics.py
Generates and stores time-series metrics for charts.
Uses realistic Ethereum gas/block patterns.
"""

import random
import time
from datetime import datetime, timedelta


class MetricsCollector:
    """
    Maintains rolling history of gas prices and block times.
    In a production system this would persist to a DB or Redis.
    """

    def __init__(self):
        self._start_time = time.time()

    def get_gas_history(self, hours: int = 24) -> list:
        """Returns 24h gas price history with realistic patterns."""
        now = datetime.now()
        data = []
        base_gas = 18.0

        for i in range(hours * 4):  # 15-min intervals
            t = now - timedelta(minutes=(hours * 60) - i * 15)
            hour = t.hour

            # Simulate realistic gas patterns: higher during US/EU hours
            if 13 <= hour <= 22:     # Peak hours (UTC)
                noise = random.uniform(5, 25)
            elif 8 <= hour <= 13:    # Morning
                noise = random.uniform(2, 15)
            else:                    # Off-peak
                noise = random.uniform(0.5, 8)

            # Occasional spikes
            if random.random() < 0.05:
                noise *= random.uniform(2, 4)

            gwei = round(base_gas + noise + random.gauss(0, 1.5), 1)
            gwei = max(3.0, gwei)

            data.append({
                "time": t.strftime("%H:%M"),
                "gwei": gwei,
            })

            # Slowly drift base gas
            base_gas += random.gauss(0, 0.3)
            base_gas = max(5.0, min(120.0, base_gas))

        return data

    def get_block_time_history(self, count: int = 50) -> list:
        """Returns recent block time history."""
        data = []
        base_block = 21_850_000

        for i in range(count):
            # Ethereum targets 12s; slight variance
            block_time = round(12.0 + random.gauss(0, 0.4), 2)
            block_time = max(11.0, min(14.0, block_time))
            data.append({
                "block": base_block + i,
                "seconds": block_time,
            })

        return data

    def get_uptime_history(self, days: int = 30) -> list:
        """Returns daily uptime percentages."""
        data = []
        now = datetime.now()

        for i in range(days):
            day = now - timedelta(days=days - i)
            # Mostly 100%, rare brief outages
            if random.random() < 0.03:
                uptime = round(random.uniform(95.0, 99.5), 2)
            else:
                uptime = round(random.uniform(99.8, 100.0), 2)

            data.append({
                "date": day.strftime("%b %d"),
                "uptime": uptime,
            })

        return data
