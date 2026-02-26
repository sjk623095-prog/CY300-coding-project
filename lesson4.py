"""
cadets = ['mac','jaxson','gael','nick']
print(cadets[1]) #referencing jaxson
cadets[1] = 'zach'
print(cadets[1])
cadets.append('jaxson')
print(cadets)
cadets.insert(3, 'tay')
print(cadets)
print(cadets[4])
name = cadets.pop(4) #pop removes a name but can be saved as a variable
print(name)
print(cadets)

#remove

cadets.remove('mac')
print(cadets)
cadets.insert(0,'mac')
cadets.append('mac')
print(cadets)
#remove looks from left to right
print('\nremove looks from left to right \n')
cadets.remove('mac')
print(cadets)
#sort and sorted-

print("\nthis is how you can see the difference between sort and sorted. \n")
print(sorted(cadets))
cadets.sort()
print(cadets)

#reverse-
cadets.reverse()
print(cadets)
print(len(cadets))
"""

def build_playlist() -> list[str]:
    playlist = []
    #forming initial list utilizing append
    playlist.append('bite marks')
    playlist.append('enter sandman')
    playlist.append('can you feel my heart')
    #utilizing the insert command to add a song into the beginning of the list
    playlist.insert(0,'bohemian rhapsody')

    #changing first term to a title
    playlist[0] = playlist[0].title()
    return playlist
result = build_playlist()
print(result)
#now add bohemian rhapsody


def curate_playlist(pl:list[str]) -> int:
    


