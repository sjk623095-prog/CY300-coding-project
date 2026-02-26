# In addition to strings, numbers are the most basic of data types in Python
# Numbers come in two types, integers and floats (decimals)

# You can add(+), subtract (-), divide (/), and multiply (*) 
print(3 + 4)
print(3 - 4)
print(4 / 2)    # Division always returns a float
print(4 * 2)

# Exponentation (**) is also possible 
print(4 ** 2)

# Order of operations behave according to PEMDAS
print( (2 + 3) ** 2)    # 2+3=5, 5**2 = 25

# Any number with decimal points is a float
print(0.1 + 0.1)
print(4.5 - 2.3)
print(2.2 * 2.5)
print(11.2 / 0.5)

# Sometimes floats behave oddly, due to floating point precision
# Python does its best representing the precise result and is usual unconcerning
print(.2 + .1)
print(3 * .1)

# When we mix integers and floats, the results are floats
print(1 + 1.0)
print(2 * 5.0)

# Division always returns a float
print(6 / 2)


# Initiating variables can often span many lines making code less readable
# Multiple assignment allows the assignment of many values in one line
a, b, c = 1, 2, 3
print(a, b, c)

#############
# FUNCTIONS #
#############

# Define a function
def create_full_name(first:str, last:str) -> str:
    """Returns a first and last name capitalized and as a single parameter """
    combined = f'{first.capitalize()} {last.capitalize()}'
    return combined


# Call the function and assign the return value to a variable
full_name = create_full_name('sylvanus', 'thayer')
print(full_name)        # Sylvanus Thayer

# we can also use the return value inside functions, like print
# but now the value returned from create_full_name() is unsaved
print(create_full_name('george', 'washington'))

############
# COMMENTS #
############

# Single line comments are denoted with the hash mark (#)
# Anything after a # is ignored on that line only
print('Comments are nice')    # Comments can be after executable code


# The Zen of Python is the Python community's philosophy
# It can be viewed by running `import this`
import this