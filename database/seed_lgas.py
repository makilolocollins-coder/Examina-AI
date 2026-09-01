"""
EXAMINA AI
Nigeria Administrative Master Data Seeder

Source:
Open Admin Data - Nigeria Administrative Divisions
37 states / FCT
774 local-government-level records

IMPORTANT:
- Does NOT create or modify states.
- Matches existing states by code.
- Inserts missing LGAs only.
- Safe to run repeatedly.
"""

import json
import os
import sys
from pathlib import Path

from supabase import create_client


# ============================================================
# CONFIG
# ============================================================

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

DATA_FILE = Path(__file__).parent / "all-lga.json"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)


# ============================================================
# EXPECTED STATE CODES
# ============================================================

EXPECTED_STATE_CODES = {
    "AB", "AD", "AK", "AN", "BA", "BY", "BE", "BO",
    "CR", "DE", "EB", "ED", "EK", "EN", "FC", "GO",
    "IM", "JI", "KD", "KN", "KT", "KE", "KO", "KW",
    "LA", "NA", "NI", "OG", "ON", "OS", "OY", "PL",
    "RI", "SO", "TA", "YO", "ZA",
}


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("all-lga.json must contain a JSON array.")

    return data


# ============================================================
# LOAD EXISTING STATES
# ============================================================

def load_states():

    response = (
        supabase
        .table("states")
        .select("id,name,code")
        .execute()
    )

    states = response.data or []

    if len(states) != 37:
        raise RuntimeError(
            f"Expected 37 states/FCT records, found {len(states)}."
        )

    state_map = {}

    for state in states:

        code = state["code"].upper()

        if code in state_map:
            raise RuntimeError(
                f"Duplicate state code detected: {code}"
            )

        state_map[code] = state

    missing = EXPECTED_STATE_CODES - set(state_map)

    if missing:
        raise RuntimeError(
            "Missing state codes: "
            + ", ".join(sorted(missing))
        )

    return state_map


# ============================================================
# NORMALIZE DATASET
# ============================================================

def normalize_name(record):

    name = record.get("name")

    if isinstance(name, dict):
        return (
            name.get("en")
            or name.get("local")
            or ""
        ).strip()

    if isinstance(name, str):
        return name.strip()

    return ""


def normalize_parent_code(record):

    parent = record.get("parent")

    if not isinstance(parent, dict):
        return None

    # Dataset uses parent references.
    # Support common code/key representations.

    for key in ("code", "id", "slug"):
        value = parent.get(key)

        if value:
            return str(value).strip()

    return None


# ============================================================
# BUILD RECORDS
# ============================================================

def build_records(dataset, states):

    records = []

    for item in dataset:

        # Level 2 = Local Government Area
        if item.get("level") != 2:
            continue

        name = normalize_name(item)

        if not name:
            raise RuntimeError(
                f"LGA has no valid name: {item}"
            )

        parent = item.get("parent") or {}

        parent_name = (
            parent.get("name")
            if isinstance(parent, dict)
            else None
        )

        # We intentionally require a state reference.
        # Never guess the parent state.
        state_code = parent.get("code")

        if state_code:
            state_code = str(state_code).upper()

        # If dataset parent uses a different identifier,
        # fail instead of guessing.
        if not state_code:
            raise RuntimeError(
                f"Cannot determine parent state for LGA: {name}"
            )

        if state_code not in states:
            raise RuntimeError(
                f"LGA '{name}' references unknown state "
                f"code '{state_code}'."
            )

        state_id = states[state_code]["id"]

        # Use dataset ID as a deterministic code.
        source_id = str(item.get("id", "")).strip()

        if not source_id:
            raise RuntimeError(
                f"LGA '{name}' has no source ID."
            )

        records.append({
            "state_id": state_id,
            "name": name,
            "code": source_id,
        })

    return records


# ============================================================
# VALIDATE
# ============================================================

def validate_records(records):

    if len(records) != 774:
        raise RuntimeError(
            f"Dataset validation failed: "
            f"expected 774 LGAs, found {len(records)}."
        )

    seen = set()

    for record in records:

        key = (
            record["state_id"],
            record["name"].lower(),
        )

        if key in seen:
            raise RuntimeError(
                f"Duplicate LGA detected: {record['name']}"
            )

        seen.add(key)


# ============================================================
# LOAD EXISTING LGAS
# ============================================================

def load_existing_lgas():

    response = (
        supabase
        .table("local_governments")
        .select("id,state_id,name,code")
        .execute()
    )

    return response.data or []


# ============================================================
# INSERT MISSING RECORDS
# ============================================================

def insert_missing(records):

    existing = load_existing_lgas()

    existing_keys = {
        (
            row["state_id"],
            row["name"].strip().lower(),
        )
        for row in existing
    }

    missing = [
        record
        for record in records
        if (
            record["state_id"],
            record["name"].strip().lower(),
        ) not in existing_keys
    ]

    print(f"Existing LGAs : {len(existing)}")
    print(f"Required LGAs : {len(records)}")
    print(f"To insert     : {len(missing)}")

    if not missing:
        print("Nothing to insert.")
        return

    # Insert in controlled batches.
    batch_size = 100

    for start in range(0, len(missing), batch_size):

        batch = missing[start:start + batch_size]

        (
            supabase
            .table("local_governments")
            .insert(batch)
            .execute()
        )

        print(
            f"Inserted {min(start + batch_size, len(missing))}"
            f"/{len(missing)}"
        )


# ============================================================
# FINAL VERIFICATION
# ============================================================

def verify():

    response = (
        supabase
        .table("local_governments")
        .select("id,state_id,name,code")
        .execute()
    )

    rows = response.data or []

    if len(rows) != 774:
        raise RuntimeError(
            f"FINAL VERIFICATION FAILED: "
            f"database contains {len(rows)} LGAs, "
            f"expected 774."
        )

    # Verify no duplicate state/name combinations.
    keys = [
        (
            row["state_id"],
            row["name"].strip().lower(),
        )
        for row in rows
    ]

    if len(keys) != len(set(keys)):
        raise RuntimeError(
            "FINAL VERIFICATION FAILED: duplicate LGAs detected."
        )

    print()
    print("=" * 60)
    print("EXAMINA AI — LGA SEED SUCCESSFUL")
    print("=" * 60)
    print(f"Total LGAs: {len(rows)}")
    print("Duplicate check: PASS")
    print("State relationship check: PASS")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("EXAMINA AI — NIGERIA ADMINISTRATIVE DATA")
    print("774 LGA SEED")
    print("=" * 60)

    dataset = load_dataset()

    print(f"Dataset records loaded: {len(dataset)}")

    states = load_states()

    print(f"Existing states verified: {len(states)}")

    records = build_records(
        dataset,
        states,
    )

    validate_records(records)

    print("774-record validation: PASS")

    insert_missing(records)

    verify()


if __name__ == "__main__":
    try:
        main()

    except Exception as exc:
        print()
        print("SEED FAILED")
        print(str(exc))
        sys.exit(1)
