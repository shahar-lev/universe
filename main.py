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
    # print(text)
    pass

def run(text):
    prnt(text)
    last = text
    count = 0
    epoch = 1
    while True:
        text = step(text)
        if text == last:
            break
        count += 1
        if count == epoch:
            last = text
            epoch <<= 1
    text = death(text)
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
    assert not re.search(r'[efpP]', text)
    text = text.replace('A', '0')
    text = text.replace('B', '1')
    prnt(text)
    return text

def simulate(text, interactions):
    start = '1000'
    marker = ''
    alphabet = sorted(set(text) | {c for x, y in interactions.items() for c in x + y} | {marker})
    idx = 0
    alpha_to_chain = {}
    for a in alphabet:
        while True:
            candidate = f'{idx:b}'
            idx += 1
            if start not in candidate:
                alpha_to_chain[a] = candidate
                break
    bitlen = max(len(chain) for chain in alpha_to_chain.values())
    codelen = len(start) + bitlen
    alpha_to_chain = {x: start + (bitlen - len(y)) * "0" + y for x, y in alpha_to_chain.items()}
    phrase_to_chain = lambda phrase: ''.join(alpha_to_chain[c] for c in phrase)
    marker_chain = alpha_to_chain[marker]
    input_text = marker_chain + phrase_to_chain(text)
    interaction_to_chain = lambda x, y: ('sp' +
        phrase_to_chain(x).replace('0', 'a').replace('1', 'b') +
        phrase_to_chain(y).replace('0', 'c').replace('1', 'd') +
        't'
    )
    whole_text = 'y' + input_text + ''.join(interaction_to_chain(x, y) for x, y in interactions.items()) + 'z'
    result = run(whole_text)
    pos = result.find(start)
    assert pos != -1
    result = result[pos:] + result[:pos]
    pos = result.find(marker_chain)
    assert pos != -1
    result = result[pos + len(marker_chain):] + result[:pos]
    chain_to_alpha = {y: x for x, y in alpha_to_chain.items()}
    assert (len(result) % codelen) == 0
    pos = 0
    output = []
    while pos < len(result):
        output.append(chain_to_alpha[result[pos:pos + codelen]])
        pos += codelen
    output = ''.join(output)
    prnt(output)
    return output


# run("y0001111111000001111100000spbbbbbbbdddtz")
# run("y0110101011111010001111101010101011101010101001110100010110110101spbababaaccddcctz")
assert simulate("I love my life", interactions={"life": "lie", "my lie": "his lie", "love his": "love their"}) == 'I love their lie'
assert simulate("+0100101101=", interactions={
    '+00': '0+',
    '+01': '1+',
    '+10': '1+',
    '+11': '1p',
    'p00': '1+',
    'p01': '0p',
    'p10': '0p',
    'p11': '1p',
    '+=': '',
    'p=': '1',
}) == '101101'
