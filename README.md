<p align="center">
  	<img alt="Header image of witlab - A Python simulation framework for
easy whole-brain neural mass modeling." src="https://github.com/WitLaboratory/witlab/raw/master/resources/readme_header.png" >
</p> 
<p align="center">
  <a href="https://github.com/WitLaboratory/witlab/actions">
  	<img alt="Build" src="https://img.shields.io/github/workflow/status/WitLaboratory/witlab/ci"></a>
  <a href="https://github.com/WitLaboratory/witlab/releases">
  	<img alt="Release" src="https://img.shields.io/github/v/release/WitLaboratory/witlab"></a>
  <br>
  <a href="https://codecov.io/gh/WitLaboratory/witlab">
  	<img alt="codecov" src="https://codecov.io/gh/WitLaboratory/witlab/branch/master/graph/badge.svg"></a>
  <a href="https://pepy.tech/project/witlab">
  	<img alt="Downloads" src="https://pepy.tech/badge/witlab"></a>
  <a href="https://github.com/psf/black">
  	<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
  <a href="https://mybinder.org/v2/gh/WitLaboratory/witlab.git/master?filepath=examples">
  	<img alt="Launch in binder" src="https://mybinder.org/badge_logo.svg"></a>
</p>


<!--include-in-documentation-->

## What is witlab?

`witlab` is a simulation and optimization framework for whole-brain modeling. It allows you to implement your own neural mass models which can simulate fMRI BOLD activity. `witlab` helps you to analyse your simulations, to load and handle structural and functional brain data, and to use powerful evolutionary algorithms to tune your model's parameters and fit it to empirical data.

You can chose from different neural mass [models](https://github.com/WitLaboratory/witlab/tree/master/witlab/models) to simulate the activity of each brain area. The main implementation is a mean-field model of spiking adaptive exponential integrate-and-fire neurons (AdEx) called `ALNModel` where each brain area contains two populations of excitatory and inhibitory neurons.
The figure below shows a schematic of how a brain network is constructed:

<p align="center">
  <img src="https://github.com/WitLaboratory/witlab/raw/master/resources/pipeline.jpg">
</p>

<p align="center">
Examples:
<a href="#single-node">Single node simulation</a> ·
<a href="#whole-brain-network">Whole-brain network</a> ·
<a href="#parameter-exploration">Parameter exploration</a> ·
<a href="#evolutionary-optimization">Evolutionary optimization</a>
<br><br>    
    
</p>

## Whole-brain modeling

Typically, in whole-brain modeling, diffusion tensor imaging (DTI) is used to infer the structural connectivity (the connection strengths) between different brain areas. In a DTI scan, the direction of the diffusion of molecules is measured across the whole brain. Using [tractography](https://en.wikipedia.org/wiki/Tractography), this information can yield the distribution of axonal fibers in the brain that connect distant brain areas, called the connectome. Together with an atlas that divides the brain into distinct areas, a matrix can be computed that encodes how many fibers go from one area to another, the so-called structural connectivity (SC) matrix. This matrix defines the coupling strengths between brain areas and acts as an adjacency matrix of the brain network. The fiber length determines the signal transmission delay between all brain areas. Combining the structural data with a computational model of the neuronal activity of each brain area, we can create a dynamical model of the whole brain.

The resulting whole-brain model consists of interconnected brain areas, with each brain area having their internal neural dynamics. The neural activity can also be used to simulate hemodynamic [BOLD](https://en.wikipedia.org/wiki/Blood-oxygen-level-dependent_imaging) activity using the Balloon-Windkessel model, which can be compared to empirical fMRI data. Often, BOLD activity is used to compute correlations of activity between brain areas, the so called [resting state functional connectivity](https://en.wikipedia.org/wiki/Resting_state_fMRI#Functional), resulting in a matrix with correlations between each brain area. This matrix can then be fitted to empirical fMRI recordings of the resting-state activity of the brain.


Below is an animation of the neuronal activity of a whole-brain model plotted on a brain.

<p align="center">
  <img src="https://github.com/WitLaboratory/witlab/raw/master/resources/brain_slow_waves_small.gif">
</p>

## Installation

The easiest way to get going is to install the pypi package using `pip`:

```
pip install witlab
```
Alternatively, you can also clone this repository and install all dependencies with

```
git clone https://github.com/WitLaboratory/witlab.git
cd witlab/
pip install -r requirements.txt
pip install .
```
It is recommended to clone or fork the entire repository since it will also include all examples and tests.

## Project layout

```
witlab/	 				# Main module
├── models/ 					# Neural mass models
	├──model.py 				# Base model class
	└── /.../ 				# Implemented mass models
├── optimize/ 					# Optimization submodule
	├── evolution/ 				# Evolutionary optimization
	└── exploration/ 			# Parameter exploration
├── data/ 					# Empirical datasets (structural, functional)
├── utils/					# Utility belt
	├── atlases.py				# Atlases (Region names, coordinates)
	├── collections.py			# Custom data types
	├── functions.py 			# Useful functions
	├── loadData.py				# Dataset loader
	├── parameterSpace.py			# Parameter space
	├── saver.py 				# Save simulation outputs
	├── signal.py				# Signal processing functions
	└── stimulus.py 			# Stimulus construction
├── examples/					# Example Jupyter notebooks
├── docs/					# Documentation 
└── tests/					# Automated tests

```

## Examples

Example [IPython Notebooks](examples/) on how to use the library can be found in the `./examples/` directory, don't forget to check them out! You can run the examples in your browser using Binder by clicking [here](https://mybinder.org/v2/gh/WitLaboratory/witlab.git/master?filepath=examples) or one of the following links:

- [Example 0.0](https://mybinder.org/v2/gh/WitLaboratory/witlab/master?filepath=examples%2Fexample-0-aln-minimal.ipynb) - Basic use of the `aln` model
- [Example 0.3](https://mybinder.org/v2/gh/WitLaboratory/witlab/master?filepath=examples%2Fexample-0.3-fhn-minimal.ipynb) - Fitz-Hugh Nagumo model `fhn` on a brain network
- [Example 0.6](https://mybinder.org/v2/gh/WitLaboratory/witlab/master?filepath=examples%2Fexample-0.6-custom-model.ipynb) - Minimal example of how to implement your own model in `witlab`
- [Example 1.2](https://mybinder.org/v2/gh/WitLaboratory/witlab/master?filepath=examples%2Fexample-1.2-brain-network-exploration.ipynb) - Parameter exploration of a brain network and fitting to BOLD data
- [Example 2.0](https://mybinder.org/v2/gh/WitLaboratory/witlab/master?filepath=examples%2Fexample-2-evolutionary-optimization-minimal.ipynb) - A simple example of the evolutionary optimization framework 

A basic overview of the functionality of `witlab` is also given in the following. 

### Single node

This example is available in detail as a [IPython Notebook](examples/example-0-aln-minimal.ipynb). 

To create a single `aln` model with the default parameters, simply run

```python
from witlab.models.aln import ALNModel

model = ALNModel()
model.params['sigma_ou'] = 0.1 # add some noise

model.run()
```

The results from this small simulation can be plotted easily:

```python
import matplotlib.pyplot as plt
plt.plot(model.t, model.output.T)

```
<p align="left">
  <img src="https://github.com/WitLaboratory/witlab/raw/master/resources/single_timeseries.png">
</p>

### Whole-brain network

A detailed example is available as a [IPython Notebook](examples/example-0-aln-minimal.ipynb). 

To simulate a whole-brain network model, first we need to load a DTI and a resting-state fMRI dataset. `witlab` already provides some example data for you:

```python
from witlab.utils.loadData import Dataset

ds = Dataset("gw")
```
The dataset that we just loaded, looks like this:

<p align="center">
  <img src="https://github.com/WitLaboratory/witlab/raw/master/resources/gw_data.png">
</p>

We initialize a model with the dataset and run it:

```python
model = ALNModel(Cmat = ds.Cmat, Dmat = ds.Dmat)
model.params['duration'] = 5*60*1000 # in ms, simulates for 5 minutes

model.run(bold=True)
```
This can take several minutes to compute, since we are simulating 80 brain regions for 5 minutes realtime. Note that we specified `bold=True` which simulates the BOLD model in parallel to the neuronal model. The resulting firing rates and BOLD functional connectivity looks like this:
<p align="center">
  <img src="https://github.com/WitLaboratory/witlab/raw/master/resources/gw_simulated.png">
</p>

The quality of the fit of this simulation can be computed by correlating the simulated functional connectivity matrix above to the empirical resting-state functional connectivity for each subject of the dataset. This gives us an estimate of how well the model reproduces inter-areal BOLD correlations. As a rule of thumb, a value above 0.5 is considered good. 

We can compute the quality of the fit of the simulated data using `func.fc()` which calculates a functional connectivity matrix of `N` (`N` = number of brain regions) time series. We use `func.matrix_correlation()` to compare this matrix to empirical data.

```python
scores = [func.matrix_correlation(func.fc(model.BOLD.BOLD[:, 5:]), fcemp) for fcemp in ds.FCs]

print("Correlation per subject:", [f"{s:.2}" for s in scores])
print(f"Mean FC/FC correlation: {np.mean(scores):.2}")
```
```
Correlation per subject: ['0.34', '0.61', '0.54', '0.7', '0.54', '0.64', '0.69', '0.47', '0.59', '0.72', '0.58']
Mean FC/FC correlation: 0.58
```
### Parameter exploration
A detailed example of a single-node exploration is available as a [IPython Notebook](examples/example-1-aln-parameter-exploration.ipynb). For an example of a brain network exploration, see [this Notebook](examples/example-1.2-brain-network-exploration.ipynb).

Whenever you work with a model, it is of great importance to know what kind of dynamics it exhibits given a certain set of parameters. It is often useful to get an overview of the state space of a given model of interest. For example in the case of `aln`, the dynamics depends a lot on the mean inputs to the excitatory and the inhibitory population. `witlab` makes it very easy to quickly explore parameter spaces of a given model:

```python
# create model
model = ALNModel()
# define the parameter space to explore
parameters = ParameterSpace({"mue_ext_mean": np.linspace(0, 3, 21),  # input to E
		"mui_ext_mean": np.linspace(0, 3, 21)}) # input to I

# define exploration              
search = BoxSearch(model, parameters)

search.run()                
```
That's it!. You can now use the builtin functions to load the simulation results from disk and perform your analysis:

```python
search.loadResults()

# calculate maximum firing rate for each parameter
for i in search.dfResults.index:
    search.dfResults.loc[i, 'max_r'] = np.max(search.results[i]['rates_exc'][:, -int(1000/model.params['dt']):])
```
We can plot the results to get something close to a bifurcation diagram!

<p align="center">
  <img src="https://github.com/WitLaboratory/witlab/raw/master/resources/exploration_aln.png">
</p>

### Evolutionary optimization

A detailed example is available as a [IPython Notebook](examples/example-2-evolutionary-optimization-minimal.ipynb). 

`witlab` also implements evolutionary parameter optimization, which works particularly well with brain networks. In an evolutionary algorithm, each simulation is represented as an individual and the parameters of the simulation, for example coupling strengths or noise level values, are represented as the genes of each individual. An individual is a part of a population. In each generation, individuals are evaluated and ranked according to a fitness criterion. For whole-brain network simulations, this could be the fit of the simulated activity to empirical data. Then, individuals with a high fitness value are `selected` as parents and `mate` to create offspring. These offspring undergo random `mutations` of their genes. After all offspring are evaluated, the best individuals of the population are selected to transition into the next generation. This process goes on for a given amount generations until a stopping criterion is reached. This could be a predefined maximum number of generations or when a large enough population with high fitness values is found. 

An example genealogy tree is shown below. You can see the evolution starting at the top and individuals reproducing generation by generation. The color indicates the fitness.

<p align="center">
  <img src="https://github.com/WitLaboratory/witlab/raw/master/resources/evolution_tree.png", width="400">
</p>

`witlab` makes it very easy to set up your own evolutionary optimization and everything else is handled under the hood. You can chose between two implemented evolutionary algorithms: `adaptive` is a gaussian mutation and rank selection algorithm with adaptive step size that ensures convergence (a schematic is shown in the image below). `nsga2` is an implementation of the popular multi-objective optimization algorithm by Deb et al. 2002. 

<p align="center">
  <img src="https://github.com/WitLaboratory/witlab/raw/master/resources/evolutionary-algorithm.png", width="400">
</p>

Of course, if you like, you can dig deeper, define your own selection, mutation and mating operators. In the following demonstration, we will simply evaluate the fitness of each individual as the distance to the unit circle. After a couple of generations of mating, mutating and selecting, only individuals who are close to the circle should survive:

```python
from witlab.utils.parameterSpace import ParameterSpace
from witlab.optimize.evolution import Evolution

def optimize_me(traj):
    ind = evolution.getIndividualFromTraj(traj)
    
    # let's make a circle
    fitness_result = abs((ind.x**2 + ind.y**2) - 1)
    
    # gather results
    fitness_tuple = (fitness_result ,)
    result_dict = {"result" : [fitness_result]}
    
    return fitness_tuple, result_dict
    
# we define a parameter space and its boundaries
pars = ParameterSpace(['x', 'y'], [[-5.0, 5.0], [-5.0, 5.0]])

# initialize the evolution and go
evolution = Evolution(optimize_me, pars, weightList = [-1.0], POP_INIT_SIZE= 100, POP_SIZE = 50, NGEN=10)
evolution.run()    
```

That's it! Now we can check the results:

```python
evolution.loadResults()
evolution.info(plot=True)
```

This will gives us a summary of the last generation and plots a distribution of the individuals (and their parameters). Below is an animation of 10 generations of the evolutionary process. Ass you can see, after a couple of generations, all remaining individuals lie very close to the unit circle.

<p align="center">
  <img src="https://github.com/WitLaboratory/witlab/raw/master/resources/evolution_animated.gif">
</p>

## More information

### Built With

`witlab` is built using other amazing open source projects:

* [pypet](https://github.com/SmokinCaterpillar/pypet) - Python parameter exploration toolbox
* [deap](https://github.com/DEAP/deap) - Distributed Evolutionary Algorithms in Python
* [numpy](https://github.com/numpy/numpy) - The fundamental package for scientific computing with Python
* [numba](https://github.com/numba/numba) - NumPy aware dynamic Python compiler using LLVM
* [Jupyter](https://github.com/jupyter/notebook) - Jupyter Interactive Notebook


<!--end-include-in-documentation-->
