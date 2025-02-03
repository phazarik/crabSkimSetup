#!/bin/bash
# Set up CMS environment
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el8_amd64_gcc11
eval `scramv1 project CMSSW CMSSW_13_0_13`
cd CMSSW_13_0_13/src
eval `scramv1 runtime -sh`
cd ../../

echo "================= Dumping Input files ===================="
python3 -c "import PSet; print ('\n'.join(list(PSet.process.source.fileNames)))"
echo "=========================================================="

#Run the RDataFrame script with input files provided by CRAB
python3 crab_script.py $1


#RunFakeJobReport
#cmsRun -j FrameworkJobReport.xml PSet.py
