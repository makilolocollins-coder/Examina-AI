# ============================================================
# EXAMINA AI
# DATABASE VERIFICATION
# ============================================================

from database.database import get_states, get_lgas


# ============================================================
# VERIFY
# ============================================================

def main():

    print("=" * 60)

    print("EXAMINA AI DATABASE VERIFICATION")

    print("=" * 60)


    states = get_states()


    print(
        f"States/FCT found: {len(states)}"
    )


    total_lgas = 0


    for state in states:

        lgas = get_lgas(
            state["id"]
        )

        count = len(lgas)

        total_lgas += count


        print(
            f"{state['name']}: {count} LGAs"
        )


    print()

    print("=" * 60)

    print(
        f"TOTAL LGAS: {total_lgas}"
    )

    print("=" * 60)


    if len(states) == 37:

        print(
            "States verification: PASS"
        )

    else:

        print(
            "States verification: FAILED"
        )


    if total_lgas == 774:

        print(
            "LGA verification: PASS"
        )

    else:

        print(
            "LGA verification: NOT COMPLETE"
        )


if __name__ == "__main__":

    main()
