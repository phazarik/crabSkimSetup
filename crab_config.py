from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config

config = config()

#-----------------------------------------------------------------------------
#datetime object
import datetime,sys
timestamp = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")

config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['nanoRDF.py','crab_script.py','FrameworkJobReport.xml']
config.JobType.outputFiles = ['ntuple_skim.root']
#config.JobType.scriptArgs = ['$(CRAB_Id)']

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2  # Number of files per job
config.Data.outLFNDirBase = '/store/user/alaha/nanoRDFjobs/'
config.Data.publication = False
#config.Data.outputDatasetTag = f'NanoRDF_{timestamp}'

config.Site.storageSite = 'T3_CH_CERNBOX'
