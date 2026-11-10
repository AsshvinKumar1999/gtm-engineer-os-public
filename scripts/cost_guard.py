"""Pre-flight spend guard with spend tiers. Refuses paid runs that are not explicitly confirmed.

<$100 proceed · $100–1,000 needs --yes · $1,000–10,000 needs --confirm-spend matching within $5 ·
>$10,000 also needs --i-mean-it. A ledger file accumulates committed estimates per job.

Usage: python scripts/cost_guard.py --rows 5000 --unit-price 0.002 [--yes] [--confirm-spend 10] [--i-mean-it] [--ledger runs/job.ledger]
"""
from __future__ import annotations
import argparse
import sys
from decimal import Decimal
from pathlib import Path


def estimate(rows: int, unit_price: Decimal) -> Decimal:
    if rows < 0 or unit_price < 0:
        raise ValueError("rows and unit price must be non-negative")
    return (Decimal(rows) * unit_price).quantize(Decimal("0.01"))


def check(est: Decimal, yes: bool, confirm: Decimal | None, mean_it: bool) -> tuple[bool, str]:
    if est < 100:
        return True, f"estimate ${est}: under $100, proceeding"
    if est < 1000:
        return (yes, f"estimate ${est}: pass --yes to proceed") if not yes else (True, f"estimate ${est}: confirmed")
    if confirm is None or abs(confirm - est) > 5:
        return False, f"estimate ${est}: pass --confirm-spend {est} (within $5)"
    if est >= 10000 and not mean_it:
        return False, f"estimate ${est}: over $10,000 also needs --i-mean-it"
    return True, f"estimate ${est}: confirmed"


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--rows", type=int, required=True)
    p.add_argument("--unit-price", type=Decimal, required=True)
    p.add_argument("--yes", action="store_true")
    p.add_argument("--confirm-spend", type=Decimal)
    p.add_argument("--i-mean-it", action="store_true")
    p.add_argument("--ledger", type=Path)
    a = p.parse_args(argv)
    est = estimate(a.rows, a.unit_price)
    prior = Decimal(0)
    if a.ledger and a.ledger.exists():
        prior = sum((Decimal(x) for x in a.ledger.read_text().split()), Decimal(0))
    ok, msg = check(prior + est, a.yes, a.confirm_spend, a.i_mean_it)
    print(msg + (f" (includes ${prior} already ledgered)" if prior else ""))
    if ok and a.ledger:
        a.ledger.parent.mkdir(parents=True, exist_ok=True)
        with a.ledger.open("a") as fh:
            fh.write(f"{est}\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
