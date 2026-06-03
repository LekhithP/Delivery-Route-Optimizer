# Delivery Route Optimizer
A graph-based delivery routing project that models a city map and finds efficient paths between a restaurant and a customer.
# What this project does
This repository builds a weighted graph from city-map data and uses it to answer common delivery-routing questions:
- Is a customer within a restaurant’s delivery range?
- What is the minimum delivery time between two locations?
- What is the best path for a driver to take?
- How does the route change when certain intersections have extra traffic delay?

The goal is to simulate the kind of routing logic a food-delivery platform would use to reduce travel time and improve delivery reliability.
# Core ideas
The city is represented as a graph:
- Nodes=restaurants, customers, intersections, or landmarks
- Edges=roads connecting those locations
- Weights=travel time along each road
Using this model, the program can evaluate routes, compare travel times, and handle traffic delays in a structured way.
# Features
- Builds a weighted graph from city map files
- Checks whether a user is within delivery range
- Builds a minimum spanning tree from a restaurant
- Finds the minimum delivery time between two nodes
- Returns the full delivery path in readable form
- Recomputes the best route when certain nodes have added delay
# How the data is stored
The city map files use the format:
```text
NODE1|NODE2|COST
1|3|4
3|7|6
7|9|8
```
This means there are roads from 1 to 3, 3 to 7, and 7 to 9, with the listed travel times.
# Project Structure
- `delivery_service.py`-main class for building the map and finding routes
- `graph.py`-graph and vertex data structures
- `city_map_*.txt`-sample map files with different graph sizes
- `test_delivery_service.py`-local tests for the delivery service methods
# Techniques used
This project uses standard graph algorithms and path-search logic, including:
- graph construction from file input
- depth-first search for service-range checks
- minimum spanning tree construction
- shortest-path style route search
- route selection with weighted delays
# Example use cases
A restaurant can use this system to:
- reject orders outside a delivery threshold
- find the fastest route to a customer
- see the routing tree for nearby locations
- account for temporary traffic congestion near an event
# Running the project
1. Place the source files and city map files in the same project folder.
2. Run the main Python script or the provided tests.
3. Use the sample map files to verify that the routing logic works as expected.
# Why this project matters
Food delivery depends on more than just finding a path from point A to point B. The route needs to be efficient, adaptable, and easy to explain. This project shows how graph theory can be used to model a real logistics problem and turn raw map data into useful routing decisions.
