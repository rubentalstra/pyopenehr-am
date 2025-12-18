import random
import string

from openehr_am.adl.parser import parse_adl
from openehr_am.odin.parser import parse_odin


def _random_text(rng: random.Random, *, max_len: int) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation + " \t\n"
    n = rng.randint(0, max_len)
    return "".join(rng.choice(alphabet) for _ in range(n))


def test_fuzz_no_crash_adl() -> None:
    rng = random.Random(0)
    for i in range(300):
        text = _random_text(rng, max_len=400)
        parse_adl(text, filename=f"fuzz_adl_{i}.adl")


def test_fuzz_no_crash_odin() -> None:
    rng = random.Random(0)
    for i in range(300):
        text = _random_text(rng, max_len=400)
        parse_odin(text, filename=f"fuzz_odin_{i}.odin")
