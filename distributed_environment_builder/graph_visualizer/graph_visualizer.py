import matplotlib.pyplot as plt
import numpy as np


class GraphVisualizer:

    def view(self,
             time_series_data1,
             time_series_data2,
             time_series_data3):
        # Create a time index (assuming equally spaced time intervals)
        time_index1 = np.arange(len(time_series_data1))
        time_index2 = np.arange(len(time_series_data2))
        time_index3 = np.arange(len(time_series_data3))
        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(time_index1, time_series_data1, marker='o', linestyle='-', color='blue')
        plt.plot(time_index2, time_series_data2, marker='o', linestyle='-', color='green')
        plt.plot(time_index3, time_series_data3, marker='o', linestyle='-', color='red')

        plt.ylim(0, 1)
        # Customize the plot (optional)
        plt.title('Resource Utilization by Processed Events')
        plt.xlabel('Processed Events')
        plt.ylabel('Utilization')
        plt.grid(True)
        # Display the plot
        plt.show()