from skeleton import *
import numpy as np
from scipy.optimize import curve_fit

def susceptibility(simulation_data):
    '''
    Computes the susceptibility of the lattice and its error. 
    Parameters
    ----------
    simulation_data : dict
        Dictionary containing the data of the simulation

    Returns
    ----------
    susc: float
        Magnetic susceptibility of the lattice.
    error_susc: float
        Error in magnetic susceptibility of the lattice.
    '''

    magn_data = simulation_data['magn_data']
    magn_data_squared = magn_data**2
    error_magn = simulation_data['error_magn']
    error_squared_magn = simulation_data['error_squared_magn']

    N = simulation_data['N']
    temp = simulation_data['temp']

    avr_magn = np.average(magn_data)
    avr_squared_magn = np.average(magn_data_squared)

    susc = (N/temp) * (avr_squared_magn - avr_magn**2)
    error_susc = (N/temp) * np.sqrt(error_squared_magn**2 + (2* avr_magn * error_magn )**2)

    return susc, error_susc

def specific_heat(simulation_data):
    '''
    Computes the specific heat per spin of the lattice and its error. 
    Parameters
    ----------
    simulation_data : dict
        Dictionary containing the data of the simulation

    Returns
    ----------
    sp_heat: float
        Specific Heat per spin of the lattice (in units of kB)   
    error_sp_heat: float
        Error in specific Heat per spin of the lattice (in units of kB)  
    '''
    energy_data = simulation_data['energy_data']
    energy_data_squared = energy_data**2
    error_energy = simulation_data['error_energy']
    error_squared_energy = simulation_data['error_squared_energy']

    N = simulation_data['N']
    temp = simulation_data['temp']

    avr_energy = np.average(energy_data)
    avr_squared_energy = np.average(energy_data_squared)
    
    sp_heat = 1/(temp**2*N) * (avr_squared_energy - avr_energy**2)

    error_sp_heat = 1/(temp**2*N) * np.sqrt(error_squared_energy**2 + (2*avr_energy*error_energy)**2 )
    
    return sp_heat, error_sp_heat

def function_to_fit(t, c, tau):
    return c*np.exp(-t/tau)    

def auto_corr_func(A):
    """
    Calculates the auto-correlation function.

    parameters
    ----------
    A : np.array
        Observable value at each timestep.

    returns
    ------
    tau : float
        The correlation time.
    error : nd.array
        error in the observable A
    """
    num_timesteps = len(A)

    x = np.zeros(num_timesteps-1)

    t_array = np.arange(num_timesteps-1)

    for t in t_array:

        A_t = A[t:] #len=N_t
        N_t = num_timesteps - t

        sum_A  = np.sum(A[:N_t])
        sum_A2 = np.sum((A*A)[:N_t])
        sum_A_t = np.sum(A_t[:N_t])

        numerator = N_t * np.sum( A_t*( A[:N_t] ) ) - sum_A * sum_A_t
        denominator = np.sqrt( N_t * sum_A2 - sum_A**2 ) * np.sqrt( N_t * np.sum(A_t*A_t) - sum_A_t**2 )

        x[t] = numerator/denominator

    #Take the well behaved part. By our convention 3/5 of our data.
    num_wb = int(num_timesteps*3/5)
    x = x[:num_wb]
    t_array = t_array[:num_wb]
    opt_params, params_cov = curve_fit(function_to_fit, t_array, x)
    tau = opt_params[1]

    error = np.sqrt( (2*tau/num_timesteps)*(np.average(A[:num_wb]*A[:num_wb]) - np.average(A[:num_wb])**2  ) )
    
    return tau, error