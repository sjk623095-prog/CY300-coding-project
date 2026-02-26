"""courses = {"Cy300":"B", "SS201":"A"}
print(courses.get("SS201"))
print(courses.get("PY201","C"))

print(courses["PY201"])
courses["CY300"] = 'C'
print(courses)"""

course_list = [
    {"CY300":"B", "SS201":"A"},
    {"CY105":"C","PY201":"D"}
]

course_list1 = []

print(course_list[0].get("SS201"))
print(course_list[1].get("CY105"))

"""for courses in course_list:
    for course, grade in courses.items():
        print(course, grade)"""

"""for courses in course_list:
    for item in courses.items():
        print(item)
        #key = item[0]
        #value = item[1]
        key,value = item #multiple assignment
        print(key,value)
    """
#printing the lists out by assignment

for courses in course_list:
    for item in courses:
        print(item)

course_list[1][0] = 'CY305'
#referencing the second list and the first element in this list
print(course_list)

#ICE 1
groups = {}
def add_to_group(groups:dict[str,list[str]],key:str,item:str):
    if key not in groups:
        groups[key] = []
    groups[key].append(item)
add_to_group(groups,"b","cow")
print(groups)

def group_by_first_letter(words:list[str]):
    dict2 = {}
    for word in words:
        key = word.lower()[0]
        if key not in dict2:
            dict2[key] = []
        dict2[key].append(word.lower())
    return dict2
example = group_by_first_letter(["Applebees","Gorge","Fred","Helldivers","Heck","Greg","greg","don"])
print(example)
        

def build_profiles(names:list[str],ages:list[int]):
    profiles = {}
    for i in range(len(names)): #for loop for integers of the lists given
        name = names[i] #name = name in dictionary in the i'th place
        age = ages[i] #age = age in dictionary in the i'th place
        profiles[name] = {"age": age} #profiles = profile according to name as a key, sets a dict with "age" as age
    return profiles #returns profiles

names = ["Ada", "Bob"]
ages = [20, 19]

build_profiles(names, ages)

