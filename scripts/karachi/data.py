"""Contribution data: load data/contributions.json and fold it into GitHub-style weeks."""
from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass

from .svg import ROOT

DATA_FILE = ROOT / "data" / "contributions.json"


@dataclass
class Day:
    date: dt.date
    count: int | None  # None = outside the 365-day window (not yet built)
    level: int  # 0..4, GitHub's own quartile level


@dataclass
class Year:
    weeks: list[list[Day]]
    start: dt.date
    end: dt.date

    @property
    def days(self):
        return [d for w in self.weeks for d in w if d.count is not None]

    @property
    def total(self):
        return sum(d.count for d in self.days)

    @property
    def active_days(self):
        return sum(1 for d in self.days if d.count)

    @property
    def best_day(self):
        return max(self.days, key=lambda d: (d.count, d.date))

    def week_total(self, i):
        return sum(d.count or 0 for d in self.weeks[i])

    @property
    def best_week(self):
        return max(range(len(self.weeks)), key=self.week_total)

    @property
    def longest_streak(self):
        best = cur = 0
        for d in self.days:
            cur = cur + 1 if d.count else 0
            best = max(best, cur)
        return best


def load(path=DATA_FILE) -> Year:
    raw = json.loads(path.read_text())
    by_date = {dt.date.fromisoformat(d["date"]): d for d in raw["days"]}
    end = dt.date.fromisoformat(raw["end"])
    start = end - dt.timedelta(days=364)
    first_sunday = start - dt.timedelta(days=(start.weekday() + 1) % 7)
    weeks, cursor = [], first_sunday
    while cursor <= end:
        week = []
        for i in range(7):
            day = cursor + dt.timedelta(days=i)
            rec = by_date.get(day)
            inside = start <= day <= end
            week.append(Day(day, (rec["count"] if rec else 0) if inside else None,
                            (rec["level"] if rec else 0) if inside else 0))
        weeks.append(week)
        cursor += dt.timedelta(days=7)
    return Year(weeks, start, end)
