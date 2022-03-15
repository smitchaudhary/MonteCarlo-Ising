from skeleton import *
from observables import * 
import numpy as np

#select algorithm
metropolis_bool = False

#turn on/off error estimation for better performance
error_estimation_bool = True

#Simulation parameters
L = 20
temp_sweep = np.concatenate( ( np.linspace(1.5,3,35) , np.linspace(3.1,3.5,5)) ) 
H = 0
J = 1
MCSteps = 10**4



#Derived parameters
N = L**2
n_tsteps = MCSteps*N

magn_list = []
energy_list = []
energy_squared_list = []
susc_list = []
sp_heat_list = []

magn_error_list = []
energy_error_list = []
energy_squared_error_list = []
susc_error_list = []
sp_heat_error_list = []

for temp in temp_sweep:

    #Simulation
    print(f'Simulation starting with temperature {temp}, J = {J}, H = {H}, for {L}x{L} lattice')

    energy_data, magn_data = simulate(L, temp, H, J, MCSteps , metropolis_bool)
    print('Simulation done! Calculating errors...')
    #only take the part that has reached the equilibrium. We allow 200 MCsteps to make sure
    energy_data = energy_data[200:]
    magn_data = np.abs(magn_data[200:])

    #Compute errors
    if error_estimation_bool:
        tau_energy, error_energy = auto_corr_func(energy_data)
        tau_energy_squared, error_squared_energy = auto_corr_func(energy_data**2)
        
        tau_magn, error_magn = auto_corr_func(magn_data)
        tau_magn_squared, error_squared_magn = auto_corr_func(magn_data**2)

    else:
        error_energy = 0
        error_magn = 0
        error_squared_energy = 0
        error_squared_magn = 0

    energy_error_list.append(error_energy)
    energy_squared_error_list.append(error_squared_energy)
    magn_error_list.append(error_magn)

    #Creating simulation data dictionary
    simulation_data = {'L' : L , 'N' : N, 'n_tsteps': n_tsteps, 'temp' : temp , 'H' : H, 'J' : J, \
    'energy_data' : energy_data, 'magn_data' : magn_data, \
    'error_energy': error_energy ,'error_squared_energy': error_squared_energy, 'error_magn': error_magn, 'error_squared_magn': error_squared_magn ,\
    'error_estimation_bool' : error_estimation_bool}
    
    magn_list.append(np.average(np.abs(magn_data)))
    energy_list.append(np.average(energy_data))
    energy_squared_list.append(np.average(energy_data**2))
    
    #obtain susceptibility,specific heat and errors
    susc , susc_error = susceptibility(simulation_data)
    sp_heat , sp_heat_error = specific_heat(simulation_data)

    print(f'Spec heat is : {sp_heat}   pm   {sp_heat_error}')
    print(f'Susceptibility is : {susc}  pm  {susc_error} ')

    susc_list.append(susc)
    susc_error_list.append(susc_error)
    sp_heat_list.append(sp_heat)
    sp_heat_error_list.append(sp_heat_error)
    

    data_collected = {'temp_sweep': temp_sweep ,\
        'magn_list':magn_list,'magn_error_list':magn_error_list,\
        'energy_list':energy_list, 'energy_error_list':energy_error_list,\
        'sp_heat_list' : sp_heat_list , 'sp_heat_error_list' : sp_heat_error_list,\
        'susc_list': susc_list , 'susc_error_list': susc_error_list  }
    if metropolis_bool:
        np.save( 'Data/metropolis_data_collected.npy', data_collected )
    else:
        np.save( 'Data/wolff_data_collected.npy', data_collected )

