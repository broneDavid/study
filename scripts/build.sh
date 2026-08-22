#!/usr/bin/env bash
# 学习网站自动重建脚本
# 用法:
#   ./scripts/build.sh          # 仅本地重建(生成markdown + vitepress build)
#   ./scripts/build.sh deploy   # 重建 + 推送到 GitHub Pages
set -euo pipefail

cd "$(dirname "$0")/.."

STUDY_WEBSITE_DIR="$(pwd)"

echo "==> [1/3] 生成网站 Markdown (从学习 JSON)"
python3 scripts/generate_site.py
if [ $? -ne 0 ]; then
  echo "❌ [1/3] 生成失败"; exit 1
fi
echo "✅ [1/3] 生成完成"

echo "==> [2/3] VitePress 构建"
pnpm docs:build
if [ $? -ne 0 ]; then
  echo "❌ [2/3] 构建失败"; exit 1
fi
echo "✅ [2/3] 构建完成 -> docs/.vitepress/dist"

if [ "${1:-}" = "deploy" ]; then
  echo "==> [3/3] 推送到 GitHub Pages"
  cd "$STUDY_WEBSITE_DIR"
  # 用 gh-pages 分支托管(标准 GitHub Pages 项目站)
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "❌ 项目尚未 init git, 请先 git init 并配置远程"; exit 1
  fi
  # 强制推送 dist 到 gh-pages 分支
  if command -v gh >/dev/null 2>&1; then
    gh deploy dist --ssh-flag --checkout=false --push --force 2>/dev/null || \
    gh deploy docs/.vitepress/dist --push --force
    echo "✅ [3/3] gh deploy 完成"
  else
    echo "⚠️ 未安装 gh CLI; 请手动推送 docs/.vitepress/dist 到 gh-pages 分支"
  fi
else
  echo "==> [3/3] 跳过部署 (加 deploy 参数可推送 GitHub Pages)"
fi
echo "🎉 全部完成"