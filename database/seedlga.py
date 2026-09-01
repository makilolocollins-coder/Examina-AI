# ============================================================
# EXAMINA AI
# NIGERIA ADMINISTRATIVE DATA SEEDER
# ============================================================

import json
from pathlib import Path

from database.supabase_client import get_supabase_client


# ============================================================
# DATABASE
# ============================================================

supabase = get_supabase_client()


# ============================================================
# JSON FILE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

JSON_FILE = BASE_DIR / "all-lga.json"


# ============================================================
# LOAD all-lga.json
# ============================================================

def load_lga_data():

    if not JSON_FILE.exists():

        raise FileNotFoundError(
            f"File not found: {JSON_FILE}"
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
# SEED LOCAL GOVERNMENTS
# ============================================================

def seed_lgas():

    data = load_lga_data()

    states = get_states()

    if not states:

        raise RuntimeError(
            "No states found in the states table."
        )

    # --------------------------------------------------------
    # STATE LOOKUP
    # --------------------------------------------------------

    state_lookup = {
        state["name"].strip().lower(): state["id"]
        for state in states
    }

    records = []

    # --------------------------------------------------------
    # READ all-lga.json
    # --------------------------------------------------------

    for state_name, lgas in data.items():

        state_id = state_lookup.get(
            state_name.strip().lower()
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
                    lga.get("name", "").strip()
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
    # REMOVE DUPLICATES
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
    # INSERT LGAs
    # --------------------------------------------------------

    batch_size = 100

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
            .insert(batch) \
            .execute()

        print(
            f"Inserted {min(start + batch_size, len(records))}"
            f"/{len(records)}"
        )

    print(
        "LGA seeding completed successfully."
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    seed_lgas()
