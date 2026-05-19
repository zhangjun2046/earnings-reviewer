# Audit Checklist — Step 4 Reference

## Purpose
Run every check below when auditing a company's reported financials. This catches internal inconsistencies, accounting red flags, and data errors before they reach the analysis report.

## Checklist

### 1. Balance Sheet Identity
**Check**: `total_assets` ≈ `total_liab` + `total_hldr_eqy_inc_min_int`
**Source**: `pro.balancesheet()`
**Pass**: Difference < 1% of total assets
**Fail**: Any meaningful gap → verify data pull, possible restatement

### 2. Cash Flow Reconciliation
**Check**: Net Income → Operating CF makes logical sense
**Method**:
- Start with `n_income`
- Add back non-cash charges (depreciation, impairment)
- Adjust for working capital changes (AR, inventory, AP)
- Result should approximate `n_cashflow_act`
**Pass**: Direction and approximate magnitude align
**Fail**: Large unexplained divergence → investigate working capital items

### 3. Gross Margin Sanity
**Check**: `grossprofit_margin` from `pro.fina_indicator()` ≈ `(total_revenue - oper_cost) / total_revenue * 100`
**Source**: Cross-check income statement vs fina_indicator
**Pass**: Values within 2 percentage points
**Fail**: Discrepancy → one source may have errors

### 4. EPS Reconciliation
**Check**: `n_income_attr_p / shares_outstanding` ≈ `basic_eps`
**Pass**: Within 5%
**Fail**: Check for dilution, preferred dividends, or reporting error

### 5. Non-Recurring Items Flag
**Check**: `n_income - profit_dedt` → amount and % of net profit
**Pass**: Non-recurring < 20% of net profit
**Fail**: >20% → flag as `[关注]` and adjust valuation to use `profit_dedt`

### 6. Segment Revenue Sum
**Check**: Sum of segment revenues ≈ `total_revenue`
**Method**: Income statement `comp_type=1` (consolidated) vs segment breakdown if available
**Pass**: Within 2%
**Fail**: Possible unallocated items or reporting inconsistency

### 7. Period-over-Period Consistency
**Check**: Accounting policies unchanged? Any restatements?
**Method**: Compare current period notes to prior period
**Pass**: No changes flagged
**Fail**: Changes flagged → mark `[关注]` and note in report

### 8. Operating CF Quality (A-shares: MOST IMPORTANT)
**Check**: `n_cashflow_act / n_income`
**Pass**: > 0.8
**Fail**: < 0.8 → flag earnings quality concern. < 0.5 → CRITICAL ALERT.

### 9. Accounts Receivable Growth vs Revenue Growth
**Check**: AR growth rate vs revenue growth rate (YoY)
**Pass**: AR growth ≤ revenue growth + 10%
**Fail**: AR growth > revenue growth + 30% → possible channel stuffing

### 10. Goodwill Impairment Risk
**Check**: `goodwill / total_hldr_eqy_inc_min_int`
**Pass**: < 30%
**Fail**: > 30% → goodwill impairment risk during earnings stress

### 11. Audit Opinion Check (A-shares only)
**Check**: `pro.fina_audit()` — `audit_opinion`
**Pass**: 标准无保留意见
**Fail**: Any other opinion → CRITICAL ALERT, surface immediately

## Output Format

Present results as:

```
## 🔍 模型审计结果

| # | 检查项 | 结果 | 详情 |
|---|--------|------|------|
| 1 | 资产负债表等式 | ✅/❌ | 差值: X% |
| 2 | 现金流核对 | ✅/❌ | |
| 3 | 毛利率一致性 | ✅/❌ | |
| 4 | EPS 核对 | ✅/❌ | |
| 5 | 非经常性损益 | ✅/⚠️/❌ | 占净利润 X% |
| 6 | 分部收入汇总 | ✅/❌ | |
| 7 | 会计政策一致性 | ✅/⚠️ | |
| 8 | 盈利质量 (OCF/NI) | ✅/⚠️/❌ | 比率: X |
| 9 | 应收/收入增长 | ✅/⚠️/❌ | AR: +X%, Rev: +Y% |
| 10 | 商誉风险 | ✅/⚠️/❌ | 商誉/净资产: X% |
| 11 | 审计意见 | ✅/❌ | 意见类型 |

通过: X/11 | 关注: X | 警告: X
```
