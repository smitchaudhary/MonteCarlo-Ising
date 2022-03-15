import numpy as np
 
def simulate(L ,temp ,H ,J , MCSteps , metropolis_bool = True ):
    """
    Monte-Carlo simulation for Ising model on a LxL lattice.

    Parameters
    ----------
    temp : float
        The (unitless) temperature of the system.
    L : int
        The size of the lattice
    H : float
        Coupling coefficient with magnetic field.
    J : float
        Nearest neighbour coupling coeficcient.
    MCSteps : int
        Number of MCSteps.
    metropolis_bool : bool
        A boolean to choose the simulation algorithm. Defaults to Metropolis, runs Wolff if False.

    Returns
    -------
    energy_data : nd.array
        A numpy array of size MCSteps storing energy at each step.
    magn_data : nd.array
        A numpy array of size MCSteps storing magnetisation at each step.

    """
    # Lattice initialization
    prob_spin_up = 1
    lattice = np.random.choice(a=[1, -1], size=(L, L), p = [prob_spin_up , 1-prob_spin_up] )
    
    #Observables
    energy_data = np.zeros((MCSteps))
    magn_data = np.zeros((MCSteps))
    
    #Initialization of observables
    energy = lattice_energy(lattice,J,H)
    magnetisation = np.average(lattice)
    
    if metropolis_bool:
        #Metropolis algorithm
        for i in range(MCSteps):
            for j in range(L**2):
                rand_location = np.random.randint(L, size=2)
                energy_difference  = diff_energy(rand_location, lattice , J, H)
                probability = np.exp(-energy_difference/temp, dtype=np.float128)
                if ((energy_difference < 0) or (np.random.rand() < probability)):
                    #Flip the spin
                    lattice[rand_location[0], rand_location[1]] = -lattice[rand_location[0], rand_location[1]]

                    #Update observables
                    energy += energy_difference
                    magnetisation += 2*lattice[rand_location[0], rand_location[1]]/(L**2)

            energy_data[i] = lattice_energy(lattice , J ,H)
            magn_data[i] = magnetisation                

    else:
        wolff_prob = 1 - np.exp(-J*2/temp)
        for i in range(MCSteps):
            location = np.random.randint(L, size=2)
            ClusterSpin = -lattice[location[0], location[1]]
            cluster_list = []
            energy, magnetisation = GrowCluster(location , lattice , cluster_list , ClusterSpin , wolff_prob , energy , magnetisation , J , H)
        
            energy_data[i] = lattice_energy(lattice , J ,H)
            magn_data[i] = np.average(lattice)

    return energy_data, magn_data


def lattice_energy(lattice, J, H):
    '''
    Calculates the energy of a given instance of the lattice.

    Parameters
    ----------
    lattice : LxL nd.array
        The lattice with configurations of al spins.
    H : float
        Coupling coefficient with magnetic field.
    J : float
        Nearest neighbour coupling coeficcient.

    Returns
    -----------
    energy : float
        Energy of the lattice
    '''

    neighbour_sum = np.roll(lattice,1,0) + np.roll(lattice, -1, 0) + np.roll(lattice, 1, 1) + np.roll(lattice, -1, 1)
    L = len(lattice)
    interaction = 0.5*np.sum(lattice*neighbour_sum)

    energy = -J*interaction - H*np.sum(lattice)
    return energy

def diff_energy(location, lattice , J, H):
    '''
    Calculates the energy difference if a spin is changed at a certain location.
    
    Parameters
    ----------
    location : 2x1 nd.array
        Location of the flipped spin.
    lattice : LxL nd.array
        The lattice with configurations of all spins.
    H : float
        Coupling coefficient with magnetic field.
    J : float
        Nearest neighbour coupling coeficcient.

    Returns
    -----------
    diff_energy : float
        Difference in energy if the spin is flipped at location.
    '''
    i = location[0]
    j = location[1]
    L = len(lattice)
    diff = 2*J*lattice[i,j]*(lattice[i-1,j]+lattice[(i+1)%L,j]+lattice[i,j-1]+lattice[i,(j+1)%L]) + 2*H*lattice[i,j]
    return diff


def GrowCluster(location , lattice , cluster_list , ClusterSpin , wolff_prob, energy, magnetisation , J , H ):
    '''
    Grows the cluster starting at given location.
    
    Parameters
    ----------
    location : 2x1 nd.array
        Location of the flipped spin.
    lattice : LxL nd.array
        The lattice with configurations of all spins.
    cluster_list : list
        A list containing locations of the spins which are part of the
    ClusterSpin : int
        The spin at the location of the cluster spin considered.
    wolff_prob : float
        The probability of a spin being added to the cluster if it satisfies other criteria.
    energy :
        Current energy of the system.
    magnetisation :
        Current magnetisation of the system.
    J : float
        Nearest neighbour coupling coeficcient.    
    H : float
        Coupling coefficient with magnetic field.

    Returns
    -----------
    energy : float
        Energy of the system at the end of an MCStep.
    magnetisation : float
        Magnetisation of the system at the end of an MCStep.
    '''
    loc_i = location[0]
    loc_j = location[1]
    
    lattice[loc_i , loc_j] = -lattice[loc_i , loc_j]  #flip spin

    L = np.shape(lattice)[0]

    energy -= diff_energy(location, lattice , J, H)
    magnetisation += 2*lattice[loc_i, loc_j]/(L**2)

    cluster_list.append( [loc_i , loc_j] )

    neighbours = [ [(loc_i -1) %L, loc_j]  , [(loc_i +1) % L, loc_j] , [loc_i  , (loc_j-1)%L ] , [loc_i  , (loc_j+1)%L] ]

    for neigh in neighbours:
        if neigh not in cluster_list:
            TryAdd(neigh , lattice , cluster_list , ClusterSpin , wolff_prob, energy, magnetisation, J , H)
    return energy, magnetisation

def TryAdd(location , lattice, cluster_list, ClusterSpin, wolff_prob, energy, magnetisation , J , H):
    '''
    Tries to add neighbouring spin to the Cluster
    
    Parameters
    ----------
    location : 2x1 nd.array
        Location of the flipped spin.
    lattice : LxL nd.array
        The lattice with configurations of all spins.
    cluster_list : list
        A list containing locations of the spins which are part of the
    ClusterSpin : int
        The spin at the location of the cluster spin considered.
    wolff_prob : float
        The probability of a spin being added to the cluster if it satisfies other criteria.
    energy :
        Current energy of the system.
    magnetisation :
        Current magnetisation of the system.
    J : float
        Nearest neighbour coupling coeficcient.
    H : float
        Coupling coefficient with magnetic field.

    Returns
    -----------
    None
    '''
    spin = lattice[location[0] , location[1] ]

    if spin!=ClusterSpin:
        if np.random.rand() < wolff_prob:
            _,_ = GrowCluster(location , lattice , cluster_list , ClusterSpin , wolff_prob, energy, magnetisation, J , H)
