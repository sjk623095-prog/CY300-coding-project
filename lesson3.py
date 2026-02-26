"""""
#numbers come in integers and floats and can be added, subtracted, multiplied, divided, floor-divided, and exponentiated.
floordiv = 10//4
#5//2 = 2 because the division removes the remainder
#modulo is when you do something like 5%2, to find the remainder. 
mod = 10%4
print(floordiv)
print(mod)
math = (-5)**2
print(math)
"""
#functions:

def make_big_number(small_num:float) -> float:
    big_num = small_num ** 5 
    return big_num
big_number = make_big_number(5)
#print(big_number)

def add(num1,num2:int) -> int:
    add_num = num1 + num2
    return add_num
addition = add(4,4)
print(addition)
