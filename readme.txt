Instructions:
---------------
key: codes: >>>


1) Use "dasgoclient" to search for datasets

>>> dasgoclient -query="dataset=/WToMuNu_M-1000_TuneCP5_13TeV-pythia8/*/*"

2) Use dataset_info.sh script to know about No of events, no of files and size of a particular dataset

>>> ./dataset_info.sh /WToMuNu_M-100_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM

output is:
Dataset: /WToMuNu_M-100_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM
Events: 1988000
Files: 15
Size: 1.74 GB

3) Processing dataset using RDataFrame and CRAB Jobs

- nanoRDF.py: a simple class based framework with RDataFrame utility (Typically for developers)
- crab_script.py: This is the user interface with some arguments (in the backend nanoRDF.py is running!!)
- crab_script_runNanoRDF_advanced_skimming.py: Advanced skimming strategy using RDataFrame based analysis techniques
    a. Involves create new column
    b. Put object selection criterias
    c. Filter objects based on object selection
    d. Put some event selection criterias and save the new skim tree.

4) Crab setup:
   - you know what to do!


P.S: Always to local test, crabjob dry run before submitting the crab jobs.
