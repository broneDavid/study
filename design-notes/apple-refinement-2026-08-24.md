# 苹果风视觉精修设计分析(视觉设计师视角)

> 基于对 `apple.css` / 三个 Vue 组件 / `generate_site.py` / `config.mts` / 生成页面的代码审计,逐条对照 Apple Design(HIG + apple.com)基线。
> 置信度标注:【高】= 与 Apple 规范/代码事实直接对应;【中】= 设计判断,存在主观空间;【低】= 试探性建议。

---

## 0. 代码审计发现的关键事实(证据)

- `QuizComponent.vue` 大量硬编码 **VitePress 默认绿 `#3eaf7c`**:`.badge`、`.actions button`、`.advance-btn`、`.result` 边框、`.sym-btn:hover` → 与苹果蓝 `#0071e3` 并存,视觉分裂。
- `MistakesReplayComponent.vue` 同样:`.btn-yes`、`.msg` 用 `#3eaf7c`;`#f56c6c`/`#ffb74d`/`#e6a23c`/`#e8f5e9` 是 Element-UI/Material 色板,非苹果。
- `generate_site.py` 的 progress 进度条渐变 `linear-gradient(90deg,#3eaf7c,#67c23a)`,与 daily 页掌握度卡的 iOS 语义色(`#34c759/#ff9500/#ff3b30`)互相矛盾。
- `config.mts` 的 `<meta name="theme-color" content="#3eaf7c">` 仍是绿色。
- `index.md` 门户四科卡片是 `#fff + #e0e0e0 边框 + 10px 圆角 + 0 1px 3px 弱阴影` — 完全没走毛玻璃体系,是门面页最"不苹果"处。
- 阴影全站单层 `0 4px 24px rgba(0,0,0,.08)`,无分层;卡片无内高光(inset highlight)。
- 按钮圆角混乱:胶囊 980px(步骤条/迷你按钮)与 8px(小测提交)/6px(符号按钮)并存。
- 深色模式在 3 个组件里**复制粘贴硬编码**(`rgba(28,28,32,.72)` 各写一遍),没走 CSS 变量,已出现漂移(如 `.mode-opt` 深色只改了背景没改边框文字)。
- 打卡日历今天=纯 `#34c759` 无描边,页面文案却写"橙框=今天"(文案过时)。
- 无 `:focus-visible`、无 transition 体系、无 `prefers-reduced-motion`。
- 全站无 `font-variant-numeric: tabular-nums`,数字(掌握度%)跳动。

---

## 1. 目前最欠缺的 8 个视觉细节(具体到 CSS 属性/数值)

| # | 欠缺 | 现状 | 苹果级目标 | 置信度 |
|---|------|------|-----------|--------|
| 1 | **品牌色不统一(绿蓝并存)** | `#3eaf7c` 残留在 3 组件+生成器+meta | 全站唯一品牌色 `#0071e3`,残留清零 | 【高】 |
| 2 | **阴影无分层** | `box-shadow: 0 4px 24px rgba(0,0,0,.08)` 单层 | 双层投影+内高光:`inset 0 1px 0 rgba(255,255,255,.65), 0 2px 4px rgba(0,0,0,.04), 0 8px 24px rgba(0,0,0,.07)`;深色改 `rgba(255,255,255,.08)` 高光 | 【高】 |
| 3 | **按钮无按压反馈** | 无 transition、无 :active 缩放 | `transition: transform .15s ease, box-shadow .25s ease, background .2s ease; :active { transform: scale(.96); }`;disabled 用 `opacity:.4`(非 .5) | 【高】 |
| 4 | **圆角体系混乱** | 980px 胶囊 vs 8px/6px/10px 并存 | 按钮=胶囊 980px;卡片=18px;标签=6-7px 小圆角;输入框=10px | 【高】 |
| 5 | **排版无层级 token** | VitePress 默认 + 零散 inline font-size | 见 §3 完整字号阶梯;数字加 `font-variant-numeric: tabular-nums` | 【中高】 |
| 6 | **无 focus-visible** | 所有交互元素无焦点样式 | `:focus-visible { outline: 2px solid rgba(0,113,227,.7); outline-offset: 2px; }` | 【高】 |
| 7 | **表格粗糙** | th 纯灰 8% 平铺、默认 1px 灰线、无行 hover | thead `rgba(128,128,128,.06)`+13px/600 次级字色;行分隔 `border-bottom:1px solid rgba(0,0,0,.06)`;行 hover `background:rgba(0,113,227,.04)` | 【中】 |
| 8 | **emoji 裸用当图标** | 📘⚙️🏭 24px 裸 emoji 做卡片主视觉,跨端(Windows/Android)字体渲染不一 | 收进 32px 圆角小容器(`border-radius:8px; background:rgba(0,113,227,.1); width:32px;height:32px; display:flex;align-items:center;justify-content:center; font-size:16px`) | 【中高】 |

补充(体验细节,非纯视觉):`window.alert()` 原生弹窗庆祝完成任务,建议改为页内内联横幅(毛玻璃+绿底)+ 轻量动效。

---

## 2. 配色系统(完整定义)

### 2.1 主色(品牌蓝,唯一)
```css
--brand:        #0071e3;  /* 浅色主蓝 */
--brand-hover:  #0077ed;  /* 浅色 hover */
--brand-pressed:#006edb;  /* 浅色按压 */
--brand-dark:   #0a84ff;  /* 深色模式主蓝 */
--brand-dark-h: #409cff;  /* 深色 hover */
--brand-soft:   rgba(0, 113, 227, .10);  /* 蓝底容器(标签/选中行) */
--brand-soft-2: rgba(0, 113, 227, .16);  /* 更强的选中底 */
```

### 2.2 辅助色(iOS 系统语义色,与现有 MODES 色板一致,保留)
```css
--green:  #34c759;  /* 完成/已打卡/掌握≥50/答对 */
--orange: #ff9500;  /* 进行中/掌握30-49/警告 */
--red:    #ff3b30;  /* 错误/掌握<30/删除/答错 */
--yellow: #ffcc00;  /* 草稿/待处理(少用,仅草稿条) */
--purple: #5856d6;  /* 可选点缀,暂不使用 */
--gray-1: #8e8e93;  /* 禁用/次要 */
--gray-2: #aeaeb2;  /* 三级/chevron */
```
> 置信度【高】:与 iOS HIG 语义色一一对应,且 daily 页已在用,应全站统一。

### 2.3 中性色(深浅双模式)
```css
/* 浅色 */
--bg:        #f5f5f7;
--grad-a:    #e8edf5;  --grad-b: #f5f5f7;
--card:      rgba(255, 255, 255, .72);
--card-grad: linear-gradient(180deg, rgba(255,255,255,.82), rgba(255,255,255,.65)); /* 玻璃厚度感 */
--border:    rgba(255, 255, 255, .7);   /* 卡片描边 */
--border-2:  rgba(0, 0, 0, .06);        /* 内部细分隔线 */
--text-1:    #1d1d1f;  --text-2: #86868b;  --text-3: #aeaeb2;
/* 深色 */
--card:      rgba(28, 28, 30, .72);
--border:    rgba(255, 255, 255, .12);
--border-2:  rgba(255, 255, 255, .08);
--text-2:    #98989d;  --text-3: #636366;
```

### 2.4 语义绑定表(消除"同一概念两套色")
| 概念 | 颜色规则 |
|------|---------|
| 掌握度进度条(填充) | 一律品牌蓝 `#0071e3`(进度条=系统行为,苹果 app 进度条皆蓝);**状态徽章/数字**才用语义色(绿/橙/红) |
| 掌握度数字 | ≥50 绿 `#34c759` / 30-49 橙 `#ff9500` / <30 红 `#ff3b30`(沿用现状) |
| 今日任务步骤 | 完成=绿 / 当前=蓝+外圈 `0 0 0 4px rgba(0,113,227,.18)`(沿用现状,达标) |
| 打卡日历 | 已打卡=绿 `rgba(52,199,89,.55)` / 今天=任何状态都加 `2px solid #0071e3` 描边(修文案"橙框=今天"为蓝框,与全局一致) |
| 答题对错 | 对=绿 soft / 错=红 soft(现状用的是 Material 绿 `#e8f5e9`,改 `rgba(52,199,89,.12)`+绿字) |
| 学习模式 | light=橙 / standard=绿 / intensive=红 / off=灰(保留) |
> 置信度【中高】:进度条用蓝是明确设计判断;语义色沿用 iOS。

---

## 3. 排版层级(苹果比例)

苹果核心:标题大而紧(负字距),正文适度,小字克制;层级靠**字重+字距**,不靠颜色堆叠。

```css
--fs-display: clamp(34px, 6vw, 44px);   /* 门户 hero,weight 700,ls -0.022em,lh 1.1 */
--fs-h1:      clamp(28px, 5vw, 34px);   /* 页面主标题,700,-0.021em,1.125 */
--fs-h2:      22px;                     /* 区块标题,650→用 600,-0.019em,1.3 */
--fs-h3:      17px;                     /* 卡片内标题,600,-0.014em,1.4 */
--fs-body:    16px;                     /* 正文,400,0,1.6(中文行高) */
--fs-list:    15px;                     /* 列表/说明 */
--fs-caption: 13px;                     /* 次级说明,400,text-2 */
--fs-tiny:    12px;                     /* 徽章/时间戳,500 */
--fs-stat:    26px;                     /* 掌握度%等数字,700,-0.02em,+tabular-nums */
```

落地要点:
- **数字一律 `font-variant-numeric: tabular-nums`**(倒计时、掌握度、打卡数)→ 消除跳动。置信度【高】
- 中文字重:SF 的 590/630 等中间值 PingFang 不支持,统一用 400/500/600/700 四档。置信度【高】
- 字距:仅大标题负字距(`-0.02em` 级),正文/小字保持 0。置信度【高】
- 行高:中文正文 1.6 优于 1.5;表格/徽章 1.3-1.4。置信度【中】
- `text-rendering: optimizeLegibility` + `font-feature-settings: "kern" 1` 加到 body。置信度【中】
- 移动端:正文可 16px 不降(现状 15px 略小);h1 28px 达标。置信度【中】

---

## 4. 卡片/按钮/表格/标签精致化配方

### 4.1 卡片 `.app-card`(玻璃配方升级)
```css
.app-card {
  background: var(--card-grad);              /* 顶部略亮的纵向渐变=玻璃厚度 */
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  backdrop-filter: saturate(180%) blur(20px);
  border: 1px solid var(--border);
  border-radius: 18px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.65),   /* 上边缘高光(浅色) */
              0 2px 4px rgba(0,0,0,.04),
              0 8px 24px rgba(0,0,0,.07);
}
/* 深色:高光改 rgba(255,255,255,.08),阴影改 0 2px 4px rgba(0,0,0,.4), 0 12px 32px rgba(0,0,0,.5) */
/* 可点击卡片 hover:translateY(-2px) + 阴影升一级 + transition .25s cubic-bezier(.25,.1,.25,1) */
```
置信度【中高】

### 4.2 按钮(统一胶囊)
```css
/* 主按钮(提交批改/选择模式/重试) */
.btn-primary {
  background: linear-gradient(180deg, #0077ed, #0071e3);  /* 苹果官网式纵向渐变 */
  box-shadow: inset 0 1px 0 rgba(255,255,255,.25);        /* 内高光 */
  border-radius: 980px; padding: 11px 22px;
  font-size: 15px; font-weight: 500; color: #fff;
  transition: transform .15s ease, box-shadow .25s ease, background .2s ease;
}
.btn-primary:hover  { filter: brightness(1.05); }
.btn-primary:active { transform: scale(.96); }
.btn-primary:disabled { opacity: .4; }
/* 次要按钮(下一轮学习):透明底+蓝字, hover 背景 var(--brand-soft) */
/* 危险/描边按钮(还不会):1px solid rgba(0,0,0,.12) 白底橙字;深色 rgba(255,255,255,.2) */
```
置信度【高】:按压缩放与渐变是 apple.com 按钮的两大特征。

### 4.3 表格
```css
.vp-doc table { border-radius: 14px; overflow: hidden; background: var(--card);
  backdrop-filter: saturate(180%) blur(20px); }
.vp-doc th { background: rgba(128,128,128,.06); font-size: 13px; font-weight: 600; color: var(--text-2); }
.vp-doc td { border-bottom: 1px solid rgba(0,0,0,.06); }          /* 深色 rgba(255,255,255,.08) */
.vp-doc tbody tr { transition: background .15s ease; }
.vp-doc tbody tr:hover { background: rgba(0,113,227,.04); }        /* 深色 rgba(10,132,255,.08) */
.vp-doc th:first-child, .vp-doc td:first-child { padding-left: 16px; }
```
置信度【中】

### 4.4 标签/徽章
- 苹果的**标签是小圆角矩形(6-7px),不是胶囊**;胶囊是按钮。现状 `.badge` 用 12px 圆角,偏胶囊 → 统一 `border-radius: 7px; padding: 3px 9px; font-size: 12px; font-weight: 600;`
- 科目徽章:蓝 soft `background: var(--brand-soft); color: #0071e3`
- 题型徽章:灰 soft `background: rgba(120,120,128,.1); color: var(--text-2)`
- 答案对/错:绿 soft / 红 soft(`rgba(52,199,89,.12)` / `rgba(255,59,48,.12)` + 对应深色文字)
- 置信度【中高】

### 4.5 里程碑/日历
- 里程碑:未达成=虚线 `1px dashed rgba(0,0,0,.12)`+图标灰度;达成=绿 soft 渐变底+实线+`0 1px 3px rgba(52,199,89,.2)` 微光。置信度【中】
- 打卡日历:细胞 `border-radius: 4px; height: 20px;`;今天统一加 `2px solid #0071e3` 描边;已打卡绿 `rgba(52,199,89,.55)`。置信度【中】

---

## 5. TOP5 优先级改动清单

| 优先级 | 改动 | 改动面 | 预期收益 | 置信度 |
|--------|------|--------|---------|--------|
| **P0** | **品牌色统一**:清除全部 `#3eaf7c/#67c23a` → `--vp-c-brand-*`(Quiz/Mistakes 组件、generate_site.py 进度条渐变、config.mts theme-color 改 `#f5f5f7`) | 3 文件+生成器 | 消除最刺眼的"绿蓝混搭",立竿见影 | 【高】 |
| **P1** | **门户页玻璃化**:index.md 四科卡片改 `.app-card` + emoji 收进圆角容器 + hero 标题用 display 字号 | 生成器 index 模板 | 门面从"白板卡片"变"苹果玻璃",第一印象跃升 | 【中高】 |
| **P2** | **按钮体系重建**:全局胶囊 980px + 蓝渐变 + 内高光 + `:active scale(.96)` + disabled .4 + 统一 transition | apple.css + 3 组件 | 交互质感=苹果的标志性手感 | 【高】 |
| **P3** | **阴影/边框分层**:双层阴影 token + `inset 0 1px 0` 内高光 + 卡片 hover 抬升 + 卡片纵向渐变 | apple.css + 组件 | 卡片"浮起来",玻璃感成型 | 【中高】 |
| **P4** | **排版 token 落地**:§3 字号阶梯进 apple.css,数字 tabular-nums,表格/标签精致化 | apple.css + 生成器 | 层级秩序感,数字不跳动 | 【中高】 |

> 后续批次(非本次):focus-visible 全站、`prefers-reduced-motion`、深色模式改 CSS 变量收敛(消除组件内复制粘贴)、`window.alert` 改内联横幅、打卡日历文案与描边对齐。

---

## 6. 一句话结论

苹果级质感 = **统一**(唯一品牌色、统一圆角/阴影/字体 token)+ **克制**(灰阶中性色、语义色只用于状态)+ **精致**(双层阴影、内高光、按压反馈、tabular-nums)。当前最大差距不在"缺设计",而在"体系没收敛":绿蓝并存 + 圆角/阴影各写各的。先做 P0-P2(纯收敛,半天工作量),视觉统一度即可显著跃升;P3-P4 再补质感细节。
