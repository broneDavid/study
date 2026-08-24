#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习网站生成器:把 ~/.hermes/study 的 JSON 学习数据自动渲染为 VitePress 网站 Markdown。
- 首页仪表盘(每日知识点 + 掌握度)
- 四科笔记(含 LaTeX 公式)
- 学习计划(来自 study_plan.md)
- 学习进度(掌握度曲线)
- 错题本
- 每周周报(来自 weekly_archive 摘要)

用法:
    python3 generate_site.py [--study-dir PATH] [--out docs]
生成后运行 pnpm build 即可出站。
"""
import argparse, json, math, re, os, shutil, subprocess, sys
from datetime import date, datetime

# ---------- 路径 ----------
STUDY_DIR = "/home/openclaw/.hermes/study"
OUT_DIR = "docs"
SUBJECTS = ["高等数学", "机械原理", "英语", "炼油化工设备"]
SUBJECT_ICONS = {"高等数学": "📘", "机械原理": "⚙️", "英语": "🇬🇧", "炼油化工设备": "🏭"}

# 每周科目轮换表(与 study-engine skill 一致): isoweekday 1=周一
WEEK_ROTATION = {
    1: ("高等数学", "炼油化工设备"),
    2: ("机械原理", "英语"),
    3: ("高等数学", "机械原理"),
    4: ("英语", "炼油化工设备"),
    5: ("高等数学", "英语"),
    6: ("机械原理", "炼油化工设备"),
    7: ("周总结", "错题总复习"),
}
WEEKDAY_CN = {1: "周一", 2: "周二", 3: "周三", 4: "周四", 5: "周五", 6: "周六", 7: "周日"}
MODE_CN = {"light": "轻量", "standard": "标准", "intensive": "加强", "off": "休息"}

# 周报存档目录(周报 cron 生成)
WEEKLY_DIR = os.path.join(STUDY_DIR, "archive", "weekly")

def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

# ---------- 知识点 JSON → 笔记 ----------
# 图示匹配: 图片文件关键词 → 知识点标题关键词(图文并茂)
# 键=知识点标题包含的词, 值=math_renders 里的图片文件名
DIAGRAM_MAP = {
    "高等数学": {
        "链式": "chain_rule.png",
        "求导": "daoshu_gongshi.png",
        "导数": "daoshu_jihe.png",
        "隐函数": "yinxianshu.png",
        "极限": "liangan_panduan.png",
        "连续": "liangan_panduan.png",
        "不定积分": "formula_248b6bb49b0e.png",
        "积分": "formula_248b6bb49b0e.png",
    },
    "机械原理": {
        "机构": "mech_jihui_0815.png",
        "自由度": "mech_jihui_0815.png",
        "齿轮": "mech_chilun_0822.png",
        "轮系": "mech_chilun_0822.png",
        "瞬心": "mech_shunxin_0822.png",
        "运动": "mech_yundongfu_0822.png",
        "连杆": "mech_sigan_0815.png",
        "凸轮": "mech_yundongfu_0822.png",
    },
    "英语": {
        "长难句": "en_sentence_0813.png",
        "翻译": "en_sentence_0813.png",
        "词汇": "en_new_0813.png",
        "单词": "en_new_0813.png",
    },
}

def _match_diagram(subject, title):
    """按关键词在 math_renders 里找匹配图。返回文件名或 None。"""
    mapping = DIAGRAM_MAP.get(subject, {})
    for kw, fname in mapping.items():
        if kw in title:
            # 确认文件存在
            p = os.path.join(STUDY_DIR, "math_renders", fname)
            if os.path.isfile(p):
                return fname
    return None

def knowledge_to_markdown(subject):
    """把单科 knowledge JSON 转成笔记页。返回 (title, markdown文本)"""
    data = load_json(os.path.join(STUDY_DIR, "knowledge", f"{subject}.json"), {"items": []})
    items = data.get("items", [])
    icon = SUBJECT_ICONS.get(subject, "📘")
    lines = []
    lines.append(f"# {icon} {subject} 知识点笔记")
    lines.append("")
    lines.append(f"> 共 **{len(items)}** 个知识点 · 隔天自动更新")
    lines.append("")

    # 按知识块分区(可以按 tag 或直接连续), 这里直接按顺序列出
    for it in items:
        title = it.get("title", "未命名知识点")
        content = it.get("content", "")
        example = it.get("example", "")
        mastery = it.get("mastery", 0)
        created = it.get("created", "")
        last = it.get("last_reviewed", "")

        lines.append(f"## {title}")
        lines.append("")
        # 元信息
        meta = []
        meta.append(f"**掌握度:** {mastery}%")
        if created: meta.append(f"**创建:** {created}")
        if last: meta.append(f"**最近复习:** {last}")
        lines.append(f">{ ' | '.join(meta) }")
        lines.append("")
        # 掌握度条
        bars = "█" * max(0, round(mastery/10)) + "░" * max(0, 10-round(mastery/10))
        lines.append(f"> 掌握度进度: {bars}")
        lines.append("")
        if content:
            lines.append("**核心内容:**")
            lines.append("")
            lines.append(content)
            lines.append("")
        # 图文并茂: 匹配到图示则渲染
        diagram = _match_diagram(subject, title)
        if diagram:
            lines.append("**图示:**")
            lines.append("")
            lines.append(f"![{title} 图示](../assets/diagrams/{diagram})")
            lines.append("")
        if example:
            lines.append("<details class=\"example-box\">")
            lines.append("<summary>💡 点击展示例题答案</summary>")
            lines.append("")
            lines.append(example)
            lines.append("")
            lines.append("</details>")
            lines.append("")
        lines.append("---")
        lines.append("")

    return lines

# ---------- 错题本 ----------
def mistakes_to_markdown():
    lines = []
    lines.append("# ❌ 错题本")
    lines.append("")
    lines.append("> 逐题重练:先回忆 → 展开核对 → 自评「记住了/还不会」。标记解决后自动移出待办。")
    lines.append("")
    lines.append("<MistakesReplayComponent />")
    lines.append("")
    total = 0
    unresolved = 0
    for subj in SUBJECTS:
        data = load_json(os.path.join(STUDY_DIR, "mistakes", f"{subj}.json"), {"items": []})
        items = data.get("items", [])
        total += len(items)
        unresolved += sum(1 for i in items if not i.get("resolved"))
        if not items:
            continue
        icon = SUBJECT_ICONS.get(subj, "📘")
        lines.append(f"## {icon} {subj} 已解决(历史)")
        lines.append("")
        closed = [i for i in items if i.get("resolved")]
        for i in closed:
            d = i.get("date", "")
            pt = i.get("point", "")
            lines.append(f"- ✅ `{d}` {pt}")
        if not closed:
            lines.append("_暂无已解决错题_")
        lines.append("")

    # 顶部摘要(定位在标题后)
    summary = f"> **未解决 {unresolved}** 题 / 共 {total} 题"
    lines.insert(1, summary)
    lines.insert(2, "")
    return lines

# ---------- 学习进度(含掌握度计) ----------
def progress_to_markdown():
    lines = []
    lines.append("# 📈 学习进度")
    lines.append("")
    data = load_json(os.path.join(STUDY_DIR, "progress", "progress.json"), {"subjects": {}})
    subs = data.get("subjects", {})
    total_days = data.get("total_days", 0)
    last_date = data.get("last_date", "")

    lines.append(f"> 累计学习 **{total_days}** 天 · 最近更新 {last_date or '未知'}")
    lines.append("")

    # 掌握度汇总表
    lines.append("## 各科掌握度")
    lines.append("")
    for subj in SUBJECTS:
        s = subs.get(subj, {})
        m = s.get("mastery", 0)
        streak = s.get("streak", 0)
        learned = s.get("learned_points", [])
        icon = SUBJECT_ICONS.get(subj, "📘")
        bars = "█" * max(0, round(m/10)) + "░" * max(0, 10-round(m/10))
        lines.append(f"### {icon} {subj} — {m}%")
        lines.append("")
        lines.append(f"> {bars} · 连击 {streak} 天")
        lines.append("")
        lines.append("**已掌握要点:**")
        lines.append("")
        if learned:
            for p in learned[-5:]:  # 最近5条
                lines.append(f"- {p}")
        else:
            lines.append("- 暂无记录")
        lines.append("")

    # 用 HTML 画一个简单掌握度条(纯 CSS, 不用图表库)
    html_above = """
<style>
  .mastery-row { display:flex; align-items:center; gap:12px; margin:8px 0; }
  .mastery-row .label { width:130px; font-weight:600; }
  .mastery-bar { flex:1; height:18px; background:#e9ecef; border-radius:9px; overflow:hidden; }
  .mastery-fill { height:100%; background:linear-gradient(90deg,#0071e3,#0a84ff); border-radius:9px; }
  .mastery-val { width:50px; text-align:right; font-weight:600; }
</style>
"""
    lines.append(html_above)
    lines.append("## 掌握度总览")
    lines.append("")
    for subj in SUBJECTS:
        s = subs.get(subj, {})
        m = s.get("mastery", 0)
        icon = SUBJECT_ICONS.get(subj, "📘")
        lines.append(f'<div class="mastery-row"><span class="label">{icon} {subj}</span>'
                     f'<div class="mastery-bar"><div class="mastery-fill" style="width:{m}%"></div></div>'
                     f'<span class="mastery-val">{m}%</span></div>')
    lines.append("")

    # 最近学习要点(总览)
    lines.append("## 最近学习要点")
    lines.append("")
    all_points = []
    for subj in SUBJECTS:
        s = subs.get(subj, {})
        for p in s.get("learned_points", []):
            all_points.append((subj, p))
    for subj, p in all_points[-10:]:
        icon = SUBJECT_ICONS.get(subj, "📘")
        lines.append(f"- {icon} **{subj}** — {p}")
    if not all_points:
        lines.append("- 暂无")
    lines.append("")
    return lines

# ---------- 周报 ----------
def reports_to_markdown():
    """从周报存档生成周报索引 + 各周页面。返回 (index_md, done_paths)。"""
    index = []
    index.append("# 📅 每周周报")
    index.append("")
    index.append("> 每周自动生成的备考进度周报。")
    index.append("")

    # 找所有周报 PDF(按名字排序, 最新的在最前)
    files = []
    if os.path.isdir(WEEKLY_DIR):
        for f in os.listdir(WEEKLY_DIR):
            if f.endswith(".pdf"):
                files.append(f)
    files.sort(reverse=True)  # 周编号倒序, 最新在前

    # 周报没有结构化的 markdown, 但我们从 weekly_archive 的运行记录里能抓到摘要文本。
    # 这里生成索引 + 说明, 每份 PDF 链接到对应文件。
    index.append("| 周次 | 报告 |")
    index.append("|------|------|")
    for f in files:
        name = f.replace(".pdf", "").replace("周报_", "").replace(".", "-W")
        index.append(f"| {name} | [下载 {f}]({'/assets/weekly/' + f}) |")
    index.append("")

    index.append("## 说明")
    index.append("")
    index.append("周报由每周学习 cron 自动生成, 含各科掌握度、错题 Top3、到期复习、考研倒计时。")
    index.append("点击上方下载链接查看对应周次的 PDF。\n")
    return index, files

# ---------- 学习计划 ----------
def plan_to_markdown():
    plan_file = os.path.join(STUDY_DIR, "study_plan.md")
    lines = []
    lines.append("# 🎯 学习计划")
    lines.append("")
    if os.path.isfile(plan_file):
        with open(plan_file, encoding="utf-8") as f:
            content = f.read().strip()
        # 去掉一级标题(避免重复)
        content = re.sub(r"^#\s+.+", "", content, count=1).strip()
        lines.append(content)
    else:
        lines.append("> 尚未生成本计划的 markdown。")
    lines.append("")
    return lines

# ---------- 每日学习页 ----------
def _today_shanghai():
    """返回 (date_str, isoweekday) 按上海时区。"""
    from datetime import datetime, timedelta, timezone
    sh = timezone(timedelta(hours=8))
    now = datetime.now(sh)
    return now.strftime("%Y-%m-%d"), now.isoweekday()

def _exam_countdown():
    """考研倒计时(含当天)。返回 (days, stage)。"""
    from datetime import date
    cfg = load_json(os.path.join(STUDY_DIR, "exam_config.json"), {})
    exam = cfg.get("exam_date", "2026-12-26")
    try:
        y, m, d = map(int, exam.split("-"))
        exam_date = date(y, m, d)
    except Exception:
        exam_date = date(2026, 12, 26)
    today, _ = _today_shanghai()
    ty, tm, td = map(int, today.split("-"))
    days = (exam_date - date(ty, tm, td)).days + 1
    if days <= 30:
        stage = "冲刺"
    elif days <= 60:
        stage = "冲刺"
    elif days <= 150:
        stage = "强化"
    else:
        stage = "基础"
    return days, stage

def _state_fields():
    st = load_json(os.path.join(STUDY_DIR, "state.json"), {})
    mode = st.get("mode", "standard")
    flags = {
        "checkin": bool(st.get("checkin_done")),
        "lesson": bool(st.get("lesson_done")),
        "quiz": bool(st.get("quiz_done")),
        "review": bool(st.get("review_done")),
    }
    streak = st.get("streak_correct", 0)
    return mode, flags, streak

def _due_items():
    """收集所有科目到期知识点(next_review <= 今天)。返回 [(科目, 条目)...]"""
    today, _ = _today_shanghai()
    due = []
    for subj in SUBJECTS:
        data = load_json(os.path.join(STUDY_DIR, "knowledge", f"{subj}.json"), {"items": []})
        for it in data.get("items", []):
            nr = it.get("next_review", "")
            if nr and nr <= today:
                due.append((subj, it))
    due.sort(key=lambda x: x[1].get("next_review", ""))
    return due

def _mastery_cards():
    """掌握度卡片 HTML(苹果质感:圆角+毛玻璃+细腻阴影)。"""
    data = load_json(os.path.join(STUDY_DIR, "progress", "progress.json"), {"subjects": {}})
    subs = data.get("subjects", {})
    out = ['<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;">']
    for subj in SUBJECTS:
        m = subs.get(subj, {}).get("mastery", 0)
        icon = SUBJECT_ICONS.get(subj, "📘")
        color = "#34c759" if m >= 50 else ("#ff9500" if m >= 30 else "#ff3b30")
        out.append(f'<div class="app-card" style="padding:14px;margin:2px;">'
                   f'<div style="font-size:13px;color:#86868b;">{icon} {subj}</div>'
                   f'<div style="font-size:26px;font-weight:700;color:{color};letter-spacing:-0.02em;margin-top:2px;">{m}%</div>'
                   f'<div style="height:6px;background:rgba(128,128,128,.15);border-radius:3px;margin-top:8px;">'
                   f'<div style="height:100%;width:{m}%;background:{color};border-radius:3px;"></div></div></div>')
    out.append('</div>')
    return "\n".join(out)

def _history_days():
    """读取打卡历史。返回 (days_dict, streak)。"""
    hist = load_json(os.path.join(STUDY_DIR, "history.json"), {"days": []})
    days = {}
    for d in hist.get("days", []):
        if d.get("checkin"):
            days[d.get("date")] = d.get("mode", "standard")
    return days

def _calendar_heatmap(months_back=3):
    """生成最近 N 个月的打卡日历热力图(纯 HTML,无 JS 依赖)。
    返回 (html, streak, total)。"""
    from datetime import date, timedelta
    days = _history_days()
    today, _ = _today_shanghai()
    ty, tm, td = map(int, today.split("-"))
    today_d = date(ty, tm, td)

    # 计算连续天数(从今天往回,今天没打从昨天开始)
    streak = 0
    cur = today_d
    if cur.strftime("%Y-%m-%d") not in days:
        cur -= timedelta(days=1)
    while cur.strftime("%Y-%m-%d") in days:
        streak += 1
        cur -= timedelta(days=1)

    # 收集最近 months_back 个月的打卡日
    start = today_d - timedelta(days=30 * months_back)
    cell_html = []
    total = 0
    cur = start
    while cur <= today_d:
        key = cur.strftime("%Y-%m-%d")
        is_today = (key == today)
        if key in days:
            total += 1
            bg = "#34c759" if is_today else "rgba(52,199,89,.55)"
            cell_html.append(f'<div title="{key}" style="background:{bg};border-radius:5px;height:20px;min-width:11px;flex:1;"></div>')
        else:
            bg = "rgba(128,128,128,.12)" if is_today else "rgba(128,128,128,.05)"
            border = "2px solid #0071e3" if is_today else "1px solid rgba(128,128,128,.1)"
            cell_html.append(f'<div title="{key}" style="background:{bg};border:{border};border-radius:5px;height:20px;min-width:11px;flex:1;"></div>')
        cur += timedelta(days=1)
    html = ('<div style="display:flex;gap:3px;flex-wrap:nowrap;overflow-x:auto;padding:4px 0;">'
            + "".join(cell_html) + '</div>')
    return html, streak, total

def _milestones():
    """里程碑徽章:基于打卡天数/掌握度/错题清零判定。返回 HTML。"""
    hist = load_json(os.path.join(STUDY_DIR, "history.json"), {"days": []})
    total_days = sum(1 for d in hist.get("days", []) if d.get("checkin"))
    _, streak, _ = _calendar_heatmap()
    prog = load_json(os.path.join(STUDY_DIR, "progress", "progress.json"), {"subjects": {}})
    subs = prog.get("subjects", {})
    mastery = {s: subs.get(s, {}).get("mastery", 0) for s in SUBJECTS}

    def badge(emoji, name, done, tip=""):
        if done:
            return (f'<div class="app-card" style="padding:12px;text-align:center;border:1px solid rgba(52,199,89,.3);">'
                    f'<div style="font-size:24px;">{emoji}</div><div style="font-size:13px;font-weight:600;color:#34c759;">{name}</div>'
                    f'<div style="font-size:11px;color:#86868b;">已达成</div></div>')
        return (f'<div style="background:rgba(128,128,128,.04);border:1px dashed rgba(128,128,128,.25);border-radius:14px;padding:12px;text-align:center;opacity:.75;">'
                f'<div style="font-size:24px;">{emoji}</div><div style="font-size:13px;color:#86868b;">{name}</div>'
                f'<div style="font-size:11px;color:#aeaeb2;">{tip}</div></div>')

    out = ['<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;">']
    out.append(badge("🔥", "连续 7 天", streak >= 7, f"还差 {max(0,7-streak)} 天"))
    out.append(badge("⚡", "连续 14 天", streak >= 14, f"还差 {max(0,14-streak)} 天"))
    out.append(badge("🏆", "连续 30 天", streak >= 30, f"还差 {max(0,30-streak)} 天"))
    out.append(badge("📘", "高数 ≥50%", mastery.get("高等数学", 0) >= 50, f"当前 {mastery.get('高等数学',0)}%"))
    out.append(badge("⚙️", "机械 ≥70%", mastery.get("机械原理", 0) >= 70, f"当前 {mastery.get('机械原理',0)}%"))
    out.append(badge("📝", "累计 30 天", total_days >= 30, f"当前 {total_days} 天"))
    out.append('</div>')
    return "\n".join(out)

def daily_to_markdown():
    """每日学习页:倒计时 + 今日任务 + 今日科目 + 到期复习 + 今日知识点 + 在线小测。"""
    today, wd = _today_shanghai()
    days, stage = _exam_countdown()
    mode, flags, streak = _state_fields()
    mode_cn = MODE_CN.get(mode, mode)

    lines = []
    lines.append("---")
    lines.append("layout: home")
    lines.append("---")
    lines.append("")
    lines.append(f"# 📅 每日学习 · {today}({WEEKDAY_CN[wd]})")
    lines.append("")
    lines.append(f"> **考研倒计时: {days} 天 · {stage}阶段** ｜ 今日模式:**{mode_cn}** ｜ 连续答对 {streak} 次")
    lines.append("")
    lines.append("📌 每天 30 分钟:知识点 → 小测 → 复习错题。本页每日自动更新。")
    lines.append("")

    # 今日科目(按轮换表,提前取值供任务卡跳转使用)
    subj_a, subj_b = WEEK_ROTATION[wd]

    # 今日任务(实时组件:状态 + 打卡交互 + 跳转)
    lines.append("## ✅ 今日任务")
    lines.append("")
    lines.append("<DailyTasksComponent />")
    lines.append("")

    # 今日科目(按轮换表)
    lines.append("## 📖 今日科目")
    lines.append("")
    if wd == 7:  # 周日:周总结 + 错题总复习,无新知识点
        lines.append(f"> 今天是 **周日总结日**:{subj_a} + {subj_b}。没有新知识点,复习本周内容为主。")
    else:
        lines.append(f"> 今日轮换:**{SUBJECT_ICONS.get(subj_a,'')} {subj_a}** + **{SUBJECT_ICONS.get(subj_b,'')} {subj_b}**(各 15 分钟)")
        lines.append("")
        for s in (subj_a, subj_b):
            data = load_json(os.path.join(STUDY_DIR, "knowledge", f"{s}.json"), {"items": []})
            n = len(data.get("items", []))
            lines.append(f"- {SUBJECT_ICONS.get(s,'')} **{s}**:知识库 {n} 条 · [查看笔记](/subjects/{s})")
    lines.append("")

    # 到期复习
    due = _due_items()
    lines.append("## ⏰ 到期复习")
    lines.append("")
    if due:
        lines.append(f"**{len(due)} 条知识到期**,按间隔复习(SM-2),优先复习再学新的:")
        lines.append("")
        for subj, it in due[:12]:
            icon = SUBJECT_ICONS.get(subj, "📘")
            m = it.get("mastery", 0)
            lines.append(f"- {icon} **{subj}** · {it.get('title','')}(掌握 {m}%)")
        if len(due) > 12:
            lines.append(f"- ...共 {len(due)} 条")
    else:
        lines.append("> 🎉 今天没有到期复习,轻松学新知识!")
    lines.append("")

    # 今日知识点(带锚点,任务卡"知识点"跳这里;周日也显示,作为本周回顾)
    lines.append('<a id="today-lesson"></a>')
    lines.append("## 📚 今日知识点")
    lines.append("")
    if wd == 7:
        lines.append("**今天是周总结日,没有新知识点——回顾一下最近的要点:**")
        lines.append("")
        # 周日:从所有科目取最近创建的知识点做回顾
        all_items = []
        for s in SUBJECTS:
            d = load_json(os.path.join(STUDY_DIR, "knowledge", f"{s}.json"), {"items": []})
            for it in d.get("items", []):
                all_items.append((s, it))
        all_items.sort(key=lambda x: x[1].get("created", ""), reverse=True)
        for subj, it in all_items[:5]:
            icon = SUBJECT_ICONS.get(subj, "📘")
            title = it.get("title", "")
            m = it.get("mastery", 0)
            created = it.get("created", "")
            content = (it.get("content", "") or "")[:200]
            example = it.get("example", "")
            lines.append(f"### {icon} {subj} · {title}")
            lines.append("")
            meta = [f"**掌握度:** {m}%"]
            if created:
                meta.append(f"**创建:** {created}")
            lines.append(f"> {' | '.join(meta)}")
            lines.append("")
            bars = "█" * max(0, round(m / 10)) + "░" * max(0, 10 - round(m / 10))
            lines.append(f"> 掌握度进度: {bars}")
            lines.append("")
            if content:
                lines.append("**核心内容:**")
                lines.append("")
                lines.append(content)
                lines.append("")
            diagram = _match_diagram(subj, title)
            if diagram:
                lines.append("**图示:**")
                lines.append("")
                lines.append(f"![{title} 图示](./assets/diagrams/{diagram})")
                lines.append("")
            if example:
                lines.append("<details class=\"example-box\">")
                lines.append("<summary>💡 点击展示例题答案</summary>")
                lines.append("")
                lines.append(example)
                lines.append("")
                lines.append("</details>")
                lines.append("")
            lines.append("---")
            lines.append("")
        if not all_items:
            lines.append("> 知识库还是空的,等明天课程推送后自动补充。")
        lines.append("")
    else:
        lines.append(f"**今日科目 {SUBJECT_ICONS.get(subj_a,'')} {subj_a}** 最新知识点:")
        lines.append("")
        data = load_json(os.path.join(STUDY_DIR, "knowledge", f"{subj_a}.json"), {"items": []})
        items = sorted(data.get("items", []), key=lambda x: x.get("created", ""), reverse=True)
        shown = 0
        for it in items[:3]:
            title = it.get("title", "")
            content = (it.get("content", "") or "")[:250]
            example = it.get("example", "")
            m = it.get("mastery", 0)
            created = it.get("created", "")
            lines.append(f"### {title}")
            lines.append("")
            meta = [f"**掌握度:** {m}%"]
            if created:
                meta.append(f"**创建:** {created}")
            lines.append(f"> {' | '.join(meta)}")
            lines.append("")
            bars = "█" * max(0, round(m / 10)) + "░" * max(0, 10 - round(m / 10))
            lines.append(f"> 掌握度进度: {bars}")
            lines.append("")
            if content:
                lines.append("**核心内容:**")
                lines.append("")
                lines.append(content)
                lines.append("")
            diagram = _match_diagram(subj_a, title)
            if diagram:
                lines.append("**图示:**")
                lines.append("")
                lines.append(f"![{title} 图示](./assets/diagrams/{diagram})")
                lines.append("")
            if example:
                lines.append("<details class=\"example-box\">")
                lines.append("<summary>💡 点击展示例题答案</summary>")
                lines.append("")
                lines.append(example)
                lines.append("")
                lines.append("</details>")
                lines.append("")
            lines.append("---")
            lines.append("")
            shown += 1
        if shown == 0:
            lines.append("> 该科目暂无知识点,等今天的课程推送后自动补充。")
        lines.append("")

    # 掌握度速览
    lines.append("## 📊 掌握度速览")
    lines.append("")
    lines.append(_mastery_cards())
    lines.append("")

    # 打卡日历热力图 + 连续天数
    cal_html, streak, cal_total = _calendar_heatmap()
    lines.append("## 📅 打卡日历(近 90 天)")
    lines.append("")
    lines.append(f"> 🔥 **连续学习 {streak} 天** · 近 90 天打卡 {cal_total} 天 · 绿=已打卡 橙框=今天")
    lines.append("")
    lines.append(cal_html)
    lines.append("")

    # 里程碑徽章
    lines.append("## 🏅 里程碑")
    lines.append("")
    lines.append(_milestones())
    lines.append("")

    # 在线小测(独立页,不再内嵌组件)
    lines.append("## 📝 在线小测")
    lines.append("")
    lines.append("今日题目已生成,去 [在线小测](/quiz) 答题(提交后 AI 自动批改 + 解题步骤,成绩写回学习进度)。")
    lines.append("")

    return lines

# ---------- 首页仪表盘 ----------
def home_to_markdown():
    """门户页:hero + 学科入口 + 快捷入口(掌握度/日历/里程碑/知识点全部移入 daily/progress)。"""
    lines = []
    lines.append("---")
    lines.append("layout: home")
    lines.append("---")
    lines.append("")
    lines.append("# 启的考研笔记 🏷️")
    lines.append("")
    days, stage = _exam_countdown()
    lines.append("> **考研备考:** 数学一 · 机械原理 · 英语一 · 炼油化工设备\\n> **考研倒计时: {} 天 · {}阶段**\\n📌 本网站由学习系统自动生成, 每日更新。".format(days, stage))
    lines.append("")
    lines.append("**👉 今天学什么? 去 [每日学习](/daily) 看今日任务与知识点。**")
    lines.append("")
    lines.append("## 📘 学科笔记")
    lines.append("")
    lines.append('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;">')
    for subj in SUBJECTS:
        icon = SUBJECT_ICONS.get(subj, "📘")
        data2 = load_json(os.path.join(STUDY_DIR, "knowledge", f"{subj}.json"), {"items": []})
        cnt = len(data2.get("items", []))
        lines.append(f'<a href="/study/subjects/{subj}" style="display:block;background:#fff;border:1px solid #e0e0e0;border-radius:10px;padding:14px;text-decoration:none;color:#333;box-shadow:0 1px 3px rgba(0,0,0,.06);">'
                     f'<div style="font-size:16px;font-weight:600;">{icon} {subj}</div>'
                     f'<div style="font-size:13px;color:#888;margin-top:4px;">{cnt} 个知识点</div></a>')
    lines.append('</div>')
    lines.append("")
    lines.append("## 🧭 快捷入口")
    lines.append("")
    lines.append("| 页面 | 说明 |")
    lines.append("|------|------|")
    lines.append("| [📅 每日学习](/daily) | 今日任务 · 知识点 · 到期复习 |")
    lines.append("| [✏️ 在线小测](/quiz) | 每日 6 题 · 即时批改 · 解题步骤 |")
    lines.append("| [❌ 错题本](/mistakes) | 按科目分组 · 点日期看解析 |")
    lines.append("| [📈 学习进度](/progress) | 掌握度 · 打卡日历 · 里程碑 |")
    lines.append("| [🗓️ 学习计划](/plan) | 考研三阶段计划 · 科目轮换 |")
    lines.append("| [📊 每周周报](/reports/) | 周报归档 PDF |")
    lines.append("")
    return lines


def main():
    global STUDY_DIR, OUT_DIR, WEEKLY_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("--study-dir", default=STUDY_DIR)
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--no-assets", action="store_true", help="不拷贝周报PDF等资产")
    args = ap.parse_args()

    STUDY_DIR = args.study_dir
    OUT_DIR = args.out
    WEEKLY_DIR = os.path.join(args.study_dir, "archive", "weekly")

    # ⚠️ fail-fast:学习数据不存在时禁止生成空壳站(防 Actions runner 覆盖真站)
    if not os.path.isdir(STUDY_DIR) or not os.path.isdir(os.path.join(STUDY_DIR, "knowledge")):
        print(f"❌ 学习数据目录不存在或知识库缺失: {STUDY_DIR}")
        print("   本生成器只在有学习数据的机器上运行(本地 y7000)。真实部署: ./scripts/build.sh deploy")
        sys.exit(2)

    # 清理上一次生成(仅删除我们生成的文件)
    for sub in ["subjects", "reports", "assets/weekly"]:
        d = os.path.join(OUT_DIR, sub)
        if os.path.isdir(d):
            shutil.rmtree(d)

    ensure_dir(os.path.join(OUT_DIR, "subjects"))
    ensure_dir(os.path.join(OUT_DIR, "reports"))
    ensure_dir(os.path.join(OUT_DIR, "assets", "weekly"))
    ensure_dir(os.path.join(OUT_DIR, "assets", "diagrams"))

    # 复制图示(图文并茂)到网站 assets/diagrams/
    copied = set()
    for subj in SUBJECTS:
        mapping = DIAGRAM_MAP.get(subj, {})
        for kw, fname in mapping.items():
            src = os.path.join(STUDY_DIR, "math_renders", fname)
            if os.path.isfile(src) and fname not in copied:
                shutil.copy2(src, os.path.join(OUT_DIR, "assets", "diagrams", fname))
                copied.add(fname)
    if copied:
        print(f"✅ 图示: 复制 {len(copied)} 张图到 assets/diagrams/")

    # 首页
    with open(os.path.join(OUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(home_to_markdown()))

    # 每日学习页
    with open(os.path.join(OUT_DIR, "daily.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(daily_to_markdown()))
    print("✅ 每日学习页: docs/daily.md")

    # 四科笔记
    for subj in SUBJECTS:
        md = knowledge_to_markdown(subj)
        with open(os.path.join(OUT_DIR, "subjects", f"{subj}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(md))

    # 错题本
    with open(os.path.join(OUT_DIR, "mistakes.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(mistakes_to_markdown()))

    # 进度
    with open(os.path.join(OUT_DIR, "progress.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(progress_to_markdown()))

    # 学习计划
    with open(os.path.join(OUT_DIR, "plan.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(plan_to_markdown()))

    # 周报
    if not args.no_assets:
        rep_index, files = reports_to_markdown()
        with open(os.path.join(OUT_DIR, "reports", "index.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(rep_index))
        # 拷贝周报 PDF 到静态资源(供下载)
        if os.path.isdir(WEEKLY_DIR):
            for fn in files:
                src = os.path.join(WEEKLY_DIR, fn)
                dst = os.path.join(OUT_DIR, "assets", "weekly", fn)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
        print(f"✅ 周报: 拷贝 {len(files)} 份 PDF 到 assets/weekly/")
    else:
        with open(os.path.join(OUT_DIR, "reports", "index.md"), "w", encoding="utf-8") as f:
            f.write("# 📅 每周周报\n\n> 每周自动生成的备考进度周报。\n")

    print("✅ 网站内容已生成到", OUT_DIR)
    for subj in SUBJECTS:
        n = len(load_json(os.path.join(STUDY_DIR, "knowledge", f"{subj}.json"), {"items": []}).get("items", []))
        print(f"   - {subj}: {n} 个知识点")

if __name__ == "__main__":
    main()