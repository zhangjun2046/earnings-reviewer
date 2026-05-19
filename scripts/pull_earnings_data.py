#!/usr/bin/env python3
"""
Earnings Data Puller — Batch pull financial data from tushare for earnings review.

Usage:
    python3 pull_earnings_data.py <ts_code> <period> [--prior-periods N]

Examples:
    # A-share: pull 2025 Q1 data + 2 prior periods
    python3 pull_earnings_data.py 002594.SZ 20250331 --prior-periods 2

    # HK stock: pull 2025 annual data
    python3 pull_earnings_data.py 0981.HK 20251231 --prior-periods 1

Output: JSON to stdout with structure:
{
  "ts_code": "...",
  "period": "...",
  "income": {...},        # Current period income statement
  "balance_sheet": {...}, # Current period balance sheet
  "cashflow": {...},      # Current period cash flow
  "indicators": {...},    # Current period financial indicators
  "audit": {...},         # Audit opinion (A-shares only)
  "prior_periods": {      # Prior periods for comparison
    "income": [...],
    "indicators": [...]
  }
}
"""

import tushare as ts
import json
import sys
import os
from datetime import datetime, timedelta

TOKEN = "a62be7a105a63458c5c2c95568f1a3c447a6906eab1f40edb445efda"

# Key fields to pull from each API
INCOME_FIELDS = [
    "ts_code", "end_date", "total_revenue", "revenue", "total_cogs",
    "oper_cost", "operate_profit", "total_profit", "n_income",
    "n_income_attr_p", "basic_eps", "diluted_eps",
    "sale_expense", "admin_expense", "fin_expense", "rad_expense",
    "int_income", "int_expense", "inv_income",
    "non_oper_income", "non_oper_expense", "less_impair_assets",
    "comp_type"
]

BALANCE_FIELDS = [
    "ts_code", "end_date", "total_assets", "total_cur_assets",
    "total_hldr_eqy_inc_min_int", "total_liab", "total_cur_liab",
    "total_ncl", "monetory_cap", "acct_rcv", "inventories",
    "fix_assets", "goodwill", "intan_assets",
    "notes_rcv", "st_borrow", "lt_borrow", "acct_payable",
    "undistributed_profit", "comp_type"
]

CASHFLOW_FIELDS = [
    "ts_code", "end_date", "n_cashflow_act", "n_cashflow_inv_act",
    "n_cashflow_fin_act", "c_inf_fr_operate_a", "st_cash_out_act",
    "oth_cash_in_act", "c_paid_p_empl_etc", "comp_type"
]

INDICATOR_FIELDS = [
    "ts_code", "end_date", "roe", "roe_dt", "roa",
    "grossprofit_margin", "netprofit_margin",
    "debt_to_assets", "current_ratio", "quick_ratio",
    "inv_turn", "ar_turn", "assets_turn",
    "basic_eps", "diluted_eps", "bps", "ocfps",
    "ebit", "ebitda", "fcff", "fcfe",
    "profit_dedt", "rd_expense"
]

AUDIT_FIELDS = [
    "ts_code", "end_date", "audit_opinion", "audit_agency"
]


def get_prior_period(period: str, steps_back: int) -> str:
    """Calculate prior period by stepping back N quarters."""
    # Period format: YYYYMMDD
    y = int(period[:4])
    m = int(period[4:6])
    d = int(period[6:8])

    dt = datetime(y, m, d)
    # Step back 3 months per quarter
    for _ in range(steps_back):
        # Go back 3 months
        new_m = dt.month - 3
        new_y = dt.year
        if new_m <= 0:
            new_m += 12
            new_y -= 1
        # Keep the same day, but clamp to month end
        try:
            dt = datetime(new_y, new_m, dt.day)
        except ValueError:
            # Day doesn't exist in month (e.g., 31st in Feb) — use last day
            if new_m == 12:
                dt = datetime(new_y + 1, 1, 1) - timedelta(days=1)
            else:
                dt = datetime(new_y, new_m + 1, 1) - timedelta(days=1)

    return dt.strftime("%Y%m%d")


def fetch_data(pro, ts_code: str, period: str, is_hk: bool) -> dict:
    """Pull all financial data for a single period."""

    result = {"ts_code": ts_code, "period": period}

    # Determine API endpoints based on market
    try:
        # Income statement
        income = pro.income(ts_code=ts_code, end_date=period, fields=",".join(INCOME_FIELDS))
        # Filter for consolidated (comp_type=1 or '1')
        if not income.empty:
            income = income[income['comp_type'].astype(str).isin(['1', '1.0'])]
        result["income"] = income.head(1).to_dict(orient="records")[0] if not income.empty else None
    except Exception as e:
        result["income"] = None
        result["income_error"] = str(e)

    try:
        balance = pro.balancesheet(ts_code=ts_code, end_date=period, fields=",".join(BALANCE_FIELDS))
        if not balance.empty:
            balance = balance[balance['comp_type'].astype(str).isin(['1', '1.0'])]
        result["balance_sheet"] = balance.head(1).to_dict(orient="records")[0] if not balance.empty else None
    except Exception as e:
        result["balance_sheet"] = None
        result["balance_error"] = str(e)

    try:
        cashflow = pro.cashflow(ts_code=ts_code, end_date=period, fields=",".join(CASHFLOW_FIELDS))
        if not cashflow.empty:
            cashflow = cashflow[cashflow['comp_type'].astype(str).isin(['1', '1.0'])]
        result["cashflow"] = cashflow.head(1).to_dict(orient="records")[0] if not cashflow.empty else None
    except Exception as e:
        result["cashflow"] = None
        result["cashflow_error"] = str(e)

    try:
        indicators = pro.fina_indicator(ts_code=ts_code, end_date=period, fields=",".join(INDICATOR_FIELDS))
        result["indicators"] = indicators.head(1).to_dict(orient="records")[0] if not indicators.empty else None
    except Exception as e:
        result["indicators"] = None
        result["indicators_error"] = str(e)

    # Audit opinion (A-shares only)
    if not is_hk:
        try:
            audit = pro.fina_audit(ts_code=ts_code, end_date=period, fields=",".join(AUDIT_FIELDS))
            result["audit"] = audit.head(1).to_dict(orient="records")[0] if not audit.empty else None
        except Exception as e:
            result["audit"] = None
            result["audit_error"] = str(e)
    else:
        result["audit"] = None  # HK stocks don't have this API

    return result


def main():
    if len(sys.argv) < 3:
        print("Usage: pull_earnings_data.py <ts_code> <period> [--prior-periods N]", file=sys.stderr)
        sys.exit(1)

    ts_code = sys.argv[1]
    period = sys.argv[2]

    # Parse optional args
    prior_count = 1  # default: pull last quarter
    args = sys.argv[3:]
    i = 0
    while i < len(args):
        if args[i] == "--prior-periods" and i + 1 < len(args):
            prior_count = int(args[i + 1])
            i += 2
        else:
            i += 1

    # Determine market
    is_hk = ".HK" in ts_code.upper()

    pro = ts.pro_api(TOKEN)

    # Fetch current period
    output = fetch_data(pro, ts_code, period, is_hk)

    # Fetch prior periods
    output["prior_periods"] = {"income": [], "indicators": []}
    for step in range(1, prior_count + 1):
        prior_period = get_prior_period(period, step)
        prior_data = fetch_data(pro, ts_code, prior_period, is_hk)
        if prior_data.get("income"):
            output["prior_periods"]["income"].append({
                "period": prior_period,
                "data": prior_data["income"]
            })
        if prior_data.get("indicators"):
            output["prior_periods"]["indicators"].append({
                "period": prior_period,
                "data": prior_data["indicators"]
            })

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
