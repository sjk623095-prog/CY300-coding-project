# 1) Outer dict plus inner containers
students = {}
students["S001"] = {
    "name": "Alex", "year": 2,
    "assignments": [], "notes": []
}
print("keys:", list(students.keys()))

# 2) Append nested dicts to a list field
students["S001"]["assignments"].append({"week": 3, "score": 92})
students["S001"]["notes"].append({"week": 3, "text": "Needs extra practice on loops"})
print("assignments:", len(students["S001"]["assignments"]), "notes:", len(students["S001"]["notes"]))

# 3) Chained access and safe reads
last = students["S001"]["assignments"][-1]
print("last score:", last["score"])
print("missing id safe read:", students.get("S999", {}).get("assignments", []))

# 4) Tiny loop over nested list
count = 0
for a in students["S001"]["assignments"]:
    count += 1
print("counted assignments:", count)
