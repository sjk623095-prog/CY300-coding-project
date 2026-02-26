def phonetic_encoder(s):
    """
    >>> phonetic_encoder("BAd13ACE2")
    ['bravo', 'alpha', 'delta', 'won', 'tree', '<break>', 'alpha', 'charlie', 'echo', 'two']
    >>> phonetic_encoder("abcde123")
    ['alpha', 'bravo', 'charlie', 'delta', 'echo', '<break>', 'won', 'two', 'tree']
    >>> phonetic_encoder("ZZ!1")
    ['won']
    """
    # Map supported characters to NATO words.
    alpha = {
        'a': 'alpha', 'b': 'bravo', 'c': 'charlie', 'd': 'delta', 'e': 'echo',
        '1': 'won', '2': 'two', '3': 'tree'
    }
    tokens = []
    for ch in s:
        key = ch.lower()
        if key in alpha:
            tokens.append(alpha[key])

    out = []
    for idx in range(len(tokens)):
        out.append(tokens[idx])
        # Add <break> after each group of 5, except after the final group.
        if ((idx + 1) % 5 == 0) and (idx != len(tokens) - 1):
            out.append('<break>')
    return out


def string_accumulator(s):
    """
    >>> string_accumulator("12ab34cd11115e9")
    '11115'
    >>> string_accumulator("a9b99c")
    '99'
    >>> string_accumulator("abc")
    ''
    """
    best_sum = -1
    best_run = ""

    cur_sum = 0
    cur_run = ""

    for ch in s:
        if ch.isdigit():
            cur_sum += int(ch)
            cur_run += ch
        else:
            if cur_run != "":
                if cur_sum > best_sum:
                    best_sum = cur_sum
                    best_run = cur_run
            cur_sum = 0
            cur_run = ""

    # commit tail run
    if cur_run != "":
        if cur_sum > best_sum:
            best_sum = cur_sum
            best_run = cur_run

    if best_sum < 0:
        return ""
    return best_run


def run_length_encode(data):
    """
    >>> run_length_encode("aaaa")
    '4a'
    >>> run_length_encode("aabb")
    '2a2b'
    >>> run_length_encode("abab")
    '1a1b1a1b'
    >>> run_length_encode("")
    ''
    """
    if data == "":
        return ""
    result = ""
    count = 1
    prev = data[0]
    for i in range(1, len(data)):
        ch = data[i]
        if ch == prev:
            count += 1
        else:
            result += str(count) + prev
            prev = ch
            count = 1
    result += str(count) + prev
    return result


def execute_cook_queue(pantry, queue):
    """
    >>> pantry = {"flour": 500, "eggs": 4, "milk": 300}
    >>> pancakes = ("pancakes", {"flour": 120, "eggs": 1, "milk": 100})
    >>> omelet = ("omelet", {"eggs": 2, "milk": 50})
    >>> execute_cook_queue(pantry, [pancakes, omelet])
    ['pancakes', 'omelet']
    >>> pantry
    {'flour': 380, 'eggs': 1, 'milk': 150}
    >>> pantry = {"flour": 200, "eggs": 2}
    >>> bread = ("bread", {"flour": 150})
    >>> cake = ("cake", {"flour": 100, "eggs": 3})
    >>> execute_cook_queue(pantry, [bread, cake])
    ['bread']
    >>> pantry
    {'flour': 50, 'eggs': 2}
    """
    cooked = []
    for recipe in queue:
        name = recipe[0]
        needs = recipe[1]

        can_make = True
        for item in needs:
            if item not in pantry or pantry[item] < needs[item]:
                can_make = False
                break

        if can_make:
            for item in needs:
                pantry[item] -= needs[item]
            cooked.append(name)

    return cooked


def min_distance(lst):
    """
    >>> min_distance([7, 1, 3, 4, 1, 7])
    (3, 1)
    >>> min_distance([1, 2, 3, 4])
    (-1, None)
    >>> min_distance([1, 1, 2, 2])
    (1, 1)
    >>> min_distance([5, 2, 5, 5])
    (1, 5)
    """
    best_dist = None
    best_elem = None
    best_first_idx = None

    n = len(lst)
    for i in range(n):
        for j in range(i + 1, n):
            if lst[i] == lst[j]:
                dist = j - i
                if best_dist is None or dist < best_dist:
                    best_dist = dist
                    best_elem = lst[i]
                    best_first_idx = i
                elif dist == best_dist and i < best_first_idx:
                    best_elem = lst[i]
                    best_first_idx = i

    if best_dist is None:
        return (-1, None)
    return (best_dist, best_elem)
