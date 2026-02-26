#If statements
#Operators: == (equivalancy), <, >, <=, >=, !=
#Operators result in a boolean value (True/False)
#Logical operators: not, and, or, not

x=5
5>3
x>3
x>8
x == x
"Tim" == "tim"

#these all return booleans (except for x=5)

#logical Operators;

name = "tim"
name == "zach" and x >3
x = 5
name = "tim"
name == "zach" or x > 3

not name == "zach" and x > 3
not name == "zach" and x > 3

#if statements
"""if conditional_is_true:
    execute code..."""

cadets = ['tim', 'alex','nick']
print('tim' in cadets)

#conditionals

name = 'tim'
if name in cadets:
    print("yes")
else:
    print("No")

answer = 10
guess = 5
if guess < answer:
    print("Too low")
elif guess == answer:
    print("Right!")
else:
    print("Too High")


#Practice

def is_confirmed(answer: str) -> bool:
    if answer.lower() == "yes":
        return True
    else:
        return False
is_confirmed("yeS")

def pass_fail(score:int) -> str:
    if score >= 70:
        return "pass"
    else:
        return "fail"
pass_fail(70)

def temp_label(temp:int) -> str:
    if temp <50:
        return "cold"
    elif temp <80:
        return "ok"
    else:
        return "hot"
temp_label(10)

def grade_letter(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
grade_letter(30)

"""def check_permissions(allowed: list[str], requested: list[str]) -> list[str]:
    blocked = []
    if allowed != requested:
        blocked.append(allowed != requested)    
        allowed.remove(blocked)
        return f"blocked: {blocked}"
    else:
        return f"ok: {allowed}""""


def check_permissions(allowed: list[str], requested: list[str]) -> list[str]:
    result = []
    for item in requested:
        if item in allowed:
            result.append(f"ok: {item}")
        else:
            result.append(f"blocked: {item}")
    return result
check_permissions(["read"],["read","delete"])

def label_scores(scores:list[int]) -> list[str]:
    