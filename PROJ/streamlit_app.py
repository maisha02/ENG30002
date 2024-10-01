import pickle
from pathlib import Path  # Import Path from pathlib
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import seaborn as sns
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import streamlit_authenticator as stauth

# Set page configuration
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Check available methods and attributes of stauth
print(dir(stauth))

houses = ["HouseA", "HouseB", "HouseC", "HouseD"]
usernames = ["Dev", "jhilam", "Jordan", "Ryan"]

# Load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pk1"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

# Combine houses and their corresponding usernames and passwords into a dictionary
credentials = {
    "usernames": {
        houses[i]: {
            "name": usernames[i], 
            "password": hashed_passwords[i]
        } 
        for i in range(len(houses))
    }
}

# Corrected code without the 'key' argument
# Corrected code with 'cookie_key' argument
authenticator = stauth.Authenticate(
    credentials=credentials, 
    cookie_name="Energy_Dashboard", 
    cookie_key="abcdef",  # This is the correct argument
    cookie_expiry_days=30
)


house, authentication_status, username = authenticator.login("Login", "main")


# Handle authentication status
if authentication_status is False:
    st.error("Username/password is incorrect!")
elif authentication_status is None:
    st.warning("Please enter your username and password!")
else:
    st.sidebar.title(f"Welcome {username}")
   
   
    # Load data
    data_set1 = pd.read_csv('data/set2_data.csv', parse_dates=['Date'])
    data_set3 = pd.read_csv('data/set3_data.csv')
    data_set3 = data_set3.values.reshape((60, 24))
    data_set4 = pd.read_csv('data/set4_data.csv')
    stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

    # Sidebar
    st.sidebar.header('Dashboard House1')
    st.sidebar.subheader('Current energy production graph')
    st.sidebar.subheader('Energy prediction graph')
    plot_data = st.sidebar.multiselect(
        'Select data', 
        ['Temperature (°C)', 'Solar Production (kWh)'], 
        ['Temperature (°C)', 'Solar Production (kWh)']
    )
    plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)
    st.sidebar.subheader('Load Management Status')
    st.sidebar.subheader('Peer-to-Peer Energy Trading Network')
    st.sidebar.subheader('Recent Transactions and Token Exchanges')

    # Row A - Metrics
    st.markdown('### Metrics')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Consumption Today", "50 kWh", "1.2 kWh")
    col2.metric("Current Solar Production", "12 kWh", "-8%")
    col3.metric("Current Token Price", " $0.35", "-4%")
    col4.metric("Current Surplus", " 5 kWh", "2%")

    def display_alerts(alerts):
        for alert in alerts:
            if alert['severity'] == 'critical':
                st.error(f"{alert['time']} - {alert['message']}")
            elif alert['severity'] == 'warning':
                st.warning(f"{alert['time']} - {alert['message']}")
            else:
                st.info(f"{alert['time']} - {alert['message']}")

    # Example usage
    alerts = [
        {'time': '2024-08-23 10:00', 'message': 'Token price increased by 15%', 'severity': 'warning'},
        {'time': '2024-08-23 12:00', 'message': 'Energy production dropped by 25%', 'severity': 'critical'}
    ]

    display_alerts(alerts)

    # Row B - Heatmap
    st.markdown('### Current energy production graph')
    plt.figure(figsize=(12, 6))
    sns.heatmap(data_set3, cmap="YlGnBu", cbar=True)
    plt.title('Heatmap of Energy Production (kWh) Over Time')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Minute')
    st.pyplot(plt)

    st.text("")
    st.text("")

    # Row C - Line Chart and Donut Chart
    c1, c2 = st.columns((5, 5))

    with c1:
        st.markdown('### Energy prediction graph')
        st.line_chart(data_set1, x='Date', y=plot_data, height=plot_height)

    with c2:
        st.markdown('### Load Management Status')
        load = data_set4['Load']
        power_usage = data_set4['PowerUsage']
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        plt.figure(figsize=(2, 2))  # Adjust the size if necessary
        plt.pie(power_usage, labels=load, startangle=80, counterclock=False, wedgeprops={'width': 0.25})
        plt.title('Current Load Distribution')
        st.pyplot(plt)

    # Row D 
    st.markdown('### Blockchain Network Overview')
    data = {
        'Timestamp': ['2024-08-22 10:15', '2024-08-22 10:12', '2024-08-22 10:09', '2024-08-22 10:07'],
        'Sender': ['House 1', 'House 2', 'House 3', 'House 4'],
        'Receiver': ['House 2', 'House 3', 'House 4', 'House 1'],
        'Tokens': [5, 3, 7, 2],
    }

    # Convert to DataFrame
    transactions_df = pd.DataFrame(data)

    # Display title and section headers
    d1, d2 = st.columns((5,5))

    with d1: 
        st.markdown('Peer-to-Peer Energy Trading Network')
        st.image('data/Image1.jpg', caption='Energy Trading Network', use_column_width=True)

    with d2:
        # Display the summary of recent transactions
        st.markdown('Recent Transactions and Token Exchanges')
        st.dataframe(transactions_df)
