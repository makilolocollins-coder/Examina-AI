# ============================================================
# EXAMINA AI
# SUBJECT AI CONFIGURATION
# ============================================================

"""
This file tells Examina AI how each subject should be handled.

Examples:

Mathematics
    → equations
    → mathematical symbols
    → calculations

Physics
    → equations
    → units
    → scientific symbols
    → calculations

Chemistry
    → chemical formulas
    → chemical equations
    → reactions
    → symbols

English
    → normal text
    → grammar
    → comprehension
"""


# ============================================================
# MATHEMATICS
# ============================================================

MATHEMATICS = {
    "name": "Mathematics",

    "category": "STEM",

    "supports": [
        "text",
        "mathematical_symbols",
        "equations",
        "fractions",
        "indices",
        "roots",
        "graphs",
        "geometry",
        "algebra",
        "calculus",
        "statistics",
        "probability",
    ],

    "ocr_mode": "mathematical",

    "solver": True,

    "ai_teacher": True,
}


# ============================================================
# FURTHER MATHEMATICS
# ============================================================

FURTHER_MATHEMATICS = {
    "name": "Further Mathematics",

    "category": "STEM",

    "supports": [
        "text",
        "mathematical_symbols",
        "equations",
        "matrices",
        "vectors",
        "calculus",
        "complex_numbers",
        "mechanics",
        "statistics",
        "probability",
        "graphs",
    ],

    "ocr_mode": "mathematical",

    "solver": True,

    "ai_teacher": True,
}


# ============================================================
# PHYSICS
# ============================================================

PHYSICS = {
    "name": "Physics",

    "category": "STEM",

    "supports": [
        "text",
        "scientific_symbols",
        "equations",
        "units",
        "graphs",
        "diagrams",
        "calculations",
        "vectors",
    ],

    "ocr_mode": "scientific",

    "solver": True,

    "ai_teacher": True,
}


# ============================================================
# CHEMISTRY
# ============================================================

CHEMISTRY = {
    "name": "Chemistry",

    "category": "STEM",

    "supports": [
        "text",
        "chemical_symbols",
        "chemical_formulas",
        "chemical_equations",
        "chemical_reactions",
        "ions",
        "subscripts",
        "superscripts",
        "structures",
        "calculations",
    ],

    "ocr_mode": "chemical",

    "solver": True,

    "ai_teacher": True,
}


# ============================================================
# BIOLOGY
# ============================================================

BIOLOGY = {
    "name": "Biology",

    "category": "STEM",

    "supports": [
        "text",
        "scientific_terms",
        "diagrams",
        "labels",
        "tables",
    ],

    "ocr_mode": "scientific",

    "solver": True,

    "ai_teacher": True,
}


# ============================================================
# ENGLISH LANGUAGE
# ============================================================

ENGLISH_LANGUAGE = {
    "name": "English Language",

    "category": "Languages",

    "supports": [
        "text",
        "grammar",
        "comprehension",
        "essay",
        "vocabulary",
        "literature",
    ],

    "ocr_mode": "text",

    "solver": True,

    "ai_teacher": True,
}


# ============================================================
# ECONOMICS
# ============================================================

ECONOMICS = {
    "name": "Economics",

    "category": "Social Science",

    "supports": [
        "text",
        "graphs",
        "tables",
        "calculations",
        "economic_symbols",
    ],

    "ocr_mode": "scientific",

    "solver": True,

    "ai_teacher": True,
}


# ============================================================
# ACCOUNTING
# ============================================================

ACCOUNTING = {
    "name": "Accounting",

    "category": "Business",

    "supports": [
        "text",
        "tables",
        "calculations",
        "accounting_formats",
        "financial_statements",
    ],

    "ocr_mode": "structured",

    "solver": True,

    "ai_teacher": True,
}


# ============================================================
# GOVERNMENT
# ============================================================

GOVERNMENT = {
    "name": "Government",

    "category": "Humanities",

    "supports": [
        "text",
        "tables",
        "structured_questions",
    ],

    "ocr_mode": "text",

    "solver": True,

    "ai_teacher": True,
}


# ============================================================
# GEOGRAPHY
# ============================================================

GEOGRAPHY = {
    "name": "Geography",

    "category": "Humanities",

    "supports": [
        "text",
        "maps",
        "diagrams",
        "graphs",
        "tables",
        "coordinates",
    ],

    "ocr_mode": "structured",

    "solver": True,

    "ai_teacher": True,
}


# ============================================================
# SUBJECT REGISTRY
# ============================================================

SUBJECT_CONFIG = {

    "Mathematics": MATHEMATICS,

    "Further Mathematics": FURTHER_MATHEMATICS,

    "Physics": PHYSICS,

    "Chemistry": CHEMISTRY,

    "Biology": BIOLOGY,

    "English Language": ENGLISH_LANGUAGE,

    "Economics": ECONOMICS,

    "Accounting": ACCOUNTING,

    "Government": GOVERNMENT,

    "Geography": GEOGRAPHY,
}


# ============================================================
# GET SUBJECT CONFIGURATION
# ============================================================

def get_subject_config(subject_name):
    """
    Return the AI configuration for a subject.
    """

    if subject_name not in SUBJECT_CONFIG:
        return {
            "name": subject_name,
            "category": "General",
            "supports": ["text"],
            "ocr_mode": "text",
            "solver": True,
            "ai_teacher": True,
        }

    return SUBJECT_CONFIG[subject_name]
