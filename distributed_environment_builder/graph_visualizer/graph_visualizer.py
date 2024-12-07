import matplotlib.pyplot as plt
import numpy as np


class GraphVisualizer:

    def __init__(self):
        self.colors = ['red', 'magenta', 'blue', 'orange', 'cyan', 'magenta']
        self.labels = ['EdgeMiner', "DFG-miner edge", "DFG-miner fog", "DFG-miner cloud"]

    def view(self, y_value_name, time_series_data):
        plt.figure(figsize=(10, 6))

        # Create a time index (assuming equally spaced time intervals)
        for i, data in enumerate(time_series_data):
            time_index = np.arange(len(data))
            # Create the plot
            plt.plot(time_index, data, marker='o', linestyle='-', color=self.colors[i], label=self.labels[i])

        #plt.ylim(0, 1)
        #plt.title(f'{y_value_name} by Processed Events', fontsize=30)
        plt.xlabel('Processed Events', fontsize=24)
        plt.ylabel(y_value_name + " (avg)", fontsize=24)
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        plt.legend(loc="upper right", fontsize=18)
        plt.grid(True)
        plt.show()

    def view_load_capacity_results(self, time_series_data):
        time_series_data1 = sorted(time_series_data, key=lambda x: x[0])
        resource = [t[0] for t in time_series_data1]
        load = [t[1] for t in time_series_data1]
        sli = [t[2] for t in time_series_data1]

        self.show_plot(
            [resource],
            [sli],
            "Load Capacity",
            "Resources",
            "Network Utilization"
        )

    def view_resource_demand_results(self, time_series_data):
        time_series_data1 = sorted(time_series_data, key=lambda x: x[0])
        resource = [t[0] for t in time_series_data1]
        sli = [t[2] for t in time_series_data1]

        self.show_plot(
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

        self.show_plot(
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

    def show_plot(self, x_values, y_values, title, x_label, y_label):
        plt.figure(figsize=(10, 6))

        for i in range(len(x_values)):
            plt.plot(x_values[i], y_values[i], marker='o', linestyle='-', color=self.colors[i], linewidth=5.0, ms=10.0)

        #   plt.ylim(0, 1500)
        plt.title(title, fontsize=44)
        plt.xlabel(x_label, fontsize=36)
        plt.ylabel(y_label, fontsize=36)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        plt.grid(True)
        plt.show()
