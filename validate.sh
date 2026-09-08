#!/usr/bin/env bash
# lifeos-media-pack 技能校验（仿 charlie947/social-media-skills validate-skills.sh，MIT）
set -u
cd "$(dirname "$0")"
pass=0; fail=0
for dir in skills/*/; do
  name="$(basename "$dir")"
  f="$dir/SKILL.md"
  [ -f "$f" ] || { echo "✗ $name: 缺 SKILL.md"; fail=$((fail+1)); continue; }
  ok=1
  head -1 "$f" | grep -q '^---' || { echo "✗ $name: 缺 frontmatter"; ok=0; }
  grep -q '^name: ' "$f" || { echo "✗ $name: 缺 name 字段"; ok=0; }
  grep "^name: " "$f" | head -1 | grep -q "$name" || { echo "✗ $name: name 与目录不一致"; ok=0; }
  grep -q '^description: ' "$f" || { echo "✗ $name: 缺 description"; ok=0; }
  desc_len=$(grep '^description: ' "$f" | head -1 | wc -c)
  [ "$desc_len" -le 1024 ] || { echo "✗ $name: description 超 1024 字符"; ok=0; }
  lines=$(wc -l < "$f")
  [ "$lines" -le 400 ] || { echo "✗ $name: 超 400 行 ($lines)"; ok=0; }
  if [ "$ok" -eq 1 ]; then echo "✓ $name ($lines 行)"; pass=$((pass+1)); else fail=$((fail+1)); fi
done
echo "----"
echo "通过: $pass  失败: $fail"
[ "$fail" -eq 0 ]
