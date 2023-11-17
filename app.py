import streamlit as st
from main import get_system_perf  

# Streamlit app
def main():
    st.title("System Performance Tracker")

    # Get system metrics
    metrics = get_system_perf()

    # Display metrics in Streamlit
    for metric, value in metrics.items():
        st.write(f"{metric}: {value}")
if __name__ == "__main__":
    main()
