import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt

# Function to extract slope data from GIS
def extract_slope_data(G):
    # Calculate the total length of the road segment
    route_length = sum(ox.utils_graph.get_route_edge_attributes(G, route, 'length'))

    # Estimate the average slope based on elevation difference between start and end points
    start_elevation = G.nodes[start_node]['elevation'] if 'elevation' in G.nodes[start_node] else None
    end_elevation = G.nodes[end_node]['elevation'] if 'elevation' in G.nodes[end_node] else None

    if start_elevation is None or end_elevation is None:
        st.warning("Insufficient elevation data to calculate average slope.")
        average_slope = None
    else:
        elevation_change = end_elevation - start_elevation
        average_slope = elevation_change / route_length

    return average_slope

# Function to extract turn data from GIS
def extract_turn_data(G, route):
    turn_angles = []
    for i in range(len(route) - 2):
        bearing1 = ox.bearing.get_bearing((G.nodes[route[i]]['y'], G.nodes[route[i]]['x']),
                                           (G.nodes[route[i + 1]]['y'], G.nodes[route[i + 1]]['x']))
        bearing2 = ox.bearing.get_bearing((G.nodes[route[i + 1]]['y'], G.nodes[route[i + 1]]['x']),
                                           (G.nodes[route[i + 2]]['y'], G.nodes[route[i + 2]]['x']))
        turn_angle = (bearing2 - bearing1 + 180) % 360 - 180
        turn_angles.append(turn_angle)

    return turn_angles

def page_data_extraction():
    st.title("Partie 1 : Extraction de données")
    place_name = st.text_input("Entrez le nom de l'emplacement (par exemple: New York City, New York, USA)", "New York City, New York, USA")
    start_point = st.text_input("Coordonnées du point de départ (lat, lon)", "40.7128, -74.0060")
    end_point = st.text_input("Coordonnées du point d'arrivée (lat, lon)", "40.7589, -73.9851")

    if st.button("Exécuter"):
        # Download the OpenStreetMap road network for the selected location
        G = ox.graph_from_place(place_name, network_type="drive")

        # Convert user input coordinates to tuple
        start_point = tuple(map(float, start_point.split(',')))
        end_point = tuple(map(float, end_point.split(',')))

        # Find the nodes closest to the start and end points
        global start_node, end_node
        start_node = ox.distance.nearest_nodes(G, start_point[0], start_point[1])
        end_node = ox.distance.nearest_nodes(G, end_point[0], end_point[1])

        # Calculate the shortest path between the start and end nodes
        global route
        route = ox.shortest_path(G, start_node, end_node, weight='length')

        # Extract slope data
        st.header("Données de pente")
        average_slope = extract_slope_data(G)
        if average_slope is not None:
            st.write(f"La pente moyenne de la route est : {average_slope:.2f} %")

        # Extract turn data
        st.header("Données de virage")
        turn_angles = extract_turn_data(G, route)
        st.write("Angles de virage:", turn_angles)

def page_visualization_3d():
    st.title("Visualisation en 3D")
    st.write("Visualisation en 3D du segment de route.")

    # Add dropdown menu for 3D visualization options
    visualization_option_3d = st.selectbox("Sélectionnez l'option de visualisation en 3D", ["Sélectionner un segment", "Paris, France"])
    st.write("Vous avez sélectionné:", visualization_option_3d)

    # Add code for each visualization option
    if visualization_option_3d == "Sélectionner un segment":
        st.write("Sélectionner un segment")
        # Add code for Option 1 visualization here
    elif visualization_option_3d == "Paris, France":
        import osmnx as ox
        import numpy as np
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        # Define the study region (in this case, Paris, France)
        place_name = "Paris, France"

        # Download the OpenStreetMap road network for this region without elevation data
        G = ox.graph_from_place(place_name, network_type="drive", retain_all=True, truncate_by_edge=True, simplify=True)

        # Choose a segment of the road network (near Paris)
        start_point = (48.858844, 2.294351)  # Coordinates near the Eiffel Tower
        end_point = (48.860731, 2.293243)  # Coordinates near the Champ de Mars

        # Find the nearest nodes to the start and end points
        start_node = ox.distance.nearest_nodes(G, start_point[0], start_point[1])
        end_node = ox.distance.nearest_nodes(G, end_point[0], end_point[1])

        # Calculate the shortest path between the start and end points
        route = ox.shortest_path(G, start_node, end_node, weight='length')

        # Get the node coordinates of the route
        route_nodes = [G.nodes[node_id] for node_id in route]

        # Extract the latitude and longitude of the nodes
        lats = [node['y'] for node in route_nodes]
        lons = [node['x'] for node in route_nodes]

        # Plot the route in 3D without elevation data
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Plot the route
        ax.plot(lons, lats, np.zeros(len(route_nodes)), color='r', linewidth=2)

        # Plot the start and end points
        ax.scatter(start_point[1], start_point[0], 0, c='b', marker='o', label='Start Point')
        ax.scatter(end_point[1], end_point[0], 0, c='g', marker='o', label='End Point')

        # Set labels and title
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_zlabel('Elevation')
        ax.set_title('3D Visualization of Route (without Elevation)')

        # Add legend
        ax.legend()

        # Show plot
        st.pyplot(fig)

def page_visualization_2d():
    st.title("Visualisation en 2D")
    st.write("Visualisation en 2D du graphe de route choisi.")

    # Add dropdown menu for 2D visualization options
    visualization_option = st.selectbox("Sélectionnez l'option de visualisation en 2D", ["City Name","New York City, New York, USA", "Paris, France"])
    st.write("Vous avez sélectionné:", visualization_option)

    if visualization_option == "New York City, New York, USA":
        # Define the study region (in this case, New York City, USA)
        place_name = "New York City, New York, USA"

        # Download the OpenStreetMap road network for this region
        G = ox.graph_from_place(place_name, network_type="drive", retain_all=True)

        # Choose a segment of the A4 motorway
        start_point = (40.7128, -74.0060)  # New York City coordinates
        end_point = (40.7589, -73.9851)     # New York City coordinates

        # Find the nearest nodes to the start and end points
        start_node = ox.distance.nearest_nodes(G, start_point[0], start_point[1])
        end_node = ox.distance.nearest_nodes(G, end_point[0], end_point[1])

        # Plot the road network
        fig, ax = ox.plot_graph(G, figsize=(10, 10), node_color='b', node_size=5, edge_color='k', show=False)

        # Plot the start and end points
        ax.scatter(start_point[1], start_point[0], c='r', s=100, label='Start Point')
        ax.scatter(end_point[1], end_point[0], c='g', s=100, label='End Point')

        # Plot the shortest path between the start and end points
        route = ox.shortest_path(G, start_node, end_node, weight='length')
        route_nodes = ox.plot_graph_route(G, route, ax=ax, route_color='r', route_linewidth=6, node_size=0, orig_dest_size=100)

        # Add legend
        ax.legend()

        # Show plot
        st.pyplot(fig)

    elif visualization_option == "Paris, France":
        # Define the study region (in this case, Paris, France)
        place_name = "Paris, France"

        # Download the OpenStreetMap road network for this region
        G = ox.graph_from_place(place_name, network_type="drive", retain_all=True)

        # Choose a segment of the road network (near Paris)
        start_point = (48.858844, 2.294351)  # Coordinates near the Eiffel Tower
        end_point = (48.860731, 2.293243)     # Coordinates near the Champ de Mars

        # Find the nearest nodes to the start and end points
        start_node = ox.distance.nearest_nodes(G, start_point[0], start_point[1])
        end_node = ox.distance.nearest_nodes(G, end_point[0], end_point[1])

        # Plot the road network
        fig, ax = ox.plot_graph(G, figsize=(10, 10), node_color='b', node_size=5, edge_color='k', show=False)

        # Plot the start and end points
        ax.scatter(start_point[1], start_point[0], c='r', s=100, label='Start Point')
        ax.scatter(end_point[1], end_point[0], c='g', s=100, label='End Point')

        # Plot the shortest path between the start and end points
        route = ox.shortest_path(G, start_node, end_node, weight='length')
        route_nodes = ox.plot_graph_route(G, route, ax=ax, route_color='r', route_linewidth=6, node_size=0, orig_dest_size=100)

        # Add legend
        ax.legend()

        # Show plot
        st.pyplot(fig)
def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.selectbox("Choisir la partie", ["Extraction de données", "Visualisation en 2D", "Visualisation en 3D"])

    if selection == "Extraction de données":
        page_data_extraction()
    elif selection == "Visualisation en 2D":
        page_visualization_2d()
    elif selection == "Visualisation en 3D":
        page_visualization_3d()

if __name__ == "__main__":
    main()
