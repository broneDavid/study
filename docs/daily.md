---
layout: home
---

# 📅 每日学习 · 2026-08-25(周二)

> **考研倒计时: 124 天 · 强化阶段** ｜ 今日模式:**标准** ｜ 连续答对 0 次

📌 每天 30 分钟:知识点 → 小测 → 复习错题。本页每日自动更新。

## ✅ 今日任务

<DailyTasksComponent />

## 📖 今日科目

> 今日轮换:**⚙️ 机械原理** + **🇬🇧 英语**(各 15 分钟)

- ⚙️ **机械原理**:知识库 12 条 · [查看笔记](/subjects/机械原理)
- 🇬🇧 **英语**:知识库 10 条 · [查看笔记](/subjects/英语)

## ⏰ 到期复习

**38 条知识到期**,按间隔复习(SM-2),优先复习再学新的:

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
- ...共 38 条

<a id="today-lesson"></a>
## 📚 今日知识点

**今日科目 ⚙️ 机械原理** 最新知识点:

### 渐开线齿轮的根切现象与最少齿数

> **掌握度:** 50% | **创建:** 2026-08-25

> 掌握度进度: █████░░░░░

**核心内容:**

用范成法(展成法)加工齿轮时,若齿数过少,刀具齿顶线超过啮合极限点N1,会把轮齿根部已切出的渐开线齿廓再切去一部分,称为根切。后果:削弱齿根强度、减小重合度,严重时破坏正确啮合。标准直齿圆柱齿轮(齿顶高系数ha*=1,压力角α=20°)不发生根切的最少齿数 z_min=2ha*/sin²α=2/sin²20°=17.1,取17。避免根切的措施:①齿数≥17;②采用正变位(x>0);③增大压力角α;④减小齿顶高系数ha*。

**图示:**

![渐开线齿轮的根切现象与最少齿数 图示](./assets/diagrams/mech_chilun_0822.png)

<details class="example-box">
<summary>💡 点击展示例题答案</summary>

标准直齿圆柱齿轮 z=14 用范成法加工是否产生根切?如何避免?答:z=14<17,会产生根切;可改用正变位齿轮(x>0),或增大压力角(如α=25°)来避免根切。

</details>

---

### 定轴轮系传动比计算

> **掌握度:** 50% | **创建:** 2026-08-25

> 掌握度进度: █████░░░░░

**核心内容:**

定轴轮系:所有齿轮几何轴线位置都固定的轮系。传动比计算公式: i_ab = n_a/n_b = (-1)^m x (所有从动轮齿数连乘积)/(所有主动轮齿数连乘积),其中 m 为外啮合齿轮对数;结果为负表示输出轮与输入轮转向相反。惰轮(介轮):只改变转向,不改变传动比大小,每加一个惰轮转向反转一次。含锥齿轮、蜗杆蜗轮的空间定轴轮系不能用 (-1)^m 判向,必须用画箭头法逐对判断转向。

**图示:**

![定轴轮系传动比计算 图示](./assets/diagrams/mech_chilun_0822.png)

<details class="example-box">
<summary>💡 点击展示例题答案</summary>

轮系各轮齿数:z1=20,z2=40,z2'=20,z3=60,z3'=25,z4=50,n1=1440r/min,求 i_14 与 n4。解:外啮合3对,m=3;i_14=(-1)^3 x (40x60x50)/(20x20x25)=-120000/10000=-12;n4=n1/i_14=1440/(-12)=-120r/min,负号表示轮4与轮1转向相反。

</details>

---

### 标准直齿圆柱齿轮的几何尺寸计算

> **掌握度:** 50% | **创建:** 2026-08-22

> 掌握度进度: █████░░░░░

**核心内容:**

标准齿轮几何尺寸由五大参数唯一确定(m、z、α=20°、ha*=1、c*=0.25)。核心公式:分度圆直径 d=mz;齿顶高 ha=m;齿根高 hf=1.25m;全齿高 h=2.25m;齿顶圆直径 da=m(z+2);齿根圆直径 df=m(z-2.5);齿距 p=πm;标准安装中心距 a=m(z1+z2)/2;传动比 i12=n1/n2=z2/z1=d2/d1。单位一律 mm。注意:分度圆是计算基准,不是实际可见圆。

**图示:**

![标准直齿圆柱齿轮的几何尺寸计算 图示](./assets/diagrams/mech_chilun_0822.png)

<details class="example-box">
<summary>💡 点击展示例题答案</summary>

标准直齿圆柱齿轮 m=2mm、z=40,求 d、da、df、p。解:d=mz=2x40=80mm;da=m(z+2)=2x42=84mm;df=m(z-2.5)=2x37.5=75mm;p=πm=3.14x2≈6.28mm。再与该轮啮合的一标准齿轮 z2=60,中心距 a=m(z1+z2)/2=2x(40+60)/2=100mm。

</details>

---


## 📊 掌握度速览

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;">
<div class="app-card" style="padding:14px;margin:2px;"><div style="font-size:13px;color:#86868b;">📘 高等数学</div><div style="font-size:26px;font-weight:700;color:#34c759;letter-spacing:-0.02em;margin-top:2px;">50%</div><div style="height:6px;background:rgba(128,128,128,.15);border-radius:3px;margin-top:8px;"><div style="height:100%;width:50%;background:#34c759;border-radius:3px;"></div></div></div>
<div class="app-card" style="padding:14px;margin:2px;"><div style="font-size:13px;color:#86868b;">⚙️ 机械原理</div><div style="font-size:26px;font-weight:700;color:#ff3b30;letter-spacing:-0.02em;margin-top:2px;">20%</div><div style="height:6px;background:rgba(128,128,128,.15);border-radius:3px;margin-top:8px;"><div style="height:100%;width:20%;background:#ff3b30;border-radius:3px;"></div></div></div>
<div class="app-card" style="padding:14px;margin:2px;"><div style="font-size:13px;color:#86868b;">🇬🇧 英语</div><div style="font-size:26px;font-weight:700;color:#34c759;letter-spacing:-0.02em;margin-top:2px;">100%</div><div style="height:6px;background:rgba(128,128,128,.15);border-radius:3px;margin-top:8px;"><div style="height:100%;width:100%;background:#34c759;border-radius:3px;"></div></div></div>
<div class="app-card" style="padding:14px;margin:2px;"><div style="font-size:13px;color:#86868b;">🏭 炼油化工设备</div><div style="font-size:26px;font-weight:700;color:#34c759;letter-spacing:-0.02em;margin-top:2px;">60%</div><div style="height:6px;background:rgba(128,128,128,.15);border-radius:3px;margin-top:8px;"><div style="height:100%;width:60%;background:#34c759;border-radius:3px;"></div></div></div>
</div>

## 📅 打卡日历(近 90 天)

> 🔥 **连续学习 0 天** · 近 90 天打卡 7 天 · 绿=已打卡 蓝框=今天

<div style="display:flex;gap:3px;flex-wrap:nowrap;overflow-x:auto;padding:4px 0;"><div title="2026-05-27" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-05-28" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-05-29" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-05-30" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-05-31" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-01" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-02" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-03" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-04" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-05" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-06" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-07" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-08" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-09" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-10" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-11" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-12" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-13" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-14" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-15" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-16" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-17" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-18" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-19" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-20" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-21" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-22" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-23" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-24" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-25" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-26" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-27" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-28" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-29" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-06-30" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-01" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-02" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-03" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-04" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-05" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-06" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-07" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-08" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-09" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-10" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-11" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-12" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-13" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-14" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-15" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-16" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-17" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-18" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-19" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-20" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-21" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-22" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-23" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-24" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-25" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-26" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-27" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-28" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-29" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-30" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-07-31" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-01" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-02" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-03" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-04" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-05" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-06" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-07" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-08" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-09" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-10" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-11" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-12" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-13" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-14" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-15" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-16" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-17" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-18" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-19" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-20" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-21" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-22" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-23" style="background:rgba(52,199,89,.55);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-24" style="background:rgba(128,128,128,.05);border:1px solid rgba(128,128,128,.1);border-radius:5px;height:20px;min-width:11px;flex:1;"></div><div title="2026-08-25" style="background:rgba(128,128,128,.12);border:2px solid #0071e3;border-radius:5px;height:20px;min-width:11px;flex:1;"></div></div>

## 🏅 里程碑

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;">
<div style="background:rgba(128,128,128,.04);border:1px dashed rgba(128,128,128,.25);border-radius:14px;padding:12px;text-align:center;opacity:.75;"><div style="font-size:24px;">🔥</div><div style="font-size:13px;color:#86868b;">连续 7 天</div><div style="font-size:11px;color:#aeaeb2;">还差 7 天</div></div>
<div style="background:rgba(128,128,128,.04);border:1px dashed rgba(128,128,128,.25);border-radius:14px;padding:12px;text-align:center;opacity:.75;"><div style="font-size:24px;">⚡</div><div style="font-size:13px;color:#86868b;">连续 14 天</div><div style="font-size:11px;color:#aeaeb2;">还差 14 天</div></div>
<div style="background:rgba(128,128,128,.04);border:1px dashed rgba(128,128,128,.25);border-radius:14px;padding:12px;text-align:center;opacity:.75;"><div style="font-size:24px;">🏆</div><div style="font-size:13px;color:#86868b;">连续 30 天</div><div style="font-size:11px;color:#aeaeb2;">还差 30 天</div></div>
<div class="app-card" style="padding:12px;text-align:center;border:1px solid rgba(52,199,89,.3);"><div style="font-size:24px;">📘</div><div style="font-size:13px;font-weight:600;color:#34c759;">高数 ≥50%</div><div style="font-size:11px;color:#86868b;">已达成</div></div>
<div style="background:rgba(128,128,128,.04);border:1px dashed rgba(128,128,128,.25);border-radius:14px;padding:12px;text-align:center;opacity:.75;"><div style="font-size:24px;">⚙️</div><div style="font-size:13px;color:#86868b;">机械 ≥70%</div><div style="font-size:11px;color:#aeaeb2;">当前 20%</div></div>
<div style="background:rgba(128,128,128,.04);border:1px dashed rgba(128,128,128,.25);border-radius:14px;padding:12px;text-align:center;opacity:.75;"><div style="font-size:24px;">📝</div><div style="font-size:13px;color:#86868b;">累计 30 天</div><div style="font-size:11px;color:#aeaeb2;">当前 7 天</div></div>
</div>

## 📝 在线小测

今日题目已生成,去 [在线小测](/quiz) 答题(提交后 AI 自动批改 + 解题步骤,成绩写回学习进度)。
