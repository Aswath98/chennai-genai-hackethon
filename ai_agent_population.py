#!/usr/bin/env python3
"""AI Agent: Populate populations for place names in an Excel file.

Reads the first column of the input Excel file (first sheet) and tries to retrieve
the most recent population for each place using Wikidata (property P1082).

Usage:
    python ai_agent_population.py --input input.xlsx --output output.xlsx

If `--input` is just a filename, it will be searched relative to the current working directory.
"""
from __future__ import annotations

import argparse
import time
from typing import Optional, Dict, Any, List

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

WIKIDATA_SEARCH_URL = "https://www.wikidata.org/w/api.php"
WIKIDATA_GETCLAIMS_URL = "https://www.wikidata.org/w/api.php"
ELECTION_SITE_URL = "https://www.elections.tn.gov.in/ACwise_Gendercount_06012025.aspx"

# cached election mapping: normalized_name -> {"name": original, "population": int}
ELECTION_DATA: dict = {}


def normalize_name(s: str) -> str:
    s2 = s or ""
    s2 = s2.strip().lower()
    s2 = re.sub(r"\s+", " ", s2)
    s2 = re.sub(r"[^a-z0-9 ]", "", s2)
    return s2


def load_election_data() -> None:
    """Fetch and parse the Tamil Nadu election page and populate ELECTION_DATA.

    This function is defensive because the website structure may change. It tries to
    find table rows and heuristically extract the constituency name and total electors.
    """
    global ELECTION_DATA
    if ELECTION_DATA:
        return
    try:
        r = requests.get(ELECTION_SITE_URL, timeout=30)
        r.raise_for_status()
    except Exception:
        return

    soup = BeautifulSoup(r.content, "lxml")
    tables = soup.find_all("table")
    rows_parsed = 0
    for table in tables:
        for tr in table.find_all("tr"):
            cells = [td.get_text(separator=" ", strip=True) for td in tr.find_all(["td", "th"])]
            if not cells:
                continue

            # ignore header rows that are clearly titles
            # attempt to find the name cell (non-numeric) and numeric cells
            nums = []
            name_parts = []
            for c in cells:
                # remove commas and check if numeric
                c_stripped = c.replace(",", "").replace(" ", "")
                if re.fullmatch(r"\d+", c_stripped):
                    try:
                        nums.append(int(c.replace(",", "")))
                    except Exception:
                        pass
                else:
                    # not purely numeric — likely contains name or header
                    name_parts.append(c)

            # heuristic: if we have at least one numeric value and some name parts
            if nums and name_parts:
                # build a name candidate from name_parts by picking the longest piece
                name_candidate = max(name_parts, key=len)
                norm = normalize_name(name_candidate)
                # prefer explicit total if present (often max of numeric columns)
                total = max(nums) if nums else None
                if total is not None:
                    ELECTION_DATA[norm] = {"name": name_candidate, "population": int(total)}
                    rows_parsed += 1

    # also attempt to parse any lists with newline-separated entries
    if not ELECTION_DATA:
        text = soup.get_text("\n")
        for line in text.splitlines():
            parts = line.split()
            if not parts:
                continue
            # if line ends with a number, assume it's "Name ... 12345"
            last = parts[-1].replace(",", "")
            if re.fullmatch(r"\d+", last) and len(parts) > 1:
                name = " ".join(parts[:-1])
                norm = normalize_name(name)
                ELECTION_DATA[norm] = {"name": name, "population": int(last)}
                rows_parsed += 1


def election_lookup(place: str) -> Optional[Dict[str, Any]]:
    load_election_data()
    if not ELECTION_DATA:
        return None
    norm_place = normalize_name(place)
    # exact match
    if norm_place in ELECTION_DATA:
        d = ELECTION_DATA[norm_place]
        return {"population": d["population"], "year": 2025}

    # try partial matches: name contains place or place contains name
    for k, v in ELECTION_DATA.items():
        if norm_place == k or norm_place in k or k in norm_place:
            return {"population": v["population"], "year": 2025}

    # try more permissive matching by words
    place_words = set(norm_place.split())
    best = None
    best_score = 0
    for k, v in ELECTION_DATA.items():
        ks = set(k.split())
        score = len(place_words & ks)
        if score > best_score and score > 0:
            best_score = score
            best = v
    if best:
        return {"population": best["population"], "year": 2025}

    return None


def search_wikidata_entity(label: str) -> Optional[Dict[str, Any]]:
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": label,
        "type": "item",
        "limit": 1,
    }
    r = requests.get(WIKIDATA_SEARCH_URL, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    results = data.get("search", [])
    if not results:
        return None
    return results[0]


def get_population_from_claims(entity_id: str) -> Optional[Dict[str, Any]]:
    params = {
        "action": "wbgetclaims",
        "entity": entity_id,
        "property": "P1082",
        "format": "json",
    }
    r = requests.get(WIKIDATA_GETCLAIMS_URL, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    claims = data.get("claims", {}).get("P1082", [])
    if not claims:
        return None

    # Choose the claim with the most recent point in time (qualifier P585) if available,
    # otherwise pick the first claim.
    best_claim = None
    best_year = None

    for claim in claims:
        mainsnak = claim.get("mainsnak", {})
        datavalue = mainsnak.get("datavalue", {})
        if not datavalue:
            continue
        value = datavalue.get("value", {})
        # numeric value can be under 'amount'
        amount = None
        if isinstance(value, dict) and "amount" in value:
            try:
                amount = float(value["amount"])
            except Exception:
                amount = None

        # check qualifiers for point in time (P585)
        qualifiers = claim.get("qualifiers", {})
        year = None
        if "P585" in qualifiers:
            # pick the first qualifier's datavalue time
            try:
                q = qualifiers["P585"][0]
                snak = q.get("datavalue", {}).get("value", {})
                time_str = snak.get("time")
                # time format: "+YYYY-MM-DDT00:00:00Z"
                if time_str:
                    # extract year as int
                    year = int(time_str.lstrip("+").split("-")[0])
            except Exception:
                year = None

        # prefer claim with later year
        if year is not None:
            if best_year is None or year > best_year:
                best_claim = claim
                best_year = year
        else:
            if best_claim is None:
                best_claim = claim

    if best_claim is None:
        return None

    mainsnak = best_claim.get("mainsnak", {})
    datavalue = mainsnak.get("datavalue", {})
    value = datavalue.get("value", {})
    amount = None
    if isinstance(value, dict) and "amount" in value:
        try:
            amount = float(value["amount"])
        except Exception:
            amount = None

    result: Dict[str, Any] = {"population": None, "year": None}
    result["population"] = int(amount) if amount is not None else None
    result["year"] = best_year
    return result


def get_population_for_place(place: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {"input_name": place, "wikidata_id": None, "wikidata_label": None, "population": None, "population_year": None, "notes": None}
    # First try the Tamil Nadu election site (AC-wise gender count)
    try:
        elect = election_lookup(place)
    except Exception as e:
        elect = None

    if elect:
        out["population"] = elect.get("population")
        out["population_year"] = elect.get("year")
        out["notes"] = "election-site"
        return out

    # Fallback to Wikidata
    try:
        search = search_wikidata_entity(place)
    except Exception as e:
        out["notes"] = f"search-error: {e}"
        return out

    if not search:
        out["notes"] = "no-wikidata-entity-found"
        return out

    entity_id = search.get("id")
    label = search.get("label") or search.get("display") or search.get("description")
    out["wikidata_id"] = entity_id
    out["wikidata_label"] = search.get("label") or search.get("title")

    # polite throttle
    time.sleep(0.1)

    try:
        pop = get_population_from_claims(entity_id)
    except Exception as e:
        out["notes"] = f"claims-error: {e}"
        return out

    if not pop:
        out["notes"] = "no-population-found"
        return out

    out["population"] = pop.get("population")
    out["population_year"] = pop.get("year")
    if out["population"] is None:
        out["notes"] = "population-parsing-failed"
    else:
        out["notes"] = "wikidata"
    return out


def process_excel(input_path: str, output_path: str, sheet_name: Optional[str] = None) -> None:
    df = pd.read_excel(input_path, sheet_name=sheet_name, engine="openpyxl")

    # If multiple sheets were returned (sheet_name=None), pick the first sheet's DataFrame
    if isinstance(df, dict):
        # take first sheet
        first_sheet_key = next(iter(df.keys()))
        df = df[first_sheet_key]

    # pick first column as place names
    if df.shape[1] < 1:
        raise ValueError("Input Excel must have at least one column with place names")

    first_col = df.columns[0]
    places = df[first_col].astype(str).fillna("")

    results: List[Dict[str, Any]] = []
    total = len(places)
    for idx, place in enumerate(places, start=1):
        if not place.strip():
            results.append({"input_name": place, "wikidata_id": None, "wikidata_label": None, "population": None, "population_year": None, "notes": "empty-input"})
            continue
        print(f"[{idx}/{total}] Querying: {place}")
        res = get_population_for_place(place)
        results.append(res)

    res_df = pd.DataFrame(results)

    # join results to original df (preserve original columns)
    out_df = pd.concat([df.reset_index(drop=True), res_df.drop(columns=["input_name"])], axis=1)

    out_df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Wrote results to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Populate populations for places from an Excel file using Wikidata")
    parser.add_argument("--input", "-i", required=True, help="Input Excel file path (e.g., input.xlsx)")
    parser.add_argument("--output", "-o", default="output_with_population.xlsx", help="Output Excel file path")
    parser.add_argument("--sheet", "-s", default=None, help="Optional sheet name or index")
    args = parser.parse_args()

    process_excel(args.input, args.output, sheet_name=args.sheet)


if __name__ == "__main__":
    main()
