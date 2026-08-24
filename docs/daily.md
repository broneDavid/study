---
layout: home
---

# 📅 每日学习 · 2026-08-24(周一)

> **考研倒计时: 125 天 · 强化阶段** ｜ 今日模式:**标准** ｜ 连续答对 0 次

📌 每天 30 分钟:知识点 → 小测 → 复习错题。本页每日自动更新。

## ✅ 今日任务

<DailyTasksComponent />

## 📖 今日科目

> 今日轮换:**📘 高等数学** + **🏭 炼油化工设备**(各 15 分钟)

- 📘 **高等数学**:知识库 14 条 · [查看笔记](/subjects/高等数学)
- 🏭 **炼油化工设备**:知识库 6 条 · [查看笔记](/subjects/炼油化工设备)

## ⏰ 到期复习

**37 条知识到期**,按间隔复习(SM-2),优先复习再学新的:

- ⚙️ **机械原理** · 运动副与机构运动简图(掌握 60%)
- 🇬🇧 **英语** · 词汇日-2026-08-07(掌握 50%)
- 🇬🇧 **英语** · 词汇日-2026-08-08(掌握 50%)
- 📘 **高等数学** · 无穷小的比较与等价无穷小替换(掌握 70%)
- 📘 **高等数学** · 函数的连续性与间断点(掌握 70%)
- 📘 **高等数学** · 极限的计算(掌握 60%)
- ⚙️ **机械原理** · 高副低代(掌握 60%)
- 🇬🇧 **英语** · lose 失去(词汇辨析)(掌握 60%)
- 🇬🇧 **英语** · 长难句翻译:by which 定语从句(掌握 30%)
- 📘 **高等数学** · 导数的定义与几何意义(掌握 60%)
- 📘 **高等数学** · 基本求导公式与四则运算法则(掌握 60%)
- 🇬🇧 **英语** · 高频词汇:maintenance 维护/eliminate 消除(掌握 60%)
- ...共 37 条

<a id="today-lesson"></a>
## 📚 今日知识点

**今日科目 📘 高等数学** 最新知识点:

### 定积分的换元积分法

> **掌握度:** 50% | **创建:** 2026-08-24

> 掌握度进度: █████░░░░░

**核心内容:**

与凑微分同理,但换元必须换限:令 u=g(x),则 x=a→u=g(a),x=b→u=g(b),求出原函数后直接代新上下限,不用换回 x

**图示:**

![定积分的换元积分法 图示](./assets/diagrams/formula_248b6bb49b0e.png)

<details class="example-box">
<summary>💡 点击展示例题答案</summary>

∫[0,1] x/(1+x²)dx:令 u=1+x²,du=2xdx→xdx=du/2;换限 x=0→u=1,x=1→u=2;原式=½∫[1,2]du/u=½ln2

</details>

---

### 定积分的概念与几何意义

> **掌握度:** 50% | **创建:** 2026-08-21

> 掌握度进度: █████░░░░░

**核心内容:**

定积分 ∫_a^b f(x)dx 表示曲边梯形(曲线y=f(x)、x轴、直线x=a与x=b所围区域)的带符号面积。定义:将[a,b]分n等份,取点ξi,作和式Σ f(ξi)Δxi,Δxi→0时极限存在且与分法、取法无关,则称f在[a,b]上可积,记该极限为定积分。必要条件:f在[a,b]上有界;充分条件:连续或只有有限个第一类间断点时可积。几何意义:轴上为正面积,轴下为负面积。

**图示:**

![定积分的概念与几何意义 图示](./assets/diagrams/formula_248b6bb49b0e.png)

<details class="example-box">
<summary>💡 点击展示例题答案</summary>

例:求 ∫_0^1 x dx。(解:被积函数y=x在[0,1]上与x轴围成直角三角形,底1高1,面积=1/2,故定积分=1/2。)

</details>

---

### 牛顿-莱布尼茨公式(微积分基本定理)

> **掌握度:** 50% | **创建:** 2026-08-21

> 掌握度进度: █████░░░░░

**核心内容:**

若F(x)是连续函数f(x)在[a,b]上的一个原函数(即F'(x)=f(x)),则 ∫_a^b f(x)dx = F(b)-F(a)。它把定积分的计算转化为求原函数再代上下限之差,是微分与积分联系的桥梁,也是定积分计算最核心的工具。求原函数(不定积分)的方法:基本公式、凑微分、分部积分、换元。

**图示:**

![牛顿-莱布尼茨公式(微积分基本定理) 图示](./assets/diagrams/formula_248b6bb49b0e.png)

<details class="example-box">
<summary>💡 点击展示例题答案</summary>

例:求 ∫_0^1 x² dx。解:F(x)=x³/3是x²的原函数,故∫_0^1 x² dx = (1³/3)-(0³/3)=1/3。

</details>

---


## 📊 掌握度速览

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;">
<div class="app-card" style="padding:14px;margin:2px;"><div style="font-size:13px;color:#86868b;">📘 高等数学</div><div style="font-size:26px;font-weight:700;color:#ff9500;letter-spacing:-0.02em;margin-top:2px;">40%</div><div style="height:6px;background:rgba(128,128,128,.15);border-radius:3px;margin-top:8px;"><div style="height:100%;width:40%;background:#ff9500;border-radius:3px;"></div></div></div>
<div class="app-card" style="padding:14px;margin:2px;"><div style="font-size:13px;color:#86868b;">⚙️ 机械原理</div><div style="font-size:26px;font-weight:700;color:#ff9500;letter-spacing:-0.02em;margin-top:2px;">40%</div><div style="height:6px;background:rgba(128,128,128,.15);border-radius:3px;margin-top:8px;"><div style="height:100%;width:40%;background:#ff9500;border-radius:3px;"></div></div></div>
<div class="app-card" style="padding:14px;margin:2px;"><div style="font-size:13px;color:#86868b;">🇬🇧 英语</div><div style="font-size:26px;font-weight:700;color:#34c759;letter-spacing:-0.02em;margin-top:2px;">100%</div><div style="height:6px;background:rgba(128,128,128,.15);border-radius:3px;margin-top:8px;"><div style="height:100%;width:100%;background:#34c759;border-radius:3px;"></div></div></div>
<div class="app-card" style="padding:14px;margin:2px;"><div style="font-size:13px;color:#86868b;">🏭 炼油化工设备</div><div style="font-size:26px;font-weight:700;color:#34c759;letter-spacing:-0.02em;margin-top:2px;">80%</div><div style="height:6px;background:rgba(128,128,128,.15);border-radius:3px;margin-top:8px;"><div style="height:100%;width:80%;background:#34c759;border-radius:3px;"></div></div></div>
</div>

## 📅 打卡日历(近 90 天)

> 🔥 **连续学习 1 天** · 近 90 天打卡 7 天 · 绿=已打卡 橙框=今天

<div style="display:flex;gap:3px;flex-wrap:nowrap;overflow-x:auto;padding:4px 0;"><div title="2026-05-26" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-05-27" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-05-28" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-05-29" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-05-30" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-05-31" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-01" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-02" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-03" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-04" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-05" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-06" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-07" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-08" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-09" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-10" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-11" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-12" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-13" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-14" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-15" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-16" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-17" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-18" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-19" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-20" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-21" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-22" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-23" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-24" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-25" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-26" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-27" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-28" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-29" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-30" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-01" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-02" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-03" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-04" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-05" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-06" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-07" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-08" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-09" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-10" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-11" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-12" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-13" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-14" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-15" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-16" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-17" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-18" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-19" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-20" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-21" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-22" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-23" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-24" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-25" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-26" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-27" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-28" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-29" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-30" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-31" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-01" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-02" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-03" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-04" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-05" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-06" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-07" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-08" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-09" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-10" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-11" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-12" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-13" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-14" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-15" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-16" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-17" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-18" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-19" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-20" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-21" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-22" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-23" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-24" style="background:rgba(128,128,128,.12);border:2px solid #0071e3;border-radius:5px;height:20px;min-width:11px;flex:1;"></div></div>

## 🏅 里程碑

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;">
<div style="background:rgba(128,128,128,.04);border:1px dashed rgba(128,128,128,.25);border-radius:14px;padding:12px;text-align:center;opacity:.75;"><div style="font-size:24px;">🔥</div><div style="font-size:13px;color:#86868b;">连续 7 天</div><div style="font-size:11px;color:#aeaeb2;">还差 6 天</div></div>
<div style="background:rgba(128,128,128,.04);border:1px dashed rgba(128,128,128,.25);border-radius:14px;padding:12px;text-align:center;opacity:.75;"><div style="font-size:24px;">⚡</div><div style="font-size:13px;color:#86868b;">连续 14 天</div><div style="font-size:11px;color:#aeaeb2;">还差 13 天</div></div>
<div style="background:rgba(128,128,128,.04);border:1px dashed rgba(128,128,128,.25);border-radius:14px;padding:12px;text-align:center;opacity:.75;"><div style="font-size:24px;">🏆</div><div style="font-size:13px;color:#86868b;">连续 30 天</div><div style="font-size:11px;color:#aeaeb2;">还差 29 天</div></div>
<div style="background:rgba(128,128,128,.04);border:1px dashed rgba(128,128,128,.25);border-radius:14px;padding:12px;text-align:center;opacity:.75;"><div style="font-size:24px;">📘</div><div style="font-size:13px;color:#86868b;">高数 ≥50%</div><div style="font-size:11px;color:#aeaeb2;">当前 40%</div></div>
<div style="background:rgba(128,128,128,.04);border:1px dashed rgba(128,128,128,.25);border-radius:14px;padding:12px;text-align:center;opacity:.75;"><div style="font-size:24px;">⚙️</div><div style="font-size:13px;color:#86868b;">机械 ≥70%</div><div style="font-size:11px;color:#aeaeb2;">当前 40%</div></div>
<div style="background:rgba(128,128,128,.04);border:1px dashed rgba(128,128,128,.25);border-radius:14px;padding:12px;text-align:center;opacity:.75;"><div style="font-size:24px;">📝</div><div style="font-size:13px;color:#86868b;">累计 30 天</div><div style="font-size:11px;color:#aeaeb2;">当前 7 天</div></div>
</div>

## 📝 在线小测

今日题目已生成,去 [在线小测](/quiz) 答题(提交后 AI 自动批改 + 解题步骤,成绩写回学习进度)。
