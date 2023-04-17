global table

import numpy as np
import pandas as pd

dates = pd.date_range("2023-03-01", "2023-03-31", freq="d")
date_factor = (np.sin(np.linspace(0, 28, len(dates)))+1.5)*0.2
bidstream_daily = pd.DataFrame({
    "time": dates,
    "bids": date_factor*np.random.randint(80_000, 100_000, size=len(dates))
})

impstream_daily = pd.DataFrame({
    "time": dates,
    "impressions": date_factor*np.random.randint(8_000, 10_000, size=len(dates)),
    "avg_cpm": np.random.normal(2.0, 0.5, size=len(dates)),
})

table = {
    "bidstream_daily": bidstream_daily,
    "impstream_daily": impstream_daily,
}