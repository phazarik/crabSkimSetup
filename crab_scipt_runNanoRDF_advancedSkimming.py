from nanoRDF import *
import PSet

pset = pset()
pset.useMT=True
pset.setBatch=True
pset.runCRAB=True


pset.inputfile=PSet.process.source.fileNames

pset.createColumn=[
    ("Muon_filter","Muon_pt>10 && abs(Muon_eta)<2.4 && Muon_mediumId>0 && Muon_pfRelIso04_all<0.15 && abs(Muon_dxy)<0.05 && abs(Muon_dz)<0.1"),
    ("Electron_filter","Electron_pt>10 && abs(Electron_eta)<2.4 && Electron_cutBased>2 &&((abs(Electron_eta)<=1.479 && abs(Electron_dxy)<0.05 && abs(Electron_dz)<0.1)||(abs(Electron_eta)>1.479 && abs(Electron_dxy)<0.1 && abs(Electron_dz)<0.2))"),
    ("Muon_N","Sum(Muon_filter>0)"),
    ("Electron_N","Sum(Electron_filter>0)"),    
]

pset.refineCollection={
    "Muon":"Muon_filter>0",
    "Electron":"Electron_filter>0"
}

pset.postProcess=[
('LeadingLeptonPt',"Reverse(Sort(Concatenate(Muon_pt,Electron_pt)))[0]")
]
#pset.forceBranch=['Muon_pt','Muon_eta']

#pset.filter='(nMuon + nElectron)>0 && All(Muon_pt>10) && All(Electron_pt>10)'
pset.filter ="(Muon_N+Electron_N)>2 && LeadingLeptonPt>50"


pset.dropBranch=['HTXS_','boostedTau_','btagWeight_','CaloMET_','LowPtElectron_',
                 'FsrPhoton_','L1_','HLT_']
pset.keepBranch=["HLT_IsoMu","HLT_Ele"]

pset.runNanoRDF()
