import json
import os
import sys
from pathlib import Path

from supabase import create_client


# ============================================================
# EXAMINA AI
# NIGERIA ADMINISTRATIVE DATA SEEDER
# ============================================================

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get(
    "SUPABASE_SERVICE_ROLE_KEY"
)

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL environment variable is missing.")

if not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError(
        "SUPABASE_SERVICE_ROLE_KEY environment variable is missing."
    )


BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "all-lga.json"


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)


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
            f"\nMissing file:\n{JSON_FILE}\n"
            "Make sure all-lga.json is in the same folder as seedlga.py."
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
# LOAD STATES FROM DATABASE
# ============================================================

def load_states():

    print()
    print("Loading states from database...")

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
            f"but database contains {len(states)}."
        )

    state_map = {}

    for state in states:

        name = clean(state.get("name"))

        if not name:
            raise RuntimeError(
                "A state record has no name."
            )

        key = normalize(name)

        if key in state_map:

            raise RuntimeError(
                f"Duplicate state in database: {name}"
            )

        state_map[key] = state

    missing = []

    for expected in EXPECTED_STATES:

        if normalize(expected) not in state_map:

            missing.append(expected)

    if missing:

        raise RuntimeError(
            "Database is missing these states/FCT:\n\n"
            + "\n".join(sorted(missing))
        )

    print("37 states/FCT verified.")

    return state_map


# ============================================================
# EXTRACT LGAS
# ============================================================

def extract_lgas(data):

    print()
    print("Extracting LGA records...")

    records = []

    for item in data:

        # ----------------------------------------------------
        # We only want level 2 = Local Government
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
        # PARENT
        # ----------------------------------------------------

        parent = item.get("parent") or {}

        if not isinstance(parent, dict):

            parent = {}

        parent_name_object = parent.get("name") or {}

        if isinstance(parent_name_object, dict):

            state_name = clean(
                parent_name_object.get("en")
                or parent_name_object.get("name")
            )

        else:

            state_name = clean(parent_name_object)

        state_source_id = clean(
            parent.get("id")
        )

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
                f"LGA without parent state: {lga_name}"
            )

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        records.append({
            "source_id": lga_code,
            "name": lga_name,
            "state_name": state_name,
            "state_source_id": state_source_id,
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

    if len(records) != 774:

        raise RuntimeError(
            f"Expected exactly 774 LGAs. "
            f"Found {len(records)}."
        )

    # --------------------------------------------------------
    # CHECK DUPLICATE SOURCE CODES
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
    # CHECK STATE RELATIONSHIPS
    # --------------------------------------------------------

    state_counts = {}

    for record in records:

        state_key = normalize(
            record["state_name"]
        )

        if state_key not in states:

            raise RuntimeError(
                f"Unknown state:\n"
                f"LGA: {record['name']}\n"
                f"State: {record['state_name']}"
            )

        state_counts[state_key] = (
            state_counts.get(state_key, 0) + 1
        )

    # --------------------------------------------------------
    # CHECK ALL 37 STATES
    # --------------------------------------------------------

    if len(state_counts) != 37:

        raise RuntimeError(
            f"Expected 37 state groups. "
            f"Found {len(state_counts)}."
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
    print("Loading existing LGAs...")

    response = (
        supabase
        .table("local_governments")
        .select("id,state_id,name,code")
        .execute()
    )

    existing = response.data or []

    print(
        f"Existing database LGAs: {len(existing)}"
    )

    return existing


# ============================================================
# BUILD INSERT LIST
# ============================================================

def prepare_inserts(records, states, existing):

    existing_keys = set()

    for row in existing:

        state_id = row.get("state_id")
        name = normalize(row.get("name"))

        if state_id and name:

            existing_keys.add(
                (state_id, name)
            )

    missing = []

    for record in records:

        state = states[
            normalize(record["state_name"])
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
            "code": record["source_id"],
        })

    return missing


# ============================================================
# INSERT LGAS
# ============================================================

def insert_lgas(records, states):

    existing = load_existing_lgas()

    missing = prepare_inserts(
        records,
        states,
        existing,
    )

    print(
        f"LGAs to insert: {len(missing)}"
    )

    if not missing:

        print()
        print(
            "Nothing to insert. "
            "All dataset LGAs already exist."
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
                f"\nFailed inserting batch "
                f"{start + 1}-{min(start + batch_size, total)}:\n"
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
        .select("id,state_id,name,code")
        .execute()
    )

    rows = response.data or []

    total = len(rows)

    print(
        f"Total local-government records: {total}"
    )

    if total != 774:

        raise RuntimeError(
            f"FAILED: expected 774 LGAs, "
            f"found {total}."
        )

    # --------------------------------------------------------
    # DUPLICATE CHECK
    # --------------------------------------------------------

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
        "Duplicate state/LGA check: PASS"
    )

    # --------------------------------------------------------
    # CODE CHECK
    # --------------------------------------------------------

    codes = set()

    for row in rows:

        code = clean(row.get("code"))

        if not code:
            raise RuntimeError(
                f"FAILED: LGA has no code: "
                f"{row['name']}"
            )

        if code in codes:

            raise RuntimeError(
                f"FAILED: duplicate LGA code: {code}"
            )

        codes.add(code)

    print(
        "LGA code check: PASS"
    )

    # --------------------------------------------------------
    # STATE COUNT
    # --------------------------------------------------------

    state_counts = {}

    for row in rows:

        state_id = row["state_id"]

        state_counts[state_id] = (
            state_counts.get(state_id, 0) + 1
        )

    if len(state_counts) != 37:

        raise RuntimeError(
            f"FAILED: expected 37 state relationships, "
            f"found {len(state_counts)}."
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

    # 1. Load JSON
    data = load_json()

    # 2. Load database states
    states = load_states()

    # 3. Extract LGAs
    records = extract_lgas(data)

    # 4. Validate dataset
    validate_lgas(
        records,
        states,
    )

    # 5. Insert missing LGAs
    insert_lgas(
        records,
        states,
    )

    # 6. Verify final database
    verify()

    print()
    print("EXAMINA AI LGA SEEDING COMPLETE.")


# ============================================================
# RUN
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
