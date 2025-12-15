import random

CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def generate_gatepass_code():
    part1 = "".join(random.choices(CHARS, k=4))
    part2 = "".join(random.choices(CHARS, k=4))
    return f"GP-{part1}-{part2}"

