# ---------- WAVE 1 ----------
# TODO 1: define rank and last_name
# TODO 2: build header string with f-string
# TODO 3: create a fixed string for the star line (20 chars)
# TODO 4: print the header between two lines of stars
# Swap Driver/Navigator Roles
# ---------- WAVE 2 ----------
# TODO 5: define strings for company, branch, major, hometown
# TODO 6: build an f-string for a "details block" using \t and \n
"""
You can create an f-string across many lines for better readability. There
is an implicit "line continuation" between parentheses.
Example:
a_long_string = (
f'The first line is {random_variable}.'
f'The second part is {yet_another_random_variable}.'
)
print(a_long_string)
"""
# TODO 7: print the details block
# TODO 8: go back through code and use string methods to ensure proper casing!

#def main():
    #rank = 'CPL'
    #ln = 'Kisiel'
    #starline = "*********************"
    #CO = 'E3'
    #BR = 'Aviation'
    #MAJ = 'Systems Engineering'
    #HT = 'Kerrville, TX'
    #biocard = f"{starline} \n CDT {rank} {ln} \n{starline}\n\t Company: {CO} \n\t Branch: {BR} \n\t Major: {MAJ} \n\t Hometown: {HT}"
    #print(biocard)
#main()
def main2():
    rank = input("Enter your rank: ")
    ln = input("Enter your last name: ")
    starline = "*********************"
    CO = input("Enter your company: ")
    BR = input("Enter your branch: ")
    MAJ = input("Enter your major: ")
    HT = input("Enter your hometown: ")
    biocard = f"{starline} \n CDT {rank} {ln} \n{starline}\n\t Company: {CO} \n\t Branch: {BR} \n\t Major: {MAJ} \n\t Hometown: {HT}"
    #question = input("Would you like to see your biocard? (y/n)")
    #if question = 'y'
    print(biocard)
main2()