#!/usr/bin/env python3
"""Refresh the AI-generated sections of the profile README.

1. Pulls recent public GitHub events for the profile owner.
2. Rewrites the ACTIVITY block with a short list of what changed.
3. If ANTHROPIC_API_KEY is set, asks Claude for a 2-3 sentence,
   recruiter-friendly summary and rewrites the AI-SUMMARY block.

Uses only the standard library so the workflow needs no installs.
"""

import json
import os
import re
import urllib.request
from pathlib import Path

USERNAME = os.environ.get("GH_USERNAME", "Amidouv")
README = Path(__file__).resolve().parent.parent / "README.md"
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5")
MAX_ITEMS = 6


def http_json(url, headers=None, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def fetch_events():
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USERNAME}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"https://api.github.com/users/{USERNAME}/events/public?per_page=50"
    return http_json(url, headers)


def describe(event):
    repo = event["repo"]["name"]
    link = f"[{repo}](https://github.com/{repo})"
    payload = event.get("payload", {})
    kind = event["type"]
    if kind == "PushEvent":
        commits = payload.get("commits") or []
        msg = commits[-1]["message"].splitlines()[0] if commits else "new commits"
        return f"🔨 Pushed to {link}: {msg}"
    if kind == "PullRequestEvent":
        pr = payload["pull_request"]
        return f"🔀 {payload['action'].capitalize()} PR in {link}: [{pr['title']}]({pr['html_url']})"
    if kind == "CreateEvent" and payload.get("ref_type") == "repository":
        return f"✨ Created {link}"
    if kind == "ReleaseEvent":
        return f"🚀 Released {payload['release']['tag_name']} of {link}"
    if kind == "WatchEvent":
        return f"⭐ Starred {link}"
    return None


def summarise(lines):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key or not lines:
        return None
    prompt = (
        "You write the 'what I'm building right now' blurb on a GitHub profile "
        f"for {USERNAME}, a DevOps/Cloud engineer moving into AI-augmented "
        "engineering. From the recent activity below, write 2-3 sentences in "
        "first person, aimed at a technical R&D recruiter. Be concrete, use "
        "Markdown bold for key technologies, no hype words, no emojis, and do "
        "not invent anything that is not in the activity.\n\n"
        + "\n".join(lines)
    )
    resp = http_json(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        {
            "model": MODEL,
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    text = "".join(b.get("text", "") for b in resp.get("content", []))
    return text.strip() or None


def replace_block(text, name, content):
    pattern = re.compile(
        rf"(<!-- {name}:START -->\n).*?(\n<!-- {name}:END -->)", re.DOTALL
    )
    return pattern.sub(lambda m: m.group(1) + content + m.group(2), text)


def main():
    lines = []
    for event in fetch_events():
        line = describe(event)
        if line and line not in lines:
            lines.append(line)
        if len(lines) == MAX_ITEMS:
            break

    readme = README.read_text()
    if lines:
        readme = replace_block(readme, "ACTIVITY", "\n".join(f"- {l}" for l in lines))
    summary = summarise(lines)
    if summary:
        readme = replace_block(readme, "AI-SUMMARY", summary)
    README.write_text(readme)


if __name__ == "__main__":
    main()
