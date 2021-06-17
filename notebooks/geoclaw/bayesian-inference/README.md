# Bayesian Inference Examples

The purpose of this project is to enable GeoClaw users to optimize GeoClaw's hyper-parameters using Bayesian Inference. The Bayesian inference engine, PyMCMCStat, treats the GeoClaw model as a black box and tries out various hyper-parameter combinations using a variation on the Metropolis-Hastings algorithm to find the best combination. This is a work-in-progress.

I had trouble getting an adequate signal from GeoClaw using first Hurricane Sandy, then Hurricane Barry, then Dennis, all located in https://github.com/mandli/surge-examples. Now, I am trying Hurricane Ike, located in https://github.com/clawpack/geoclaw/tree/master/examples/storm-surge/ike. This implementation uses Ike. I worked on this project between 2020-2021, and I am handing it off to Xiao Huang during the summer of 2021.  

Some of the problems encountered also included lining up the model's output with the reference data, from NOAA, and stretching the smaller curve to match the longer one. For the former problem, the user is obliged to choose the dates that match the storm file, while, for the latter problem, I have implemented interpolation in my code. The main script is optimize_ike.py, which calls the methods of the class, GeoClawExecutionWrapper, that wraps the GeoClaw model.
