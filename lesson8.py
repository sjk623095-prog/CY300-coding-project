#dictionaries
inventory1 = {"Arrows": 10, "Potions": 5, "Gold": 20}
"""inventory.get('Arrows')
inventory["Arrows"]
'Arrows' in inventory
'sword' in inventory
print(inventory.get('sword')) #will print none
print(inventory.get('sword','hello')) #will print the second value because it beccomes the default since there is no 'sword'
print(inventory.get('Arrows','hello')) #gives the default value back (1st val)"""


#adding and removing to inventories
"""inventory['Arrows'] = 15
print(inventory)
inventory['Arrows'] = inventory['Arrows'] + 5
inventory['Sword'] = 1
print(inventory)
inventory['sword'] = inventory['sword'] - 1
print(inventory)"""
#removing items
#inventory.pop('Arrows')

inv = {"Arrows": 20, "Potions": 5, "Gold": 20,"Crafting Supplies": 50}
#ICE
#example functions for using dictionaries
def get_qty(inv: dict[str, int], item: str) -> int:
    """Return the quantity for item, or 0 if missing."""
    return inv.get(item, 0)
get_qty(inv,"Arrows")


def add_item(inv: dict[str, int], item: str, amount: int) -> None:
    """Add to the count for item (create it if missing)."""
    inv[item] = inv.get(item, 0) + amount
add_item(inv,"Arrows",100)
print(inv)


def set_item(inv: dict[str, int], item: str, qty: int) -> None:
    """Set the item quantity, overwriting if it already exists."""
    inv[item] = qty
set_item(inv, "Wand",1)
print(inv)

def use_expendable(inv:dict[str, int], item: str, amount: int) -> None:
    allowed = {"Arrows","Gold","Potions","Crafting Supplies"}
    if item in inv and item in allowed:
        inv[item] = inv.get(item,0) - amount
        if inv[item] <= 0:
            del inv[item]
    else:
        print("You cannot expend this item!")
use_expendable(inv,"Arrows",20)
use_expendable(inv,"Wand",1)

print(inv)

#PT 2:
def use_one(inv: dict[str, int], item: str) -> bool:
    """Use one of the item. Remove if it hits 0. Return True if used, False if missing."""
    if inv.get(item, 0) == 0:
        return False
    inv[item] -= 1
    if inv[item] == 0:
        del inv[item]  # remove the key completely
    return True
use_one(inv,"Arrows")
print(inv)

def summary_lines(inv: dict[str, int]) -> list[str]:
    """Return a list of lines like '[3] potion', sorted by item name."""
    lines = []
    for item in sorted(inv.keys()):
        lines.append(f"[{inv[item]}] {item}")
    return lines
print(summary_lines(inv))
summary_lines(inv)


def can_craft(inv: dict[str, int], recipe: dict[str, int]) -> bool:
    """Return True if inv has enough quantity for every recipe item."""
    for item, needed_qty in recipe.items():
        if inv.get(item, 0) < needed_qty:
            return False
    return True
recipe1 = {"Arrows": 10}
can_craft(inv,recipe1)
recipe2 = {"Crafting Supplies":10,"Arrows": 10}
can_craft(inv,recipe2)

#not working
def craft(inv: dict[str, int], recipe: dict[str, int]):
    for item in recipe:
        inv[item] -= recipe: dict[str, int]
craft(inv,recipe2)