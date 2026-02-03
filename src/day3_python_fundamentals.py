#list Examples
numbers=[10,20,30,40]

#tuple exampe
coordinates=(5,10)

print("list: ",numbers)
print("tuples : ",coordinates)

#indexing
#2 types - positive and negative
#positive -> 0,1,2,3,4,...left to right
#negative -> -1,-2,-3,-4... right to left

list=[100,200,300,500,400,600,700,800,900,1000]

#range indexing
#negative indec can't be done in reverse order!!!
print("Reverse: ",list[-3:-1])

#steps or skips start_index:end_index:skip
print("Skip one value:",list[1:4:1])
print("skip two values:",list[1:4:2])
print("skip three values:",list[1:4:3])
print("skip two values but from 2nd index to 5th index: ",list[2:9:2])
print("skip three values \" \" :",list[2:9:3])
print("printing values from minus index: ",list[-8:-1])

#append, insert, extend, pop, sort,delete, clear
list.sort(reverse=True)
print("reverse order: ",list)
print("correct order: ",list[::-1])

list.append(2000)
print("adding to last: ",list)
print()
