import streamlit as st
import psutil
import GPUtil
import time
from auth import authenticate
from main import get_cpu_perf,get_gpu_stats ,get_process_cpu_usage
import pandas as pd


class SystemResourceMonitor:
    """
    A class to monitor the system resource usage including CPU usage, memory usage, disk usage,
    and network bandwidth used.
    """

    def __init__(self, interval=1):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the initial values of all attributes 
        and other operations that are necessary to do when the object is being created.

        :param self: Represent the instance of the class
        :param interval: Set the time interval between each data point
        :return: The following:
        """

        self.interval = interval
        self.columns = [
            'Time',
            'CPU Usage',
            'Memory Used',
            'Disk Usage',
            'Network Bandwith Used'
        ]
        self.resource_df = pd.DataFrame(columns=self.columns)
        self.cpu_chart_data = pd.DataFrame(columns=['Time', 'CPU Usage'])
        self.memory_chart_data = pd.DataFrame(columns=['Time', 'Memory Used'])
        self.disk_chart_data = pd.DataFrame(columns=['Time', 'Disk Usage'])
        self.network_bandwith_used_data = pd.DataFrame(
            columns=['Time', 'Network Bandwith Used'])

        self.col1, self.col2 = st.columns(2)  # Divide screen into 3 columns

        self.cpu_chart = self.create_chart(self.col1, 'CPU Usage')
        self.memory_chart = self.create_chart(self.col2, 'Memory Usage')
        self.disk_chart = self.create_chart(self.col1, 'Disk Usage')
        self.network_bandwith_used_chart = self.create_chart(
            self.col2, 'Network Bandwith Used')

    def create_chart(self, column, title):
        """
        The create_chart function creates a line chart in the column object passed to it.
        It takes three arguments:
            - self: The streamlit app instance.
            - column: A streamlit Column object where the chart will be displayed.

        :param self: Represent the instance of the class
        :param column: Specify the column in which to create the chart
        :param title: Name the chart
        :return: A chart object
        """
        column.write(title)
        chart = column.line_chart(pd.DataFrame(columns=['Time', title]))
        return chart

    def start_monitoring(self):
        """
        The start_monitoring function is the main function of this class.
        It will run in a loop, and update the dataframe, charts and 
        other variables with new information every interval seconds.

        :param self: Represent the instance of the class
        :return: A none object
        """
        while True:
            current_time = pd.Timestamp.now()

            cpu_percent = self.get_cpu_usage()
            memory_percent = self.get_memory_usage()
            disk_percent = self.get_disk_usage()
            network_bandwith_used = self.get_network_bandwidth_usage()

            new_row = pd.Series({
                'Time': current_time,
                'CPU Usage': cpu_percent,
                'Memory Used': memory_percent,
                'Disk Usage': disk_percent,
                'Network Bandwith Used': network_bandwith_used
            })

            self.update_dataframe(new_row)
            self.cpu_chart_data = self.update_chart(
                self.cpu_chart, self.cpu_chart_data, current_time, cpu_percent)
            self.memory_chart_data = self.update_chart(
                self.memory_chart, self.memory_chart_data, current_time, memory_percent)
            self.disk_chart_data = self.update_chart(
                self.disk_chart, self.disk_chart_data, current_time, disk_percent)
            self.network_bandwith_used_data = self.update_chart(
                self.network_bandwith_used_chart,
                self.network_bandwith_used_data,
                current_time,
                network_bandwith_used)

            time.sleep(self.interval)

    def get_cpu_usage(self):
        """
        The get_cpu_usage function returns the CPU usage as a percentage.

        :param self: Represent the instance of the class
        :return: The cpu usage in percent
        """
        return psutil.cpu_percent()

    def get_memory_usage(self):
        """
        The get_memory_usage function returns the percentage of memory usage.

        :param self: Represent the instance of the class
        :return: The percentage of the total memory used by the system
        """
        return psutil.virtual_memory().percent

    def get_disk_usage(self):
        """
        The get_disk_usage function returns the disk usage of the root directory in percentage.

        :param self: Represent the instance of the class
        :return: The disk usage in percentage
        """
        return psutil.disk_usage('/').percent

    def get_network_bandwidth_usage(self):
        """
        The get_network_bandwidth_usage function returns the total network bandwidth usage in GB.

        :param self: Represent the instance of the class
        :return: The total network bandwidth usage in gb
        """
        network_stats = psutil.net_io_counters()
        # In GB
        return (network_stats.bytes_sent / (1024**3)) + (network_stats.bytes_recv / (1024**3))

    def update_dataframe(self, new_row):
        """
        The update_dataframe function takes a new row of data 
        and appends it to the existing resource_df.
            Args:
                self (object): The object that is calling this function.
                new_row (pandas DataFrame): A single row of data to be added to the resource_df.

        :param self: Represent the instance of the class
        :param new_row: Add a new row to the dataframe
        :return: A dataframe
        """
        self.resource_df = pd.concat(
            [self.resource_df, new_row], ignore_index=True)

    def update_chart(self, chart, chart_data, current_time, value):
        """
        The update_chart function takes in the following arguments:
            - self: a reference to the class instance.
            - chart: a reference to the Streamlit chart object.
            - chart_data: a Pandas DataFrame containing data 
                for plotting on the Streamlit chart object.

        :param self: Allow an object to refer to itself inside of a method
        :param chart: Update the chart with new data
        :param chart_data: Store the data that is used to create the chart
        :param current_time: Set the time of the data point
        :param value: Update the chart with new data
        :return: The chart_data dataframe
        """
        chart_data = pd.concat([chart_data, pd.DataFrame(
            {'Time': current_time, chart_data.columns[1]: value}, index=[0])], ignore_index=True)
        chart.line_chart(chart_data.set_index('Time'))
        return chart_data
    

# Streamlit app


def show_system_performance():         
    # Get system metrics
    metrics_cpu = get_cpu_perf()
    metrics_gpu = get_gpu_stats()
    process_cpu_usage = get_process_cpu_usage()

    cpu_container = st.container()

    col1, col2 ,col3 = st.columns(3)

    st.sidebar.write("APPS")
    col1_sidebar, col2_sidebar = st.sidebar.columns(2)


    
    with col1_sidebar:
        st.write("Name")
        for process_info in process_cpu_usage:
            process_name = process_info['Name'].split(".exe")[0]  # Remove ".exe" suffix
            st.write(process_name)

    with col2_sidebar:
        st.write("CPU Usage")
        for process_info in process_cpu_usage:
            st.write(f"{process_info['CPU Usage']}%")
    
    with col1:
        cpu_progress_bar = st.progress(metrics_cpu['CPU Usage'] / 100)
        st.write(f"CPU Usage: {metrics_cpu['CPU Usage']}%")

        gpu_progress_bar = st.progress(metrics_gpu['GPU Usage'] / 100)
        st.write(f"GPU Usage: {metrics_gpu['GPU Usage']}%")

    # Display metrics in Streamlit
    with col2:
        with st.expander("CPU Stats"):
            for metric, value in metrics_cpu.items():
                st.write(f"{metric}: {value}")

        with st.expander("GPU Stats"):
            for metric, value in metrics_gpu.items():
                st.write(f"{metric}: {value}")
    
    with col3:
        with st.expander("Memory Stats"):
            mem_progress_bar = st.progress(metrics_cpu["Memory Usage (%)"] / 100)
            st.write(f"Memory usage: {metrics_cpu['Memory Usage (%)']}%")
        with st.expander("Disk Stats"):
            disk_progress_bar = st.progress(metrics_cpu["Disk Usage (%)"] / 100)
            st.write(f"Disk usage: {metrics_cpu['Disk Usage (%)']}%")

    monitor = SystemResourceMonitor(interval=1)
    monitor.start_monitoring()

def main():
    
    st.title("System Performance Tracker")

    # Add a sign-in section
    st.header("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Check if the sign-in button is pressed
    if st.button("Sign In"):
        if authenticate(username, password):
            # If authentication is successful, clear the page and show system performance
            st.balloons()
            st.success("Logged in successfully!")
              # This will clear the entire page
            show_system_performance()
    # Create a placeholder for the sign-in section
    # sign_in_container = st.empty()
    # with sign_in_container:
    #     # Add a sign-in section
    #     st.header("Sign In")
    #     username = st.text_input("Username")
    #     password = st.text_input("Password", type="password")

    #     # Check if the sign-in button is pressed
    #     if st.button("Sign In"):
    #         if authenticate(username, password):
    #             # If authentication is successful, clear the page and show system performance
    #             st.balloons()
    #             st.success("Logged in successfully!")
    #             sign_in_container.empty()  # This will clear the entire page
    #             time.sleep(2)
    #             show_system_performance()
    #         else:
    #             st.error("Invalid username or password") 

if __name__ == "__main__":
    main()
