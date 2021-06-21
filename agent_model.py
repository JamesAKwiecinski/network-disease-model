# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 13:17:24 2021

@author: James A. Kwiecinski
"""
#=============================================================================
# A simple agent-based network model involving "N" individuals with 
# incorporated susceptible-infected dynamics. 
#
# Key parameters:
#   - p    : Transmission probabilty
#   - tf   : Final simulation time
#   - ti   : Number of days individual is infected.
#   - ta   : Number of days recovered individual has antibody response.
#   - te_no: Number of individuals to be tested per group, which should be 
#             much less than N.
#
# Input:
#   - pop  : 1 x N row matrix specifying state of each person in population.
#             "0" corresponds to non-infectious, "1" corresponds to infectious.
#   - adj  : N x N adjacency matrix specifying connections between individuals.
# 
# Output (supposing simulation does not prematurely finish):
#   - pop         : 1 x ((tf+1)*N) matrix with state of each person 
#                    at each time step.
#   - ran_cumul   : 1 x (tf+1) matrix with the number of infected 
#                    in random test group.
#   - friend_cumul: 1 x (tf+1) " " " " " " " friend " ".   
#
#=============================================================================
# 
# The general idea is that we look at infected nodes in a population,
# denoted by the state "1", and determine susceptible individuals, denoted by 
# the state "0", that are in contact with them. We suppose that they pass on 
# the infection to these individuals with a constant probability of "p" in a 
# given time step, only if the agent is non-infectious and does not have an 
# active antibody response. 
#
# After this is done for every infected agent, we check to see whether the 
# infected agent has overcome the infection (i.e. have they been infected for
# more than ti days). If so, they become non-infectious and they are briefly
# immune to catching the infection.
#
# We then check whether every non-infectious individual with an antibody 
# response has lost their immunity (i.e. have they been immune for more than
# ta days). If so, the non-infectious individual is now susceptible.
#
# Cycle to the next day and repeat the aforementioned steps.
#
#=============================================================================

import random              # Needed to generate random numbers.
        
def net_model(pop,adj,p,tf,ti,ta,te_no):
    
    n        = len(pop)    # Extract number of agents from initial infected.
    t        = 0           # Set initial time
    inf_list = ['none']*n  # Running list of infected individuals.
    re_list  = ['none']*n  # " " " recovered ".
    
    """
    Generate a list of random individuals, without duplicate indices, to be
     tested for infection.
    """
    
    ran_group    = random.sample(range(n),te_no)
    ran_cumul    = []      # Start cumulative count of infected in this group.
    
    """
    Now take a single close contact (i.e. friend) from each individual in the 
    randomly sampled group and make a new group out of them.
    """
    
    friend_group    = []
    friend_cumul    = []
    
    for ran in ran_group:
        
        """Generate a list of friends for the random individual."""
        
        friend_pop = [index for index, value in 
                           enumerate(adj[ran][:]) if value == 1]
        
        for friend in friend_pop:
            
            """Randomly choose a friend of the random individual."""
            
            friend_group.append(friend_pop[random.randint(
                0,len(friend_pop)-1)])
    
    while t < tf:   # Start looping in time
    
        new_pop   = pop[(n*t):(n*t+n)]
        ran_count = 0
        friend_count = 0
        
        """Check to see if there are any infected."""
        
        if sum(new_pop) ==0:
            break            # Stop the simulation; there's no infections!
        else:                # There's an infection; keep the simulation going!
            pass
        
        """Find the infected individuals in this timestep"""            
            
        inf_pop = [index for index, value in 
                       enumerate(new_pop) if value == 1]
                        
        """Find all the recovered/immune individuals."""
                
        re_pop = [index for index, value in 
                       enumerate(re_list) if value != 'none']  
        
        for inf in inf_pop:
                
                """Update inf_list to include day first infected."""
                
                if inf_list[inf]=='none':
                    
                    inf_list[inf]=t
                
                    """If the infected individual is in the test groups..."""
                    
                    if inf in ran_group:
                        ran_count += 1   # Add 1 to random count
                        
                    elif inf in friend_group:
                        friend_count += 1   # Add 1 to friend count
                    
                    else:
                        pass
                    
                else:
                    pass

                """Find the contacts of an infected individual."""                    
                        
                con_pop = [index for index, value in 
                           enumerate(adj[inf][:]) if value == 1] 
                        
                """
                If the recovered individual is one of the contacts, remove
                 this contact (as no infection can occur) and make a new 
                 con_pop.
                """
                
                con_pop = [con for con in con_pop if con not in re_pop]
                
                """
                Apply the same thinking if there are infected individuals who
                 are contacts because you cannot pass the infection to an 
                 individual who is already infectious.
                """
                
                con_pop = [con for con in con_pop if con not in inf_pop]
                
                """Loop through the susceptible contacts of the infected."""
            
                for con in con_pop:
                    
                    """
                    Simulate the propagation of the infection by generating 
                     a random integer between 1 and 100.
                    """
                
                    random_integer = random.randint(1,100)
                
                    """
                    If this randomly generated number is less than the
                     infection probabilty, the contact is infected.
                    """
                     
                    if p >= random_integer/100: 
                        new_pop[con] = 1   # Contact is infected.
                    else: 
                        new_pop[con] = 0   # Contact is still susceptible.
                    
                """
                Simulate recovery from infection if time > time 
                 being infectious.
                """
                    
                if t >= ti:
                    
                    """
                    The following statement checks whether the individual
                     has been infectious for ti days. If so, individual is 
                     now recovered.
                    """
                        
                    if t-inf_list[inf]==ti:
                        new_pop[inf] = 0        # Individual is recovered.
                        inf_list[inf] = 'none'  # Reset day infection occurred.
                        re_list[inf] = t        # Store day recovery occurred.
                        
                        """
                        Individual is no longer infected, 
                         continue onto next infectious agent.
                        """
                        
                    else:
                        pass
                    
        """
        Simulate removal of antibody response so that recovered individual
         is susceptible again.
        """
            
        if t >= ta:
            
            """Loop through the recovered individuals."""
            
            for re in re_pop:
                
                """
                The following statement checks whether the recovered 
                 individual is still immune within ta days. If not, individual 
                 is now susceptible.
                """
                
                if t - re_list[re]==ta:
                    re_list[re] = 'none'  # Reset the day individual recovered.
                else:
                    pass
                        
        """Add the new state of the population and keep looping in time"""            
                    
        pop = pop + new_pop        
        t   = t + 1 
        
        """
        Record the number of infected in the random and friend group for the
         day.
        """
        
        ran_cumul.append(ran_count)
        friend_cumul.append(friend_count)
        
    return pop, ran_cumul, friend_cumul   # Spit out results.