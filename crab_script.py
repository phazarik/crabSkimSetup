from nanoRDF import *
import PSet

pset = pset()
pset.useMT=True
pset.setBatch=True
pset.runCRAB=True

pset.inputfile=PSet.process.source.fileNames

pset.filter="Sum(Concatenate(Muon_pt,Electron_pt)>10)>2"

#pset.dropBranch=['HTXS_','boostedTau_','btagWeight_','CaloMET_','LowPtElectron_',
#                 'FsrPhoton_','L1_','HLT_']
#pset.keepBranch=["HLT_IsoMu","HLT_Ele","HLT_IsoTkMu"]
pset.keepBranch=['run','luminosityBlock','event','Muon_','Electron_',]
pset.runNanoRDF()
