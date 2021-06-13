#!/usr/bin/env python
# coding: utf-8

#SBATCH --account=apam           # The account name for the job.
#SBATCH --exclusive
#SBATCH --job-name=GeoClawIke  # The job name.
#SBATCH --nodes=1
#SBATCH --time=96:00:00             # The time the job will take to run.

import pandas as pd
import joblib
import dill
import os, sys
from datetime import datetime, timedelta
from GeoClawExecutionWrapper import GeoClawExecutionWrapper, days2seconds, seconds2days
import logging
import numpy as np
import scipy
from pymcmcstat.MCMC import MCMC
from pymcmcstat.plotting import MCMCPlotting
np.seterr(over='ignore');
SEED = 117
np.random.seed(SEED)

os.environ['OMP_NUM_THREADS'] = '24'
os.environ['OMP_STACKSIZE'] = '16M' 

# In[2]:

model = GeoClawExecutionWrapper()
model.parameter_name = 'max_wind_speed'


def geofun(time, thetas, y0, xdata):
    return model.run(model.parameter_name, thetas, days2seconds(0), days2seconds(10), 1)

def interpolate_data(model_times, reference_times, ydata):
    return np.interp(model_times, reference_times, ydata)

def geoss(thetas, data):
    print ('shapes:', data.ydata[0].shape, len(data.ydata), len(data.ydata))
    print ('dir(data):', dir(data))
    ydata = data.ydata[0][:, 0]
    xdata = data.xdata[0][:, 0]
    assert len(ydata) > 0, "ydata is empty!"
    tmodel, ymodel = geofun(None, thetas, ydata[0], [])
    with open('tmodel.npy', 'w') as f:
        f.write(str(tmodel.tolist()))
    with open('ymodel.npy', 'w') as f:
        f.write(str(ymodel.tolist()))
    model_times = tmodel - tmodel.min()
    print (ydata.shape, xdata.shape)
    ydata_new = interpolate_data(model_times, xdata, ydata) 
    length = min(ymodel.shape[0], ydata_new.shape[0])
    res = ymodel.reshape(-1, 1)[:length] - ydata_new.reshape(-1, 1)[:length]
    return (res**2).sum(axis=0)



filepath = 'CO-OPS_8771450_met.csv'
ref_data = pd.read_csv(filepath)
ref_data["datetime"] = ref_data.apply(lambda x: datetime.strptime(x['Date'] + ' ' + x["Time (LST)"], '%Y/%m/%d %H:%M'), axis = 1)
max_value = ref_data['Verified (m)'].max()
ref_data['Verified (m)'] = ref_data['Verified (m)'].replace('-', np.nan)
ref_data['Verified (m)'] = ref_data['Verified (m)'].astype(float)
ref_data.dropna(subset=['Verified (m)'], inplace = True)
ref_data["y"] = ref_data['Verified (m)'].values - ref_data['Predicted (m)'].values

start_timestamp = datetime.strptime('2008-09-13T07:00:00', '%Y-%m-%dT%H:%M:%S')
time_offset = lambda dt: (dt - start_timestamp).total_seconds()
ref_data['time_elapsed'] = ref_data['datetime'].apply(time_offset).values

# In[10]:
tmodel, ymodel = geofun(None, None, None, [])
model_times = tmodel
ydata_new = interpolate_data(model_times, ref_data['time_elapsed'].values.ravel(), ref_data['y'].values.ravel())

with open('ydata_new.npy', 'w') as f:
    f.write(str(ydata_new.tolist()))

print ('model times:', model_times.shape, 'y_data_new:', ydata_new.shape)

# initialize MCMC object
mcstat = MCMC()

# initialize data structure 
mcstat.data.add_data_set(x = model_times,
                         y = ydata_new)

# initialize parameter array
#theta = [0.5, 0.03, 0.1, 10, 0.02, 1.14, 0.77, 1.3, 10]

# add model parameters
dimension = model.getStorm().getParameterDimension()
for t in range(dimension[0]):
    mcstat.parameters.add_model_parameter(name='max_wind_speed_%f' % float(t), theta0=40, minimum=0, maximum = 70)

# Generate options
mcstat.simulation_options.define_simulation_options(
    nsimu=1.0e3, updatesigma=True)

# Define model object
mcstat.model_settings.define_model_settings(
    sos_function=geoss,
    sigma2=0.01**2
)


# In[11]:


# check model evaluation
theta = dimension[0] * [40.]
ss = geoss(theta, mcstat.data)
print('ss = {}'.format(ss))


# In[ ]:


# Run simulation
print ('running simulation ...')
mcstat.run_simulation()

# dump run times
with open ('runtimes.txt', 'w') as f:
    f.write(str(model.runtimes))

# extract info from results
results = mcstat.simulation_results.results
burnin = int(results['nsimu']/2)
chain = results['chain'][burnin:, :]
s2chain = results['s2chain'][burnin:, :]
names = results['names'] # parameter names

# dump chainstats
stats = mcstat.chainstats(chain, results, returnstats = True)
with open ('stats.txt', 'w') as f:
    f.write(str(stats))

from pymcmcstat import mcmcplot as mcp
settings = dict(
    fig=dict(figsize=(7, 6))
)

# plot chain panel
f = mcp.plot_chain_panel(chain, names, settings)
f.savefig('chain_panel.png')

# plot density panel
f = mcp.plot_density_panel(chain, names, settings)
f.savefig('density_panel.png')

# pairwise correlation
f = mcp.plot_pairwise_correlation_panel(chain, names, settings)
f.savefig('correlation_panel.png')

# dump results object
with open('results.dill', 'wb') as f:
    dill.dump(results, f)

from pymcmcstat import propagation as up

def predmodel(q, data):
    tmodel, ymodel = geofun(None, q, None, [])
    return ymodel

intervals = up.calculate_intervals(chain, results, mcstat.data, predmodel, s2chain=s2chain)

# dump intervals
with open ('intervals.dill', 'wb') as f:
    dill.dump(intervals, f)

# dump entire mcstat object
with open('mcstat.dill', 'wb') as f:
    dill.dump(mcstat, f)


'''
results = mcstat.simulation_results.results
burnin = int(results['nsimu']/2)
chain = results['chain'][burnin:, :]
s2chain = results['s2chain'][burnin:, :]
names = results['names'] # parameter names

# display chain stats
mcstat.chainstats(chain, results)

from pymcmcstat import mcmcplot as mcp
settings = dict(
    fig=dict(figsize=(7, 6))
)
# plot chain panel
mcp.plot_chain_panel(chain, names, settings)
# plot density panel
mcp.plot_density_panel(chain, names, settings)
# pairwise correlation
f = mcp.plot_pairwise_correlation_panel(chain, names, settings)
'''

# In[ ]:


print ('done')
