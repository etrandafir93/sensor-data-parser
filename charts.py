
import matplotlib.pyplot as plt

x_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y_axis = [5, 16, 34, 56, 32, 56, 32, 12, 76, 89]

plt.title("Valori xxx")
plt.plot(x_axis, y_axis, alpha=0.3, color='red', marker='o', label="item 1", )

plt.xlabel("Time")
plt.ylabel("Temperature")

plt.grid(True)
plt.legend()

# plt.savefig('C:\\Users\\etr\\Desktop\\chart.jpg')

plt.show()
