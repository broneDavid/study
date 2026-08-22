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
        if example:
            lines.append("**例题:**")
            lines.append("")
            lines.append("> " + example)
            lines.append("")
        lines.append("---")
        lines.append("")

    return lines

# ---------- 错题本 ----------
def mistakes_to_markdown():
    lines = []
    lines.append("# ❌ 错题本")
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
        lines.append(f"## {icon} {subj}")
        lines.append("")
        open_items = [i for i in items if not i.get("resolved")]
        closed = [i for i in items if i.get("resolved")]
        for i in open_items:
            d = i.get("date", "")
            pt = i.get("point", "")
            lines.append(f"- 🔴 `{d}` {pt} (未解决)")
        for i in closed:
            d = i.get("date", "")
            pt = i.get("point", "")
            lines.append(f"- ✅ `{d}` {pt}")
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
  .mastery-fill { height:100%; background:linear-gradient(90deg,#3eaf7c,#67c23a); border-radius:9px; }
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

# ---------- 首页仪表盘 ----------
def home_to_markdown():
    lines = []
    lines.append("---")
    lines.append("layout: home")
    lines.append("---")
    lines.append("")
    lines.append("# 启的考研笔记 🏷️")
    lines.append("")
    lines.append("> **考研备考:** 数学一 · 机械原理 · 英语一 · 炼油化工设备\n> **考研倒计时: 126 天 · 强化阶段**\n📌 本网站由学习系统自动生成, 每日更新。")
    lines.append("")

    # 掌握度速览卡(HTML)
    lines.append("## 📊 掌握度速览")
    lines.append("")
    data = load_json(os.path.join(STUDY_DIR, "progress", "progress.json"), {"subjects": {}})
    subs = data.get("subjects", {})
    lines.append('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;">')
    for subj in SUBJECTS:
        m = subs.get(subj, {}).get("mastery", 0)
        icon = SUBJECT_ICONS.get(subj, "📘")
        color = "#3eaf7c" if m >= 50 else ("#e6a23c" if m >= 30 else "#f56c6c")
        lines.append(f'<div style="background:#fff;border:1px solid #e0e0e0;border-radius:10px;padding:12px;box-shadow:0 1px 3px rgba(0,0,0,.06);">'
                     f'<div style="font-size:14px;color:#666;">{icon} {subj}</div>'
                     f'<div style="font-size:26px;font-weight:700;color:{color};">{m}%</div>'
                     f'<div style="height:6px;background:#eee;border-radius:3px;margin-top:6px;">'
                     f'<div style="height:100%;width:{m}%;background:{color};border-radius:3px;"></div></div></div>')
    lines.append('</div>')
    lines.append("")

    # 今日知识点练习
    lines.append("## 📚 最近的知识点")
    lines.append("")
    # 从四科里取最近创建的几个作为"今日"
    latest = []
    for subj in SUBJECTS:
        data2 = load_json(os.path.join(STUDY_DIR, "knowledge", f"{subj}.json"), {"items": []})
        for it in data2.get("items", []):
            latest.append((subj, it))
    latest.sort(key=lambda x: x[1].get("created", ""), reverse=True)
    lines.append('**本网站以四科笔记库为主: 点击左侧"学科笔记"深入浏览。**')
    lines.append("")
    for subj, it in latest[:5]:
        icon = SUBJECT_ICONS.get(subj, "📘")
        title = it.get("title", "")
        m = it.get("mastery", 0)
        lines.append(f"### {icon} {subj} · {title}")
        lines.append(f"> 掌握 {m}% · 创建 {it.get('created','')}")
        content = (it.get("content", "") or "")[:200]
        example = it.get("example", "")
        if content:
            lines.append("")
            lines.append(content)
        if example:
            lines.append("")
            lines.append(f"> **例题:** {example}")
        lines.append("")

    # 快捷入口(含链接要用相对路径)
    lines.append("## 🚀 快捷入口")
    lines.append("")
    lines.append("| 页面 | 说明 |")
    lines.append("|------|------|")
    lines.append("| [📈 学习进度](/progress) | 各科掌握度曲线 & 最近学习要点 |")
    lines.append("| [❌ 错题本](/mistakes) | 未解决错题 & 复习记录 |")
    lines.append("| [🎯 学习计划](/plan) | 考研三阶段备考计划 |")
    lines.append("| [📅 每周周报](/reports/) | 每周备考周报 |")
    lines.append("| [📘 高等数学笔记](/subjects/高等数学) | 极限/导数/积分知识库 |")
    lines.append("| [⚙️ 机械原理笔记](/subjects/机械原理) | 机构/运动学/齿轮知识库 |")
    lines.append("")
    return lines

# ---------- 主流程 ----------
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

    # 清理上一次生成(仅删除我们生成的文件)
    for sub in ["subjects", "reports", "assets/weekly"]:
        d = os.path.join(OUT_DIR, sub)
        if os.path.isdir(d):
            shutil.rmtree(d)

    ensure_dir(os.path.join(OUT_DIR, "subjects"))
    ensure_dir(os.path.join(OUT_DIR, "reports"))
    ensure_dir(os.path.join(OUT_DIR, "assets", "weekly"))

    # 首页
    with open(os.path.join(OUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(home_to_markdown()))

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