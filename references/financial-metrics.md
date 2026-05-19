# Chinese Financial Metrics & Red Flags Guide

## Critical A-Share Specific Metrics

### 1. 扣非净利润 (Deducted Non-Recurring Net Profit)
**Field**: `profit_dedt` in `fina_indicator`, or calculate: `n_income - non_recurring_items`

**Why it matters**: Chinese companies frequently book large non-recurring gains (asset sales, government subsidies, investment revaluations). Net profit can look stellar while core operations deteriorate. **扣非净利润** removes these one-offs and reveals the true operating performance.

**Red flag**: `n_income` grows 50% while `profit_dedt` declines → company is propping up earnings with non-core income.

**Threshold**: If non-recurring items > 20% of net profit for two consecutive quarters → warning signal.

### 2. 经营性现金流 vs. 净利润 (OCF vs. Net Income)
**Field**: `n_cashflow_act` (from cashflow) vs `n_income` (from income)

**Ratio**: `n_cashflow_act / n_income`

| Ratio | Interpretation |
|-------|---------------|
| > 1.0 | High earnings quality — profits backed by cash |
| 0.8-1.0 | Normal — slight timing differences |
| 0.5-0.8 | ⚠️ Caution — possible aggressive revenue recognition |
| < 0.5 | 🔴 Significant risk — profits may be accounting fiction |
| < 0 | 🔴🔴 Severe — burning cash while reporting profits |

### 3. 应收账款 / 营业收入 (AR / Revenue)
**Fields**: `acct_rcv` / `total_revenue`

**What it detects**: Channel stuffing — booking sales but not collecting cash.

**Red flag**: AR grows >30% while revenue grows <10% for two consecutive quarters.

### 4. 商誉 (Goodwill)
**Field**: `goodwill` in balance sheet

**Why it matters**: Massive goodwill from M&A during 2014-2018 boom years is a ticking time bomb. Impairment can wipe out years of profit.

**Red flag**: Goodwill / Net Assets > 30% → impairment risk during earnings downturn.

### 5. 毛利率趋势 (Gross Margin Trend)
**Fields**: `grossprofit_margin` from fina_indicator

**Pattern recognition**:
- Rising margin + stable revenue → pricing power (bullish)
- Rising margin + falling revenue → cutting costs/losing volume (mixed)
- Falling margin + stable revenue → competition pressure (bearish)  
- Falling margin + falling revenue → secular decline (very bearish)

### 6. 研发费用资本化 (R&D Capitalization)
**Field**: `rad_expense` — check if large portion is capitalized (moved to intangible assets on BS)

**Red flag**: Aggressive R&D capitalization inflates current profits at the cost of future amortization charges. Common in pharma/tech.

## HK-Specific Considerations

### 7. 分红率 (Dividend Payout Ratio)
**HK stocks**: `dividend_per_share / eps`

HK investors value dividends highly. A cut in dividend is often more damaging to share price than an EPS miss.

### 8. 汇率影响 (Currency Impact)
Many HK-listed Chinese companies report in CNY but trade in HKD. Check for:
- RMB depreciation → lower HKD value of earnings (negative for H-share price)
- Companies with USD debt → FX losses in `fin_expense` when RMB weakens

## Quality of Earnings Scorecard

Score each factor 0 (worst) to 2 (best):

| Factor | 0 | 1 | 2 |
|-----------|---|---|---|
| OCF / Net Income | < 0.5 | 0.5-0.8 | > 0.8 |
| AR / Revenue trend | AR up >30% | AR up 10-30% | AR stable or down |
| Non-recurring / Net Profit | > 50% | 20-50% | < 20% |
| Gross margin trend | Declining YoY | Flat | Improving YoY |
| Goodwill / Net Assets | > 50% | 30-50% | < 30% |
| Audit opinion | Non-standard | Standard with EoM | Standard clean |
| R&D capitalization rate | > 50% | 20-50% | < 20% |

**Total score interpretation**:
- 12-14: High quality earnings
- 8-11: Acceptable, watch the weak spots
- 4-7: Questionable quality — dig deeper
- 0-3: Likely earnings manipulation — avoid
