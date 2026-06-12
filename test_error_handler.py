from utils.error_handler import (
    get_friendly_error
)

print(
    get_friendly_error(
        "Sensitive columns blocked: {'email'}"
    )
)