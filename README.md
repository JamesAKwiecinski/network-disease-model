# network-disease-model
<p align="center">
<img src="https://user-images.githubusercontent.com/86231828/122758663-6ab7ca80-d2dc-11eb-802e-8c95e4f8a6ac.gif" width="400" height="400">
</p>  

### A simple agent-based model written in Python to simulate network disease propagation.
  This repository is a Python implementation of the algorithm simulating disease transmission throughout a network of individuals, as discussed in "When Science and Mathematics Collide: Agent-Based Modeling of COVID-19 Spread", which will soon make a appearance in the publication _LabTalk_ (to be updated with issue number soon). Although I encourage you to try programming the algorithm yourself, my code is made available here so that you can delve head-first into investigating many of the epidemiology concepts covered in the article.

### Installation and usage
  You will require an already installed Python 3.x environment to use my code. If you do not have an installation, an exhaustive guide for all major computer operating systems can be found [here](https://realpython.com/installing-python/). Simply download the scripts into your path directory and run `network_transmission` in your Python kernel, which will run the exact simulation that produced the results in _LabTalk_ article. 4 figures are produced at the end of the simulation, corresponding to the network on the 0th day, the network at the end of the simulation, the cumulative counts of infected individuals in the random and friend-nominated groups, and lastly an animation showing the time evolution of the network as the disease spreads through the connected contacts. This animation is also saved as a mp4 movie and animated gif in your path directory.

  To change any of the parameters, the initial infected population, or the contact network structure, open `network_transmission.py` in your favorite editor and edit lines 18-37. For the default code, the simulation takes no more than 20 seconds, with the generation of the animation taking up most of the computing time. You should expect this time to increase with increasing numbers of agents in the network or simulation time.
  
  For all the possible network structures offered by NetworkX and their descriptions, see the page on [graph generators](https://networkx.org/documentation/stable/reference/generators.html). It's a lot of fun to run the simulation for different networks!
  
  You can also change the layout of how the code draws the network by replacing line 30 with any of the options under the ["Graph Layouts" section](https://networkx.org/documentation/stable/reference/drawing.html?highlight=layout#module-networkx.drawing.layout).
  
### Troubleshooting
  
  The main issue that you will likely run into is not having one of the necessary packages to run the code. This problem can be solved by installing the necessary packages via pip, with the command `pip install networkx`, if you needed to install NetworkX, for instance.
  
  One other issue I ran into initially was drawing the Barabási-Albert network, due to a conflict with the NetworkX and Matplotlib packages. To resolve this, you have to downgrade the Decorator module of Matplotlib with the command `pip install decorator==4.3`. 
