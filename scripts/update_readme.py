#!/usr/bin/env python3
"""Auto-generate the profile README from GitHub repo data.

This file is the source of truth for github.com/sameerhimati. The workflow in
.github/workflows/ runs it daily and force-commits the result, so editing README.md
by hand does nothing that survives a day. Edit BIO / PRODUCTION / OPEN_SOURCE / OTHER
below instead.

Kept deliberately in step with sameerhimati.com/projects: same three groups, same
descriptions, same claims. If one changes, change both.
"""
import json
import subprocess
from datetime import datetime

# === BIO ===
BIO = [
    "# Sameer Himati\n",
    "I build AI systems for businesses I already have direct access to. I find the problem "
    "myself, build it, and run it in production. That work goes out under "
    "**[Itamih](https://itamih.com)**, which is bootstrapped and self-funded.\n",
    "Most of what I care about comes down to one habit: a system should refuse before it "
    "guesses. Per-field confidence, provenance on every number, and a rule that routes the "
    "uncertain cases to a person.\n",
    # No job titles here on purpose. This is a dev profile, not a resume -- the work and the
    # kind of business it was for, not the role I held while doing it. It also means this file
    # can never contradict the resume, because it makes no claim the resume could disagree with.
    "Before this I built **[Fend](https://thefend.com)** solo, front to back, a B2B-pilots "
    "marketplace that went 0 to 1,000+ users. And before that, document extraction for "
    "mortgage origination at Fundmore. In SF.\n",
    "[sameerhimati.com](https://sameerhimati.com) · "
    "[Projects](https://sameerhimati.com/projects) · "
    "[Writing](https://sameerhimati.com/blog)\n",
]

# === IN PRODUCTION ===
# Private repos, so these link to the write-up rather than to code.
PRODUCTION = [
    {
        "name": "Clinic",
        "desc": "From-scratch practice-management system that replaced a 26-year-old on-premise "
                "setup at a dental hospital. In daily use by doctors, billing, and ops.",
        "link": "https://itamih.com/case-studies/clinic",
        "link_label": "Case study",
    },
    {
        "name": "Bean",
        "desc": "Support-email agent that drafts replies grounded only in facts it can source, "
                "and refuses to draft when it isn't confident instead of guessing.",
        "link": "https://bean.itamih.com/join",
        "link_label": "Join the beta",
    },
    {
        "name": "Atlas",
        "desc": "Private-markets agent platform for CRE. It ran end to end on real deals. Wound "
                "down May 2026, because the constraint was access rather than analysis.",
        "link": "https://itamih.com/case-studies/atlas",
        "link_label": "Post-mortem",
    },
]

# === OPEN SOURCE ===
# Keys must match the GitHub repo name exactly; dates come from the API.
OPEN_SOURCE = {
    "hunt": {
        "emoji": "🎯",
        "desc": "The whole job hunt in one local-first app. BYOK, so nothing leaves your machine",
    },
    "sourcery": {
        "emoji": "🔍",
        "desc": "Find the best search API for your agent. Same query, same judge, swap the provider",
    },
    "delta-learning": {
        "emoji": "🎬",
        "desc": "Only what you don't already know: a timecoded cut list, as a graph set difference",
    },
    "LibStack": {
        "emoji": "📖",
        "desc": "Offline-capable reading viewer for a knowledge vault",
    },
}

# === OTHER ===
OTHER = {
    "nanogpt-mlx": "a GPT from scratch by hand in MLX, in progress",
    "claude-code-kit": "my Claude Code setup",
    "Learnt": "iOS app for tracking daily learnings",
    "economic-dashboard": "economic data dashboard",
    "PaperBuddy": "read papers better and retain more",
}


def fetch_repos():
    """Fetch all public repos via gh CLI."""
    result = subprocess.run(
        ["gh", "api", "users/sameerhimati/repos", "--paginate",
         "--jq", '.[] | select(.fork == false) | {name: .name, pushed_at: .pushed_at}'],
        capture_output=True, text=True,
    )
    repos = {}
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            data = json.loads(line)
            repos[data["name"]] = data["pushed_at"]
    return repos


def format_date(iso_date):
    """Convert ISO date to 'Mon YYYY'."""
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.strftime("%b %Y")


def generate_readme(repos):
    lines = list(BIO)

    lines += [
        "## In production\n",
        "Built for real businesses. People depend on these, so the repos are private and these "
        "link to the write-up.\n",
    ]
    for project in PRODUCTION:
        lines.append(
            f'- **{project["name"]}** — {project["desc"]} '
            f'[{project["link_label"]} →]({project["link"]})'
        )
    lines.append("")

    lines += [
        "## Open source\n",
        "| | Project | Description | Updated |",
        "|---|---------|-------------|---------|",
    ]
    for name, info in OPEN_SOURCE.items():
        date = format_date(repos.get(name, "2020-01-01T00:00:00Z"))
        lines.append(
            f'| {info["emoji"]} | [{name}](https://github.com/sameerhimati/{name}) '
            f'| {info["desc"]} | {date} |'
        )
    lines.append("")

    others = ", ".join(
        f"[{name}](https://github.com/sameerhimati/{name}) ({desc})"
        for name, desc in OTHER.items()
    )
    lines.append(f"<sub>Also: {others}.</sub>")

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    repos = fetch_repos()
    readme = generate_readme(repos)
    with open("README.md", "w") as f:
        f.write(readme)
    print("README.md updated")
