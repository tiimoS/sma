# Social Media Analytics
## Project 1 – Community Detection in a Facebook network

### Results
All visualizations - louvain and random walk - are stored in the ~/results folder. It is recommended to download the results .pdf files, to better zoom on the individual nodes. 

### Setup
The project is running on Anaconda distribution of Python 3.7. 
Run the Runner.py File to start the louvain detection, network visualization and random walk. 

### Aim
The aim of this project is to build a tool to identify communities and influencers in a social network. The tool should be able to:
- Load a social graph
- Run community detection and some analytical algorithms
- Visualize the network

### Tasks: 
#### 1. Load the dataset
-  Load the following Facebook dataset (The nodes represent the users and links represent the friendships between users) provided from: http://snap.stanford.edu/data/egonets-Facebook.html
#### 2. Implementation
- Implement Louvain method of community detection
- Implement Degree centrality measure
- Implement Random Walk algorithm
Perform the following tasks using the previous implementations:
- Identify users’ communities in the Facebook network using Louvain method.
- Identify top 2 users with the highest degree centrality in each community.
- Distribute three messages across the Facebook network using the random walk
algorithm, start each walk from a different community using its highest degree centrality user. Terminate the walk when at least one node from each community has been reached.
#### 3 Visualization
- Visualize the output of Louvain method by coloring nodes according to their assigned communities.
- Visualize the output of applying Random Walk algorithm, by highlighting the sequence of nodes selected in a path.


