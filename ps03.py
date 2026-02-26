# Samuel Kisiel
# 4 February 2026
# Problem Set 3

# Problem 1

"""
This function allows the addition of multiple round results to be added
to a given dictionary (scores_dict) and the tuple contains a name and a score.
"""


def add_multiple_scores(round_results: tuple, scores_dict: dict):
    for name, score in round_results:  # tuple unpacking
        scores_dict[name] = scores_dict.get(name, 0) + score


# Problem 2

"""
This function allows the removal of multiple golfers as a list from a given 
dictionary (scores_dict) and updates the dictionary.
"""


def remove_multiple_golfers(names_to_remove: list, scores_dict):
    for names in names_to_remove:  # for statement for determinine if the name is in the names to remove
        if names in scores_dict:
            key = names
            del scores_dict[key]
    return scores_dict


# Problem 3

"""
A simple function to determine the relative score when given a raw and par score.
"""


def relative_par_score(raw_score, par_score):
    if raw_score == par_score:
        return 0
    else:
        relative_par = raw_score-par_score
        return relative_par

# Problem 4


"""
This function creates a sorted leaderboard as a list of names based off of
their scores.It uses a for loop and the previous problem 3 relative par score
function to determine the places of the individuals within the leaderboard.
"""


def gen_round_leaderboard(scores: dict, par_scores: int):
    leaderboard = []
    for name, total_score in scores.items():  #Finding the key
        difference = relative_par_score(total_score, par_scores)
        leaderboard.append((difference, name))
    leaderboard.sort()
    return leaderboard

# Problem 5


"""
This function combines functions from problems 1 and 4 to create a cohesive 
top 5 leaderboard for golfing scores inputted as a list of tuples. It sets 
up an empty dictionary, empty list, sets several variables, and then utilizes
a for loop to creat the leaderboard itself.
"""


def top5_leaderboard(name_and_round_score: list[tuple[str, int]], number_rounds: int):
    scores_dict = {}  # creates an empty dictionary
    # utilizes the add_multiple_scores_ to append to dictionary
    add_multiple_scores(name_and_round_score, scores_dict)
    tournament_par = number_rounds * 72
    # creates a leaderboard for the round according to the previous function
    leaderboard = gen_round_leaderboard(scores_dict, tournament_par)
    top5 = []  # creates an empty list of the top 5 scores
    rank = 1  # sets the rank counter at 1
    for entry in leaderboard:  # for loop for the given entries in the leaderboard
        if rank > 5:
            break
        relative_score, name = entry  # setting up what entry is
        if relative_score == 0:  # if statement for if the relative score is 0
            display_score = 'E'
        else:  # else, execute as normal
            display_score = relative_score
        top5.append((rank, name, display_score))
        rank += 1  # add to rank and repeat for loop
    return top5
