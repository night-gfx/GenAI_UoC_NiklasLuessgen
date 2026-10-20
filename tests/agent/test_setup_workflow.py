"""Structural validation of the research-task workflow setup (no task execution)."""

import hashlib
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TASKS = [
    "01_collect_data",
    "02_prepare_returns",
    "03_estimate_beta",
    "04_partial_correlation",
    "05_results",
]
SECTIONS = ["GOAL", "FILES", "CONSTRAINTS", "STEPS", "CHECK", "OUTPUT", "STOP"]
STATUSES = {"Planned", "In Progress", "In Review", "Completed"}
SKILL = ROOT / ".agents/skills/research-task-workflow/SKILL.md"
BASELINE = json.loads((ROOT / "tests/agent/setup_baseline.json").read_text())

# Files outside the authorized setup scope must match the pre-setup baseline.
PROTECTED = [
    ".gitattributes",
    ".gitignore",
    "README.md",
    "proposal.md",
    "requirements.txt",
    "data/raw/README.md",
    "data/raw/12_Industry_Portfolios_Daily.csv",
    "data/raw/F-F_Research_Data_Factors_daily.csv",
    "literature/literature_matrix.md",
]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


@pytest.mark.parametrize("task", TASKS)
def test_task_sections_in_order(task):
    headings = re.findall(r"^## (\w+)\s*$", read(f"tasks/{task}.md"), re.M)
    assert headings == SECTIONS


@pytest.mark.parametrize("task", TASKS)
def test_task_names_expected_branch(task):
    assert f"**Expected branch:** `agent/{task}`." in read(f"tasks/{task}.md")


def test_readme_order_and_status():
    rows = re.findall(
        r"^\| (\d\d) \| \[(\w+)\.md\]\(\w+\.md\) \| [^|]+ \| `agent/(\w+)` \| ([^|]+?) \|",
        read("tasks/README.md"),
        re.M,
    )
    assert [r[1] for r in rows] == TASKS
    assert [r[0] for r in rows] == [t[:2] for t in TASKS]
    assert all(r[1] == r[2] for r in rows)
    # Setup must not start any task.
    assert all(r[3] == "Planned" for r in rows)


def test_status_sequence_and_researcher_control():
    readme = read("tasks/README.md")
    assert "Planned → In Progress → In Review → Completed" in readme
    assert "Only the\n  researcher may set this status." in readme
    for text in (readme, read("AGENTS.md"), SKILL.read_text()):
        used = set(re.findall(r"`(Planned|In Progress|In Review|Completed)`", text))
        assert used <= STATUSES


def test_skill_frontmatter_and_rules():
    text = SKILL.read_text()
    match = re.match(r"---\nname: (\S+)\ndescription: (.+)\n---\n", text)
    assert match and match.group(1) == "research-task-workflow"
    for phrase in (
        "git branch --show-current",
        "Require the exact expected branch",
        "Run its relevant checks",
        "create one descriptive commit for the\n     verified step",
        "Only the researcher may mark a task `Completed` and perform merges.",
        "Do not push or open pull requests",
    ):
        assert phrase in text


def test_agents_references_skill_and_readme_exception():
    text = read("AGENTS.md")
    assert "## Research Task Workflow" in text
    assert "`.agents/skills/research-task-workflow/SKILL.md`" in text
    assert "may additionally update `tasks/README.md` solely to track task status" in text
    assert "Only the researcher may set `Completed`" in text
    # Original rules are preserved: the setup only appends a section.
    assert text.index("## Restrictions (Task Boundaries)") < text.index("## Research Task Workflow")


def test_obsolete_setup_helpers_removed():
    assert not (ROOT / "tasks/AGENTS_workflow_update.md").exists()
    assert not (ROOT / "tasks/research-task-workflow").exists()
    assert "tasks/research-task-workflow/SKILL.md" not in read("AGENTS.md")


def test_skill_identical_to_prepared_version():
    digest = hashlib.sha256(SKILL.read_bytes()).hexdigest()
    assert digest == BASELINE["sha256"]["tasks/research-task-workflow/SKILL.md"]


@pytest.mark.parametrize("rel", PROTECTED)
def test_protected_files_unchanged(rel):
    digest = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
    assert digest == BASELINE["sha256"][rel]


def test_no_research_artifacts_created():
    assert not list((ROOT / "code").glob("*.py"))
    adjusted = ROOT / "data/adjusted"
    assert not adjusted.exists() or not any(adjusted.iterdir())
