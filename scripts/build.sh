#!/usr/bin/env bash
# 学习网站自动重建脚本
# 用法:
#   ./scripts/build.sh            # 仅本地重建(生成markdown + vitepress build)
#   ./scripts/build.sh deploy     # 重建 + 部署到 GitHub Pages (gh-pages 分支)
set -euo pipefail

cd "$(dirname "$0")/.."
ROOT="$(pwd)"
TOKEN_FILE="$ROOT/.dev_token"

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
  echo "==> [3/3] 部署到 GitHub Pages (gh-pages 分支)"
  if [ ! -f "$TOKEN_FILE" ]; then
    echo "❌ 缺少部署凭证 $TOKEN_FILE"; exit 1
  fi
  GH_TOKEN="$(cat "$TOKEN_FILE")"
  export GH_TOKEN

  DEPLOY=/tmp/ghpages_deploy_$$
  rm -rf "$DEPLOY"; mkdir -p "$DEPLOY"
  cp -r docs/.vitepress/dist/* "$DEPLOY/"
  touch "$DEPLOY/.nojekyll"   # 关键:禁用 GitHub Pages 的 Jekyll 处理(防 {{ }} 导致整站404)
  cd "$DEPLOY"
  git init -q -b gh-pages
  git config user.name "broneDavid"
  git config user.email "broneDavid@users.noreply.github.com"
  git add -A
  git commit -q -m "Deploy website $(date '+%Y-%m-%d %H:%M')"

  # 用 askpass 传 token,避免明文落历史
  cat > "$DEPLOY/askpass.sh" <<'EOF'
#!/bin/bash
echo "$GH_TOKEN"
EOF
  chmod 700 "$DEPLOY/askpass.sh"

  GIT_ASKPASS="$DEPLOY/askpass.sh" \
    git push -q -f https://github.com/broneDavid/study.git gh-pages
  echo "✅ [3/3] 部署完成: https://bronedavid.github.io/study/"
  rm -rf "$DEPLOY"

  # 2026-08-25 新增:部署后校验(线上首页 200 + 最新周报 PDF 可达),失败告警不阻断
  HOME_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 "https://bronedavid.github.io/study/" || true)
  LATEST_PDF=$(ls -t docs/.vitepress/dist/weekly/*.pdf 2>/dev/null | head -1 | xargs -r basename)
  PDF_CODE=000
  if [ -n "$LATEST_PDF" ]; then
    PDF_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 "https://bronedavid.github.io/study/weekly/$LATEST_PDF" || true)
  fi
  if [ "$HOME_CODE" != "200" ]; then
    echo "⚠️ 部署后校验:线上首页返回 $HOME_CODE(异常,请检查 GitHub Pages)"
  else
    echo "✅ 部署后校验:首页 200"
  fi
  if [ -n "$LATEST_PDF" ] && [ "$PDF_CODE" != "200" ]; then
    echo "⚠️ 部署后校验:周报 PDF($LATEST_PDF)线上返回 $PDF_CODE(拷贝链路异常)"
  fi
else
  echo "==> [3/3] 跳过部署 (加 deploy 参数可推送 GitHub Pages)"
fi

echo "🎉 全部完成"