# tushare API Field Mapping

## Income Statement (利润表)

tushare API: `pro.income(ts_code='...', period='YYYYMMDD', fields='...')`

### A-shares (fields from `pro.income()`)

| tushare Field | Chinese Name | English | Notes |
|---------------|-------------|---------|-------|
| `ts_code` | 股票代码 | Ticker | e.g., 000001.SZ |
| `end_date` | 报告期 | Period End | YYYYMMDD |
| `total_revenue` | 营业总收入 | Total Revenue | Top line |
| `revenue` | 营业收入 | Operating Revenue | Revenue from core business |
| `total_cogs` | 营业总成本 | Total COGS | All costs |
| `oper_cost` | 营业成本 | Operating Cost | Direct cost of revenue |
| `operate_profit` | 营业利润 | Operating Profit | Revenue - COGS - SG&A |
| `total_profit` | 利润总额 | Total Profit | Before tax |
| `n_income` | 净利润 | Net Income | Bottom line |
| `n_income_attr_p` | 归属母公司净利润 | Net Income to Parent | Attributable to parent co |
| `undist_profit` | 未分配利润 | Undistributed Profit | |
| `basic_eps` | 基本每股收益 | Basic EPS | yuan per share |
| `diluted_eps` | 稀释每股收益 | Diluted EPS | |
| `sale_expense` | 销售费用 | Selling Expenses | |
| `admin_expense` | 管理费用 | Admin Expenses | |
| `fin_expense` | 财务费用 | Finance Expenses | Net interest + FX |
| `rad_expense` | 研发费用 | R&D Expenses | |
| `int_income` | 利息收入 | Interest Income | |
| `int_expense` | 利息支出 | Interest Expense | |
| `inv_income` | 投资收益 | Investment Income | |
| `oper_tax` | 营业税金及附加 | Business Tax & Surcharges | |
| `less_impair_assets` | 资产减值损失 | Asset Impairment Loss | |
| `non_oper_income` | 营业外收入 | Non-Operating Income | One-off gains |
| `non_oper_expense` | 营业外支出 | Non-Operating Expenses | |
| `comp_type` | 报表类型 | Report Type | 1=合并, 2=母公司, etc. |

### HK stocks (fields from `pro.income()`)

Same field names as A-shares. Key difference: HK data may be:
- Semi-annual only (Q2, Q4 — periods ending 0630 and 1231)
- Some stocks provide quarterly (Q1, Q2, Q3, Q4)
- Currency: typically CNY for mainland companies listed in HK, but some report in HKD

## Balance Sheet (资产负债表)

tushare API: `pro.balancesheet(ts_code='...', period='YYYYMMDD')`

| tushare Field | Chinese Name | English | Notes |
|---------------|-------------|---------|-------|
| `total_assets` | 资产总计 | Total Assets | |
| `total_cur_assets` | 流动资产合计 | Total Current Assets | |
| `total_hldr_eqy_inc_min_int` | 股东权益合计 | Total Shareholders' Equity | |
| `total_liab` | 负债合计 | Total Liabilities | |
| `total_cur_liab` | 流动负债合计 | Total Current Liabilities | |
| `total_ncl` | 非流动负债合计 | Total Non-Current Liabilities | |
| `monetory_cap` | 货币资金 | Cash & Cash Equivalents | |
| `acct_rcv` | 应收账款 | Accounts Receivable | |
| `inventories` | 存货 | Inventories | |
| `fix_assets` | 固定资产 | Fixed Assets | |
| `goodwill` | 商誉 | Goodwill | Impairment risk signal |
| `intan_assets` | 无形资产 | Intangible Assets | |
| `notes_rcv` | 应收票据 | Notes Receivable | |
| `st_borrow` | 短期借款 | Short-term Borrowings | |
| `lt_borrow` | 长期借款 | Long-term Borrowings | |
| `acct_payable` | 应付账款 | Accounts Payable | |
| `undistributed_profit` | 未分配利润 | Retained Earnings | |

## Cash Flow Statement (现金流量表)

tushare API: `pro.cashflow(ts_code='...', period='YYYYMMDD')`

| tushare Field | Chinese Name | English | Notes |
|---------------|-------------|---------|-------|
| `n_cashflow_act` | 经营活动现金流量净额 | Operating CF | Key quality-of-earnings signal |
| `n_cashflow_inv_act` | 投资活动现金流量净额 | Investing CF | CapEx-heavy if negative |
| `n_cashflow_fin_act` | 筹资活动现金流量净额 | Financing CF | Dividends, debt, equity |
| `c_inf_fr_operate_a` | 销售商品提供劳务收到的现金 | Cash from Sales | Compare to revenue |
| `st_cash_out_act` | 购买商品接受劳务支付的现金 | Cash Paid to Suppliers | |
| `oth_cash_in_act` | 收到的其他与经营活动有关的现金 | Other Operating Cash In | |
| `c_paid_p_empl_etc` | 支付给职工以及为职工支付的现金 | Cash Paid to Employees | |

## Financial Indicators (财务指标)

tushare API: `pro.fina_indicator(ts_code='...', period='YYYYMMDD')`

| tushare Field | Chinese Name | English | Notes |
|---------------|-------------|---------|-------|
| `roe` | 净资产收益率 | ROE | Net income / avg equity |
| `roe_dt` | 净资产收益率(扣非) | ROE (deducted) | After removing non-recurring |
| `roa` | 总资产收益率 | ROA | |
| `grossprofit_margin` | 销售毛利率 | Gross Margin % | |
| `netprofit_margin` | 销售净利率 | Net Margin % | |
| `debt_to_assets` | 资产负债率 | Debt-to-Assets % | |
| `current_ratio` | 流动比率 | Current Ratio | |
| `quick_ratio` | 速动比率 | Quick Ratio | |
| `inv_turn` | 存货周转率 | Inventory Turnover | |
| `ar_turn` | 应收账款周转率 | AR Turnover | |
| `assets_turn` | 总资产周转率 | Asset Turnover | |
| `basic_eps` | 基本每股收益 | Basic EPS | |
| `diluted_eps` | 稀释每股收益 | Diluted EPS | |
| `bps` | 每股净资产 | Book Value Per Share | |
| `ocfps` | 每股经营活动现金流量 | Operating CF Per Share | |
| `ebit` | 息税前利润 | EBIT | |
| `ebitda` | 息税折旧摊销前利润 | EBITDA | |
| `fcff` | 企业自由现金流 | FCFF | Firm free cash flow |
| `fcfe` | 股权自由现金流 | FCFE | Equity free cash flow |
| `profit_dedt` | 扣除非经常性损益后的净利润 | Deducted Net Profit | **CRITICAL for A-shares** |
| `rd_expense` | 研发费用 | R&D Expense | |

## Audit Opinion (审计意见)

tushare API: `pro.fina_audit(ts_code='...', period='YYYYMMDD')` — A-shares only

| tushare Field | Chinese Name | English | Notes |
|---------------|-------------|---------|-------|
| `audit_opinion` | 审计意见 | Audit Opinion | Key values below |
| `audit_agency` | 审计机构 | Audit Firm | |

Audit opinion values:
- 标准无保留意见 = Standard Unqualified (✅ 正常)
- 带强调事项段的无保留意见 = Unqualified with Emphasis of Matter (⚠️ 需关注)
- 保留意见 = Qualified (🔴 严重警告)
- 无法表示意见 = Disclaimer (🔴🔴 极度危险)
- 否定意见 = Adverse (🔴🔴 极度危险)

## Period Format

tushare period format is `YYYYMMDD`:
- Q1 report: YYYY0331
- Semi-annual: YYYY0630
- Q3 report: YYYY0930
- Annual: YYYY1231

For prior periods: subtract 3, 6, or 12 months accordingly.

## Key Computed Ratios

Calculate these from raw fields if not available in fina_indicator:

```python
# Gross Margin
gross_margin = (total_revenue - oper_cost) / total_revenue * 100

# Operating Margin  
operating_margin = operate_profit / total_revenue * 100

# Net Margin
net_margin = n_income / total_revenue * 100

# Debt-to-Equity
d_e_ratio = total_liab / total_hldr_eqy_inc_min_int

# Operating CF / Net Income (Quality of Earnings)
earnings_quality = n_cashflow_act / n_income

# Revenue Growth YoY
revenue_growth_yoy = (current_revenue / prior_year_same_period_revenue - 1) * 100

# Receivables / Revenue (channel stuffing check)
recv_to_rev = acct_rcv / total_revenue
```
