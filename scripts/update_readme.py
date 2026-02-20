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
    "PaperBuddy":            {"emoji": "📚", "desc": "Read papers better and retain more knowledge"},
    "economic-dashboard":    {"emoji": "📈", "desc": "Economic data dashboard"},
    "PapersApplied-ID3":     {"emoji": "🌳", "desc": "Implementation of J.R. Quinlan's ID3 paper"},
    "PapersApplied-Apriori": {"emoji": "🔗", "desc": "Implementation of Agrawal's Association Rule paper"},
    "Analysing_SEC_Filings": {"emoji": "📊", "desc": "NLP on M&A filings from the SEC"},
    "muteAd":                {"emoji": "🔇", "desc": "Chrome extension that mutes ads on streaming platforms"},
    "Pokeman-Langchains":    {"emoji": "⚡", "desc": "LangChain exploration"},
}

COMING_SOON = {
    "costar-puller":    {"emoji": "🏢", "desc": "Browser agent that automates CoStar CSV exports"},
    "property-scorer":  {"emoji": "🏠", "desc": "Scores CRE properties on motivated seller signals"},
    "underwriter":      {"emoji": "💰", "desc": "CRE financial modeling and pro forma engine"},
    "comp-puller":      {"emoji": "📊", "desc": "Market comparable data extraction and benchmarking"},
    "contact-enricher": {"emoji": "📇", "desc": "Enriches property owner records from public sources"},
    "deal-boxer":       {"emoji": "📦", "desc": "Filters properties against investment criteria"},
    "entity-classifier":{"emoji": "🏷️", "desc": "Classifies property owner names into entity types"},
    "memo-writer":      {"emoji": "📝", "desc": "Evidence-linked CRE deal memo generation"},
    "skip-tracer":      {"emoji": "🔍", "desc": "Owner contact skip tracing via DealMachine"},
    "voice-caller":     {"emoji": "📞", "desc": "AI voice calling agent for owner outreach"},
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
        "Tinkerer. I just like building stuff.\n",
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
