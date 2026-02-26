"""
CY300 Lists III - List Comprehensions Quick Tour
"""

print("\n--- 1) Transform (numbers) ---")
nums = [1, 2, 3, 4, 5]
squares = [n * n for n in nums]
halves = [n / 2 for n in nums]
print(squares)  # [1, 4, 9, 16, 25]
print(halves)   # [0.5, 1.0, 1.5, 2.0, 2.5]

print("\n--- 2) Transform (strings) ---")
raw = ["  ada ", "BOB", "eVe  "]
clean = [s.strip().title() for s in raw]
print(clean)  # ['Ada', 'Bob', 'Eve']

# Preview only — we haven't covered if/conditions formally yet.
print("\n--- 3) Filter (preview) ---")
evens = [n for n in range(10) if n % 2 == 0]
short_names = [s for s in clean if len(s) <= 3]
print(evens)       # [0, 2, 4, 6, 8]
print(short_names) # ['Ada', 'Bob', 'Eve']

print("\n--- 4) Filter + transform in one pass ---")
curved_capped = [min(x + 5, 100) for x in [72, 88, 91, 100] if x > 0]
print(curved_capped)  # [77, 93, 96, 100]

print("\n--- 5) Comprehension vs loop (readability chooses) ---")
triples = [n * 3 for n in nums]
print(triples)  # [3, 6, 9, 12, 15]

triples_loop = []
for n in nums:
    triples_loop.append(n * 3)
print(triples_loop)  # [3, 6, 9, 12, 15]


############
# CODE STYLE
############

# BAD: Hard to scan
nums=[1,2,3]
def total(x):print(sum(x))
def describe(data): print(f"Total: {sum(data)} Avg/day: {sum(data)/len(data)} Max: {max(data)} Min: {min(data)} All: {data}")
for n in nums:
  print(n)  # mixed indentation and cramped layout


# GOOD: Clear and consistent
nums = [1, 2, 3]

def total(values):
    """Return the sum."""
    s = 0
    for v in values:            # 4-space indentation
        s += v
    return s


def describe(data):
    """Pretty print a short summary."""
    total_minutes = total(data)
    average = total_minutes / len(data)

    # Wrap long line under the ruler using parentheses
    msg = (
        f"Total: {total_minutes}  Avg/day: {average:.1f}  "
        f"Max: {max(data)}  Min: {min(data)}"
    )
    print(msg)
