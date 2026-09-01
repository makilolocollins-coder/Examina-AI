# ============================================================
# EXAMINA AI
# NIGERIA ADMINISTRATIVE DATA SEEDER
# ============================================================

import json
from pathlib import Path

from database.supabase_client import get_supabase_client


# ============================================================
# FILE LOCATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

JSON_FILE = BASE_DIR / "all-lga.json"


# ============================================================
# GET SUPABASE CLIENT
# ============================================================

supabase = get_supabase_client()


# ============================================================
# LOAD JSON
# ============================================================

def load_lga_data():

    if not JSON_FILE.exists():

        raise FileNotFoundError(
            f"Could not find: {JSON_FILE}"
        )

    with open(
        JSON_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# ============================================================
# GET STATES
# ============================================================

def get_states():

    response = (
        supabase
        .table("states")
        .select("id,name,code")
        .execute()
    )

    return response.data or []


# ============================================================
# SEED LGAs
# ============================================================

def seed_lgas():

    data = load_lga_data()

    states = get_states()

    if not states:

        raise RuntimeError(
            "No states found in the states table."
        )

    # --------------------------------------------------------
    # Create state lookup
    # --------------------------------------------------------

    state_lookup = {}

    for state in states:

        state_lookup[
            state["name"].strip().lower()
        ] = state["id"]

    # --------------------------------------------------------
    # Prepare LGA records
    # --------------------------------------------------------

    records = []

    for state_name, lgas in data.items():

        state_key = (
            state_name
            .strip()
            .lower()
        )

        state_id = state_lookup.get(
            state_key
        )

        if not state_id:

            print(
                f"WARNING: State not found: {state_name}"
            )

            continue

        for lga in lgas:

            if isinstance(lga, str):

                lga_name = lga.strip()

                lga_code = None

            else:

                lga_name = (
                    lga.get("name", "")
                    .strip()
                )

                lga_code = lga.get("code")

            if not lga_name:
                continue

            records.append(
                {
                    "name": lga_name,
                    "code": lga_code,
                    "state_id": state_id,
                }
            )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    unique_records = {}

    for record in records:

        key = (
            record["state_id"],
            record["name"].lower(),
        )

        unique_records[key] = record

    records = list(
        unique_records.values()
    )

    print(
        f"Prepared {len(records)} LGAs."
    )

    # --------------------------------------------------------
    # Insert in batches
    # --------------------------------------------------------

    batch_size = 100

    inserted = 0

    for start in range(
        0,
        len(records),
        batch_size,
    ):

        batch = records[
            start:start + batch_size
        ]

        supabase \
            .table("local_governments") \
            .upsert(
                batch,
                on_conflict="state_id,name",
            ) \
            .execute()

        inserted += len(batch)

        print(
            f"Inserted: {inserted}/{len(records)}"
        )

    print("")
    print(
        "LGA seeding completed successfully."
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    seed_lgas()
