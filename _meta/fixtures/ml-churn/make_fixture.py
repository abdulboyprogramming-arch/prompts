"""Build a small churn-style dataset with three planted leakage paths.

The fixture is deliberately realistic: a signup cohort over 18 months, a monthly
label, and columns that a data team would plausibly have added. Three columns leak
the label, one leaks through time because the split is random, and one is a subtle
post-hoc aggregate that looks innocuous.
"""
import csv, random, datetime, os

random.seed(7)
start = datetime.date(2024, 1, 1)
rows = []
for i in range(1200):
    signup = start + datetime.timedelta(days=random.randint(0, 500))
    plan = random.choice(["free", "pro", "team"])
    seats = random.randint(1, 40)
    mrr = {"free": 0, "pro": 29, "team": 199}[plan] * max(1, seats // 5)
    logins = max(0, int(random.gauss(20, 8)))
    support = max(0, int(random.gauss(2, 2)))
    # label: churn in the 30 days after the observation month
    risk = 0.10 + (0.35 if plan == "free" else 0) + (0.20 if logins < 8 else 0) + (0.05 * support)
    churned = 1 if random.random() < min(risk, 0.9) else 0
    # TRAP 1: only populated for churned accounts
    cancel_reason = random.choice(["price", "missing_feature", "switched"]) if churned else ""
    # TRAP 2: a status column that is a function of the label
    status = "cancelled" if churned else "active"
    # TRAP 3 (subtle): days since last login, measured *after* the outcome window
    last_login_days = random.randint(31, 40) if churned else random.randint(0, 20)
    rows.append({
        "account_id": f"A{i:05d}",
        "signup_date": signup.isoformat(),
        "obs_month": (signup + datetime.timedelta(days=30)).replace(day=1).isoformat(),
        "plan": plan, "seats": seats, "mrr": mrr,
        "logins_30d": logins, "support_tickets_30d": support,
        "last_login_days": last_login_days,
        "status": status, "cancel_reason": cancel_reason,
        "churned_30d": churned,
    })
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "accounts.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
print(f"{len(rows)} rows, churn rate {sum(r['churned_30d'] for r in rows)/len(rows):.2%}")
