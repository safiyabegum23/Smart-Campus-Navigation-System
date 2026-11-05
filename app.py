import streamlit as st
import pandas as pd
import folium

from streamlit_folium import st_folium
from src.navigation import find_shortest_route


# Page configuration
st.set_page_config(
    page_title="Campus Navigation System",
    page_icon="🗺️",
    layout="wide"
)


# Application title
st.title("🗺️ Smart Campus Navigation System")

st.write(
    "Find the shortest route between campus locations."
)


# Load campus locations
locations = pd.read_csv("data/locations.csv")

location_names = dict(
    zip(locations["name"], locations["id"])
)


# Initialize session state
if "route" not in st.session_state:
    st.session_state.route = None

if "distance" not in st.session_state:
    st.session_state.distance = None


# Location selection
col1, col2 = st.columns(2)

with col1:
    start_name = st.selectbox(
        "Starting Location",
        list(location_names.keys())
    )

with col2:
    end_name = st.selectbox(
        "Destination",
        list(location_names.keys())
    )


# Find route button
if st.button("Find Shortest Route"):

    if start_name == end_name:

        st.warning("Please select different locations.")

        st.session_state.route = None

    else:

        try:

            route, distance, campus = find_shortest_route(
                int(location_names[start_name]),
                int(location_names[end_name])
            )

            st.session_state.route = route
            st.session_state.distance = distance

        except Exception as error:

            st.error(f"Navigation error: {error}")

            st.session_state.route = None


# Display route results
if st.session_state.route is not None:

    route = st.session_state.route
    distance = st.session_state.distance

    st.success("Route Found Successfully!")

    st.metric(
        "Total Distance",
        f"{distance} metres"
    )


    # Navigation directions
    st.subheader("Navigation Directions")

    route_names = locations.set_index("id")["name"]

    for i, location_id in enumerate(route):

        st.write(
            f"{i + 1}. {route_names[location_id]}"
        )


    # Create campus map
    campus_map = folium.Map(
        location=[
            locations["latitude"].mean(),
            locations["longitude"].mean()
        ],
        zoom_start=17
    )


    # Add campus markers
    for _, row in locations.iterrows():

        folium.Marker(
            location=[
                row["latitude"],
                row["longitude"]
            ],
            popup=row["name"],
            tooltip=row["name"]
        ).add_to(campus_map)


    # Draw shortest route
    route_coordinates = []

    for location_id in route:

        row = locations[
            locations["id"] == location_id
        ].iloc[0]

        route_coordinates.append([
            row["latitude"],
            row["longitude"]
        ])


    folium.PolyLine(
        route_coordinates,
        color="blue",
        weight=6,
        tooltip="Shortest Route"
    ).add_to(campus_map)


    # Display map
    st.subheader("Campus Navigation Map")

    st_folium(
        campus_map,
        width=1000,
        height=600,
        key="campus_navigation_map",
        returned_objects=[]
    )