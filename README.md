# earnings-reviewer

A股/港股季报分析 Skill — 6步自动化管线，tushare 数据驱动。

参照 anthropics/financial-services 的 Earnings Reviewer 方法论设计。

## 6 步管线

1. **拉季报数据** — tushare 拉利润表/资产负债表/现金流/财务指标
2. **分析季报叙事** — 提取关键信号、管理层指引
3. **更新财务模型** — 实际 vs 预期差异表 + 预测修正
4. **审计模型** — 11项审计清单
5. **写分析报告** — 标准化模板
6. **标注待审** — 数据缺口、假设、待验证项

## 结构

- SKILL.md — 核心工作流
- scripts/pull_earnings_data.py — tushare 数据拉取
- references/ — 字段对照、盈利质量评分卡、审计清单
- assets/report-template.md — 报告模板

## 安装

openclaw skill install earnings-reviewer.skill

## 触发

/earnings <ts_code> <period>
