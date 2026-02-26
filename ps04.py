# Samuel Kisiel
# 24 February 2026
# Problem Set 4

# Problem 1

"""
This function utilises a 'greedy coin change' while loop to create a dictionary
of denominations of coins (25, 10, 5, 1) and only pastes the items in the 
dictionary that have values. This utilises a while loop and then dictionary
logic with an if statement to ensure the output is according to the set rules.
"""


def make_change(cents: int) -> dict:

    # set up dictionary
    coin_dict = {25: 0, 10: 0, 5: 0, 1: 0}

    # set up greedy while loop that adds values to dictionary
    # plus subtracts from the int value of cents
    while cents > 0:
        if cents >= 25:
            coin_dict[25] += 1
            cents -= 25
        elif cents >= 10:
            coin_dict[10] += 1
            cents -= 10
        elif cents >= 5:
            coin_dict[5] += 1
            cents -= 5
        else:
            coin_dict[1] += 1
            cents -= 1

    # only return keys with values utilising dictionary logic and if statement
    coin_dict = {key: value for key, value in coin_dict.items() if value > 0}
    return coin_dict

# Problem 2


"""
This function reads values as lower or higher than the given lo or hi input 
variable from a 'values' list, then appends to a changed count. The clipped
values are then appended to a clipped_values string, and a list is returned
as a list of the clipped values and the changed count at the end.
"""


def clip_range(values: list[int], lo: int, hi: int):
    # set changed_count to 0
    changed_count = 0
    # Empty list of clipped values
    clipped_values = []

    # For loop for the values given, appends lo, hi, or value given whether or
    # not the value meets the criteria
    for value in values:
        if value < lo:
            clipped_values.append(lo)
            changed_count += 1
        elif value > hi:
            clipped_values.append(hi)
            changed_count += 1
        else:
            clipped_values.append(value)

    # returns new list
    return (clipped_values, changed_count)

# Problem 3


"""
This function adds to different dictionaries of numerical keys and values to 
create a single new dictionary of the combined sums. This is done through
creating a new dictionary, compiling keys through a union of all keys,
and then returning the value sum as long as it is not equal to zero.
"""


def add_sparse_vectors(v1: dict[int, int], v2: dict[int, int]):
    # creating a new dictionary
    new_dictionary = {}

    # getting a collection of a union of all keys
    all_keys = set(v1.keys()) | set(v2.keys())  # ChatGPT

    # for loop set up which adds the values of keys together

    for index in all_keys:
        value_sum = v1.get(index, 0) + v2.get(index, 0)

        # if statement sets so that the nonzero items are added to
        # the new dictionary
        if value_sum != 0:
            new_dictionary[index] = value_sum
    return new_dictionary

# Problem 4


"""
This function quantizes pixels by a certain equation and sets them to a certain
value in a new list as specified by the problem instructions. It utilizes a 
for loop and includes the step value as an input, appending the quantized
values to the new list.
"""


def quantize_pixels(pixels: list[tuple[int, int, int]], step: int):
    # Set up an empty list for qunatized pixels
    quantized = []

    # for loop for the pixels within the tuple
    for pixel in pixels:
        # setting the values for r, g, and b = to their respective points in the
        # pixels tuple.
        r, g, b = pixel

        # quantizing r, g, and b by the given formula
        quantized_r = (r // step) * step
        quantized_g = (g // step) * step
        quantized_b = (b // step) * step

        # designating new pixel as the new values
        new_pixel = (quantized_r, quantized_g, quantized_b)
        # appending the new pixel to the quantized list
        quantized.append(new_pixel)
    return quantized

# Problem 5


"""
This function gives the frequency of a word in a given string of text, returning
a dictionary of the amount of times a word (the key) was said. It eliminates
punctuation and lowers the text string so that the keys all count for the same 
letter combinations. To accomplish this it sets up an empty dictionary, a for
loop, and cleans the given textstring after it is lowered and split.
"""


def word_frequencies(text: str):

    # sets an empty dictioanry to append to later
    text_dict = {}
    # lowers all text within the text string
    text = text.lower()
    # splits text string into tokens
    tokens = text.split()
    for token in tokens:
        # strips the token of any punctuation
        cleaned = token.strip("!#$%&*,.:;?")

        # checks to make sure that the cleaned token is not empty
        if cleaned == "":
            continue  # continue allows the instance of cleaned to be skipped

        # utilizes the text dictionary and adds 1 to the text dict for that
        # given key
        text_dict[cleaned] = text_dict.get(cleaned, 0) + 1
        # returns text dict
    return text_dict

# Problem 6


"""
This function returns a boolean value of whether or not the given list of
numbers is a 'mountain' or not given the parameters that the mountain must
always ascend, reach a single peak, then descend numerically. It must
also be 3 or more values as a list. it utilizes if/else statements and indexing
throughthe list 'nums'.
"""


def is_mountain(nums: list):

    # checks if the list is of minimum length
    if len(nums) < 3:
        return False

    # tracking 'direction', since a valid mountain allows goes up
    going_down = False

    # iterates through the list by indexing through nums
    for i in range(len(nums) - 1):

        # if two adjacent numbers are equal, false
        if nums[i] == nums[i+1]:
            return False

        # if true- we are going up
        elif nums[i] < nums[i+1]:

            # if already descending (going down = true) return false
            if going_down:
                return False

        # if current number greater than next- going down
        else:  # nums[i] > nums[i+1]
            going_down = True

    # only return true if going down is true and num 0 is less than num 1
    return going_down and nums[0] < nums[1]
