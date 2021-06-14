from clawpack.pyclaw.gauges import GaugeSolution
from clawpack.geoclaw.surge.storm import Storm

import os  
import sys 
import datetime 

import numpy as np 
import matplotlib.pyplot as plt 
from scipy.interpolate import barycentric_interpolate 
from scipy.interpolate import interp1d 
import scipy.interpolate as interpolate 

class Surge(): 

    def __init__(self, geo_storm_path=None, storm_path=None,
                file_format="geoclaw", gauge_output=None): 

        if storm_path is not None: 
            print("storm path in surge:", storm_path)
            self.storm = Storm(path=storm_path, file_format="geoclaw")
            self.num_forecasts = len(self.storm.t)
            self.storm_duration = 3600*(self.num_forecasts - 1) * 6 # seconds
            self.num_hourly_timesteps = 3600*(self.num_forecasts - 1) * 6 + 3600 # seconds

        self.gauge = None
        
        self.t = None 
        self.time_offset = None 
        self.eye_location = None 
        self.max_wind_speed = None 
        self.max_wind_radius = None 
        self.central_pressure = None 
        self.storm_radius = None 
        self.geo_storm_path = None 

        # Storm descriptions - not all formats provide these
        self.name = None 
        self.basin = None                   # Basin containing storm
        self.ID = None                      # ID code - depends on format
        self.classification = None          # Classification of storm (e.g. HU)
        self.event = None                   # Event (e.g. landfall) - HURDAT
        
        if geo_storm_path is not None: 
            self.read_geosurge(geo_storm_path, file_format=file_format) 
 
    def read_gauges(self, output=None, gauge_id=None,
                    file_format='geoclaw_surge'): 
        r"""
        Read input from geoclaw gauge text files 
        to populate the gauge height attribute
        of the surge class object 
        """
        '''
	self.gauge = np.empty((self.num_hourly_timesteps, num_gauges))
        
        for i in range(0, num_gauges): 
            gauge = GaugeSolution(gauge_id = i+1, path=output)
            num_gauge_data = gauge.q[3].shape[0]
            width = int(num_gauge_data/self.num_hourly_timesteps)
            for j in range(0, self.num_hourly_timesteps): 
                self.gauge[j, i] = gauge.q[3][width * j]
	'''
        gauge = GaugeSolution(gauge_id = gauge_id, path=output)
        return gauge.t, gauge.q[3]
	
    def update_geosurge(self, output=None, file_format='geoclaw_surge'): 
        
        self.eye_location = np.zeros((self.storm_duration+1,2))
        self.t = [self.storm.t[0] + i for i in range(self.storm_duration+1)]
                    
        # Convert the list of datetime objects to an array and 
        # subtract the initial time from each datetime object 
        # and convert the list to an array. Transform the array 
        # to be in units of seconds.
        n_hours = (self.num_forecasts - 1) * 6 
        times_obs = np.linspace(0, self.num_forecasts-1, self.num_forecasts) * 6 * 3600 
        times = np.array([3600 * i for i in range(0, n_hours+1)])
        print(times.shape)

        # Now interpolate data points given the times in seconds 
        p_obs = self.storm.central_pressure 
        mws_obs = self.storm.max_wind_speed
        mwr_obs = self.storm.max_wind_radius 
        lon_obs = self.storm.eye_location[:, 0]
        lat_obs = self.storm.eye_location[:, 1] 
        storm_radius_obs = self.storm.storm_radius

        print(mwr_obs.shape) 
            
        lon = np.linspace(np.min(lon_obs), np.max(lon_obs), n_hours+1) 
        
        # Create interpolation functions to linearly interpolate 
        # the observations 
        f_central_pressure = interp1d(times_obs, p_obs, kind='linear')
        f_max_wind_speed = interp1d(times_obs, mws_obs, kind='linear')
        f_max_wind_radius = interp1d(times_obs, mwr_obs, kind='linear')
        f_lat = interp1d(lon_obs, lat_obs, kind='linear')
        f_storm_radius = interp1d(times_obs, storm_radius_obs, kind='linear')

        # Update the attributes with the interpolations 
        self.central_pressure = f_central_pressure(times)
        self.max_wind_speed = f_max_wind_speed(times)
        self.max_wind_radius = f_max_wind_radius(times)
        self.eye_location[:, 0] = lon
        self.eye_location[:, 1] = f_lat(lon)
        self.storm_radius = f_storm_radius(times)

        print(self.max_wind_speed.shape)

        #sys.exit()
        
        #fig = plt.subplots(2, 2,figsize=(10,10))
        #ax = plt.subplot(3, 2, 1)
        #ax.plot(times_obs, self.storm.central_pressure, "o", 
        #        label="pressure observation")
        #ax.plot(times, p, label="linear interpolation")
        #ax.legend()

        #ax = plt.subplot(3, 2, 2)
        #ax.plot(times_obs, self.storm.max_wind_speed, "o", 
        #        label="max wind speed observation")
        #ax.plot(times, self.max_wind_speed, label="linear interpolation")
        #ax.legend()

        #ax = plt.subplot(3, 2, 3)
        #ax.plot(times_obs, self.storm.max_wind_radius, "o", 
        #        label="max wind radius observation")
        #ax.plot(times, self.max_wind_radius, label="linear interpolation")
        #ax.legend()

        #ax = plt.subplot(3, 2, 4)
        #ax.plot(self.storm.eye_location[:, 0], self.storm.eye_location[:, 1],
        #        "o", label="lat/lon observation")
        #ax.plot(self.eye_location[:, 0], self.eye_location[:, 1], 
        #        label="linear interpolation")
        #ax.legend()
        #
        #ax = plt.subplot(3, 2, 5)
        #ax.plot(times_obs, self.storm.storm_radius,
        #        "o", label="storm radius observation")
        #ax.plot(times, self.storm_radius, label="linear interpolation")
        #ax.legend()
        #
        #plt.savefig('interpolation_graphs', file_format='pdf') 

    def read_geosurge(self, path, file_format='geoclaw_surge', verbose=False):
        r"""Read in a GeoClaw formatted storm file

        GeoClaw storm files are read in by the Fortran code and are not meant
        to be human readable.

        :Input:
         - *path* (string) Path to the file to be read.
         - *verbose* (bool) Output more info regarding reading.
        """

        with open(path, 'r') as data_file:
            num_casts = int(data_file.readline())
            self.time_offset = datetime.datetime.strptime(
                                                      data_file.readline()[:19],
                                                      '%Y-%m-%dT%H:%M:%S')

        data = np.loadtxt(path, skiprows=3)
        num_forecasts = data.shape[0]
        self.eye_location = np.empty((num_forecasts, 2))
        assert(num_casts == num_forecasts)
        self.t = [self.time_offset + datetime.timedelta(seconds=data[i, 0])
                  for i in range(num_forecasts)]
        self.eye_location[:, 0] = data[:, 1]
        self.eye_location[:, 1] = data[:, 2]
        self.max_wind_speed = data[:, 3]
        self.max_wind_radius = data[:, 4]
        self.central_pressure = data[:, 5]
        self.storm_radius = data[:, 6]
        self.gauge = data[:, 6:]
        
        self.num_forecasts = len(self.t)
        self.storm_duration = 3600*(self.num_forecasts - 1) * 6
        self.num_hourly_timesteps = 3600*(self.num_forecasts - 1) * 6 + 3600
        
        self.geo_storm_path = path         
    
    def write_geosurge(self, path, verbose=False, max_wind_radius_fill=None,
                        storm_radius_fill=None, seconds_exist=False): 
        r"""
        Write out a geoclaw formated storm file with gauge heights attached 
        
        GeoClaw storm files are read in by the GeoClaw Fortran code.

        :Input:
         - *path* (string) Path to the file to be written.
         - *verbose* (bool) Print out additional information when writing.
         - *max_wind_radius_fill* (func) Function that can be used to fill in
           missing data for `max_wind_radius` values.  This defaults to simply
           setting the value to -1.  The function signature should be
           `max_wind_radius(t, storm)` where t is the time of the forecast and
           `storm` is the storm object.  Note that if this or `storm_radius`
           field remains -1 that this data line will be assumed to be redundant
           and not be written out.
         - *storm_radius_fill* (func) Function that can be used to fill in
           missing data for `storm_radius` values.  This defaults to simply
           setting the value to -1.  The function signature should be
           `storm_radius(t, storm)` where t is the time of the forecast and
           `storm` is the storm object.  Note that if this or `max_wind_radius`
           field remains -1 that this data line will be assumed to be redundant
           and not be written
        """

        if max_wind_radius_fill is None:
            max_wind_radius_fill = lambda t, storm: -1
        if storm_radius_fill is None:
            storm_radius_fill = lambda t, storm: -1

        # Create list for output
        # Leave this first line blank as we need to count the actual valid lines
        # that will be left in the file below
        num_casts = 0
        data_string = [""]
        if self.time_offset is None:
            # Use the first time in sequence if not provided
            self.time_offset = self.t[0]
        data_string.append("%s\n\n" % self.time_offset.isoformat())
        print(len(self.t))
        for n in range(len(self.t)):
            # Remove duplicate times
            if n > 0:
                if self.t[n] == self.t[n - 1]:
                    continue

            num_columns = 7 + self.gauge.shape[1]
            format_string = ("{:19,.8e} " * num_columns)[:-1] + "\n"
            data = []

            if seconds_exist:
                data.append(self.t[n] - self.time_offset)
            else:
                data.append((self.t[n] - self.time_offset).total_seconds())

            #data.append((self.t[n] - self.time_offset).total_seconds())
            data.append(self.eye_location[n, 0])
            data.append(self.eye_location[n, 1])

            if self.max_wind_speed[n] == -1:
                continue
            data.append(self.max_wind_speed[n])

            # Allow custom function to set max wind radius if not
            # available
            if self.max_wind_radius[n] == -1:
                new_wind_radius = max_wind_radius_fill(self.t[n], self)
                if new_wind_radius == -1:
                    continue
                else:
                    data.append(new_wind_radius)
            else:
                data.append(self.max_wind_radius[n])

            if self.central_pressure[n] == -1:
                continue
            data.append(self.central_pressure[n])

            # Allow custom function to set storm radius if not available
            if self.storm_radius[n] == -1:
                new_storm_radius = storm_radius_fill(self.t[n], self)
                if new_storm_radius == -1:
                    continue
                else:
                    data.append(new_storm_radius)
            else:
                data.append(self.storm_radius[n])

            num_gauges = self.gauge.shape[1]
            for j in range(0, num_gauges): 
                data.append(self.gauge[n, j])
                
            data_string.append(format_string.format(*data))
            num_casts += 1


        # Write to actual file now that we know exactly how many lines it will
        # contain
        try:
            # Update number of forecasts here
            data_string[0] = "%s\n" % num_casts
            with open(path, "w") as data_file:
                for data_line in data_string:
                    data_file.write(data_line)

        except Exception as e:
            # Remove possibly partially generated file if not successful
            if os.path.exists(path):
                os.remove(path)
            raise e

        
if __name__ == '__main__': 
   
    #data = sys.argv[1]
    #base_path = sys.argv[2]
    #job_name = sys.argv[3]
    #job_prefix = sys.argv[4]

    ## Check to see if directory that will store new geoclaw 
    ## storm surge files exists. If not then create directory.  
    #geoclaw_surge_directory = os.path.join(base_path, 'geoclaw-surges') 
    #if not os.path.exists(geoclaw_surge_directory): 
    #    os.mkdir(geoclaw_surge_directory)

    ## Check to see if directory that will store new geoclaw 
    ## storm surge files for a specific data set exists. 
    ## If not then create directory.  
    #job_output_directory = os.path.join(geoclaw_surge_directory, job_name) 
    #if not os.path.exists(job_output_directory): 
    #    os.mkdir(job_output_directory)  

    ## Construct the file name for the geoclaw storm surge files 
    #geoclaw_surges_fname = "storm_%s.geoclaw_surge" %(job_prefix)
    #storm_fname = "LongIsland_%s.storm" %(job_prefix) 

    #geoclaw_longisland_tracks = "/rigel/apam/users/hq2152/data/storms/geoclaw-longisland-tracks"
    #storm_track_path = os.path.join(geoclaw_longisland_tracks, storm_fname)

    #surge = Surge(storm_path=os.path.join(geoclaw_longisland_tracks,
    #              storm_fname), file_format='geoclaw') 
    #surge.update_geosurge(output=None, file_format='geoclaw_surge')

    #num_gauges = 7  
    #surge.read_gauges(output=data, num_gauges=num_gauges, file_format='geoclaw_surge')
    #print(os.path.join(job_output_directory, geoclaw_surges_fname))
    #surge.write_geosurge(path=os.path.join(job_output_directory,
    #                    geoclaw_surges_fname), seconds_exist=False) 
    
    gauge_dir = os.path.join(os.getcwd(), '0000_output/') 
    surge = Surge(storm_path=os.path.join(gauge_dir, 'LongIsland_0000.storm'), file_format='geoclaw')
    surge.update_geosurge(output=None, file_format='geoclaw_surge')
    surge.read_gauges(output=gauge_dir, num_gauges=1, file_format='geoclaw_surge')
    
    
    surge.write_geosurge(path='LongIsland_0000.geoclaw_surge', seconds_exist=False)
    s = Surge(geo_storm_path = 'LongIsland_0000.geoclaw_surge', storm_path=None, 
              file_format="geoclaw_surge", gauge_output=None)
    print(s.max_wind_speed)
    print(surge.max_wind_speed)
    
    # print(s.max_wind_speed)
    # print(s.central_pressure)
   
     
     
    


















 

