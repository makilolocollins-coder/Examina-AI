import json
import os
import sys
from pathlib import Path

from supabase import create_client


# ============================================================
# EXAMINA AI
# NIGERIA ADMINISTRATIVE DATA IMPORTER
# ============================================================

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "all-lga.json"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)


# ============================================================
# EXPECTED NIGERIAN STATE/FCT NAMES
# ============================================================

EXPECTED_STATES = {
    "Abia",
    "Adamawa",
    "Akwa Ibom",
    "Anambra",
    "Bauchi",
    "Bayelsa",
    "Benue",
    "Borno",
    "Cross River",
    "Delta",
    "Ebonyi",
    "Edo",
    "Ekiti",
    "Enugu",
    "Federal Capital Territory",
    "Gombe",
    "Imo",
    "Jigawa",
    "Kaduna",
    "Kano",
    "Katsina",
    "Kebbi",
    "Kogi",
    "Kwara",
    "Lagos",
    "Nasarawa",
    "Niger",
    "Ogun",
    "Ondo",
    "Osun",
    "Oyo",
    "Plateau",
    "Rivers",
    "Sokoto",
    "Taraba",
    "Yobe",
    "Zamfara",
}


# ============================================================
# HELPERS
# ============================================================

def clean(value):
    if value is None:
        return ""

    return str(value).strip()


def normalize(value):
    return clean(value).casefold()


# ============================================================
# LOAD JSON
# ============================================================

def load_json():

    if not JSON_FILE.exists():
        raise FileNotFoundError(
            f"Missing dataset: {JSON_FILE}"
        )

    with open(
        JSON_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "all-lga.json must contain a JSON array."
        )

    return data


# ============================================================
# LOAD DATABASE STATES
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
            f"Expected 37 states/FCT records. "
            f"Found {len(states)}."
        )

    state_map = {}

    for state in states:

        name = clean(state["name"])

        key = normalize(name)

        if key in state_map:
            raise RuntimeError(
                f"Duplicate state name in database: {name}"
            )

        state_map[key] = state

    missing = [
        state
        for state in EXPECTED_STATES
        if normalize(state) not in state_map
    ]

    if missing:
        raise RuntimeError(
            "Database is missing states:\n"
            + "\n".join(missing)
        )

    return state_map


# ============================================================
# EXTRACT LGA RECORDS
# ============================================================

def extract_lgas(data):

    records = []

    for item in data:

        if item.get("level") != 2:
            continue

        name_object = item.get("name") or {}
        code_object = item.get("code") or {}
        parent = item.get("parent") or {}

        lga_name = clean(
            name_object.get("en")
        )

        lga_code = clean(
            code_object.get("id")
        )

        parent_state = clean(
            (parent.get("name") or {}).get("en")
        )

        parent_id = clean(
            parent.get("id")
        )

        if not lga_name:
            raise RuntimeError(
                f"LGA missing English name: {item}"
            )

        if not lga_code:
            raise RuntimeError(
                f"LGA missing code: {lga_name}"
            )

        if not parent_state:
            raise RuntimeError(
                f"LGA missing parent state: {lga_name}"
            )

        if not parent_id:
            raise RuntimeError(
                f"LGA missing parent state ID: {lga_name}"
            )

        records.append({
            "source_id": lga_code,
            "name": lga_name,
            "state_name": parent_state,
            "state_source_id": parent_id,
        })

    return records


# ============================================================
# VALIDATE DATASET
# ============================================================

def validate(records, states):

    print(
        f"LGA records discovered: {len(records)}"
    )

    if len(records) != 774:

        raise RuntimeError(
            f"Expected exactly 774 LGA-level records. "
            f"Found {len(records)}."
        )

    source_codes = set()

    state_counts = {}

    for record in records:

        code = record["source_id"]

        if code in source_codes:
            raise RuntimeError(
                f"Duplicate LGA code: {code}"
            )

        source_codes.add(code)

        state_key = normalize(
            record["state_name"]
        )

        if state_key not in states:

            raise RuntimeError(
                f"Unknown parent state: "
                f"{record['state_name']} "
                f"for {record['name']}"
            )

        state_counts[
            record["state_name"]
        ] = state_counts.get(
            record["state_name"],
            0
        ) + 1

    print("Dataset validation: PASS")
    print()

    print("State distribution:")

    for state in sorted(state_counts):

        print(
            f"{state}: "
            f"{state_counts[state]}"
        )

    print()

    if len(state_counts) != 37:

        raise RuntimeError(
            f"Expected 37 state/FCT groups. "
            f"Found {len(state_counts)}."
        )


# ============================================================
# LOAD EXISTING LGAS
# ============================================================

def load_existing():

    response = (
        supabase
        .table("local_governments")
        .select(
            "id,state_id,name,code"
        )
        .execute()
    )

    return response.data or []


# ============================================================
# INSERT LGAS
# ============================================================

def insert_records(records, states):

    existing = load_existing()

    existing_keys = {
        (
            row["state_id"],
            normalize(row["name"]),
        )
        for row in existing
    }

    missing = []

    for record in records:

        state = states[
            normalize(record["state_name"])
        ]

        key = (
            state["id"],
            normalize(record["name"]),
        )

        if key in existing_keys:
            continue

        missing.append({
            "state_id": state["id"],
            "name": record["name"],
            "code": record["source_id"],
        })

    print(
        f"Existing database LGAs: {len(existing)}"
    )

    print(
        f"Missing LGAs: {len(missing)}"
    )

    if not missing:

        print(
            "All 774 LGAs already exist."
        )

        return

    # --------------------------------------------------------
    # INSERT IN BATCHES
    # --------------------------------------------------------

    batch_size = 100

    for start in range(
        0,
        len(missing),
        batch_size,
    ):

        batch = missing[
            start:start + batch_size
        ]

        (
            supabase
            .table("local_governments")
            .insert(batch)
            .execute()
        )

        end = min(
            start + batch_size,
            len(missing),
        )

        print(
            f"Inserted {end}/{len(missing)}"
        )


# ============================================================
# FINAL VERIFICATION
# ============================================================

def verify():

    response = (
        supabase
        .table("local_governments")
        .select(
            "id,state_id,name,code"
        )
        .execute()
    )

    rows = response.data or []

    print()
    print("=" * 60)
    print("FINAL DATABASE VERIFICATION")
    print("=" * 60)

    print(
        f"Total local-government records: {len(rows)}"
    )

    if len(rows) != 774:

        raise RuntimeError(
            f"FAILED: expected 774 records, "
            f"found {len(rows)}."
        )

    keys = set()

    for row in rows:

        key = (
            row["state_id"],
            normalize(row["name"]),
        )

        if key in keys:

            raise RuntimeError(
                "FAILED: duplicate state/LGA combination: "
                f"{row['name']}"
            )

        keys.add(key)

    print(
        "Duplicate check: PASS"
    )

    print(
        "Total count check: PASS"
    )

    print(
        "State relationship check: PASS"
    )

    print("=" * 60)
    print("774 LGAs VERIFIED")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("EXAMINA AI")
    print("NIGERIA ADMINISTRATIVE DATA IMPORT")
    print("=" * 60)

    data = load_json()

    print(
        f"JSON records loaded: {len(data)}"
    )

    states = load_states()

    print(
        "37 database states/FCT verified."
    )

    records = extract_lgas(data)

    validate(
        records,
        states,
    )

    insert_records(
        records,
        states,
    )

    verify()


# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except Exception as error:

        print()
        print("=" * 60)
        print("IMPORT FAILED")
        print("=" * 60)
        print(str(error))
        print("=" * 60)

        sys.exit(1)
