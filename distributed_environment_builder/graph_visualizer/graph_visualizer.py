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
        plt.title('Resource Utilization by Processed Events')
        plt.xlabel('Processed Events')
        plt.ylabel('Utilization')
        plt.grid(True)
        plt.show()

    def view_load_capacity_results(self, time_series_data):
        time_series_data1 = sorted(time_series_data, key=lambda x: x[1])
        resource = [t[0] for t in time_series_data1]
        load = [t[1] for t in time_series_data1]
        sli = [t[2] for t in time_series_data1]

        self._show_plot(
            load,
            sli,
            "Load Capacity",
            "Load",
            "Network Utilization"
        )

    def view_resource_demand_results(self, time_series_data):
        time_series_data1 = sorted(time_series_data, key=lambda x: x[0])
        resource = [t[0] for t in time_series_data1]
        sli = [t[2] for t in time_series_data1]

        self._show_plot(
            resource,
            sli,
            "Resource Demand",
            "Resources",
            "Network Utilization"
        )

    def view_scalability(self, time_series_data):
        time_series_data1 = sorted(time_series_data, key=lambda x: x[0])
        resource = [t[0] for t in time_series_data1]
        load = [t[1] for t in time_series_data1]
        sli = [t[2] for t in time_series_data1]

        self._show_plot(
            resource,
            load,
            "Scalability",
            "Resources",
            "Network Utilization"
        )

    def view2(
            self,
            time_series_data
    ):
        time_series_data1 = sorted(time_series_data, key=lambda x: x[0])
        resource = [t[0] for t in time_series_data1]
        load = [t[1] for t in time_series_data1]
        sli = [t[2] for t in time_series_data1]

        plt.figure(figsize=(10, 6))
        plt.plot(resource, sli, marker='o', linestyle='-', color='blue')

        plt.ylim(0, 20)
        plt.title('Resource Utilization by Processed Events')
        plt.xlabel('Processed Events')
        plt.ylabel('Utilization')
        plt.grid(True)
        plt.show()

    def _show_plot(self, x_values, y_values, title, x_label, y_label):
        plt.figure(figsize=(10, 6))

        for i in range(x_values):
            plt.plot(x_values[i], y_values[i], marker='o', linestyle='-', color=colors[i])

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        plt.show()
