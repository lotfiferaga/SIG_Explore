# SIG Data Extraction with OSMnx

## Description
This Python script utilizes the OSMnx library to extract data from a Geographic Information System (GIS), specifically OpenStreetMap (OSM). The script focuses on extracting two types of parameters:

1. **Slopes**: It calculates the degree of inclination of road segments.
2. **Turn Angles**: It calculates the rotation angles at intersections.

The code defines a study region, downloads the road network data from OSM, selects a segment of the road network (in this case, the A4 or A86 highway), finds the nearest nodes to the start and end points of the segment, and calculates the shortest path between them.

Then, it calculates the total length of the road segment and the average slope. For slope calculation, it retrieves elevation data for the nodes along the route and calculates the slope using the elevation difference between the start and end points.

Finally, it calculates the turn angles at intersections along the route.

## Code Breakdown

1. **Defining Study Region**: The script begins by defining the study region (e.g., Paris, France).

2. **Downloading Road Network Data**: It downloads the OpenStreetMap road network data for the specified region using OSMnx.

3. **Selecting Road Segment**: A segment of the road network (e.g., A4 or A86 highway) is chosen for analysis.

4. **Finding Nearest Nodes**: Nearest nodes to the start and end points of the segment are identified.

5. **Shortest Path Calculation**: It calculates the shortest path between the start and end nodes using Dijkstra's algorithm.

6. **Calculating Road Segment Length**: The total length of the road segment is computed.

7. **Calculating Slope**: Elevation data for the nodes along the route is retrieved, and the average slope of the segment is calculated based on the elevation difference.

8. **Calculating Turn Angles**: Turn angles at intersections along the route are calculated.

## Usage
1. Ensure you have Python installed on your system.
2. Install the required libraries (`osmnx`, `geopy`, `numpy`, `requests`).
3. Copy the provided code into a Python script file (`.py`).
4. Run the script in your preferred Python environment (e.g., Jupyter Notebook, Python IDE).

## Dependencies
- `osmnx`: For downloading GIS data and network analysis.
- `geopy`: For calculating distances between points.
- `numpy`: For numerical calculations.
- `requests`: For making HTTP requests to the elevation API.

## References
- [OSMnx Documentation](https://osmnx.readthedocs.io/)
- [OpenStreetMap](https://www.openstreetmap.org/)

