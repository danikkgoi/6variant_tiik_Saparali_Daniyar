import math

N_ALPHABET = 87
PREFIX_CODE = {"A": "0", "B": "10", "C": "110", "D": "111"}
MESSAGE = "0101101110"

INFO_BITS = "0011"
ERROR_POSITION = 5

def min_uniform_bits(n: int) -> int:
    k = 0
    while 2 ** k < n:
        k += 1
    return k


def satisfies_fano(code: dict) -> bool:
    words = list(code.values())
    return not any(a != b and b.startswith(a) for a in words for b in words)

def decode_prefix(message: str, code: dict) -> str:
    inverse = {v: k for k, v in code.items()}
    result, buf, parts = [], "", []
    for bit in message:
        buf += bit
        if buf in inverse:
            result.append(inverse[buf])
            parts.append(buf)
            buf = ""
    if buf:
        raise ValueError("Декодталмай қалған қалдық: {buf}")
    return "".join(result), parts


def seminar_8():
    print("=" * 60)
    print("Префикстік кодтар. Фано шарты")
    print("=" * 60)
    k = min_uniform_bits(N_ALPHABET)
    print(f"1-есеп. N = {N_ALPHABET}")
    print(f"  2^{k-1} = {2**(k-1)} < {N_ALPHABET} <= 2^{k} = {2**k}")
    print(f"  Жауап: k = {k} бит")
    print(f"2-есеп. Код: {PREFIX_CODE}")
    print(f"  Фано шарты орындала ма? -> {satisfies_fano(PREFIX_CODE)}")
    decoded, parts = decode_prefix(MESSAGE, PREFIX_CODE)
    print(f"  Хабар: {MESSAGE}")
    print(f"  Бөлінуі: {' | '.join(parts)}")
    print(f"  Жауап: {decoded}")

def check_bits_count(n_i: int) -> int:
    n_k = 1
    while 2 ** n_k < n_i + n_k + 1:
        n_k += 1
    return n_k


def is_power_of_two(x: int) -> bool:
    return x & (x - 1) == 0


def check_positions(p: int, n: int) -> list:
        return [i for i in range(1, n + 1) if i & p]


def hamming_encode(info: str, verbose: bool = True) -> str:
    n_i = len(info)
    n_k = check_bits_count(n_i)
    n = n_i + n_k
    ctrl = [2 ** i for i in range(n_k)]
    a = [None] * (n + 1)
    it = iter(info)
    for pos in range(1, n + 1):
        if not is_power_of_two(pos):
            a[pos] = int(next(it))
    if verbose:
        layout = " ".join("_" if a[i] is None else str(a[i]) for i in range(1, n + 1))
        print(f"  n_i={n_i}, n_k={n_k}, n={n}; бақылау позициялары: {ctrl}")
        print(f"  Макет: C = {layout}")
    for p in ctrl:
        pos = [i for i in check_positions(p, n) if i != p]
        a[p] = sum(a[i] for i in pos) % 2
        if verbose:
            left = " ⊕ ".join(f"a{i}" for i in pos)
            vals = " ⊕ ".join(str(a[i]) for i in pos)
            print(f"  a{p} = {left} = {vals} = {a[p]}")
    return "".join(str(a[i]) for i in range(1, n + 1))


def hamming_syndrome(word: str, verbose: bool = True) -> int:
    n = len(word)
    n_k = 0
    while 2 ** n_k < n + 1:
        n_k += 1
    a = [None] + [int(c) for c in word]
    E = []
    for i in range(n_k):
        p = 2 ** i
        pos = check_positions(p, n)
        e = sum(a[j] for j in pos) % 2
        E.append(e)
        if verbose:
            left = " ⊕ ".join(f"a{j}" for j in pos)
            vals = " ⊕ ".join(str(a[j]) for j in pos)
            print(f"  E{i+1} = {left} = {vals} = {e}")
    s = sum(e << i for i, e in enumerate(E))
    if verbose:
        bits = "".join(str(e) for e in reversed(E))
        terms = " + ".join(f"{e}·2^{i}" for i, e in enumerate(E))
        print(f"  S = E{n_k}...E1 = {bits}₂ = {terms} = {s}₁₀")
    return s


def flip(word: str, pos: int) -> str:
    i = pos - 1
    return word[:i] + ("1" if word[i] == "0" else "0") + word[i + 1:]


def seminar_9():
    print("n" + "=" * 60)
    print("Кедергіге төзімді кодтау. Хэмминг коды")
    print("=" * 60)
    print("1-есеп. Ақпараттық комбинация: {INFO_BITS}")
    C = hamming_encode(INFO_BITS)
    print(f"  Жауап: C = {C}")

    print("2-есеп. {ERROR_POSITION}-разряд бұрмаланды")
    C_err = flip(C, ERROR_POSITION)
    print(f"  C* = {C_err}")
    s = hamming_syndrome(C_err)
    print(f"  Қате разряд нөмірі: {s}")
    fixed = flip(C_err, s) if s else C_err
    print(f"  Түзетілген: {fixed}  (бастапқы C-мен сәйкес: {fixed == C})")


if __name__ == "__main__":
    seminar_8()
    seminar_9()
