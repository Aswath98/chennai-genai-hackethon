#!/usr/bin/env python3
"""Literacy Agent

Reads the first column of an input Excel file (place names) and attempts to scrape
the literacy rate for each place from Wikipedia pages.

Usage:
    python literacy_agent.py --input input.xlsx --output output_with_literacy.xlsx

Notes:
- The script searches Wikipedia for the place, fetches the page HTML, and looks for
  literacy values in the infobox (rows with 'Literacy') or elsewhere on the page.
"""
from __future__ import annotations

import argparse
import time
import urllib.parse
import re
from typing import Optional, Dict, Any, List

import requests
from bs4 import BeautifulSoup
import pandas as pd

WIKI_SEARCH_URL = "https://en.wikipedia.org/w/api.php"
WIKI_BASE = "https://en.wikipedia.org/wiki/"


def wiki_search(title: str) -> Optional[Dict[str, Any]]:
    params = {
        "action": "query",
        "list": "search",
        "srsearch": title,
        "format": "json",
        "srlimit": 1,
    }
    r = requests.get(WIKI_SEARCH_URL, params=params, timeout=30, headers={"User-Agent": "literacy-agent/1.0"})
    r.raise_for_status()
    data = r.json()
    items = data.get("query", {}).get("search", [])
    if not items:
        return None
    return items[0]


def fetch_wiki_html(page_title: str) -> Optional[str]:
    url = WIKI_BASE + urllib.parse.quote(page_title.replace(" ", "_"))
    r = requests.get(url, timeout=30, headers={"User-Agent": "literacy-agent/1.0"})
    if r.status_code != 200:
        return None
    return r.text


def extract_percentage(text: str) -> Optional[float]:
    # find first percentage like 74.04% or 74%
    m = re.search(r"(\d{1,3}(?:\.\d+)?)\s*%", text)
    if not m:
        return None
    try:
        return float(m.group(1))
    except Exception:
        return None


def parse_infobox_for_literacy(soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
    # infobox tables usually have class 'infobox'
    table = soup.find("table", class_=lambda c: c and "infobox" in c)
    if not table:
        return None

    for tr in table.find_all("tr"):
        th = tr.find("th")
        td = tr.find("td")
        if not th or not td:
            continue
        label = th.get_text(separator=" ", strip=True).lower()
        if "literacy" in label or "literates" in label:
            text = td.get_text(separator=" ", strip=True)
            pct = extract_percentage(text)
            year = None
            # try to find a year in parentheses near the value
            ym = re.search(r"\((\d{4})\)", text)
            if ym:
                year = int(ym.group(1))
            return {"literacy": pct, "year": year, "source": "wikipedia-infobox", "raw": text}

    return None


def parse_body_for_literacy(soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
    # search for the word 'literacy' in paragraphs and try to extract a percentage nearby
    for p in soup.find_all(["p", "li"]):
        txt = p.get_text(" ", strip=True)
        if "literacy" in txt.lower() or "literate" in txt.lower():
            pct = extract_percentage(txt)
            year = None
            ym = re.search(r"(\d{4})", txt)
            if ym:
                year = int(ym.group(1))
            if pct is not None:
                return {"literacy": pct, "year": year, "source": "wikipedia-body", "raw": txt}
    return None


def get_literacy_for_place(place: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {"input_name": place, "wiki_title": None, "literacy": None, "literacy_year": None, "notes": None}
    try:
        search = wiki_search(place)
    except Exception as e:
        out["notes"] = f"search-error: {e}"
        return out

    if not search:
        out["notes"] = "no-wikipedia-search-result"
        return out

    title = search.get("title")
    out["wiki_title"] = title

    # fetch HTML
    time.sleep(0.1)
    html = fetch_wiki_html(title)
    if not html:
        out["notes"] = "failed-fetch-page"
        return out

    soup = BeautifulSoup(html, "lxml")

    # Try infobox first
    try:
        info = parse_infobox_for_literacy(soup)
    except Exception:
        info = None

    if info and info.get("literacy") is not None:
        out["literacy"] = info.get("literacy")
        out["literacy_year"] = info.get("year")
        out["notes"] = info.get("source")
        return out

    # fallback: parse body
    try:
        body = parse_body_for_literacy(soup)
    except Exception:
        body = None

    if body and body.get("literacy") is not None:
        out["literacy"] = body.get("literacy")
        out["literacy_year"] = body.get("year")
        out["notes"] = body.get("source")
        return out

    out["notes"] = "no-literacy-found"
    return out


def process_excel(input_path: str, output_path: str, sheet_name: Optional[str] = None) -> None:
    df = pd.read_excel(input_path, sheet_name=sheet_name, engine="openpyxl")
    if isinstance(df, dict):
        df = next(iter(df.values()))

    if df.shape[1] < 1:
        raise ValueError("Input Excel must have at least one column with place names")

    first_col = df.columns[0]
    places = df[first_col].astype(str).fillna("")

    results: List[Dict[str, Any]] = []
    total = len(places)
    for idx, place in enumerate(places, start=1):
        if not place.strip():
            results.append({"input_name": place, "wiki_title": None, "literacy": None, "literacy_year": None, "notes": "empty-input"})
            continue
        print(f"[{idx}/{total}] Looking up literacy: {place}")
        try:
            res = get_literacy_for_place(place)
        except Exception as e:
            res = {"input_name": place, "wiki_title": None, "literacy": None, "literacy_year": None, "notes": f"error: {e}"}
        results.append(res)

    res_df = pd.DataFrame(results)
    out_df = pd.concat([df.reset_index(drop=True), res_df.drop(columns=["input_name"])], axis=1)
    out_df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Wrote results to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape literacy rates for places using Wikipedia")
    parser.add_argument("--input", "-i", required=True, help="Input Excel file path (first column = place names)")
    parser.add_argument("--output", "-o", default="output_with_literacy.xlsx", help="Output Excel file path")
    parser.add_argument("--sheet", "-s", default=None, help="Optional sheet name or index")
    args = parser.parse_args()
    process_excel(args.input, args.output, sheet_name=args.sheet)


if __name__ == "__main__":
    main()
