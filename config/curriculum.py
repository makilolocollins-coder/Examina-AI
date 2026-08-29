# ============================================================
# EXAMINA AI
# NIGERIAN CURRICULUM CONFIGURATION
# ============================================================

"""
Examina AI Nigerian Curriculum

Academic structure:

Primary 1 - 3
Primary 4 - 6
JSS 1 - 3
SS 1 - 3

Senior Secondary fields:

    Science
    Humanities
    Business

IMPORTANT
---------
This file contains the SUBJECT CATALOGUE.

It does NOT automatically assign every subject
to a student.

The actual subjects taken by a student are stored
in the StudentSubject database table.

Therefore:

    curriculum.py
          ↓
    Available subjects
          ↓
    Teacher selects actual subjects
          ↓
    StudentSubject
          ↓
    Results
"""


# ============================================================
# PRIMARY 1 - 3
# ============================================================

PRIMARY_1_3_SUBJECTS = [
    "English Studies",
    "Mathematics",
    "Nigerian Language",
    "Basic Science",
    "Physical and Health Education",
    "Christian Religious Studies / Islamic Studies",
    "Nigerian History",
    "Social and Citizenship Studies",
    "Cultural and Creative Arts",
    "Arabic Language",
]


# ============================================================
# PRIMARY 4 - 6
# ============================================================

PRIMARY_4_6_SUBJECTS = [
    "English Studies",
    "Mathematics",
    "Nigerian Language",
    "Basic Science and Technology",
    "Physical and Health Education",
    "Basic Digital Literacy",
    "Christian Religious Studies / Islamic Studies",
    "Nigerian History",
    "Social and Citizenship Studies",
    "Cultural and Creative Arts",
    "Pre-Vocational Studies",
    "French",
    "Arabic Language",
]


# ============================================================
# JUNIOR SECONDARY SCHOOL
# JSS 1 - 3
# ============================================================

JSS_1_3_SUBJECTS = [
    "English Studies",
    "Mathematics",
    "Basic Science and Technology",
    "National Values",
    "Pre-Vocational Studies",
    "Business Studies",
    "Cultural and Creative Arts",
    "History",
    "Christian Religious Studies",
    "Islamic Studies",
    "Nigerian Language",
    "French",
    "Arabic",
]


# ============================================================
# SENIOR SECONDARY SCHOOL
# COMMON CORE SUBJECTS
# ============================================================

SS_CORE_SUBJECTS = [
    "English Language",
    "General Mathematics",
    "Citizenship and Heritage Studies",
    "Digital Technologies",
]


# ============================================================
# SENIOR SECONDARY
# SCIENCE
# ============================================================

SS_SCIENCE_SUBJECTS = [
    "Biology",
    "Chemistry",
    "Physics",
    "Agriculture",
    "Further Mathematics",
    "Physical Education",
    "Health Education",
    "Food and Nutrition",
    "Geography",
    "Technical Drawing",
]


# ============================================================
# SENIOR SECONDARY
# HUMANITIES
# ============================================================

SS_HUMANITIES_SUBJECTS = [
    "Nigerian History",
    "Government",
    "Christian Religious Studies",
    "Islamic Studies",
    "Nigerian Language",
    "French",
    "Arabic",
    "Visual Arts",
    "Music",
    "Literature in English",
    "Home Management",
    "Catering Craft",
]


# ============================================================
# SENIOR SECONDARY
# BUSINESS
# ============================================================

SS_BUSINESS_SUBJECTS = [
    "Accounting",
    "Commerce",
    "Marketing",
    "Economics",
]


# ============================================================
# SENIOR SECONDARY
# TRADE SUBJECTS
# ============================================================

SS_TRADE_SUBJECTS = [
    "Solar Photovoltaic Installation and Maintenance",
    "Fashion Design and Garment Making",
    "Livestock Farming",
    "Beauty and Cosmetology",
    "Computer Hardware and GSM Repairs",
    "Horticulture and Crop Production",
]


# ============================================================
# SENIOR SECONDARY FIELDS
# ============================================================

SS_FIELDS = {
    "Science": SS_SCIENCE_SUBJECTS,
    "Humanities": SS_HUMANITIES_SUBJECTS,
    "Business": SS_BUSINESS_SUBJECTS,
}


# ============================================================
# EDUCATION LEVELS
# ============================================================

EDUCATION_LEVELS = {

    "Primary": [
        "Primary 1",
        "Primary 2",
        "Primary 3",
        "Primary 4",
        "Primary 5",
        "Primary 6",
    ],

    "Junior Secondary School": [
        "JSS 1",
        "JSS 2",
        "JSS 3",
    ],

    "Senior Secondary School": [
        "SS 1",
        "SS 2",
        "SS 3",
    ],
}


# ============================================================
# SENIOR SECONDARY FIELDS
# ============================================================

SENIOR_SECONDARY_FIELDS = [
    "Science",
    "Humanities",
    "Business",
]


# ============================================================
# GET SUBJECTS FOR A CLASS
# ============================================================

def get_subjects_for_class(
    class_name: str,
    field: str | None = None,
) -> list[str]:
    """
    Return all subjects available for a class.

    IMPORTANT:
    This function returns AVAILABLE subjects only.

    It does not mean the student automatically takes
    every subject returned.

    Actual student subject registration is stored in
    StudentSubject.
    """

    # --------------------------------------------------------
    # PRIMARY 1 - 3
    # --------------------------------------------------------

    if class_name in {
        "Primary 1",
        "Primary 2",
        "Primary 3",
    }:

        return PRIMARY_1_3_SUBJECTS.copy()


    # --------------------------------------------------------
    # PRIMARY 4 - 6
    # --------------------------------------------------------

    if class_name in {
        "Primary 4",
        "Primary 5",
        "Primary 6",
    }:

        return PRIMARY_4_6_SUBJECTS.copy()


    # --------------------------------------------------------
    # JSS 1 - 3
    # --------------------------------------------------------

    if class_name in {
        "JSS 1",
        "JSS 2",
        "JSS 3",
    }:

        return JSS_1_3_SUBJECTS.copy()


    # --------------------------------------------------------
    # SS 1 - 3
    # --------------------------------------------------------

    if class_name in {
        "SS 1",
        "SS 2",
        "SS 3",
    }:

        if field is None:

            raise ValueError(
                "Senior Secondary students must have "
                "a field: Science, Humanities, or Business."
            )

        if field not in SS_FIELDS:

            raise ValueError(
                f"Invalid SS field: {field}. "
                f"Choose from: {SENIOR_SECONDARY_FIELDS}"
            )

        return (
            SS_CORE_SUBJECTS.copy()
            + SS_FIELDS[field].copy()
            + SS_TRADE_SUBJECTS.copy()
        )


    # --------------------------------------------------------
    # INVALID CLASS
    # --------------------------------------------------------

    raise ValueError(
        f"Unknown class: {class_name}"
    )


# ============================================================
# VALIDATE CLASS
# ============================================================

def is_valid_class(
    class_name: str,
) -> bool:
    """
    Check whether a class exists in the curriculum.
    """

    all_classes = []

    for classes in EDUCATION_LEVELS.values():

        all_classes.extend(classes)

    return class_name in all_classes


# ============================================================
# VALIDATE SENIOR SECONDARY FIELD
# ============================================================

def is_valid_field(
    field: str | None,
) -> bool:
    """
    Check whether an SS field is valid.
    """

    return field in SENIOR_SECONDARY_FIELDS


# ============================================================
# CHECK SUBJECT AVAILABILITY
# ============================================================

def is_valid_subject_for_class(
    class_name: str,
    subject_name: str,
    field: str | None = None,
) -> bool:
    """
    Check whether a subject is available for
    a particular class and field.
    """

    subjects = get_subjects_for_class(
        class_name=class_name,
        field=field,
    )

    return subject_name in subjects


# ============================================================
# GET SUBJECT CATEGORY
# ============================================================

def get_subject_category(
    class_name: str,
    subject_name: str,
    field: str | None = None,
) -> str:
    """
    Determine the category of a subject.

    Returns:

        Core
        Science
        Humanities
        Business
        Trade
        Primary
        JSS
        Unknown
    """

    # --------------------------------------------------------
    # Validate subject
    # --------------------------------------------------------

    if not is_valid_subject_for_class(
        class_name=class_name,
        subject_name=subject_name,
        field=field,
    ):

        return "Unknown"


    # --------------------------------------------------------
    # Senior Secondary
    # --------------------------------------------------------

    if class_name in {
        "SS 1",
        "SS 2",
        "SS 3",
    }:

        if subject_name in SS_CORE_SUBJECTS:

            return "Core"

        if subject_name in SS_SCIENCE_SUBJECTS:

            return "Science"

        if subject_name in SS_HUMANITIES_SUBJECTS:

            return "Humanities"

        if subject_name in SS_BUSINESS_SUBJECTS:

            return "Business"

        if subject_name in SS_TRADE_SUBJECTS:

            return "Trade"


    # --------------------------------------------------------
    # JSS
    # --------------------------------------------------------

    if class_name in {
        "JSS 1",
        "JSS 2",
        "JSS 3",
    }:

        return "JSS"


    # --------------------------------------------------------
    # Primary
    # --------------------------------------------------------

    if class_name in {
        "Primary 1",
        "Primary 2",
        "Primary 3",
        "Primary 4",
        "Primary 5",
        "Primary 6",
    }:

        return "Primary"


    return "Unknown"


# ============================================================
# GET ALL CLASSES
# ============================================================

def get_all_classes() -> list[str]:
    """
    Return every class available in Examina AI.
    """

    classes = []

    for level_classes in EDUCATION_LEVELS.values():

        classes.extend(level_classes)

    return classes


# ============================================================
# GET ALL SUBJECTS
# ============================================================

def get_all_subjects() -> list[str]:
    """
    Return every unique subject in the curriculum.
    """

    subjects = set()

    subjects.update(PRIMARY_1_3_SUBJECTS)
    subjects.update(PRIMARY_4_6_SUBJECTS)
    subjects.update(JSS_1_3_SUBJECTS)
    subjects.update(SS_CORE_SUBJECTS)
    subjects.update(SS_SCIENCE_SUBJECTS)
    subjects.update(SS_HUMANITIES_SUBJECTS)
    subjects.update(SS_BUSINESS_SUBJECTS)
    subjects.update(SS_TRADE_SUBJECTS)

    return sorted(subjects)


# ============================================================
# CURRICULUM SUMMARY
# ============================================================

def get_curriculum_summary() -> dict:
    """
    Return a summary of the Examina AI curriculum.
    """

    return {
        "education_levels": EDUCATION_LEVELS,
        "senior_secondary_fields": SENIOR_SECONDARY_FIELDS,
        "total_classes": len(get_all_classes()),
        "total_subjects": len(get_all_subjects()),
    }
