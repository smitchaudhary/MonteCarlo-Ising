import numpy as np
import matplotlib.pyplot as plt

# method:  'metropolis'   or   'wolff'
method = 'wolff' 


file_name = method+'_data_collected.npy'
data_collected = np.load(f'Data/{file_name}',allow_pickle=True)[()]
locals().update(data_collected)

def plt_data(data, error , name):
    '''
    Shows and saves plots for a given collection of data.
    Parameters
    ----------
    data : nd.array
        Array of the collected data of the obsevable
    error : nd.array
        Array of the error in the collected data of the obsevable
    name : str
        Name of the observable    

    '''
    plt.plot(temp_sweep,data,'o-' , zorder=1)
    plt.errorbar(temp_sweep, data, yerr=error , ecolor='red',elinewidth=2,capsize=2,capthick=2,zorder=2,fmt='none')
    plt.xlabel('Temperature')
    plt.ylabel(name)
    plt.savefig(f'figures/{method}_{name}.svg')
    plt.show()

plt_data(magn_list,magn_error_list,'Average absolute Magnetisation')

plt_data(energy_list,energy_error_list,'Average Energy')

plt_data(sp_heat_list,sp_heat_error_list,'Specific heat')

plt_data(susc_list,susc_error_list,'Susceptibility')
