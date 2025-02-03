#####################################
##     nanoRDF framework           ##
##   skim/process NanoAOD datasets ##
#####################################

import ROOT
import sys

class pset(object):
    
    def __setattr__(self,key,value):
        if not hasattr(self,key):
            raise TypeError("%r is not a valid pset parameter" % key)
        object.__setattr__(self,key,value)
    
    def __init__(self):
        pass
    
    #set params
    useMT=False
    setBatch=True
    runCRAB=True
    debug_=False
    
    inputfile=None
    outputfile='ntuple_skim.root'
    configjson=None
    filter=None

    dropBranch=[]
    keepBranch=[]
    forceBranch=[]
    
    createColumn=[]
    refineCollection={}
    postProcess=[]
    
    #Filtering branches to save for output tree
    def func_filterbranchlist(self,fullbranchlist):
        filtered_branches=[]
        keep_branches=[]
        if self.dropBranch:
            filtered_branches = [col for col in fullbranchlist if not any(col.startswith(prefix) for prefix in self.dropBranch)]

        if self.keepBranch:
            keep_branches=[col for col in fullbranchlist if any(col.startswith(prefix) for prefix in self.keepBranch)]

        if self.debug_:print(filtered_branches)
        if self.debug_:print(keep_branches)

        return filtered_branches+keep_branches

    def process_crabinputFiles(self,redirector='root://cms-xrd-global.cern.ch//'):
        inputfiles = ROOT.std.vector("string")()
        for files in self.inputfile:
            file_lfn = redirector+files
            inputfiles.push_back(str(file_lfn))
            print(f"processing >>>{file_lfn}")
        
        return inputfiles
    
    
    def runNanoRDF(self):
        print("nanoRDF::begin")
        
        #General ROOT settings
        if(self.useMT):ROOT.EnableImplicitMT()#multithreding
        if(self.setBatch):ROOT.gROOT.SetBatch(True)#ROOT setbatch(no GUI)

        #ForCRABsubmit
        if self.runCRAB:
            self.inputfile=self.process_crabinputFiles()
        
        #create a dataframe
        df = ROOT.RDataFrame("Events",self.inputfile)
        ROOT.SetOwnership(df, False)
        print(f"input file opened successfully...")

        #existing branches(as a python list)
        fullbranchlist=[str(col) for col in df.GetColumnNames()]
        nevtGen=df.Count().GetValue()
        df = df.Define("nEvtGen",f"{nevtGen}")
        
        #create new column/branches[NOT KEPT IN SNAPSHOT]
        for colName,colExp in self.createColumn:
            if(df.HasColumn(colName)):
                pass
            else:
                df=df.Define(colName,colExp)
        #
        if self.createColumn:print('created new column/branches as defined...')
        
        #refinement of filtered columns
        for objects,filterexp in self.refineCollection.items():
            for branch in fullbranchlist:
                if(branch.startswith(objects)):
                    df=df.Redefine(branch,f'{branch}[{filterexp}]')
                    df=df.Redefine(f'n{objects}',f'Sum({filterexp})')
        #            
        if self.refineCollection:
            print('created refined collection after applying object filtering...')
        
        #post-process branches
        for branch,branchExp in self.postProcess:
            if(df.HasColumn(branch)):
                df=df.Redefine(branch,branchExp)
                print(f'forcefully defined post-process branch: {branch}')
            else:
                df=df.Define(branch,branchExp)
        #
        if self.postProcess:
            print('created new branches as defined in postProcess step...')

        if self.debug_:
            print("New Columns \n")
            print(self.createColumn)
            print("Post Process Columns [depends on refined collections] \n")
            print(self.postProcess)
            print("Drop Branches:: \n")
            print(self.dropBranch)
            print("Keep Branches:: \n")
            print(self.keepBranch)
            
        #Apply event selection filter
        #It can use new defined branches
        df = df.Filter(self.filter)
        nevtSel=df.Count().GetValue()
        
        ##branchesToKeep
        branches=self.func_filterbranchlist(fullbranchlist)
        branches.append('nEvtGen')
        if(self.dropBranch):print('drop branches successfully...')
        if(self.keepBranch):print('keep branches successfully...')
        for branch,_ in self.postProcess:
            if(branch.endswith('__')):continue
            branches.append(branch)
        #force branch list to fall back to external settings
        if(len(self.forceBranch)):
            branches=self.forceBranch
            print("forced branches in skimTree...")
        _branches=ROOT.std.vector("string")()
        for branch in branches:_branches.push_back(str(branch))

        print('applied Event selection filter...')
        print('saving new tree using Snapshot method...')
        print(f'saving {len(branches)}/{len(fullbranchlist)} branches in new tree...')
        #save tree in disk
        df.Snapshot("Events",self.outputfile,_branches)
                
        #metadata
        hCount=ROOT.TH1F("hCount","hCount",4,0.5,4.5)
        hCount.SetBinContent(1,nevtGen)
        hCount.SetBinContent(2,nevtSel)
        hCount.GetXaxis().SetBinLabel(1,"All")
        hCount.GetXaxis().SetBinLabel(2,"Pass")

        tmpFile=ROOT.TFile.Open(self.outputfile,'UPDATE')
        tmpFile.cd()
        hCount.Write('hCount')
        ROOT.SetOwnership(tmpFile,False)
        tmpFile.Close()

        print('successfully created skim tree...')
        print('\n-------JOB REPORT---------\n')
        print(f'Filter Efficiency (raw): {nevtGen}->{nevtSel}')
        print(f'Filter:{self.filter}')
        print(f'InputFile : {self.inputfile}')
        print(f'OutputFile: {self.outputfile}')
        print()
        print("nanoRDF::end")
