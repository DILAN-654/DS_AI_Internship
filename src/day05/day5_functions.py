#ex1
def greet():
    print("Hello, welcome to day 5 class of Interships!")
greet()

#ex2
def add_numbers(a,b):
    return a + b
result = add_numbers(5, 3)
print("The sum of 5 and 3 is:", result)

#ex3
x=10
def show_value():
    x=5
    print("Value of x inside the function:", x)
show_value()
print("Value of x outside the function:", x)

#ex4
icecream = "vanilla"
def food():
    fruit = "apple"
    vegetable = "carrot"
    print(fruit,"is good for health")
    print(icecream,"is a good flavour")
food()
print("Icecream flavour outside the function:", icecream)
#print("Vegetable is also good for health:", vegetable)

#ex5
import math
import random
print("math.sqrt(16) =", math.sqrt(16))
print("random numbers =", random.randint(1, 10))

