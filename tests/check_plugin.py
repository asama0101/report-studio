"""report-studio の構成検査。成功で終了コード 0、失敗で 1。"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def frontmatter(path):
    m = re.match(r"---\r?\n(.*?)\r?\n---", path.read_text(encoding="utf-8"), re.S)
    return m.group(1) if m else ""


def main() -> int:
    errors = []

    pj = ROOT / ".claude-plugin" / "plugin.json"
    if not pj.exists():
        errors.append("plugin.json がない")
    else:
        try:
            data = json.loads(pj.read_text(encoding="utf-8"))
            if data.get("name") != "report-studio":
                errors.append("plugin.json の name が report-studio ではない")
            if not data.get("description"):
                errors.append("plugin.json の description が空")
        except json.JSONDecodeError as e:
            errors.append(f"plugin.json が不正な JSON: {e}")

    skill = ROOT / "skills" / "create" / "SKILL.md"
    if not skill.exists():
        errors.append("skills/create/SKILL.md がない")
    else:
        fm = frontmatter(skill)
        if not re.search(r"^name:\s*create\s*$", fm, re.M):
            errors.append("SKILL.md の frontmatter に name: create がない")
        if not re.search(r"^description:\s*\S", fm, re.M):
            errors.append("SKILL.md の frontmatter に description がない")

    doctor = ROOT / "commands" / "doctor.md"
    if not doctor.exists():
        errors.append("commands/doctor.md がない")
    elif not re.search(r"^description:\s*\S", frontmatter(doctor), re.M):
        errors.append("doctor.md の frontmatter に description がない")

    readme = ROOT / "README.md"
    if not readme.exists():
        errors.append("README.md がない")
    else:
        text = readme.read_text(encoding="utf-8")
        for word in ("--plugin-dir", "Playwright", "frontend-design"):
            if word not in text:
                errors.append(f"README.md に {word} がない")

    for e in errors:
        print("NG:", e)
    if not errors:
        print("OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
