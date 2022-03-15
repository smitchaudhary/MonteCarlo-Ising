# Project 2: Monte Carlo simulation of the Ising model

This project aims to simulate the Ising Model with two different Monte Carlo algorithms: Metropolis algorithm and Wolff algorithm. A detailed explanation of both algorithms, as well as a comparison between them simulating a 20x20 Ising lattice, can be found in the report.pdf file.  

## File description
- `skeleton.py`: Code that performs Monte Carlo experiment.
- `observables.py`: Contains functions that calculate susceptibility and specific heat along with their errors. 
- `collect_data.py`: Collects data upon running for a sweep of temperatures and calculates observables and their errors. Saves all data in the `Data` folder.
- `plots.py`: Produces plots for the data that were collected from `collect_data.py`. Saves them in the `figures` folder.
- `journal.md`: Contains our progress throughout the duration of the project.



## Usage
1. clone the repository `git clone https://gitlab.kwant-project.org/computational_physics/projects/Project-2---Ising_idonfernandezg_smitchaudhary_ysotiropoulos.git`
2. Run the simulation for your choice of algorithm
    * `metropolis_bool = True` in `collect_data.py` for Metropolis Algorithm.
    * `metropolis_bool = False` in `collect_data.py` for Wolff Algorithm.
3. Run `plots.py` to plot average absolute magnetisation, energy, susceptibility, and specific heat.
    * `method = 'metropolis'` in `plots.py` for Metropolis Algorithm.
    * `method = 'wolff'` in `plots.py` for Metropolis Algorith.
    
## Requirements
- Python 3
- numpy
- scipy
- matplotlib


## Authors
- Smit Chaudhary
- Ignacio Fernández Graña
- Georgios Sotiropoulos