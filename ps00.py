# 1. COMPLETE THIS SKELETON  (first taste of a unit-testable function)
def circle_area(radius: float) -> float:
    area = 3.14159 * radius**2
    return area
circlearea = circle_area(1)
"""This is a function that gives the area of a circle on a given input, creating
a proper system for the creation of a circle"""

# 2–4. WRITE FROM SCRATCH  (students supply def, params, docstring, return)
#TODO   adjusted_celsius(temp_f)
def adjust_celsius(temp_f: float) -> float:
    adjusted = (temp_f-32) * 5/9
    bias = adjusted + 2
    return bias

#TODO   hours_from_minutes(total_minutes)
#TODO   leftover_minutes(total_minutes)


'''
The block below runs **only** when you execute this file directly
(e.g., `python 03_ice_ps00_starter.py`). When Gradescope imports your
functions for testing, __name__ will *not* be "__main__", so this
self-check code is skipped by the autograder.

In other words, do all your local testing in a block of code like the one below
'''
if __name__ == "__main__":
    # your test code goes here.
    pass

