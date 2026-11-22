"""Render an SVG from a GitHub profile's public contribution calendar."""

import argparse
import calendar
from datetime import date, timedelta
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.request import Request, urlopen

CARD_PATH = Path(__file__).resolve().parents[1] / "cards" / "activity.svg"
COLORS = ("#263650", "#245961", "#277b78", "#38a99b", "#76e6cb")
DAY = timedelta(days=1)


class ContributionCalendar(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.grid = {}
        self.labels = {}
        self.tooltip = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "td" and {"data-date", "data-level", "id"} <= attributes.keys():
            self.grid[attributes["id"]] = (
                date.fromisoformat(attributes["data-date"]),
                int(attributes["data-level"]),
            )
        if tag == "tool-tip":
            self.tooltip = attributes.get("for")
            if self.tooltip:
                self.labels[self.tooltip] = []

    def handle_data(self, data):
        if self.tooltip:
            self.labels[self.tooltip].append(data)

    def handle_endtag(self, tag):
        if tag == "tool-tip":
            self.tooltip = None

    def days(self):
        days = {}
        for identifier, (day, level) in self.grid.items():
            label = "".join(self.labels.get(identifier, [])).strip().lower()
            match = re.match(r"([0-9,]+) contributions?\b", label)
            if match:
                count = int(match.group(1).replace(",", ""))
            elif label.startswith("no contributions"):
                count = 0
            else:
                raise ValueError(f"Missing or unrecognized contribution tooltip for {day}")
            if not 0 <= level < len(COLORS):
                raise ValueError(f"Unexpected heatmap level for {day}: {level}")
            days[day] = (count, level)
        if not 360 <= len(days) <= 371 or (max(days) - min(days)).days + 1 != len(days):
            raise ValueError("GitHub did not return a complete calendar. The previous card was kept.")
        return days


def fetch_days(username):
    request = Request(
        f"https://github.com/users/{username}/contributions",
        headers={"User-Agent": "GitHub profile artwork", "Accept-Language": "en"},
    )
    with urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8")
    parser = ContributionCalendar()
    parser.feed(html)
    return parser.days()


def render(days):
    first, last = min(days), max(days)
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    total = sum(count for count, _ in days.values())
    active = sum(count > 0 for count, _ in days.values())
    busiest = max(count for count, _ in days.values())
    parts = []
    for day, (_, level) in sorted(days.items()):
        week, weekday = divmod((day - start).days, 7)
        x = 37 + week * 12
        y = 101 + weekday * 12
        parts.append(f'<rect x="{x}" y="{y}" width="9" height="9" rx="2" fill="{COLORS[level]}"/>')
        if day.day == 1:
            month = calendar.month_abbr[day.month]
            parts.append(f'<text x="{x}" y="89">{month}</text>')

    legend = []
    for index, color in enumerate(COLORS):
        legend.append(f'<rect x="{110 + 13 * index}" y="194" width="10" height="10" rx="2" fill="{color}"/>')
    summary = escape(f"{total:,} contributions across {active} active days. Busiest day: {busiest}.")
    graphic = "\n    ".join(parts)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 236" role="img" aria-labelledby="title summary">
  <title id="title">GitHub activity in the last year</title>
  <desc id="summary">{summary}</desc>
  <rect x="1" y="1" width="918" height="234" rx="20" fill="#111a2f" stroke="#4b776e" stroke-width="2"/>
  <g font-family="system-ui, sans-serif">
    <text x="36" y="49" fill="#f4f8ff" font-size="30" font-weight="700">GitHub activity</text>
    <text x="883" y="47" text-anchor="end" fill="#b8c9e4" font-size="15">Through {last:%d %b %Y}</text>
    <g fill="#b8c9e4" font-family="ui-monospace, monospace" font-size="11">
    {graphic}
    </g>
    <text x="36" y="204" fill="#b8c9e4" font-size="13">Fewer</text>
    {''.join(legend)}
    <text x="181" y="204" fill="#b8c9e4" font-size="13">More</text>
    <path d="M705 75v129" stroke="#38566a"/>
    <text x="729" y="110" fill="#76e6cb" font-size="34" font-weight="750">{total:,}</text>
    <text x="729" y="133" fill="#ecf3ff" font-size="17">contributions</text>
    <text x="729" y="165" fill="#b8c9e4" font-size="16">{active} active days</text>
    <text x="729" y="192" fill="#b8c9e4" font-size="16">Best day · {busiest}</text>
  </g>
</svg>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("username")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", args.username):
        parser.error("Enter a valid GitHub username.")
    days = fetch_days(args.username)
    CARD_PATH.write_text(render(days), encoding="utf-8")


if __name__ == "__main__":
    main()
