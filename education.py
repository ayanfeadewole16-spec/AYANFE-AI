# ============================================
# AYANFE AI V2 — EDUCATION SYSTEM
# ============================================

EDUCATION_SUBJECTS = [
    "mathematics",
    "math",
    "physics",
    "chemistry",
    "biology",
    "english",
    "literature",
    "economics",
    "government",
    "computer science",
    "computer",
    "science"
]


EXAMINATIONS = [
    "waec",
    "jamb",
    "neco"
]


def is_education_request(text):

    text = text.lower()

    education_words = [
        "study",
        "learn",
        "explain",
        "solve",
        "homework",
        "assignment",
        "revision",
        "quiz",
        "practice",
        "exam",
        "question"
    ]

    if any(
        word in text
        for word in education_words
    ):

        return True

    if any(
        subject in text
        for subject in EDUCATION_SUBJECTS
    ):

        return True

    if any(
        exam in text
        for exam in EXAMINATIONS
    ):

        return True

    return False


def get_education_format():

    return [
        "Simple explanation",
        "Detailed explanation",
        "Example",
        "Practice question",
        "Quiz"
    ]


def education_context():

    return """
You are helping a student.

When appropriate, structure educational answers as:

1. Simple explanation
2. Detailed explanation
3. Example
4. Practice question
5. Quiz

Use clear language appropriate for the student's level.

Support:

- Mathematics
- Physics
- Chemistry
- Biology
- English
- Literature
- Economics
- Government
- Computer Science
- WAEC
- JAMB
- NECO
- Other examinations

Do not force this structure when it would be unnatural.
"""
