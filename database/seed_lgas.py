import json
import os
import sys
from pathlib import Path

from supabase import create_client


# ============================================================
# EXAMINA AI
# NIGERIA ADMINISTRATIVE DATA SEEDER
# ============================================================


# ============================================================
# FILE LOCATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "all-lga.json"


# ============================================================
# SUPABASE CREDENTIALS
#
# Streamlit Secrets:
#
# SUPABASE_URL = "https://xxxxx.supabase.co"
# SUPABASE_KEY = "your-secret-key"
#
# The same names are also supported as environment variables.
# ============================================================

def get_supabase_credentials():

    # --------------------------------------------------------
    # STREAMLIT CLOUD
    # --------------------------------------------------------

    try:

        import streamlit as st

        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")

        if url and key:

            return url, key

    except Exception:
        pass


    # --------------------------------------------------------
    # ENVIRONMENT VARIABLES
    # --------------------------------------------------------

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url:

        raise RuntimeError(
            "SUPABASE_URL is not configured.\n\n"
            "Add SUPABASE_URL to your Streamlit Secrets."
        )

    if not key:

        raise RuntimeError(
            "SUPABASE_KEY is not configured.\n\n"
            "Add SUPABASE_KEY to your Streamlit Secrets."
        )

    return url, key


# ============================================================
# CREATE SUPABASE CLIENT
# ============================================================

SUPABASE_URL, SUPABASE_KEY = get_supabase_credentials()

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
)


# ============================================================
# EXPECTED NIGERIAN STATES + FCT
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

    print()
    print("Loading LGA JSON dataset...")

    if not JSON_FILE.exists():

        raise FileNotFoundError(
            f"\nMissing file:\n{JSON_FILE}\n\n"
            "Expected structure:\n"
            "services/\n"
            "├── seedlga.py\n"
            "└── all-lga.json"
        )

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
# TEST SUPABASE CONNECTION
# ============================================================

def test_connection():

    print()
    print("Testing Supabase connection...")

    try:

        response = (
            supabase
            .table("states")
            .select("id,name,code")
            .limit(1)
            .execute()
        )

        if response.data is None:

            raise RuntimeError(
                "Supabase returned no data."
            )

    except Exception as error:

        raise RuntimeError(
            "Could not connect to Supabase.\n\n"
            f"{error}"
        )

    print("Supabase connection: PASS")


# ============================================================
# LOAD STATES
# ============================================================

def load_states():

    print()
    print("Loading states from Supabase...")

    try:

        response = (
            supabase
            .table("states")
            .select("id,name,code")
            .execute()
        )

    except Exception as error:

        raise RuntimeError(
            f"Failed to load states from Supabase:\n{error}"
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

        state_id = clean(
            state.get("id")
        )

        state_name = clean(
            state.get("name")
        )

        state_code = clean(
            state.get("code")
        )

        if not state_id:

            raise RuntimeError(
                f"State has no UUID: {state}"
            )

        if not state_name:

            raise RuntimeError(
                f"State has no name: {state}"
            )

        if not state_code:

            raise RuntimeError(
                f"State has no code: {state}"
            )

        key = normalize(state_name)

        if key in state_map:

            raise RuntimeError(
                f"Duplicate state name:\n{state_name}"
            )

        state_map[key] = {
            "id": state_id,
            "name": state_name,
            "code": state_code,
        }

    # --------------------------------------------------------
    # CHECK EXPECTED STATES
    # --------------------------------------------------------

    missing = []

    for expected_state in EXPECTED_STATES:

        if normalize(expected_state) not in state_map:

            missing.append(expected_state)

    if missing:

        raise RuntimeError(
            "Supabase is missing these states/FCT:\n\n"
            + "\n".join(sorted(missing))
        )

    print("37 states/FCT verified: PASS")

    return state_map


# ============================================================
# EXTRACT LGAS FROM JSON
# ============================================================

def extract_lgas(data):

    print()
    print("Extracting LGA records...")

    records = []

    for item in data:

        # ----------------------------------------------------
        # LEVEL 2 = LOCAL GOVERNMENT
        # ----------------------------------------------------

        if item.get("level") != 2:

            continue


        # ----------------------------------------------------
        # LGA NAME
        # ----------------------------------------------------

        name_object = item.get("name") or {}

        if isinstance(name_object, dict):

            lga_name = clean(
                name_object.get("en")
                or name_object.get("name")
            )

        else:

            lga_name = clean(
                name_object
            )


        # ----------------------------------------------------
        # LGA CODE
        # ----------------------------------------------------

        code_object = item.get("code") or {}

        if isinstance(code_object, dict):

            lga_code = clean(
                code_object.get("id")
                or code_object.get("code")
            )

        else:

            lga_code = clean(
                code_object
            )


        # ----------------------------------------------------
        # PARENT STATE
        # ----------------------------------------------------

        parent = item.get("parent") or {}

        if not isinstance(parent, dict):

            parent = {}


        parent_name_object = (
            parent.get("name") or {}
        )

        if isinstance(parent_name_object, dict):

            state_name = clean(
                parent_name_object.get("en")
                or parent_name_object.get("name")
            )

        else:

            state_name = clean(
                parent_name_object
            )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not lga_name:

            raise RuntimeError(
                f"LGA has no name:\n{item}"
            )

        if not lga_code:

            raise RuntimeError(
                f"LGA has no code:\n{lga_name}"
            )

        if not state_name:

            raise RuntimeError(
                f"LGA has no parent state:\n{lga_name}"
            )


        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        records.append({

            "source_id": lga_code,

            "name": lga_name,

            "state_name": state_name,

        })


    print(
        f"LGA records discovered: {len(records)}"
    )

    return records


# ============================================================
# VALIDATE LGAS
# ============================================================

def validate_lgas(records, states):

    print()
    print("Validating LGA dataset...")

    # --------------------------------------------------------
    # TOTAL COUNT
    # --------------------------------------------------------

    if len(records) != 774:

        raise RuntimeError(
            f"Expected exactly 774 LGAs, "
            f"but found {len(records)}."
        )


    # --------------------------------------------------------
    # DUPLICATE SOURCE CODES
    # --------------------------------------------------------

    codes = set()

    for record in records:

        code = record["source_id"]

        if code in codes:

            raise RuntimeError(
                f"Duplicate LGA source code: {code}"
            )

        codes.add(code)


    # --------------------------------------------------------
    # STATE RELATIONSHIPS
    # --------------------------------------------------------

    state_counts = {}

    for record in records:

        state_key = normalize(
            record["state_name"]
        )

        if state_key not in states:

            raise RuntimeError(
                f"Unknown state in JSON:\n\n"
                f"LGA: {record['name']}\n"
                f"State: {record['state_name']}"
            )

        state_counts[state_key] = (
            state_counts.get(state_key, 0) + 1
        )


    # --------------------------------------------------------
    # ALL 37 STATES
    # --------------------------------------------------------

    if len(state_counts) != 37:

        raise RuntimeError(
            f"Expected 37 state groups, "
            f"but found {len(state_counts)}."
        )


    print("LGA count: PASS")
    print("Duplicate LGA code check: PASS")
    print("State relationship check: PASS")

    print()
    print("LGA distribution:")

    for state_key in sorted(state_counts):

        print(
            f"  {states[state_key]['name']}: "
            f"{state_counts[state_key]}"
        )

    print()
    print("Dataset validation: PASS")


# ============================================================
# LOAD EXISTING LGAS
# ============================================================

def load_existing_lgas():

    print()
    print("Checking existing LGAs in Supabase...")

    try:

        response = (
            supabase
            .table("local_governments")
            .select(
                "id,state_id,name,code"
            )
            .execute()
        )

    except Exception as error:

        raise RuntimeError(
            "Could not read local_governments table:\n"
            f"{error}"
        )

    existing = response.data or []

    print(
        f"Existing database LGAs: {len(existing)}"
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

    print()
    print("Preparing LGA records for insertion...")

    existing_keys = set()

    for row in existing:

        state_id = row.get("state_id")

        name = normalize(
            row.get("name")
        )

        if state_id and name:

            existing_keys.add(
                (
                    state_id,
                    name,
                )
            )


    missing = []

    for record in records:

        state_key = normalize(
            record["state_name"]
        )

        state = states[state_key]

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

            "code": record["source_id"],

        })


    print(
        f"LGAs already present: "
        f"{len(records) - len(missing)}"
    )

    print(
        f"LGAs to insert: {len(missing)}"
    )

    return missing


# ============================================================
# INSERT LGAS
# ============================================================

def insert_lgas(missing):

    if not missing:

        print()
        print(
            "All 774 LGAs already exist in Supabase."
        )

        return


    print()
    print("Starting LGA import...")

    batch_size = 100

    total = len(missing)

    for start in range(
        0,
        total,
        batch_size,
    ):

        end = min(
            start + batch_size,
            total,
        )

        batch = missing[
            start:end
        ]

        print(
            f"Inserting LGAs "
            f"{start + 1}-{end}..."
        )

        try:

            (
                supabase
                .table("local_governments")
                .insert(batch)
                .execute()
            )

        except Exception as error:

            raise RuntimeError(
                f"\nFailed inserting LGAs "
                f"{start + 1}-{end}:\n\n"
                f"{error}"
            )

        print(
            f"Inserted {end}/{total}"
        )

    print()
    print("LGA insertion completed successfully.")


# ============================================================
# FINAL VERIFICATION
# ============================================================

def verify():

    print()
    print("=" * 60)
    print("FINAL DATABASE VERIFICATION")
    print("=" * 60)

    try:

        response = (
            supabase
            .table("local_governments")
            .select(
                "id,state_id,name,code"
            )
            .execute()
        )

    except Exception as error:

        raise RuntimeError(
            f"Could not verify local_governments:\n{error}"
        )

    rows = response.data or []

    total = len(rows)

    print(
        f"Total local-government records: {total}"
    )


    # --------------------------------------------------------
    # TOTAL COUNT
    # --------------------------------------------------------

    if total != 774:

        raise RuntimeError(
            f"FAILED: expected 774 LGAs, "
            f"found {total}."
        )

    print(
        "Total count check: PASS"
    )


    # --------------------------------------------------------
    # STATE/LGA DUPLICATES
    # --------------------------------------------------------

    keys = set()

    for row in rows:

        key = (
            row["state_id"],
            normalize(row["name"]),
        )

        if key in keys:

            raise RuntimeError(
                "FAILED: duplicate "
                "state/LGA combination:\n"
                f"{row['name']}"
            )

        keys.add(key)

    print(
        "Duplicate state/LGA check: PASS"
    )


    # --------------------------------------------------------
    # LGA CODE CHECK
    # --------------------------------------------------------

    codes = set()

    for row in rows:

        code = clean(
            row.get("code")
        )

        if not code:

            raise RuntimeError(
                f"FAILED: LGA has no code:\n"
                f"{row['name']}"
            )

        if code in codes:

            raise RuntimeError(
                f"FAILED: duplicate LGA code:\n"
                f"{code}"
            )

        codes.add(code)

    print(
        "LGA code check: PASS"
    )


    # --------------------------------------------------------
    # STATE RELATIONSHIP CHECK
    # --------------------------------------------------------

    state_counts = {}

    for row in rows:

        state_id = row["state_id"]

        state_counts[state_id] = (
            state_counts.get(state_id, 0) + 1
        )

    if len(state_counts) != 37:

        raise RuntimeError(
            f"FAILED: expected LGAs belonging "
            f"to 37 states/FCT, "
            f"found {len(state_counts)}."
        )

    print(
        "37 state relationships: PASS"
    )


    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 1. TEST SUPABASE
    # --------------------------------------------------------

    test_connection()


    # --------------------------------------------------------
    # 2. LOAD JSON
    # --------------------------------------------------------

    data = load_json()


    # --------------------------------------------------------
    # 3. LOAD STATES
    # --------------------------------------------------------

    states = load_states()


    # --------------------------------------------------------
    # 4. EXTRACT LGAS
    # --------------------------------------------------------

    records = extract_lgas(data)


    # --------------------------------------------------------
    # 5. VALIDATE JSON
    # --------------------------------------------------------

    validate_lgas(
        records,
        states,
    )


    # --------------------------------------------------------
    # 6. LOAD EXISTING LGAS
    # --------------------------------------------------------

    existing = load_existing_lgas()


    # --------------------------------------------------------
    # 7. PREPARE INSERTS
    # --------------------------------------------------------

    missing = prepare_inserts(
        records,
        states,
        existing,
    )


    # --------------------------------------------------------
    # 8. INSERT
    # --------------------------------------------------------

    insert_lgas(
        missing,
    )


    # --------------------------------------------------------
    # 9. VERIFY
    # --------------------------------------------------------

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
        print(error)
        print("=" * 60)

        sys.exit(1)
