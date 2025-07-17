# meridian_model_template.py

import pandas as pd
import numpy as np

def run_meridian_model(df, media_cols, target):
    X = df[media_cols]
    y = df[target]

    # Simple linear contribution model
    contributions = {}
    total_contribution = 0

    for col in media_cols:
        correlation = np.corrcoef(X[col], y)[0, 1]
        correlation = 0 if np.isnan(correlation) else correlation
        contributions[col] = max(0, correlation)  # no negative contribution

    total = sum(contributions.values())
    results = []

    for col in media_cols:
        contrib = contributions[col]
        normalized = contrib / total if total > 0 else 0
        avg_spend = X[col].mean()
        est_roi = (normalized * y.mean()) / avg_spend if avg_spend > 0 else 0

        results.append({
            "media_channel": col,
            "estimated_roi": round(est_roi, 2),
            "normalized_contribution": round(normalized, 3)
        })

    return pd.DataFrame(results)
