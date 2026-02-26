---
type: persona-research
project: overseas-amazon-seller-agent
version: v1.2
status: completed
updated_bjt: 2026-02-26 21:40
scope: 海外亚马逊卖家（剔除中国卖家）
exclude: China-based sellers
search_strategy: direct-source-fetch (非 Brave 检索)
---

# Amazon Seller ICP 画像调研 v1.2（已完成）

## 0) 方法说明（按你的要求）
本版已切换为**直接来源抓取**，不依赖原搜索 API 连续检索：
- 直接读取 Amazon 官方报告页
- 直接读取 Jungle Scout 年度报告页
- 用可公开访问的一手/二手行业页面做交叉

---

## 1) 结论先行：主战 ICP（推荐）

### ICP-Primary：US/EU 私牌 SMB 卖家（3P，非中国主体）

**画像定义**
- 主体：美国/欧洲公司主体的 Amazon 3P 卖家
- 团队：2-15 人（创始人 + 运营 + 广告/供应链）
- 规模：已有稳定上架与广告投放，不是纯新手
- 目标：利润率稳定增长，而非只追 GMV

**核心痛点（按优先级）**
1. 成本上行挤压利润（运费/货品/广告）
2. 运营复杂度高（多 SKU、多广告组、跨站点）
3. 风险响应慢（断货、差评突增、合规变化）

**付费触发点**
- 能直接给“可执行动作 + 预期收益区间”
- 能减少每周 5-10 小时运营时间
- 能把 ACOS/库存周转/断货率做出连续改善

**不做人群（明确排除）**
- 中国主体卖家（本项目策略排除）

---

## 2) 次级 ICP

### ICP-Secondary：US/EU 多店铺运营团队（10-30 人）
- 痛点：协同与标准化、跨市场复用、报表归因
- 机会：流程编排 Agent + 跨团队周报复盘
- 风险：采购链条长，决策周期更长，落地速度慢于 SMB

---

## 3) 反画像（Negative ICP）
- 仅想“免费拿建议”，不执行动作闭环
- 无稳定预算、无基本运营数据沉淀
- 只追爆款短期套利，不关心系统化经营

原因：难形成可复用 ROI 与产品口碑样本。

---

## 4) 证据与来源（可追溯）

1. **Amazon 官方（2023 Small Business Empowerment Report）**  
   https://www.aboutamazon.com/news/small-business/amazon-2023-small-business-empowerment-report  
   关键点：Amazon 店内销售中独立卖家占比超过 60%，且以中小企业为主。

2. **Jungle Scout（State of the Amazon Seller 2025）**  
   https://www.junglescout.com/resources/reports/amazon-seller-report-2025/  
   关键点：样本约 1,500，覆盖多国与卖家层级；成本上升（shipping/cogs/ads）为核心挑战。

3. **行业佐证（公开二手）**  
   https://www.pymnts.com/amazon/2023/amazon-independent-sellers-make-up-60percent-of-ecommerce-sales/  
   关键点：复述 Amazon 报告中独立卖家占比与 SMB 结构，作为媒体侧交叉引用。

---

## 5) 置信度评估
- **总体置信度：7.8 / 10（中高）**
- 优势：有官方源 + 行业年度样本源 + 媒体交叉
- 局限：本版尚未接入你客户私有经营数据（广告/库存/利润），下一版需补行为数据验证

---

## 6) 产品映射（v1.2 可执行）

### 面向 ICP-Primary 的首版功能包（按价值排序）
1. 利润保护 Agent：广告成本预警 + 预算迁移建议
2. 库存风险 Agent：断货预测 + 补货优先级
3. 竞品脉冲 Agent：价格/评论/排名突变告警

**成功指标（4 周）**
- ACOS 下降 8-15%
- 断货天数下降 20%+
- 每周人工运营时长下降 5 小时+

---

## 7) 下一步（v1.3）
- 引入 5-10 个真实卖家访谈样本
- 增加“行为数据层”验证（广告、库存、利润）
- 输出最终唯一 ICP 与分层定价建议
