# ============================================================
# EXAMINA AI
# NIGERIA ADMINISTRATIVE DATA SEEDER
# ============================================================

import json
import sys
from pathlib import Path

import streamlit as st
from supabase import create_client


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "all-lga.json"


# ============================================================
# SUPABASE CONNECTION
# ============================================================

def get_supabase_client():

    try:

        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]

    except KeyError as error:

        raise RuntimeError(
            "Missing Streamlit Secret. "
            "Required secrets are: "
            "SUPABASE_URL and SUPABASE_KEY."
        ) from error

    if not url:

        raise RuntimeError(
            "SUPABASE_URL is empty."
        )

    if not key:

        raise RuntimeError(
            "SUPABASE_KEY is empty."
        )

    try:

        return create_client(
            url,
            key,
        )

    except Exception as error:

        raise RuntimeError(
            f"Unable to connect to Supabase: {error}"
        ) from error


supabase = get_supabase_client()


# ============================================================
# EXPECTED STATES
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
            f"Missing file:\n{JSON_FILE}\n"
            "Make sure all-lga.json is in the "
            "same folder as seedlga.py."
        )

    print(f"Loading: {JSON_FILE}")

    try:

        with open(
            JSON_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

    except json.JSONDecodeError as error:

        raise RuntimeError(
            f"Invalid JSON file:\n{error}"
        )

    if not isinstance(data, list):

        raise RuntimeError(
            "all-lga.json must contain a JSON array."
        )

    print(
        f"JSON records loaded: {len(data)}"
    )

    return data


# ============================================================
# LOAD STATES
# ============================================================

def load_states():

    print()
    print("Loading states from Supabase...")

    response = (
        supabase
        .table("states")
        .select("id,name,code")
        .execute()
    )

    states = response.data or []

    print(
        f"Database states found: {len(states)}"
    )

    if len(states) != 37:

        raise RuntimeError(
            f"Expected 37 states/FCT records, "
            f"but found {len(states)}."
        )

    state_map = {}

    for state in states:

        name = clean(
            state.get("name")
        )

        if not name:

            raise RuntimeError(
                "A state record has no name."
            )

        key = normalize(name)

        if key in state_map:

            raise RuntimeError(
                f"Duplicate state: {name}"
            )

        state_map[key] = state

    missing = []

    for expected in EXPECTED_STATES:

        if normalize(expected) not in state_map:

            missing.append(expected)

    if missing:

        raise RuntimeError(
            "Missing states/FCT:\n"
            + "\n".join(sorted(missing))
        )

    print("37 states/FCT verified.")

    return state_map


# ============================================================
# EXTRACT LGAS FROM JSON
# ============================================================

def extract_lgas(data):

    print()
    print("Extracting LGAs from JSON...")

    records = []

    for item in data:

        # ----------------------------------------------------
        # ONLY LEVEL 2 = LGA
        # ----------------------------------------------------

        if item.get("level") != 2:
            continue

        # ----------------------------------------------------
        # NAME
        # ----------------------------------------------------

        name_object = item.get("name") or {}

        if isinstance(name_object, dict):

            lga_name = clean(
                name_object.get("en")
                or name_object.get("name")
            )

        else:

            lga_name = clean(name_object)

        # ----------------------------------------------------
        # CODE
        # ----------------------------------------------------

        code_object = item.get("code") or {}

        if isinstance(code_object, dict):

            lga_code = clean(
                code_object.get("id")
                or code_object.get("code")
            )

        else:

            lga_code = clean(code_object)

        # ----------------------------------------------------
        # PARENT STATE
        # ----------------------------------------------------

        parent = item.get("parent") or {}

        if not isinstance(parent, dict):

            parent = {}

        parent_name = parent.get("name") or {}

        if isinstance(parent_name, dict):

            state_name = clean(
                parent_name.get("en")
                or parent_name.get("name")
            )

        else:

            state_name = clean(parent_name)

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not lga_name:

            raise RuntimeError(
                f"LGA without name:\n{item}"
            )

        if not lga_code:

            raise RuntimeError(
                f"LGA without code: {lga_name}"
            )

        if not state_name:

            raise RuntimeError(
                f"LGA without parent state: "
                f"{lga_name}"
            )

        records.append({
            "name": lga_name,
            "code": lga_code,
            "state_name": state_name,
        })

    print(
        f"LGA records discovered: {len(records)}"
    )

    return records


# ============================================================
# VALIDATE JSON
# ============================================================

def validate_lgas(records, states):

    print()
    print("Validating LGA dataset...")

    if len(records) != 774:

        raise RuntimeError(
            f"Expected 774 LGAs, "
            f"found {len(records)}."
        )

    codes = set()

    state_counts = {}

    for record in records:

        code = record["code"]

        if code in codes:

            raise RuntimeError(
                f"Duplicate LGA code: {code}"
            )

        codes.add(code)

        state_key = normalize(
            record["state_name"]
        )

        if state_key not in states:

            raise RuntimeError(
                f"Unknown state: "
                f"{record['state_name']} "
                f"for LGA {record['name']}"
            )

        state_counts[state_key] = (
            state_counts.get(state_key, 0) + 1
        )

    if len(state_counts) != 37:

        raise RuntimeError(
            f"Expected 37 state groups, "
            f"found {len(state_counts)}."
        )

    print("774 LGA count: PASS")
    print("Duplicate code check: PASS")
    print("State relationship check: PASS")
    print("Dataset validation: PASS")


# ============================================================
# LOAD EXISTING LGAS
# ============================================================

def load_existing_lgas():

    print()
    print("Checking existing LGAs in Supabase...")

    response = (
        supabase
        .table("local_governments")
        .select(
            "id,state_id,name,code"
        )
        .execute()
    )

    existing = response.data or []

    print(
        f"Existing LGAs: {len(existing)}"
    )

    return existing


# ============================================================
# PREPARE INSERTS
# ============================================================

def prepare_inserts(
    records,
    states,
    existing,
):

    existing_keys = set()

    for row in existing:

        state_id = row.get("state_id")
        name = normalize(
            row.get("name")
        )

        if state_id and name:

            existing_keys.add(
                (state_id, name)
            )

    missing = []

    for record in records:

        state = states[
            normalize(
                record["state_name"]
            )
        ]

        state_id = state["id"]

        key = (
            state_id,
            normalize(record["name"]),
        )

        if key in existing_keys:

            continue

        missing.append({
            "state_id": state_id,
            "name": record["name"],
            "code": record["code"],
        })

    return missing


# ============================================================
# INSERT LGAS
# ============================================================

def insert_lgas(
    records,
    states,
):

    existing = load_existing_lgas()

    missing = prepare_inserts(
        records,
        states,
        existing,
    )

    print()
    print(
        f"LGAs to insert: {len(missing)}"
    )

    if not missing:

        print(
            "All 774 LGAs already exist."
        )

        return

    batch_size = 100

    total = len(missing)

    print()
    print("Starting LGA insertion...")

    for start in range(
        0,
        total,
        batch_size,
    ):

        batch = missing[
            start:start + batch_size
        ]

        try:

            (
                supabase
                .table("local_governments")
                .insert(batch)
                .execute()
            )

        except Exception as error:

            raise RuntimeError(
                f"Failed inserting batch "
                f"{start + 1}-"
                f"{min(start + batch_size, total)}:\n"
                f"{error}"
            )

        end = min(
            start + batch_size,
            total,
        )

        print(
            f"Inserted {end}/{total}"
        )

    print()
    print("LGA insertion completed.")


# ============================================================
# FINAL VERIFICATION
# ============================================================

def verify():

    print()
    print("=" * 60)
    print("FINAL DATABASE VERIFICATION")
    print("=" * 60)

    response = (
        supabase
        .table("local_governments")
        .select(
            "id,state_id,name,code"
        )
        .execute()
    )

    rows = response.data or []

    total = len(rows)

    print(
        f"Total LGAs in Supabase: {total}"
    )

    if total != 774:

        raise RuntimeError(
            f"FAILED: expected 774 LGAs, "
            f"found {total}."
        )

    keys = set()

    for row in rows:

        key = (
            row["state_id"],
            normalize(row["name"]),
        )

        if key in keys:

            raise RuntimeError(
                f"Duplicate state/LGA: "
                f"{row['name']}"
            )

        keys.add(key)

    print(
        "Duplicate state/LGA check: PASS"
    )

    codes = set()

    for row in rows:

        code = clean(
            row.get("code")
        )

        if not code:

            raise RuntimeError(
                f"LGA has no code: "
                f"{row['name']}"
            )

        if code in codes:

            raise RuntimeError(
                f"Duplicate LGA code: {code}"
            )

        codes.add(code)

    print(
        "LGA code check: PASS"
    )

    state_ids = {
        row["state_id"]
        for row in rows
    }

    if len(state_ids) != 37:

        raise RuntimeError(
            f"Expected 37 state relationships, "
            f"found {len(state_ids)}."
        )

    print(
        "37 state relationships: PASS"
    )

    print()
    print("=" * 60)
    print("774 LGAs VERIFIED SUCCESSFULLY")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("EXAMINA AI")
    print("NIGERIA ADMINISTRATIVE DATA IMPORT")
    print("=" * 60)

    # 1. Read all-lga.json
    data = load_json()

    # 2. Read the 37 states from Supabase
    states = load_states()

    # 3. Extract 774 LGAs
    records = extract_lgas(data)

    # 4. Validate the JSON
    validate_lgas(
        records,
        states,
    )

    # 5. Insert missing LGAs
    insert_lgas(
        records,
        states,
    )

    # 6. Verify Supabase
    verify()

    print()
    print(
        "EXAMINA AI LGA SEEDING COMPLETE."
    )


# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()
        print("Import cancelled.")
        sys.exit(1)

    except Exception as error:

        print()
        print("=" * 60)
        print("IMPORT FAILED")
        print("=" * 60)
        print(str(error))
        print("=" * 60)

        sys.exit(1)
