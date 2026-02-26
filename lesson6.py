

restaurants = ['Buccees','Mcdonalds','Whataburger','iron chef','roadhouse']
print(restaurants[0:2])
restaurants[0:5:2] #slicing allows you to select specific parts of your list.
#formatted in same way as range (start, stop, step)
#slice from the tail end
restaurants[-2:] #gives the last two entries
#splicing and range functions are similar but different.
#range is a built in function giving a series of integers.
#slicing is an operation you can do on lists to give a part of the list.
new_list = restaurants
new_list.append('arbys')
new_list
restaurants

new_list = restaurants[:] #slices and seperates the two lists
new_list.remove('arbys')
new_list
restaurants

"""#for index in range(0,5,1):
    restaurants[index]=restaurants[index].titleprint(restaurants)"""

title_restaurants = [restaurant.title() for restaurant in restaurants]
print(restaurants)
print(title_restaurants)
#utilising a different type of system for capitalizing

#tuples
my_some = (1,2,3)
my_some[1]
nested = [(1,2),(3,4)]
nested[0]
type(nested[0])
