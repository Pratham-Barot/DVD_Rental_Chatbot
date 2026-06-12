import re


BLOCKED_OUTPUT_PATTERNS = [

    r"system prompt",

    r"developer message",

    r"hidden instructions",

    r"internal instructions",

    r"api key",

    r"secret key",

    r"access token",

    r"database password",

    r"db password",

    r"postgres password",

    r"environment variable",

    r"\.env",

    r"langsmith api key",

    r"gemini api key",
]


def validate_output(response):

    response_lower = response.lower()

    for pattern in BLOCKED_OUTPUT_PATTERNS:

        if re.search(
            pattern,
            response_lower
        ):

            raise ValueError(
                "Blocked by Output Guardrail"
            )

    return response