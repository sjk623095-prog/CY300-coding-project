"""
ICE: Run Distance Analyzer

Inputs are numeric strings (ints or floats). Use list iteration, slicing, and
indexing. Round to 1 decimal anywhere you perform division
(e.g., moving averages, per-day averages).
"""

RAW = ["0", "2.5", "3", "4.2", "5", "0", "6.3",
       "7.0", "4", "3.8", "0", "2.2", "6", "8.1"]


def parse_distances(vals: list[str]) -> list[float]:
    dist = [float(num) for num in vals]
    return dist
    """
    Convert each string to a float, preserving order.

    Examples:
    # >>> parse_distances(["0", "2.5", "3"])
    [0.0, 2.5, 3.0]
    """
    #raise NotImplementedError("parse_distances not implemented yet")
print(parse_distances(RAW))
RAW = parse_distances(RAW)

def week_sums(vals: list[float]) -> list[float]:
    sums = []
    for i in range(0,len(vals),7):
        week_chunk = vals[i:i+7]
        sums.append(sum(week_chunk))
    return sums
    """
    Sum each consecutive block of 7 days. The last week may be short.
    No rounding required here.

    Examples:
    #>>> week_sums([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 10.0, 20.0])
    [28.0, 30.0]
    """
    #raise NotImplementedError("week_sums not implemented yet")
print(week_sums(RAW))


def moving_avg_3(vals: list[float]) -> list[float]:


    """
    Three-day simple moving average for every full window.
    Round each average to 1 decimal.

    Examples:
    #>>> moving_avg_3([0.0, 3.0, 6.0, 9.0])
    [3.0, 6.0]
    """
    #raise NotImplementedError("moving_avg_3 not implemented yet")

def best_day_of_week(vals: list[float]) -> int:
    """
    Treat index 0 as day 0 of the week. For each day 0..6, total vals[d], vals[d+7], ...
    Return the day index with the largest total. If there is a tie, return the smallest index.

    Examples:
    >>> best_day_of_week([1.0, 9.0, 1.0, 1.0, 1.0, 1.0, 1.0, 5.0])
    1
    """
    raise NotImplementedError("best_day_of_week not implemented yet")


def summary(vals: list[float]) -> tuple[int, float, float, float]:
    """
    Return (total_days, total_miles, max_day, average_day).
    Round average_day to 1 decimal.

    Examples:
    >>> summary([1.0, 2.0, 3.0, 4.0])
    (4, 10.0, 4.0, 2.5)
    """
    raise NotImplementedError("summary not implemented yet")


def main() -> None:
    try:
        miles = parse_distances(RAW)
        print("miles:", miles)
        print("week_sums:", week_sums(miles))
        print("moving_avg_3:", moving_avg_3(miles))
        print("best_day_of_week:", best_day_of_week(miles))
        print("summary:", summary(miles))
    except NotImplementedError as e:
        print(e)
if __name__ == "__main__":
    main()
