"""
Demo Code for Lists 1 - Introduction to Lists

   Covered:
   - Creating list literals
   - Indexing (positive & negative)
   - Modifying, appending, inserting
   - Deleting with del, pop(), remove()
   - Sorting & reversing
   - len() inspection
   - Two tiny functions to reinforce 'return, not print'
"""


############################
# 1. Create and Inspect
############################
players = ["Ana", "Ben", "Cai"]
empty_list = []
empty_list2 = list()

print(players)               # ['Ana', 'Ben', 'Cai']
print(players[0])            # Ana  (zero-based index)
print(players[-1])           # Cai  (negative index = last)
print(players[-2])           # Ben  (negative indices count all the way down)

print("There are", len(players), "players.")   # len() for size


############################
# 2. Modify, Append, Insert
############################
players[1] = "Bea"           # overwrite
print(players)               # ['Ana', 'Bea', 'Cai']

players.append("Dan")        # add to end
players.insert(0, "Zoe")     # add to front (index 0)
print(players)         # ['Zoe', 'Ana', 'Bea', 'Cai', 'Dan']


############################
# 3. Delete, Pop, Remove
############################
del players[0]               # delete by index
popped = players.pop()       # pop last and save
print("Popped:", popped)     # Dan
players.remove("Bea")        # remove by value
print(players, "\n")         # ['Ana', 'Cai']


############################
# 4. Sorting & Reversing
############################
players.append("Ben")
print("Original order: ", players)              # ['Ana', 'Cai', 'Ben']

print("Temporarily sorted:", sorted(players))   # non-destructive
print("After sorted():   ", players)            # original unchanged

players.sort()                                  # in-place alphabetical
print("After sort():     ", players)

players.reverse()                               # reverse current order
print("After reverse():  ", players, "\n")



############################
# 4. Counting
############################
print(players)
num_players = len(players)
print(f'There are {num_players} players')

print(f'{players.count('Dan')} are named Dan.')