#Topic 1: Broadcasting & Vectorization Fundamentals
import numpy as np
ab=np.array(42)
print("zero Dimesnsions: \n",ab)
arr1=np.array([1,2,3])
print("\nOne Dimenstions: \n",arr1)

arr2=np.array([[1,2,3],
               [4,5,6]])
print("\nTwo Dimenstions : \n",arr2)

arr3=np.array([[[1,2],[3,4]],
              [[5,6],[7,8]]])
print("\nThree Dimensions: \n",arr3) 

print("Dimensions of ab: ",ab.ndim)
print("Dimensions of arr1: ",arr1.ndim)
print("Dimensions of arr2: ",arr2.ndim)
print("Dimensions of arr3: ",arr3.ndim)

result=arr1+arr2
print("\nAddition Operation take place here: \n",result)
print("\nMultiplication by scalar:", arr1 * 2)
print("\nElement-wise multiplication:", arr1 * arr2)
print("\nMean of array arr1:", np.mean(arr1))

abc=np.array([1,2,3,4,6,7])
print("Shape of abc: ",abc.shape)


#vectorized vs loop example
arr4=np.random.rand(1,10)
print("\nRandom Values Array: \n",arr4)
#vectorized operation
squared=arr4**2
print("Squared Matric:\n",squared)

#Topic 2: Array Manipulation – Reshape, Stack & Combine 
#reshape
arr=np.arange(12)
print("\nArray: \n",arr)
reshaped=arr.reshape(3,4)
print("Reshaped Array: \n",reshaped)

#stacking array vertically and horizontal
a = np.array([[1, 2]])
b = np.array([[3, 4]])

vstacked = np.vstack((a, b))
print("\nVertical Stack:\n",vstacked)

hstacked = np.hstack((a,b))
print("\nhorizontal Stacked: \n",hstacked)

#Topic 3: Statistical Functions in NumPy
data=np.array([[10,20,30],
               [40,50,60]])
print("\nMean of all elements: ",np.mean(data))
print(np.mean(data,axis=0))

#
A=np.array([[1,2],[3,4]])
B=np.array([[5,6],[7,8]])
print("Dot Product of A and B: \n",np.dot(A,B))

#Topic 4: Advanced Indexing and Slicing
# Simple Indexing
ab1 = np.array([[1,2,3,4,5], [6,7,8,9,10]])
print('2nd element on 1st row:', ab1[0, 1])

#3d indexing
a1=np.array([[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]])
print("3d Indexing:",a1[1,0,2])

#1D slicing
a2=np.array([1,2,3,4,5,6,7])
print("1D Slicing",a2[1:5])

# Using arange (Start, Stop, Step)
a3=np.arange(40,55,3)
print("Array a3: \n",a3)
print("Shape of a3: \n",a3.shape)
a4=np.arange(1,17).reshape(4,4)
print(a4)

#create 3d array using arange function
a5=np.arange(0,12,2)
print("shape before reshape: ",a5.shape)

a6=a5.reshape(1,2,3)
print("shape after reshape: ",a6.shape)
print(a6)

# Using linspace (Evenly spaced)
A1=np.linspace(0,2,5)
print("A1: ",A1)

A2=np.random.randn(2,3)
print("A2: \n",A2)

A3=np.random.uniform(20,20,size=(2,2))
print("A3: \n",A3)
print("Data type of A3: ",A3.dtype)

arr_1 = np.random.randint(10, 15, size=(3, 3))
print(arr_1)
print("Size of arr_1:",arr_1.size)

# Array Inspection
arr_2 = np.array([[1, 2], [3, 4]])
print("Shape of arr_2:", arr_2.shape)  # Shape (rows, columns)

arr_3 = np.array([1, 2, 3])
print("Data type of arr:", arr_3.dtype)

arr_4 = np.array([[1, 2, 3], [4, 5, 6]])
print("Size of arr_4:", arr_4.size)

# Universal Functions (ufuncs)
##Square root
arr_5 = np.array([1, 4, 9])
print(np.sqrt(arr_5))

##sine function
arr = np.array([0, np.pi/2])
print(np.sin(arr))

##Exponential function
arr = np.array([1, 2])
print(np.exp(arr))

A4=np.array([1.2,2.8,-3.7])
print("Floor of A4: ",np.floor(A4))
print("Ceil of A4: ",np.ceil(A4))
print("Round of A4: ",np.round(A4))
print("Trunc of A4: ",np.trunc(A4))

arr_6 = np.array([1, np.e, np.e**2])
print("Natural log of arr_6:", np.log(arr_6))