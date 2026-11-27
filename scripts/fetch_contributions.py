"""Fetch the last year of GitHub contributions into data/contributions.json.

Uses the GraphQL API with the token in $GITHUB_TOKEN (the Actions token is enough for
public contributions). Standard library only.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

USER = os.environ.get("PROFILE_USER", "BashairYaqoob")
OUT = Path(__file__).resolve().parents[1] / "data" / "contributions.json"
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}

QUERY = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    contributionsCollection(from:$from, to:$to) {
      contributionCalendar { weeks { contributionDays { date contributionCount contributionLevel } } }
    }
  }
}"""


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is not set; keeping the existing data file.", file=sys.stderr)
        return 0
    today = dt.datetime.now(dt.timezone.utc).date()
    start = today - dt.timedelta(days=364)
    body = json.dumps({"query": QUERY, "variables": {
        "login": USER, "from": f"{start}T00:00:00Z", "to": f"{today}T23:59:59Z"}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-renderer"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        print(payload["errors"], file=sys.stderr)
        return 1
    weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [{"date": d["date"], "count": d["contributionCount"], "level": LEVELS[d["contributionLevel"]]}
            for w in weeks for d in w["contributionDays"]]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"user": USER, "end": str(today), "days": days}, indent=0) + "\n")
    print(f"wrote {len(days)} days, {sum(d['count'] for d in days)} contributions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
