def myFunction():
    return 1, 2

myList = [
    [0, 1, 2],
    [3, 4, 5]
]

print(len(myList))
print(len(myList[0]))

for row in range(len(myList)):
    for val in myList[row]:
        print(val, end = " ")
    print()
