#revisiting lists
#lesson: For loops, loops/iterations
"""restaurants = ['Buccees','Mcdonalds','Whataburger','iron chef','roadhouse']

for restaurant in restaurants:
    restaurants[0]=restaurants[0].title()

for index in range(0,5,1):
    restaurants[index] = restaurants[index].title()
print(restaurants)

numbers = [1,5,3,4,6]
for number in numbers:
    square = number ** 2
    print(square)
    print(numbers)"""
#ranges: Start, stop, step
#range(start,stop,step)
"""for num in range(2,12,2):
    print(num)


for num1 in range(1,12,2):
    print(num1)
for num2 in range(4,13,4):
    print(num2)
for num3 in range(5,0,-1):
    print(num3)"""
def build_odds(n:int) -> int:
    list =[]
    num = n
    for num in range(1,2*n+1,2):
        list.append(num)
    return list
print(build_odds(5))

"""def count_divisible(nums:int,k:int):
    remainders = [n % k for n in nums]
    return remainders.count(0)
test = count_divisible([2,4,5,6,7,9,12],3)
print(test)"""
``