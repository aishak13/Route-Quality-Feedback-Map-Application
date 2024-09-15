import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
route_data = pd.read_csv('synthetic_route_data.csv')
feedback_data = pd.read_csv('synthetic_feedback_data.csv')
geospatial_data = pd.read_csv('synthetic_geospatial_data.csv')

# Streamlit App
st.title("Real-Time Route Quality Feedback App")
st.sidebar.title("Navigation")

# Select an option for displaying the data
option = st.sidebar.selectbox("Choose an option", ['Route Data', 'Feedback Data', 'Geospatial Data'])

# Function to plot the map
def plot_map(data):
    fig = px.scatter_mapbox(
        data,
        lat="latitude",
        lon="longitude",
        hover_name="route_id",
        hover_data=["traffic", "road_condition", "safety"],
        color="route_id",
        zoom=10,
        height=500
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

# Display Route Data
if option == 'Route Data':
    st.subheader("Route Data")
    st.write(route_data)

    # Plot the map with route data
    st.subheader("Map of Routes")
    plot_map(route_data)

# Display Feedback Data
elif option == 'Feedback Data':
    st.subheader("Feedback Data")
    st.write(feedback_data)

    # Summarize feedback data
    st.subheader("Summary of Feedback")
    feedback_summary = feedback_data.groupby('route_id').mean()[['traffic', 'road_condition', 'safety']]
    st.write(feedback_summary)

# Display Geospatial Data
elif option == 'Geospatial Data':
    st.subheader("Geospatial Data")
    st.write(geospatial_data)

    # Plot geospatial data on a map
    st.subheader("Map of Geospatial Data")
    plot_map(geospatial_data)

# Collect user feedback
st.sidebar.subheader("Provide Feedback")
route_id = st.sidebar.selectbox("Select Route", route_data['route_id'].unique())
traffic_feedback = st.sidebar.slider("Traffic", 1, 5, 3)
road_condition_feedback = st.sidebar.slider("Road Condition", 1, 5, 3)
safety_feedback = st.sidebar.slider("Safety", 1, 5, 3)

# Button to submit feedback
if st.sidebar.button("Submit Feedback"):
    new_feedback = pd.DataFrame({
        'route_id': [route_id],
        'traffic': [traffic_feedback],
        'road_condition': [road_condition_feedback],
        'safety': [safety_feedback]
    })
    feedback_data = pd.concat([feedback_data, new_feedback], ignore_index=True)
    feedback_data.to_csv('synthetic_feedback_data.csv', index=False)
    st.sidebar.success("Feedback submitted!")

# Display new feedback data
st.sidebar.subheader("Updated Feedback Data")
st.sidebar.write(feedback_data)
