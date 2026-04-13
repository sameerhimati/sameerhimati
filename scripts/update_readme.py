#!/usr/bin/env python3
"""Auto-generate profile README from GitHub repo data."""
import json
import subprocess
import sys
from datetime import datetime

# === CONFIG ===
# Add new repos here. Emoji + category is all you need — dates come from the API.
PROJECTS = {
    "Learnt":                {"emoji": "📱", "desc": "iOS app for tracking daily learnings"},
    "claude-code-kit":       {"emoji": "🛠️", "desc": "Dev skills and agents for Claude Code"},
    "claude-marketing-kit":  {"emoji": "📣", "desc": "Marketing skills for Claude Code"},
    "blogpost":              {"emoji": "✍️", "desc": "CLI tool for creating blog post markdown files"},
    "economic-dashboard":    {"emoji": "📈", "desc": "Economic data dashboard"},
    "PaperBuddy":            {"emoji": "📚", "desc": "Read papers better and retain more knowledge"},
    "PapersApplied-ID3":     {"emoji": "🌳", "desc": "Implementation of J.R. Quinlan's ID3 paper"},
    "PapersApplied-Apriori": {"emoji": "🔗", "desc": "Implementation of Agrawal's Association Rule paper"},
    "Analysing_SEC_Filings": {"emoji": "📊", "desc": "NLP on M&A filings from the SEC"},
}

def fetch_repos():
    """Fetch all public repos via gh CLI."""
    result = subprocess.run(
        ["gh", "api", "users/sameerhimati/repos", "--paginate",
         "--jq", '.[] | select(.fork == false) | {name: .name, pushed_at: .pushed_at}'],
        capture_output=True, text=True
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
    lines = [
        "# Sameer Himati\n",
        "I love reading, starting companies, and investing. Currently building **Atlas**, an AI-native investment firm for private markets. Also founded **[Itamih](https://itamih.com)** (AI integration for small businesses) and **[Fend](https://thefend.com)** (a members-only startup network). More coming soon.\n",
        "[sameerhimati.com](https://sameerhimati.com) · [itamih.com](https://itamih.com) · [thefend.com](https://thefend.com)\n",
        "## Projects\n",
        "| | Project | Description | Updated |",
        "|---|---------|-------------|---------|",
    ]

    for name, info in PROJECTS.items():
        date = format_date(repos.get(name, "2020-01-01T00:00:00Z"))
        lines.append(
            f'| {info["emoji"]} | [{name}](https://github.com/sameerhimati/{name}) '
            f'| {info["desc"]} | {date} |'
        )

    lines.extend([
        "",
        "## Coming Soon\n",
        "| | Project | Description |",
        "|---|---------|-------------|",
    ])

    for name, info in COMING_SOON.items():
        lines.append(
            f'| {info["emoji"]} | [{name}](https://github.com/sameerhimati/{name}) '
            f'| {info["desc"]} |'
        )

    return "\n".join(lines) + "\n"

if __name__ == "__main__":
    repos = fetch_repos()
    readme = generate_readme(repos)
    with open("README.md", "w") as f:
        f.write(readme)
    print("README.md updated")
