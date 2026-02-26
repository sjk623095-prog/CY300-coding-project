# Samuel Kisiel
# 17 January 2026
# Problem Set 1

# prob 1
def num_556_ball(m4soldier: int) -> int:  # a simple input function to determine
    # m4 rounds needed per soldeir utilising simple python arithmetic.
    numberrounds = m4soldier * 210
    return numberrounds


# prob 2
def num_762_link(m240g, ag: int) -> int:  # function adds two different values
    # multiplied by respective 762 round counts to achieve a full  count of ammo
    num240 = m240g * 300
    numag = ag * 400
    numtotal = numag + num240
    return numtotal


# prob 3
def num_crates_required(totalrounds: int, rpc: int) -> int:  # function that evaluates
    # number of crates needed utilizing floor division and (a + b - 1)//b logic
    roundsincrate = (totalrounds + rpc - 1)//rpc
    return roundsincrate


# prob 4
def fuel_required(milestoobjective: float, mpg: float) -> float:  # function that gives
    # the necessary gallons needed for a field operation and rounds the float to
    # 2 decimal places. This allows for the return of approximate gallons.
    totdist = milestoobjective * 2
    totgal = totdist/mpg + 10
    return round(totgal, 2)


# prob 5
def report_header(unit_name: str, operation_name: str, headerwidth: int):  # function
    # that takes an operation name, a unit name, and creats a header. Utilizes
    # len() to determine amount of "=" needed to pad out the header after taking
    # headerwidth as an integer.
    message = operation_name.upper() + " - " + unit_name.upper()
    padding = headerwidth - len(message)
    leftpad = padding // 2
    rightpad = padding - leftpad
    header = "=" * leftpad + message + "=" * rightpad
    return header


# prob 6
# this function calls all of the previous functions, combining them together
# into a single string which can be printed as a composed document on the
# entrance of the required inputs. This is done with f strings and calling
# the functions with their new inputted values.
def mission_requirements(unit_name: str, operation_name: str, m4soldier: int, m240g: int, ag: int, vehicles: int, milestoobjective: float, mpg: float):
    mission = f"""{report_header(unit_name, operation_name, 60)}\nThis mission requires:\n  5.56 BALL: {num_crates_required(num_556_ball(m4soldier), 1680)} crate(s)\n  7.62 LINK: {num_crates_required(num_762_link(m240g, ag), 800)} crate(s)\n  FUEL: {fuel_required(milestoobjective, mpg)*vehicles} gallon(s)"""
    return mission


missiontest = mission_requirements(
    'CRUSHER BN', 'SILENT BUT DEADLY', 200, 50, 50, 30, 56.5, 10.1)
print(missiontest)
