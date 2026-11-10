"""生成した HTML の検査。外部読み込みと印刷 CSS の有無を見る。

使い方: python tests/check_html.py <html のパス>
問題があれば 1 行ずつ出して終了コード 1、なければ 0。
"""

import re
import sys
from pathlib import Path

_URL = r"""["']?\s*(?:https?:)?//"""
_EXTERNAL_LOADS = [
    re.compile(rf"\bsrc\s*=\s*{_URL}", re.I),
    re.compile(r"""\bsrcset\s*=\s*["']?[^"'>]*https?://""", re.I),
    re.compile(rf"\bposter\s*=\s*{_URL}", re.I),
    re.compile(rf"<object\b[^>]*\bdata\s*=\s*{_URL}", re.I),
    re.compile(rf"<(?:link|image|use)\b[^>]*\b(?:xlink:)?href\s*=\s*{_URL}", re.I),
    re.compile(rf"@import\s+(?:url\(\s*)?{_URL}", re.I),
    re.compile(rf"\burl\(\s*{_URL}", re.I),
]
_PRINT_CSS = re.compile(r"@media\s+print", re.I)


def find_problems(html: str) -> list[str]:
    problems = []
    for pattern in _EXTERNAL_LOADS:
        for m in pattern.finditer(html):
            problems.append(f"外部読み込み: {m.group(0).strip()}")
    if not _PRINT_CSS.search(html):
        problems.append("印刷 CSS（@media print）がない")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("使い方: python tests/check_html.py <html のパス>")
        return 2
    problems = find_problems(Path(argv[1]).read_text(encoding="utf-8"))
    for p in problems:
        print("NG:", p)
    if not problems:
        print("OK")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
