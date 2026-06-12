import re


BLOCKED_PATTERNS = [

    r"ignore previous instructions",

    r"ignore all instructions",

    r"system prompt",

    r"hidden prompt",

    r"reveal prompt",

    r"show prompt",

    r"developer message",

    r"act as admin",

    r"act as dba",

    r"bypass security",

    r"disable guardrails",

    r"ignore security",

    r"password",

    r"database password",

    r"give me password",

    r"show password",

    r"reveal password",

    r"credentials",

    r"internal instructions",

    r"hidden rules",

    r"instructions before our conversation",

    r"what instructions",

    r"how were you instructed",

    r"reveal instructions",

    r"describe your rules",

    r"hidden behavior",

    r"internal behavior",

    r"database credentials",

    r"admin credentials",

    r"database password",

    r"db password",

    r"api key",

    r"secret key",

    r"access token",
]


def validate_user_input(question):

    question_lower = question.lower()

    for pattern in BLOCKED_PATTERNS:

        if re.search(
            pattern,
            question_lower
        ):

            raise ValueError(
                "Blocked by Input Guardrail"
            )

    return question

