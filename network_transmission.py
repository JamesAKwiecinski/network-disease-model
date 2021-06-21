# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 13:17:24 2021

@author: James A. Kwiecinski
"""

import networkx as nx                # Needed to generate network geometries.
from agent_model import net_model    # Needed to simulate disease propagation.
import matplotlib.pyplot as plt      # Needed to draw our results.
from matplotlib.animation import FuncAnimation # Needed to make animation.
import pandas as pd                  # Needed to plot node colors in network.
import numpy as np                   # Needed to analyze network structure

##############################################################################
# SPECIFY PARAMETERS HERE
##############################################################################
n      = 1000             # Specify the number of individuals in the network.
p      = 0.2              # " " transmission probability.
ti     = 10               # " " time to overcome being infectious.
ta     = 30               # " " time antibody response occurs.
te_no  = 80               # " " number of individuals per group to be tested.
tf     = 100              # " " final simulation time.   
##############################################################################

##############################################################################
# SPECIFY NETWORK GEOMETRY AND GRAPH LAYOUT HERE, SEE README.MD FOR OPTIONS
##############################################################################
graph = nx.barabasi_albert_graph(n,1)
pos = nx.spring_layout(graph)
##############################################################################

##############################################################################
# SPECIFY INITIAL INFECTED POPULATION HERE
##############################################################################
pop = [0]*n
pop[0] = 1
##############################################################################

"""Do not edit beyond here unless you know what you are doing!"""

adj = nx.adjacency_matrix(graph) #Create adjacency matrix from graph
adj = adj.toarray()       # Convert it so that it can be used in the algorithm
adj = adj.tolist()

"""
Run simulation with specified parameters, initial infected population and
network geometry.
"""

results, ran_cumul, friend_cumul = net_model(pop,adj,p,tf,ti,ta,te_no)

"""
Draw the initial and final state of the network, the cumulative infected
counts of the random and friend groups, and make an animation of the disease
propagation throughout the network.
"""

# SHOW THE INITIAL AND FINAL NETWORK STATE

plt.close('all')
plt.figure(1)
edges = nx.from_numpy_matrix(np.array(adj))
weights = pd.DataFrame({
        'ID': list(range(1,n+1)), 
        'myvalue': pop
        })
nx.draw(edges,pos=pos,node_size = 75,node_color=weights['myvalue'].astype(int),
        edgecolors='black',cmap=plt.cm.Reds)

plt.figure(2)
weights = pd.DataFrame({
        'ID': list(range(1,n+1)), 
        'myvalue': results[len(results)-n:]
        })
nx.draw(edges,pos=pos,node_size = 75,node_color=weights['myvalue'].astype(int),
        edgecolors='black',cmap=plt.cm.Reds)

plt.figure(3)
plt.step(list(range(int((len(results)/n))-1)),
         np.cumsum(ran_cumul),'b',linewidth=2)
plt.step(list(range(int((len(results)/n))-1)),
         np.cumsum(friend_cumul),'r',linewidth=2)

# CREATE ANIMATION

fig, ax = plt.subplots(figsize=(8,8))
weights = pd.DataFrame({
        'ID': list(range(1,n+1)), 
        'myvalue': pop
        })
nc    = weights['myvalue'].astype(int)
nodes = nx.draw_networkx_nodes(edges,pos,node_size = 75,node_color=nc,
                               edgecolors='black',cmap=plt.cm.Reds)
edges = nx.draw_networkx_edges(edges,pos) 


def update(t):
    weights = pd.DataFrame({
        'ID': list(range(1,n+1)), 
        'myvalue': results[(n*t):(n*t+n)]
        })
    nc = weights['myvalue'].astype(int)
    nodes.set_array(nc)
    ax.set_title("Time {}".format(t))
    return nodes,

anim = FuncAnimation(fig, update, frames=int((len(results)/n)), blit=False)
anim.save('test_animation.mp4', fps=2, extra_args=['-vcodec', 'libx264'])
anim.save('animation_1.gif', writer='imagemagick')