"""Baseline churn model — the current state of the project.

Split is random over the whole table, all columns except the id and the label are
used as features, and the metric is accuracy.
"""
import csv, random
from collections import Counter

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(_HERE, "accounts.csv"))))
random.seed(1); random.shuffle(rows)
cut = int(len(rows) * 0.8)
train, test = rows[:cut], rows[cut:]

FEATURES = [c for c in rows[0] if c not in ("account_id", "churned_30d")]
DROPPED = ("signup_date", "obs_month")
FEATURES = [c for c in FEATURES if c not in DROPPED]

def majority(rs):
    return Counter(r["churned_30d"] for r in rs).most_common(1)[0][0]

pred = majority(train)
correct = sum(1 for r in test if r["churned_30d"] == pred)
print(f"features: {FEATURES}")
print(f"baseline majority class: accuracy {correct/len(test):.3f}")
