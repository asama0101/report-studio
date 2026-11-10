"""プラグインの形式を検査する（plugin-rules E1 の 1〜7）。"""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "report-studio"
SKILLS = sorted(PLUGIN.glob("skills/*/SKILL.md"))
NAME = "report-studio"


def ids(paths):
    return [p.parent.name for p in paths]


def read(path):
    return path.read_text(encoding="utf-8")


def frontmatter(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    assert m, "先頭に frontmatter がない"
    fields = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def test_スキルが揃っている():
    assert {p.parent.name for p in SKILLS} == {"create", "doctor"}


@pytest.mark.parametrize("skill", SKILLS, ids=ids(SKILLS))
def test_nameがディレクトリ名と一致しdescriptionがある(skill):
    fm = frontmatter(read(skill))
    assert fm["name"] == skill.parent.name
    assert fm["description"]


def test_doctorは自動起動しない():
    fm = frontmatter(read(PLUGIN / "skills" / "doctor" / "SKILL.md"))
    assert fm["disable-model-invocation"] == "true"


@pytest.mark.parametrize("skill", SKILLS, ids=ids(SKILLS))
def test_絶対パスとCLAUDE_SKILL_DIRがない(skill):
    text = read(skill)
    pattern = r"(?<![A-Za-z])[A-Za-z]:[\/]+\w|/(?:Users|home)/\w"
    assert re.findall(pattern, text) == []
    assert "CLAUDE_SKILL_DIR" not in text


@pytest.mark.parametrize("skill", SKILLS, ids=ids(SKILLS))
def test_CLAUDE_PLUGIN_ROOT_が指すファイルが実在する(skill):
    refs = re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\s\"'`)]+)", read(skill))
    assert [r for r in refs if not (PLUGIN / r).is_file()] == []


@pytest.mark.parametrize("skill", SKILLS, ids=ids(SKILLS))
def test_相対リンクと地の文の相対パスがない(skill):
    text = read(skill)
    assert re.findall(r"\]\((?!https?://|mailto:|#)[^)]*\)", text) == []
    assert re.findall(r"(?:^|[\s`(\"'])\.{1,2}/", text, re.MULTILINE) == []


def test_MCPを同梱していない():
    assert not (PLUGIN / ".mcp.json").exists()
    plugin = json.loads(read(PLUGIN / ".claude-plugin" / "plugin.json"))
    assert "mcpServers" not in plugin


def test_versionがplugin_jsonにあり_marketplaceには書かない():
    plugin = json.loads(read(PLUGIN / ".claude-plugin" / "plugin.json"))
    market = json.loads(read(ROOT / ".claude-plugin" / "marketplace.json"))
    assert re.fullmatch(r"\d+\.\d+\.\d+", plugin["version"])
    assert all("version" not in p for p in market["plugins"])


def test_配布に必要なファイルがgit管理下にある():
    out = subprocess.run(  # noqa: S603
        ["git", "ls-files", "plugins/report-studio"],  # noqa: S607
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    ).stdout.split()
    for rel in (
        ".claude-plugin/plugin.json",
        "NOTICE",
        "skills/create/SKILL.md",
        "skills/doctor/SKILL.md",
    ):
        assert f"plugins/report-studio/{rel}" in out


@pytest.mark.skipif(shutil.which("claude") is None, reason="claude CLI がない")
def test_claude_plugin_validateが通る():
    for target in (PLUGIN, ROOT):
        r = subprocess.run(  # noqa: S603
            [shutil.which("claude"), "plugin", "validate", str(target), "--strict"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        assert r.returncode == 0, r.stdout + r.stderr
