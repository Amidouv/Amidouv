#!/usr/bin/env python3
"""Refresh the AI-generated sections of the profile README.

1. Pulls recent public GitHub events for the profile owner.
2. Rewrites the ACTIVITY block, if the README has one.
3. Asks an LLM for a one-line "now building" summary and
   rewrites the AI-SUMMARY block. The LLM backend is:
   - AWS Bedrock (Converse API) when BEDROCK_MODEL_ID is set and AWS
     credentials are available (the workflow gets them keylessly via OIDC);
   - otherwise the Claude API when ANTHROPIC_API_KEY is set;
   - otherwise the summary is left as is.

Only Bedrock needs a dependency (boto3); everything else is standard library.
"""

import json
import os
import re
import urllib.request
from pathlib import Path

USERNAME = os.environ.get("GH_USERNAME", "Amidouv")
README = Path(__file__).resolve().parent.parent / os.environ.get("TARGET_FILE", "README.md")
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


def ask_bedrock(prompt, model_id):
    import boto3

    client = boto3.client("bedrock-runtime")
    resp = client.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 300},
    )
    return "".join(b.get("text", "") for b in resp["output"]["message"]["content"])


def ask_claude(prompt, key):
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
    return "".join(b.get("text", "") for b in resp.get("content", []))


def summarise(lines):
    bedrock_model = os.environ.get("BEDROCK_MODEL_ID")
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not (bedrock_model or key):
        return None
    context = ""
    profile = README.parent / "profile.toml"
    if profile.exists():
        import tomllib

        context = tomllib.loads(profile.read_text()).get("now_context", "")
    prompt = (
        "You write the 'now building' line on the GitHub profile of "
        f"{USERNAME}, a Platform & AI Engineer. Using only the context and "
        "recent activity below, write ONE line of at most 22 words describing "
        "what they are building now. Start with the thing itself (no 'I am'), "
        "confident with a touch of playfulness, concrete technologies, no "
        "emojis, no Markdown, and invent nothing that is not below.\n\n"
        f"Context:\n{context.strip()}\n\nRecent public activity:\n"
        + ("\n".join(lines) or "(none)")
    )
    if bedrock_model:
        text = ask_bedrock(prompt, bedrock_model)
    else:
        text = ask_claude(prompt, key)
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
