# Samuel Kisiel
# 26 January 2026
# Problem Set 2

# prob 1

"""
This function creates takesa list of tuples and returns them as a pair of
lists. The first list is that of payments, the second is that of the costs.
The point of this function is to seperate the tupled list into two lists.
"""


def build_logs(records):
    payments = []
    costs = []
    for payment, cost in records:
        payments.append(payment)
        costs.append(cost)
    return payments, costs

# prob 2


"""
This function is a demosntration of utilizing the index function.
The index function allows a user to input corrected data and modify the 
respective variables.
"""


def correct_entry(payments, costs, index: int, new_pay, new_cost):
    payments[index] = new_pay
    costs[index] = new_cost

# prob 3


"""
This function utilizes the pop task to create a list of 'removed' jobs.
This function creates an empty list and then appends removed jobs according to 
the indexed value.
"""


def remove_jobs(payments: float, costs: float, remove_indices: int):
    removed = []
    for i in sorted(remove_indices, reverse=True):
        removed.append((payments.pop(i), costs.pop(i)))
    return removed

# prob 4


"""
This function performs a basic calculation and rounds to two decimals.It 
calculates the profit of a given job based off of two lists, assembling it 
into a new list.
"""


def profits_list(payments, costs):
    profit = []
    for payment, cost in zip(payments, costs):
        profit.append(round(payment-cost, 2))
    return profit

# prob 5


"""
This function utilizes a previous function to accumalte profits according to 
the variables 'payments' and 'costs' to give a ranking of the most profitable 
jobs by profit.Utilizing an empty list called 'flipped' to flip tuples so that 
the index was first and the profit was second, the function correctly returns
the rankings in the right way. It then assembles a list of ranked jobs utilizing 
the reversed list, creating a proper function.
"""


def rank_jobs(payments, costs):
    profits = profits_list(payments, costs)  # use previous function

    flipped = []  # making a seperate string to flip the tuples

    for i in range(len(profits)):
        flipped.append((profits[i], i))
    flipped.sort(reverse=True)
    ranked = []
    for item in flipped:  # primary part of function for ranking
        ranked.append((item[1], item[0]))
    return ranked


test = rank_jobs([10.0, 20.0, 30.0], [2.0, 20.0, 25.0])
print(test)

# prob 6

"""
This function analyzes profit for a range of jobs along a certain index of
two parallel lists.It does so through setting up an index system, a window of 
payments, a window of costs, and a window of pofits.
The function returns a net profit of the span of the index requested by the 
input into the function, gives the most profitable job in the index given.
"""


def analyze_work_range(payments, costs, starting_index: int, count):
    end_index = starting_index + count  
    """
    setting up index system
    utilizing slice to start the index at startingindex and end at end_index
    """
    window_payments = payments[starting_index:end_index]
    window_costs = costs[starting_index:end_index]
    window_profits = []
    for i in range(len(window_payments)):
        profit = window_payments[i]-window_costs[i]
        window_profits.append((profit, starting_index + i))
    """
    The above code sets up the profit range that creates the system for reading
    the indices of the given strings.
    """
    most_profitable = max(window_profits)
    most_profitable_index = most_profitable[1]
    net_profit = round(sum(profit for profit, index in window_profits), 2)
    """
    this sets up the most profit utilising a sum function.
    """
    return f'Net ${net_profit:.2f}; most profitable job #{most_profitable_index}'
