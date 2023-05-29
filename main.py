import re

"""
0   1
a A b B
c   d
e   f
s S
p P
t
y z
"""

INTERACTIONS = {
    # Swap
    "1a": "a1",
    "0A": "A0",
    "1B": "B1",
    "0b": "b0",
    "0c": "c0",
    "1c": "c1",
    "0d": "d0",
    "1d": "d1",
    "0t": "t0",
    "1t": "t1",
    "pA": "Ap",
    "pB": "Bp",
    "pc": "cp",
    "pd": "dp",
    "Aa": "aA",
    "Bb": "bB",
    "0e": "e0",
    "1e": "e1",
    "ae": "ea",
    "Ae": "eA",
    "be": "eb",
    "Be": "eB",
    "ce": "ec",
    "de": "ed",
    "se": "es",
    "Se": "eS",
    "pe": "ep",
    "Pe": "eP",
    "te": "et",
    "0f": "f0",
    "1f": "f1",
    "af": "fa",
    "Af": "fA",
    "bf": "fb",
    "Bf": "fB",
    "cf": "fc",
    "df": "fd",
    "sf": "fs",
    "Sf": "fS",
    "pf": "fp",
    "Pf": "fP",
    "tf": "ft",

    # Interception
    "0a": "A",
    "1A": "a10",
    "Ba": "ba1",
    "1b": "B",
    "0B": "b01",
    "Ab": "ab0",

    # Forward
    "sa": "Sa",
    "sb": "Sb",
    "sP": "S",
    "0S": "sp0",
    "1S": "sp1",

    # Mismatch
    "pa": "a",
    "pb": "b",

    # Match
    "pt": "Pt",

    # Replacement
    "AP": "Pa",
    "BP": "Pb",
    "cP": "Pc0",
    "dP": "Pd1",

    # Rotation
    "0z": "ez",
    "1z": "fz",
    "ye": "y0",
    "yf": "y1",
}

INTERACTIONS_RE = re.compile((r'|').join(r'(?:' + re.escape(s) + r')' for s in INTERACTIONS))
def step(text):
    return INTERACTIONS_RE.sub(lambda m: INTERACTIONS[m.group()], text)
def prnt(text):
    # print(f'\r\x1b[2K{text}', end='')
    print(text)
def run(text):
    prnt(text)
    history = {text}
    while True:
        text = step(text)
        prnt(text)
        if text in history:
            break
        history.add(text)
    text = death(text)
    print()
    return text
def death(text):
    assert text.endswith('z')
    text = text[:-1]
    while True:
        t = step(text)
        same = t == text
        text = t
        prnt(text)
        if same:
            break
    assert text.startswith('y')
    text = text[1:]
    text = re.sub(r'[abcdSt]', '', text)
    prnt(text)
    return text
"""
result = run("y0110101011111010001111101010101011101010101001110100010110110101spbababaaccddcctz")
print("011010101111101000111110101010101110100011001110100010110110101")
"""
run("y0001111111000001111100000spbbbbbbbdddtz")
# run("y0110101011111010001111101010101011101010101001110100010110110101spbababaaccddcctz")

