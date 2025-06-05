import matplotlib.pyplot as plt

class ConformanceViewer:
    def show(self, values):
        # Plotting
        plt.figure(figsize=(8, 4))
        plt.plot(values, marker='o', linestyle='-')
        plt.title("Simple Value Plot")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.grid(True)
        plt.tight_layout()
        plt.show()