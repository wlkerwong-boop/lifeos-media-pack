#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Markdown -> 排版良好的 PDF（中文优先，Mac）
用法： python3 md2pdf.py 输入.md 输出.pdf "文档标题"
原理： 自写 md->HTML（支持标题/表格/列表/引用/分隔线/粗体/行内代码/链接）
      + Chrome headless --print-to-pdf（Chrome 对中文字体和 CSS 排版支持最好）
"""
import sys, os, re, html, subprocess, tempfile

CSS = """
@page { size: A4; margin: 15mm 13mm 16mm 13mm; }
* { box-sizing: border-box; }
html, body { margin:0; padding:0; background:#fff; }
body {
  font-family: "PingFang SC","Hiragino Sans GB","Heiti SC","Songti SC",-apple-system,sans-serif;
  font-size: 10.5pt; line-height: 1.85; color: #23201B;
  -webkit-font-smoothing: antialiased;
  word-break: normal;            /* 不要从单词中间断开（ChatGPT 被切成 ChatGP/T 的问题） */
  overflow-wrap: break-word;     /* 只在真的放不下时才断 */
}
.doc { max-width: 100%; }
h1 {
  font-size: 19pt; line-height:1.35; font-weight:700; margin: 0 0 6px 0;
  padding-bottom: 8px; border-bottom: 2.5px solid #A8843C; letter-spacing:.01em;
}
h2 {
  font-size: 13.5pt; font-weight:700; color:#7A5F22; margin: 22px 0 8px 0;
  padding-left: 9px; border-left: 4px solid #A8843C; line-height:1.45;
  page-break-after: avoid;
}
h3 {
  font-size: 11.5pt; font-weight:700; margin: 16px 0 6px 0; color:#23201B;
  page-break-after: avoid;
}
h4 { font-size: 10.5pt; font-weight:700; margin: 12px 0 4px 0; color:#5A5348; page-break-after: avoid; }
p { margin: 7px 0; text-align: justify; }
strong { font-weight: 700; }
em { font-style: normal; color:#7A5F22; font-weight:600; }
code {
  font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 9pt;
  background:#F5F1E8; padding: 1px 4px; border-radius: 3px; color:#7A4A22;
}
a { color:#7A5F22; text-decoration: none; }
hr { border: none; border-top: 1px dashed #D8CDB8; margin: 16px 0; }
blockquote {
  margin: 9px 0; padding: 8px 12px; background:#FBF7F0;
  border-left: 3px solid #D9C79A; color:#5A5348; font-size: 9.8pt; line-height:1.75;
}
blockquote p { margin: 3px 0; text-align: left; }
pre {
  background:#F7F4EC; border:1px solid #E3D9C4; border-left:3px solid #A8843C;
  padding: 8px 10px; margin: 8px 0; white-space: pre-wrap; word-break: break-word;
  page-break-inside: avoid;
}
pre code { background:none; padding:0; color:#33302A; font-size: 9.2pt; line-height:1.65; }
ul, ol { margin: 6px 0 6px 0; padding-left: 1.35em; }
li { margin: 4px 0; }
table {
  width: 100%; border-collapse: collapse; margin: 10px 0 12px 0;
  font-size: 9.4pt; line-height: 1.6; page-break-inside: auto;
}
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th {
  background: #F2EADA; border: 1px solid #DCCFB4; padding: 6px 8px;
  text-align: left; font-weight: 700; color:#4A3D1E;
}
td { border: 1px solid #E3D9C4; padding: 6px 8px; vertical-align: top; }
tbody tr:nth-child(even) td { background: #FCFAF5; }
td strong, th strong { font-weight:700; }
.foot-note { margin-top: 18px; padding-top: 8px; border-top: 1px solid #E3D9C4;
  font-size: 9pt; color: #8A8272; }
"""


def inline(t: str) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t


def md_to_html(md: str) -> str:
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]

        # 代码块
        if ln.strip().startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append("<pre><code>" + "\n".join(buf) + "</code></pre>")
            continue

        # 表格
        if ln.strip().startswith("|") and i + 1 < len(lines) and re.match(r'^\s*\|[\s:\-|]+\|\s*$', lines[i + 1]):
            header = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ["<table><thead><tr>"]
            t += ["<th>%s</th>" % inline(c) for c in header]
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)$', ln)
        if m:
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2).strip()), lvl))
            i += 1
            continue

        # 分隔线
        if re.match(r'^\s*(-{3,}|\*{3,}|_{3,})\s*$', ln):
            out.append("<hr>")
            i += 1
            continue

        # 引用
        if ln.strip().startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>" + "".join("<p>%s</p>" % inline(b) for b in buf if b) + "</blockquote>")
            continue

        # 列表
        if re.match(r'^\s*([-*+]|\d+\.)\s+', ln):
            ordered = bool(re.match(r'^\s*\d+\.\s+', ln))
            tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines) and re.match(r'^\s*([-*+]|\d+\.)\s+', lines[i]):
                items.append(re.sub(r'^\s*([-*+]|\d+\.)\s+', '', lines[i]))
                i += 1
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
            continue

        # 空行
        if not ln.strip():
            i += 1
            continue

        # 普通段落（连续行合并）
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r'^(#{1,6}\s|\s*[-*+]\s|\s*\d+\.\s|>|\s*\|)', lines[i]) and not lines[i].strip().startswith("```"):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append("<p>%s</p>" % inline(" ".join(buf)))
    return "\n".join(out)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else os.path.basename(src)
    md = open(src, encoding="utf-8").read()
    body = md_to_html(md)
    page = ("<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>"
            "<title>%s</title><style>%s</style></head><body><div class='doc'>%s</div></body></html>"
            % (html.escape(title), CSS, body))
    tmp = tempfile.mktemp(suffix=".html")
    open(tmp, "w", encoding="utf-8").write(page)
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    cmd = [chrome, "--headless", "--disable-gpu", "--no-sandbox",
           "--no-pdf-header-footer", "--virtual-time-budget=8000",
           "--print-to-pdf=%s" % dst, "file://" + tmp]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(dst):
        print("PDF 生成失败：", r.stderr[-1500:])
        sys.exit(1)
    print("OK  %s  (%.1f KB)" % (dst, os.path.getsize(dst) / 1024))


if __name__ == "__main__":
    main()
