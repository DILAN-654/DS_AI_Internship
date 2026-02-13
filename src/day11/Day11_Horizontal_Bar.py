import matplotlib.pyplot as plt

names = ["Amit", "Sara", "John", "Priya"]
marks = [85, 90, 78, 88]
plt.barh(names, marks)
plt.xlabel("Marks")
plt.ylabel("Students")
plt.title("Horizontal Bar Graph")
plt.grid(axis='x')
plt.show()














