from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')

###### set here a name for this task
config.General.requestName = 'BuToJpsiK_BMuonFilter_2016_AODSIM'
#request name is the name of the folder where crab log is saved

config.General.workArea = 'crab3_projects'
config.General.transferOutputs = True

config.section_('JobType')

###### specify here the .py config file to run
config.JobType.psetName = 'cfg_MC_aod.py'

config.JobType.pluginName = 'Analysis'
config.JobType.outputFiles = ['ntu.root']
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')

###### specify here the dataset to process
config.Data.inputDataset = '/BuToJpsiK_BMuonFilter_SoftQCDnonD_TuneCUEP8M1_13TeV-pythia8-evtgen/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM'

config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
#NJOBS = 200  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
#config.Data.totalUnits = config.Data.unitsPerJob * NJOBS

###### set here the path of a storage area you can write to
config.Data.outLFNDirBase = '/store/user/abragagn'
config.Data.publication = False

############## 

#config.Data.ignoreLocality = True

config.section_("Site")

# set here a storage site you can write to
config.Site.storageSite = 'T2_IT_Legnaro'





