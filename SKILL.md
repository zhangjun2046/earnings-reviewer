---
name: earnings-reviewer
description: >-
  End-to-end earnings analysis workflow for A-share and HK stocks using tushare data.
  Follows a structured 6-step pipeline (pull financial data, analyze earnings call transcripts,
  update financial models, audit the model, draft the analysis report, and surface for review).
  Use when a covered A-share or HK-listed company releases quarterly/annual earnings,
  or when the user asks for earnings review, 季报分析, 年报分析, post-earnings analysis,
  financial report review, or any variation of "analyze this earnings report".
  Also triggers on /earnings command.
---

# Earnings Reviewer — A股/港股季报分析

## Overview

End-to-end earnings analysis for A-share and HK-listed stocks. Follow a structured 6-step pipeline adapted from the anthropics/financial-services framework, using **tushare** as the sole data source (per project rules).

**Maximum 2-3 tushare API calls per step, at most 15 API calls total.** Batch related queries to minimize roundtrips.

## The 6-Step Pipeline

Execute steps in order. Surface findings after each step for user checkpoint before proceeding. Never skip the audit step (Step 4).

### Step 1: Pull Earnings Data

Objective: Gather all reported financials for the period.

**For A-shares** (ts_code format: `000001.SZ` / `600000.SH`):
- `pro.income(ts_code='xxxxxx.SZ', period='YYYYMMDD')` — revenue, costs, operating profit, net profit
- `pro.balancesheet(ts_code='xxxxxx.SZ', period='YYYYMMDD')` — total assets, liabilities, equity
- `pro.cashflow(ts_code='xxxxxx.SZ', period='YYYYMMDD')` — operating/investing/financing cash flows
- `pro.fina_indicator(ts_code='xxxxxx.SZ', period='YYYYMMDD')` — ROE, ROA, gross margin, net margin, debt ratio, current ratio, EPS

**For HK stocks** (ts_code format: `02513.HK`):
- `pro.income(ts_code='xxxxx.HK', period='YYYYMMDD')` — same fields (note: HK data may be semi-annual/annual only)
- `pro.balancesheet(ts_code='xxxxx.HK', period='YYYYMMDD')`
- `pro.cashflow(ts_code='xxxxx.HK', period='YYYYMMDD')`
- `pro.fina_indicator(ts_code='xxxxx.HK', period='YYYYMMDD')`

**Compare with prior period**: Pull the same statements for the previous quarter and same quarter last year (YoY).

**Action**: Present a summary table of key metrics vs. prior quarter and YoY. Flag anomalies (>20% divergence).

---

### Step 2: Analyze Earnings Context

Objective: Understand the narrative behind the numbers.

**Data sources** (no tushare for this — use available tools):
- Search for earnings call transcripts (use multi-search-engine skill or web_fetch on trusted financial news sites)
- Company announcements (沪深交易所公告 / 港交所公告)
- Management guidance changes

**Analysis points**:
- Revenue drivers: volume vs. price, segment performance
- Margin trends: gross margin, operating margin, net margin — what drove the change?
- Non-recurring items: mark any one-off gains/losses
- Management tone: guidance raised/lowered/maintained, key concerns addressed/dodged?
- Segment breakdown: which business lines outperformed/underperformed?

**⚠️ Important**: Chinese A-share companies rarely publish full earnings call transcripts publicly. If unavailable:
- Use annual/semi-annual report management discussion sections (董事会报告/管理层讨论与分析)
- Flag as `[无电话会记录]` and work from filing text instead

**Action**: Produce a narrative summary structured by: revenue drivers → margin analysis → segment performance → management outlook → red flags.

---

### Step 3: Update Financial Model

Objective: Compare actuals vs. prior estimates and roll forward forecasts.

**What to produce**:
1. **Variance table**: Actual vs. estimated for key metrics (revenue, gross profit, operating profit, net profit, EPS, OCF)
2. **Estimate revision**: Adjust forward estimates based on new actuals and guidance
3. **Growth trajectory**: Plot the trend line — accelerating/decelerating/stable?

**Key metrics to track**:

| Metric | Current Period | Prior Quarter | YoY | Estimate | Variance |
|--------|---------------|---------------|-----|----------|----------|
| Revenue | — | — | — | — | — |
| Gross Margin % | — | — | — | — | — |
| Operating Profit | — | — | — | — | — |
| Net Profit | — | — | — | — | — |
| EPS | — | — | — | — | — |
| Operating Cash Flow | — | — | — | — | — |
| ROE % | — | — | — | — | — |

**For A-shares**, pay special attention to:
- 扣非净利润 (deducted non-recurring P&L) — a critical metric for Chinese stocks
- 经营性现金流 vs. 净利润 divergence (quality of earnings signal)

**For HK stocks**, pay attention to:
- Dividend payout ratio trend (HK investors value dividends highly)
- Currency exposure (RMB vs HKD reporting differences)

**Action**: Present the variance table and highlight the 2-3 biggest surprises (positive or negative). Ask user whether to proceed with estimate revision.

---

### Step 4: Audit the Model

Objective: Ensure numbers are internally consistent before drafting conclusions.

**Audit checklist**:
1. **Balance check**: Total Assets = Total Liabilities + Equity? (from balance sheet)
2. **Cash flow reconciliation**: Net Income → Operating Cash Flow walk makes sense?
3. **Gross margin sanity**: Is the reported gross margin consistent with the revenue/COGS numbers?
4. **EPS check**: Net Profit / Shares Outstanding ≈ reported EPS?
5. **Non-recurring items**: Are large non-recurring items properly flagged and excluded from normalized earnings?
6. **Segment reconciliation**: Do segment revenues sum to total revenue?
7. **Period-over-period consistency**: Are accounting policy changes or restatements flagged?

**Red flags to surface immediately**:
- Operating cash flow significantly diverges from net profit (possible earnings quality issue)
- Large increase in receivables without corresponding revenue growth (channel stuffing risk)
- Sudden gross margin expansion without clear cost-side driver (aggressive accounting?)
- Auditor opinion: anything other than 标准无保留意见 (standard unqualified opinion)

Use `pro.fina_audit(ts_code='...', period='YYYYMMDD')` to check audit opinion for A-shares.

**Action**: Run each check and present a pass/fail table. If any check fails, flag it prominently before proceeding to Step 5.

---

### Step 5: Write Analysis Report

Objective: Produce a structured earnings review report in the voice of 赛博巴菲特.

**Report structure** (use `assets/report-template.md`):

1. **Headers**: Company name, ticker, period, report date, analyst (赛博巴菲特)
2. **Executive Summary** (3-5 sentences): The one-sentence verdict on the quarter, top 2 surprises, investment thesis status
3. **Key Metrics Dashboard**: The variance table from Step 3
4. **Revenue Analysis**: By segment if available, volume/price breakdown
5. **Profitability Analysis**: Gross margin → Operating margin → Net margin walk
6. **Cash Flow & Balance Sheet Health**: Quality of earnings assessment
7. **Segment Performance**: If conglomerate with multiple business lines
8. **Management Outlook**: Guidance, strategy shifts, capital allocation plans
9. **Investment Thesis Check**: Revisit original thesis — confirmed, challenged, or neutral?
10. **Valuation Update**: Quick re-anchor to DCF range or comparable multiples
11. **Risk Factors**: New or elevated risks identified this quarter
12. **Actionable Conclusion**: 看好/谨慎看好/观望/谨慎看空/看空 + specific price/valuation trigger points

**Writing style** (per SOUL.md):
- Professional but not stiff
- Data-driven, every number cited to source
- Honest: flag concerns, don't sugar-coat
- Occasional humor, but never at the expense of rigor
- Mark unsourced numbers as `[待验证]`

---

### Step 6: Surface for Review

Objective: Present the report with clear annotation of what needs human review.

**Annotation system**:

| Tag | Meaning |
|-----|---------|
| `[待验证]` | Data point that could not be confirmed from primary sources |
| `[假设]` | Modeling assumption that needs user input |
| `[关注]` | Red flag or area requiring deeper investigation |
| `[已确认]` | Data point verified from filings |

**What to present**:
1. The full report (drafted in Step 5)
2. A reviewer's checklist at the top:
   - Top 3 things that need human judgment
   - Items tagged `[待验证]` or `[假设]`
   - Audit flags from Step 4 that didn't pass
3. Price alert recommendation (offer to create/update cron-based price alerts via the cron tool)

**Delivery**: Present directly in chat. If user is on 飞书, adhere to feishu-channel-rules skill (structured Markdown, no unsolicited messages).

---

## Quick Reference

### tushare API Map

| Need | For A-shares | For HK stocks |
|------|-------------|---------------|
| Income Statement | `pro.income(ts_code='xxx.SZ')` | `pro.income(ts_code='xxx.HK')` |
| Balance Sheet | `pro.balancesheet(ts_code='xxx.SZ')` | `pro.balancesheet(ts_code='xxx.HK')` |
| Cash Flow | `pro.cashflow(ts_code='xxx.SZ')` | `pro.cashflow(ts_code='xxx.HK')` |
| Financial Indicators | `pro.fina_indicator(ts_code='xxx.SZ')` | `pro.fina_indicator(ts_code='xxx.HK')` |
| Daily Price | `pro.daily(ts_code='xxx.SZ')` | `pro.hk_daily(ts_code='xxx.HK')` |
| Audit Opinion | `pro.fina_audit(ts_code='xxx.SZ')` | N/A (HK stocks use different audit disclosure) |
| Stock Basic Info | `pro.stock_basic()` | `pro.hk_basic()` |
| Dividend | `pro.dividend(ts_code='xxx.SZ')` | N/A for HK |

### tushare Token
Token: `a62be7a105a63458c5c2c95568f1a3c447a6906eab1f40edb445efda`

Set via: `pro = ts.pro_api('a62be7a105a63458c5c2c95568f1a3c447a6906eab1f40edb445efda')`

## Resources

### scripts/
- `pull_earnings_data.py` — Batch pull income, balance sheet, cash flow, and indicators from tushare in one run. Accepts ts_code, period, and prior periods for comparison. Outputs JSON.

### references/
- `tushare-mapping.md` — Detailed field mapping for tushare financial APIs (Chinese → English, key metrics extraction)
- `financial-metrics.md` — Definition and interpretation of Chinese financial metrics (扣非净利润, 经营性现金流, etc.)
- `report-checklist.md` — Step 4 audit checklist with detailed pass/fail criteria

### assets/
- `report-template.md` — Full analysis report template in 赛博巴菲特 style
