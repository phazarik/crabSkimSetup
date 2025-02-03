import os,sys
import datetime

samples=[
('DYM50',"/DYto2L-4Jets_MLL-50_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM"),
#('DYM50_ext',"/DYto2L-4Jets_MLL-50_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM"),
#('DYM10-50',"/DYto2L-4Jets_MLL-10to50_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/NANOAODSIM"),
#('TTto2L2nu',"/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM"),
#('TTto2L2nu_ext',"/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM"),
#('WZto3Lnu',"/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM"),
#('ZZto4L',"/ZZto4L_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM"),
#('ZZto4L_ext',"/ZZto4L_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM"),
#('WtoLNu-4Jets','/WtoLNu-4Jets_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM'),
#('WtoLNu-4Jets_ext','/WtoLNu-4Jets_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM'),
#('WtoLnu-amcatnlo','/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM'),
#('WWto2L2nu','/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM'),
#('WWto2L2nu_ext','/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM'),
#('ZGamma',"/ZGto2LG-1Jets_ntgc_5f_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM")
#('Run3Summer22_EraC_SingleMuon',"/SingleMuon/Run2022C-22Sep2023-v1/NANOAOD"),
#('Run3Summer22_EraC_Muon'      ,"/Muon/Run2022C-22Sep2023-v1/NANOAOD"),
#('Run3Summer22_EraD_Muon'      ,"/Muon/Run2022D-22Sep2023-v1/NANOAOD"),
#('Run3Summer22EE_EraE_Muon'    ,"/Muon/Run2022E-22Sep2023-v1/NANOAOD"),
#('Run3Summer22EE_EraF_Muon'    ,"/Muon/Run2022F-22Sep2023-v2/NANOAOD"),
#('Run3Summer22EE_EraG_Muon'    ,"/Muon/Run2022G-22Sep2023-v1/NANOAOD"),
]


jobname ="nanoRDF"
timestamp = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")

for name, dataset in samples:
    requestname = jobname + '_' + name
    workarea = 'crabjob_' + jobname + '_' + name+timestamp
    
    #Setting the arguments:
    argument1 = 'General.requestName=' + requestname
    argument2 = 'General.workArea=' + workarea
    argument3 = 'Data.inputDataset=' + dataset
    argument4 = 'Data.outputDatasetTag=' +requestname
    
    #Main process line:
    processline = f'crab submit crab_config.py {argument1} {argument2} {argument3} {argument4}'
    print('\nprocessing ... ' + processline)
    os.system(processline)
    print('Done!\n')
    #break
