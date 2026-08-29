# ============================================================
# EXAMINA AI
# NIGERIAN CURRICULUM CONFIGURATION
# ============================================================

"""
This file defines the academic structure used by Examina AI.

Structure:

Primary 1 - 3
Primary 4 - 6
JSS 1 - 3
SS 1 - 3
    ├── Science
    ├── Humanities
    └── Business

Important:
A student does NOT automatically receive every subject.
The school will select the subjects actually registered
for that student.
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
# SCIENCE FIELD
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
# HUMANITIES FIELD
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
# BUSINESS FIELD
# ============================================================

SS_BUSINESS_SUBJECTS = [
    "Accounting",
    "Commerce",
    "Marketing",
    "Economics",
]


# ============================================================
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
# GET SUBJECTS FOR A CLASS
# ============================================================

def get_subjects_for_class(
    class_name,
    field=None,
):
    """
    Return the subjects available for a particular class.

    Parameters
    ----------
    class_name : str
        Example:
        Primary 2
        Primary 5
        JSS 1
        SS 2

    field : str, optional
        Required for Senior Secondary School.

        Valid options:
        Science
        Humanities
        Business

    Returns
    -------
    list
        List of subjects available for the class.
    """

    # -------------------------
    # PRIMARY 1 - 3
    # -------------------------

    if class_name in [
        "Primary 1",
        "Primary 2",
        "Primary 3",
    ]:
        return PRIMARY_1_3_SUBJECTS.copy()


    # -------------------------
    # PRIMARY 4 - 6
    # -------------------------

    if class_name in [
        "Primary 4",
        "Primary 5",
        "Primary 6",
    ]:
        return PRIMARY_4_6_SUBJECTS.copy()


    # -------------------------
    # JSS 1 - 3
    # -------------------------

    if class_name in [
        "JSS 1",
        "JSS 2",
        "JSS 3",
    ]:
        return JSS_1_3_SUBJECTS.copy()


    # -------------------------
    # SS 1 - 3
    # -------------------------

    if class_name in [
        "SS 1",
        "SS 2",
        "SS 3",
    ]:

        if field is None:
            raise ValueError(
                "Senior Secondary students must have "
                "a field: Science, Humanities, or Business."
            )

        if field not in SS_FIELDS:
            raise ValueError(
                f"Invalid SS field: {field}. "
                f"Choose from: {list(SS_FIELDS.keys())}"
            )

        return (
            SS_CORE_SUBJECTS
            + SS_FIELDS[field]
            + SS_TRADE_SUBJECTS
        )


    # -------------------------
    # INVALID CLASS
    # -------------------------

    raise ValueError(
        f"Unknown class: {class_name}"
    )
