from batch.batch import Job, BatchController
import os
import time
import gzip
from clawpack.clawutil.data import ClawRunData
import clawpack.clawutil as clawutil
from clawpack.geoclaw.surge.storm import Storm
import setrun
from get_hourly_gauge import Surge

def days2seconds(days):
    return days * 60.0**2 * 24.0

def seconds2days(seconds):
    return seconds/(60.0**2 * 24.0)

class CustomStorm(Storm):
    
    def __init__(self, filepath, path=None, file_format="ATCF", **kwargs):
        self.stormFile = filepath
        self.parameterName = "max_wind_speed"
        super().__init__(path, file_format, **kwargs)
        
    def updateParameter(self, values):
        if values is None:
            return
        # update max_wind_speed specifically
        vals = self.__getattribute__(self.parameterName)
        assert len(vals) == len(values), '%d != %d' % (len(vals), len(values))
        self.__setattr__(self.parameterName, values)
   
    def getParameterDimension(self):
        return self.__getattribute__(self.parameterName).shape
 
    def getStormFile(self):
        return self.stormFile
    

class GeoClawExecutionWrapper(object):

    def __init__(self):
        # get storm data, in order to create a storm object
        # Convert ATCF data to GeoClaw format
        self.runtimes = 0
        self.gauge_dir = os.path.join(os.getcwd(), '_output') 
        if not os.path.exists(self.gauge_dir):
            os.makedirs(self.gauge_dir)
        self.atcf_path = os.path.join(os.environ["CLAW"], "geoclaw", "scratch", "bal042005.dat")

        # Note that the get_remote_file function does not support gzip files which
        # are not also tar files.  The following code handles this
        with gzip.open(".".join((self.atcf_path, 'gz')), 'rb') as atcf_file:
            with open(self.atcf_path, 'w') as atcf_unzipped_file:
                atcf_unzipped_file.write(atcf_file.read().decode('ascii'))
        self.storm_file = os.path.join(os.getcwd(), os.path.join(self.gauge_dir, 'new_ike.storm'))
        self.ike = CustomStorm(self.storm_file, path=self.atcf_path, file_format="ATCF")

    def run(self, parameter_name, parameter_value, start_time_in_seconds, end_time_in_seconds, gauge_id):
        self.runtimes += 1
        job = Job()
        job.executable = 'xgeoclaw'
        job.type = "storm-surge"
        job.name = 'test'
        job.prefix = 'ike'
        job.rundata = setrun.setrun()
        job.rundata = setrun.setgeo(job.rundata)
        job.rundata.clawdata.t0 = start_time_in_seconds
        job.rundata.clawdata.tfinal = end_time_in_seconds

        # update parameter
        self.ike = CustomStorm(self.storm_file, path=self.atcf_path, file_format="ATCF")
        self.ike.updateParameter(parameter_value)

        # write storm and run job to generate storm predictions
        self.ike.write(path = self.storm_file, file_format='geoclaw')
        
        # execute job
        job.rundata.surge_data.storm_file = self.storm_file
        controller = BatchController(jobs = [job])
        controller.wait = True
        controller.verbose = False
        controller.run()

        # get gauge data from disk
        surge = Surge(storm_path = self.storm_file, file_format='ATCF')     
        return surge.read_gauges(output=self.gauge_dir, gauge_id = gauge_id, file_format='ATCF') 

    def getStorm(self):
        return self.ike
