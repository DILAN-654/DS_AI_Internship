import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [10, 20, 15, 25, 30]
plt.plot(x, y, marker='o', label="Line Data")
plt.xlabel("X values")
plt.ylabel("Y values")
plt.title("Line Graph Example")
plt.grid(True)
plt.legend()
plt.show()