#!/usr/bin/env python
import os
import argparse
import ROOT
import logging
import datetime
import string
import random
import re
import CombineHarvester.Run2HTT_Combine.CategoryConfigurations as cfg
import CombineHarvester.Run2HTT_Combine.CategoryMaps as CategoryMaps
from CombineHarvester.Run2HTT_Combine.EmbeddedConfiguration import EmbeddedConfiguration as embedded_cfg
from CombineHarvester.Run2HTT_Combine.SplitUncertainty import UncertaintySplitter
from CombineHarvester.Run2HTT_Combine.ThreadManager import ThreadManager
import CombineHarvester.Run2HTT_Combine.outputArea as outputArea

parser = argparse.ArgumentParser(description="Centralized script for running combine fits on dynamically changing analysis categories.")
parser.add_argument('--analysisStyle',nargs="+",choices=['Standard','WH','ZH'],help="Specify which analysis's models are to be run",required=True)
parser.add_argument('--years',nargs="+",choices=['2016','2017','2018'],help="Specify the year(s) to run the fit for",required=True)
parser.add_argument('--channels',nargs="+",choices=['mt','et','tt','em'],help="specify the channels to create standard data cards for")
parser.add_argument('--WHChannels',nargs="+",choices=['emt','ett','mmt','mtt'],help="specify the channels to create WH datacards for")
parser.add_argument('--ZHChannels',nargs="+",choices=['eeet','eemt','eett','mmet','mmmt','mmtt'],help='specify the channels to create ZH datacards for')
parser.add_argument('--RunShapeless',help="Run combine model without using any shape uncertainties",action="store_true")
parser.add_argument('--RunWithBinByBin',help="Run combine model without using bin-by-bin uncertainties",action="store_true")
parser.add_argument('--RunWithoutAutoMCStats',help="Run with auto mc stats command appended to data cards",action="store_true")
parser.add_argument('--RunInclusiveggH',help="Run using an inclusive ggH distribution (no STXS bins), using either this or the the inclusive qqH will cancel STXS bin measurements",action="store_true")
parser.add_argument('--RunInclusiveqqH',help="Run using an inclusive qqH distribution (no STXS bins), using either this or the inclusive ggH will cancel STXS bin measurements.",action="store_true")
parser.add_argument('--RunSTXS',help="Run using STXS categories 1.2.",action="store_true")
parser.add_argument('--ComputeSignificance',help="Compute expected significances instead of expected POIs",action="store_true")
parser.add_argument('--ComputeImpacts',help="Compute expected impacts on Inclusive POI",action="store_true")
parser.add_argument('--ComputeGOF',help="Compute saturated GOF use on forcefully blinded datacards",action="store_true")
#parser.add_argument('--DisableCategoryFits',help="Disable category card creation and fits",action="store_true")
parser.add_argument('--Timeout', help="Trigger timeout as conditions on fits (prevents infinitely running fits)", action="store_true")
parser.add_argument('--TimeoutTime',nargs='?',help="Time allotted before a timeout (linux timeout syntax)",default="180s")
parser.add_argument('--SplitUncertainties', help="Submit condor grid jobs for splitting uncertainties. Also uses nGridPoints",action="store_true")
parser.add_argument('--RunParallel',help='Run all fits in parallel using threads',action="store_true")
parser.add_argument('--numthreads',nargs='?',help='Number of threads to use to run fits in parallel',type=int,default=12)
parser.add_argument('--DecorrelateForMe',help="Run the decorrelator as part of the overall run. Looks for a datacard named smh<year><channel>_nocorrelation.root",action="store_true")
parser.add_argument('--StoreShapes', help = "Store pre and post-fit shapes for use later",action = "store_true")
parser.add_argument('--RunKappaVKappaF',help="Runs kappa_V and kappa_F scan",action="store_true")
parser.add_argument('--RealData',help="Use the RealData dataset in the limit calculation - only available for kappa_V and kappa_F scan at the moment",action="store_true")
parser.add_argument('--ControlMode',help="Run in control mode, for making accurate error control plots",action="store_true")
parser.add_argument('--ExperimentalSpeedup',help="Run experimental acceleration options. May speed up fits at slight cost to accuracy",action = "store_true")
parser.add_argument('--CorrelationMatrix',help="Generate correlation matrices for the STXS fits",action="store_true")
parser.add_argument('--Unblind',help="Unblind the analysis, and do it for real. BE SURE ABOUT THIS.",action="store_true")
parser.add_argument('--DontPrintResults',help='For use in unblinding carefully. Doesn\'t print the acutal results to screen or draw them on any plots',action="store_true")
parser.add_argument('--UseGrid',help='Sweep grid points to generate results, instead of using the approximate singles algorithm',action='store_true')
parser.add_argument('--nGridPoints',help='Number of grid points to use when using grid algorithms.',type=int,default=100)
parser.add_argument('--workspaceOnly',help='Create the text cards, and workspaces only, and then exit. Do not attempt any fits.',action='store_true')
parser.add_argument('--stage0CrossSection',help='Create workspaces for a stage 0 cross section measurements. Removes some uncertainties.',action='store_true')
parser.add_argument('--stage1CrossSection',help='Create workspaces for a stage 1 cross section measurements. Removes some uncertainties.',action='store_true')
parser.add_argument('--RunInclusiveVH',help='Run using an inclusive set of VH distributions (no STXS bins)',action="store_true")
parser.add_argument('--UseHWWSTXS',help='Run using HWW split up into its STXS components',action="store_true")

print("Parsing command line arguments.")
args = parser.parse_args() 

if 'Standard' in args.analysisStyle and args.channels == None:
    raise RuntimeError("Standard style analysis with no specified channels run!")

if 'WH' in args.analysisStyle and args.WHChannels == None:
    raise RuntimeError("WH channel analysis with no specified channels run!")

if 'ZH' in args.analysisStyle and args.ZHChannels == None:
    raise RuntimeError("ZH channel analysis with no specified channels run!")

if args.stage0CrossSection and args.stage1CrossSection:
    raise RuntimeError("Cannot do both stage 0 and stage 1 cross section workspace creation!")

if args.RunParallel:
    ThreadHandler = ThreadManager(args.numthreads)

DateTag,OutputDir = outputArea.PrepareNewOutputArea()

logging.basicConfig(filename=OutputDir+"CombineHistory_"+DateTag+".log",filemode="w",level=logging.INFO,format='%(asctime)s %(message)s')

DataCardCreationCommand = ""

outputLoggingFile = "outputLog_"+DateTag+".txt"

if 'Standard' in args.analysisStyle:
    for year in args.years:        
        for channel in args.channels:
            if args.DecorrelateForMe:
                if args.ControlMode:
                    NegativeBinCommand="python scripts/RemoveNegativeBins.py "+os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/"+channel+"_controls_"+year+".root"
                    AddShapeCommand="python scripts/PrepDecorrelatedCard.py --year "+year+" --DataCard "+os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/"+channel+"_controls_"+year+"_nocorrelation.root --OutputFileName "+os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/"+channel+"_controls_"+year+"_correlated.root "
                    SmoothingCommand = "python scripts/SmoothJESsignal.py -c "+channel+" -i "+os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/"+channel+"_controls_"+year+"_correlated.root -o "+os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/"+channel+"_controls_"+year+".root -y "+year                
                elif args.ComputeGOF:
                    print "Working on GOF with data outside signal region"
                    if not args.Unblind:
                        NegativeBinCommand="python scripts/RemoveNegativeBins.py "+os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+"_GOF.root"
                        AddShapeCommand="python scripts/PrepDecorrelatedCard.py --year "+year+" --DataCard "+os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+"_GOF_nocorrelation.root --OutputFileName "+os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+"_GOF_correlated.root "
                        SmoothingCommand = "python scripts/SmoothJESsignal.py -c "+channel+" -i "+os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+"_GOF_correlated.root -o "+os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+"_GOF.root -y "+year
                    
                    else:
                        NegativeBinCommand="python scripts/RemoveNegativeBins.py ../../auxiliaries/shapes/smh"+year+channel+".root"
                        AddShapeCommand="python scripts/PrepDecorrelatedCard.py --year "+year+" --DataCard ../../auxiliaries/shapes/smh"+year+channel+"_nocorrelation.root --OutputFileName ../../auxiliaries/shapes/smh"+year+channel+"_correlated.root "
                        SmoothingCommand = "python scripts/SmoothJESsignal.py -c "+channel+" -i ../../auxiliaries/shapes/smh"+year+channel+"_correlated.root -o ../../auxiliaries/shapes/smh"+year+channel+".root -y "+year
                else:
                    NegativeBinCommand="python scripts/RemoveNegativeBins.py ../../auxiliaries/shapes/smh"+year+channel+".root"
                    AddShapeCommand="python scripts/PrepDecorrelatedCard.py --year "+year+" --DataCard ../../auxiliaries/shapes/smh"+year+channel+"_nocorrelation.root --OutputFileName ../../auxiliaries/shapes/smh"+year+channel+"_correlated.root "
                    SmoothingCommand = "python scripts/SmoothJESsignal.py -c "+channel+" -i ../../auxiliaries/shapes/smh"+year+channel+"_correlated.root -o ../../auxiliaries/shapes/smh"+year+channel+".root -y "+year
                    normalizedTheoryCommand = "prepNormalizedTheoryUncertainties.py ../../auxiliaries/shapes/smh"+year+channel+".root"
                if channel=="et" or channel=="em":
                    AddShapeCommand+="--TrimYears "
                print("Duplicating shapes for year correlations")
                logging.info("Shape duplication command:")
                logging.info('\n\n'+AddShapeCommand+'\n')
                os.system(AddShapeCommand+" | tee -a "+outputLoggingFile)            
                print("Smoothing out signal JES shapes")
                logging.info("Shape smoothing command:")
                logging.info('\n\n'+SmoothingCommand+'\n')
                os.system(SmoothingCommand+" | tee -a "+outputLoggingFile)
                print("Removing Negative Bins")
                logging.info("Negative Bin Removal Command:")
                logging.info('\n\n'+NegativeBinCommand+'\n')
                os.system(NegativeBinCommand+" | tee -a "+outputLoggingFile)

                print("Creating Normalized Theory Shapes For XS Measurements")
                logging.info("Normalized Theory Command:")
                logging.info("\n\n"+normalizedTheoryCommand+"\n")
                os.system(normalizedTheoryCommand+" | tee -a "+outputLoggingFile)

            DataCardCreationCommand="SMHTT"+year
            DataCardCreationCommand+="_"+channel+" "+OutputDir
            if args.ControlMode:
                DataCardCreationCommand+=" -c"
            if args.ComputeGOF and not args.Unblind:
                DataCardCreationCommand+=" -gf"
            if args.RunShapeless:
                DataCardCreationCommand+=" -s"
            if not args.RunWithBinByBin:
                DataCardCreationCommand+=" -b"            
            if not embedded_cfg[str(year)+str(channel)]: #load from config. If false, run embedded less
                DataCardCreationCommand+=" -e"
            if args.RunInclusiveggH:
                DataCardCreationCommand+=" -g"
            if args.RunInclusiveqqH:
                DataCardCreationCommand+=" -q"
            if args.stage0CrossSection:
                DataCardCreationCommand+=" -x0"
            if args.stage1CrossSection:
                DataCardCreationCommand+=" -x1"
            if args.RunInclusiveVH:
                DataCardCreationCommand+=' --IncVH'
            if args.UseHWWSTXS:
                DataCardCreationCommand+=' --STXS_HWW'
            DataCardCreationCommand+=" --Categories"
            if args.ControlMode:
                TheFile = ROOT.TFile(os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/"+channel+"_controls_"+year+".root")
                for Directory in TheFile.GetListOfKeys():
                    DataCardCreationCommand+=" "+Directory.GetName()
            elif args.ComputeGOF:
                if not args.Unblind:
                    TheFile = ROOT.TFile(os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+"_GOF.root")
                    for Directory in TheFile.GetListOfKeys():
                        DataCardCreationCommand+=" "+Directory.GetName()
                else:
                    for Category in cfg.Categories[channel]:
                        DataCardCreationCommand+=" "+Category
            else:
                for Category in cfg.Categories[channel]:
                    DataCardCreationCommand+=" "+Category
            print("Creating data cards")
            logging.info("Data Card Creation Command:")
            logging.info('\n\n'+DataCardCreationCommand+'\n')
            assert os.system(DataCardCreationCommand+" | tee -a "+outputLoggingFile) == 0,"Model exited with status != 0. Please check for errors"

if 'WH' in args.analysisStyle:
    for year in args.years:        
        for channel in args.WHChannels:
            DataCardCreationCommand="WH"+year+"_"+channel+" "+OutputDir
            if args.RunInclusiveVH:
                DataCardCreationCommand+=' --IncVH'
            if args.UseHWWSTXS:
                DataCardCreationCommand+=' --STXS_HWW'
            logging.info("WH Datacard Creation Command:")
            logging.info('\n\n'+DataCardCreationCommand+'\n')
            assert os.system(DataCardCreationCommand+" | tee -a "+outputLoggingFile) == 0, "Model exited with status !=0. Please check for errors"

if 'ZH' in args.analysisStyle:
    for year in args.years:
        #one executable handles all channels now, so multiples don't have to be called.
        #for channel in args.ZHChannels:
        DataCardCreationCommand="ZH"+year+" "+OutputDir
        if args.RunInclusiveVH:
            DataCardCreationCommand+=' --IncVH'
        if args.UseHWWSTXS:
            DataCardCreationCommand+=' --STXS_HWW'
        logging.info("ZH Datacard Creation Command:")
        logging.info('\n\n'+DataCardCreationCommand+'\n')
        assert os.system(DataCardCreationCommand+" | tee -a "+outputLoggingFile) == 0, "Model exited with status !=0. Please check for errors"

#combine all cards together
#we can't do this the old way of first mashing all channels together and then mashing those into a final card
#messes with paths somewhere
#we have to do this in one fell swoop.
CombinedCardName = OutputDir+"FinalCard_"+DateTag+".txt"
CardCombiningCommand = "combineCards.py"
if args.SplitUncertainties:
    Splitter = UncertaintySplitter()

if 'Standard' in args.analysisStyle:
    for year in args.years:
        for channel in args.channels:
            CardNum = 1
            if args.ControlMode:
                TheFile = ROOT.TFile(os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/"+channel+"_controls_"+year+".root")
            elif args.ComputeGOF:
                if not args.Unblind:
                    TheFile = ROOT.TFile(os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+"_GOF.root")
                    print "Working on GOF with data outside signal region"
                else:
                    TheFile = ROOT.TFile(os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+".root")
            else:
                TheFile = ROOT.TFile(os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+".root")

            for Directory in TheFile.GetListOfKeys():
                if not args.ControlMode and not (Directory.GetName() in cfg.Categories[channel]):
                    continue
                if not args.RunWithoutAutoMCStats:
                    CardFile = open(OutputDir+"smh"+year+"_"+channel+"_"+str(CardNum)+"_13TeV_125.txt","a+")
                    CardFile.write("* autoMCStats 0.0\n")
                    CardFile.close()                
                if args.SplitUncertainties:                    
                    Splitter.FindAndTagGroups(OutputDir+"smh"+year+"_"+channel+"_"+str(CardNum)+"_13TeV_125.txt")
                CardCombiningCommand += " "+Directory.GetName()+"_"+year+"="+OutputDir+"smh"+year+"_"+channel+"_"+str(CardNum)+"_13TeV_125.txt "
                CardNum+=1

#now let's catch all of our WH cards if that's a part of the analysis
if 'WH' in args.analysisStyle:
    for year in args.years:
        for channel in args.WHChannels:
            whCardName="wh_"+channel+"_1_"+year+"_125.txt"
            CardFile = open(OutputDir+whCardName,"a+")
            CardFile.write("* autoMCStats 0.0\n")
            CardFile.close()
            CardCombiningCommand += " "+"WH_"+channel+"_"+year+"="+OutputDir+whCardName

if 'ZH' in args.analysisStyle:
    for year in args.years:
        zhCardIndex={
            'eeet': 1,
            'eemt': 2,
            'eett': 3,
            'mmet': 4,
            'mmmt': 5,
            'mmtt': 6,
        }#these are now handled in the same executable, and are indexed specifically
        for channel in args.ZHChannels:
            zhCardName="zh_all8_"+str(zhCardIndex[channel])+"_"+year+"_125.txt"
            CardFile = open(OutputDir+zhCardName,"a+")
            CardFile.write("* autoMCStats 0.0\n")
            CardFile.close()
            CardCombiningCommand+=" "+"ZH_"+channel+"_"+year+"="+OutputDir+zhCardName
        
CardCombiningCommand+= " > "+CombinedCardName
logging.info("Final Card Combining Command:")
logging.info('\n\n'+CardCombiningCommand+'\n')
os.system(CardCombiningCommand+" | tee -a "+outputLoggingFile)

#per signal card workspace set up
print("Setting up per signal workspace")
PerSignalName = OutputDir+"Workspace_per_signal_breakdown_cmb_"+DateTag+".root"
PerSignalWorkspaceCommand = "text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel "
if 'Standard' in args.analysisStyle:
    PerSignalWorkspaceCommand+= "--PO 'map=.*/ggH.*htt.*:r_ggH[1,-25,25]' "
    PerSignalWorkspaceCommand+= "--PO 'map=.*/qqH.*htt.*:r_qqH[1,-25,25]' "
    if args.RunInclusiveggH:
        PerSignalWorkspaceCommand+= "--PO 'map=.*/ggZH_had.*htt.*:r_ggH[1,-25,25]' "
    else:
        PerSignalWorkspaceCommand+= "--PO 'map=.*/ggZH_PTH.*htt.*:r_ggH[1,-25,25]' "
    if args.RunInclusiveqqH:
        PerSignalWorkspaceCommand+= "--PO 'map=.*/ZH_had.*htt.*:r_qqH[1,-25,25]' "
        PerSignalWorkspaceCommand+= "--PO 'map=.*/WH_had.*htt.*:r_qqH[1,-25,25]' "
    else:
        PerSignalWorkspaceCommand+= "--PO 'map=.*/ZH_0J.*htt.*:r_qqH[1,-25,25]' "
        PerSignalWorkspaceCommand+= "--PO 'map=.*/ZH_1J.*htt.*:r_qqH[1,-25,25]' "
        PerSignalWorkspaceCommand+= "--PO 'map=.*/ZH_GE2J.*htt.*:r_qqH[1,-25,25]' "
        PerSignalWorkspaceCommand+= "--PO 'map=.*/WH_0J.*htt.*:r_qqH[1,-25,25]' "
        PerSignalWorkspaceCommand+= "--PO 'map=.*/WH_1J.*htt.*:r_qqH[1,-25,25]' "
        PerSignalWorkspaceCommand+= "--PO 'map=.*/WH_GE2J.*htt.*:r_qqH[1,-25,25]' "
if 'WH' in args.analysisStyle and not 'ZH' in args.analysisStyle:
    PerSignalWorkspaceCommand+="--PO 'map=.*/WH_lep.*:r_WH[1,-25,25]' "
if 'ZH' in args.analysisStyle and not 'WH' in args.analysisStyle:
    PerSignalWorkspaceCommand+="--PO 'map=.*/ZH_lep.*:r_ZH[1,-25,25]' "
    PerSignalWorkspaceCommand+="--PO 'map=.*/ggZH_lep.*:r_ZH[1,-25,25]' "
if 'WH' in args.analysisStyle and 'ZH' in args.analysisStyle:
    PerSignalWorkspaceCommand+="--PO 'map=.*/WH_lep.*:r_VH[1,-25,25]' "
    PerSignalWorkspaceCommand+="--PO 'map=.*/ZH_lep.*:r_VH[1,-25,25]' "
    PerSignalWorkspaceCommand+="--PO 'map=.*/ggZH_lep.*:r_VH[1,-25,25]' "

PerSignalWorkspaceCommand+= CombinedCardName +" -o "+PerSignalName+" -m 125"

logging.info("Per Signal Workspace Command:")
logging.info('\n\n'+PerSignalWorkspaceCommand+'\n')
os.system(PerSignalWorkspaceCommand+" | tee -a "+outputLoggingFile)

#Set up the possible STXS bins list
#if not (args.RunInclusiveggH or args.RunInclusiveqqH):
if args.RunSTXS:
    print("Setting up STXS commands")
    
    #add in the merged ones
    PerMergedBinName = OutputDir+"workspace_per_Merged_breakdown_cmb_"+DateTag+".root"
    PerMergedBinWorkSpaceCommand = "text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel "
    MergedSignalNames=[]
    if 'Standard' in args.analysisStyle:
        ##qqH, non-VBF-topology
        MergedSignalNames.append("qqH_NONVBFTOPO")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_0J_htt.*:r_qqH_NONVBFTOPO[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_1J_htt.*:r_qqH_NONVBFTOPO[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_0_60_htt.*:r_qqH_NONVBFTOPO[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_60_120_htt.*:r_qqH_NONVBFTOPO[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_120_350_htt.*:r_qqH_NONVBFTOPO[1,-25,25]' "
        #qqH mjj 350-700, all pth
        MergedSignalNames.append("qqH_GE2J_MJJ_350_700_PTH_0_200")    
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt.*:r_qqH_GE2J_MJJ_350_700_PTH_0_200[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt.*:r_qqH_GE2J_MJJ_350_700_PTH_0_200[1,-25,25]' "
        MergedSignalNames.append("qqH_GE2J_MJJ_GE700_PTH_0_200")    
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt.*:r_qqH_GE2J_MJJ_GE700_PTH_0_200[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt.*:r_qqH_GE2J_MJJ_GE700_PTH_0_200[1,-25,25]' "
        #ggH 2 Jets
        MergedSignalNames.append("ggH_PTH_0_200_GE2J")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' " 
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' " 
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' "             
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt.*:r_ggH_PTH_0_200_GE2J[1,-25,25]' "         
        #qqH ptH>200, BSM topo
        MergedSignalNames.append("qqH_BSM")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_GE350_PTH_GE200_htt.*:r_qqH_BSM[1,-25,25]' "
        #ggH 2jets, non VBF like    
        #ggH, PTH 200+
        MergedSignalNames.append("ggH_PTH_200_300")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_200_300_htt.*:r_ggH_PTH_200_300[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_200_300_htt.*:r_ggH_PTH_200_300[1,-25,25]' "
        MergedSignalNames.append("ggH_PTH_GE300")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_300_450_htt.*:r_ggH_PTH_GE300[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_450_650_htt.*:r_ggH_PTH_GE300[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_GE650_htt.*:r_ggH_PTH_GE300[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_300_450_htt.*:r_ggH_PTH_GE300[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_450_650_htt.*:r_ggH_PTH_GE300[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_GE650_htt.*:r_ggH_PTH_GE300[1,-25,25]' "
        #0 jet general parameter
        MergedSignalNames.append("ggH_0J")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_0J_PTH_0_10_htt.*:r_ggH_0J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_0J_PTH_10_200_htt.*:r_ggH_0J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_0J_PTH_0_10_htt.*:r_ggH_0J[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_0J_PTH_10_200_htt.*:r_ggH_0J[1,-25,25]' "
        #ggH, 0j low
        #MergedSignalNames.append("ggH_0J_PTH_0_10")
        #PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_0J_PTH_0_10_htt.*:r_ggH_0J_PTH_0_10[1,-25,25]' "
        #ggH, 0j high
        #MergedSignalNames.append("ggH_0J_PTH_10_200")
        #PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_0J_PTH_10_200_htt.*:r_ggH_0J_PTH_10_200[1,-25,25]' "
        #ggH, 1j low
        MergedSignalNames.append("ggH_1J_PTH_0_60")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_1J_PTH_0_60_htt.*:r_ggH_1J_PTH_0_60[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_1J_PTH_0_60_htt.*:r_ggH_1J_PTH_0_60[1,-25,25]' "
        #ggH, 1j med
        MergedSignalNames.append("ggH_1J_PTH_60_120")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_1J_PTH_60_120_htt.*:r_ggH_1J_PTH_60_120[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_1J_PTH_60_120_htt.*:r_ggH_1J_PTH_60_120[1,-25,25]' "
        #ggH, 1j high
        MergedSignalNames.append("ggH_1J_PTH_120_200")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_1J_PTH_120_200_htt.*:r_ggH_1J_PTH_120_200[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_1J_PTH_120_200_htt.*:r_ggH_1J_PTH_120_200[1,-25,25]' "
    if 'WH' in args.analysisStyle:
        MergedSignalNames.append("WH_PTH_LT_150")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/WH_lep_PTV_0_75_htt.*:r_WH_PTH_LT_150[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/WH_lep_PTV_75_150_htt.*:r_WH_PTH_LT_150[1,-25,25]' "
        MergedSignalNames.append("WH_PTH_GT_150")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/WH_lep_PTV_150_250_0J_htt.*:r_WH_PTH_GT_150[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/WH_lep_PTV_150_250_GE1J_htt.*:r_WH_PTH_GT_150[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/WH_lep_PTV_GT250_htt.*:r_WH_PTH_GT_150[1,-25,25]' "
    if 'ZH' in args.analysisStyle:
        MergedSignalNames.append("ZH_PTH_LT_150")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ZH_lep_PTV_0_75_htt.*:r_ZH_PTH_LT_150[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ZH_lep_PTV_75_150_htt.*:r_ZH_PTH_LT_150[1,-25,25]' "
        MergedSignalNames.append("ZH_PTH_GT_150")
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ZH_lep_PTV_150_250_0J_htt.*:r_ZH_PTH_GT_150[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ZH_lep_PTV_150_250_GE1J_htt.*:r_ZH_PTH_GT_150[1,-25,25]' "
        PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ZH_lep_PTV_GT250_htt.*:r_ZH_PTH_GT_150[1,-25,25]' "

    PerMergedBinWorkSpaceCommand += CombinedCardName+" -o "+PerMergedBinName+" -m 125"

    logging.info("Per Merged Bin Work Space Command")
    logging.info('\n\n'+PerMergedBinWorkSpaceCommand+'\n')
    os.system(PerMergedBinWorkSpaceCommand+" | tee -a "+outputLoggingFile)

    #add in the aux merged ones
    PerAuxMergedBinName = OutputDir+"workspace_per_Merged_Auxiliary_breakdown_cmb_"+DateTag+".root"
    PerAuxMergedBinWorkSpaceCommand = "text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel "
    AuxMergedSignalNames=[]
    if 'Standard' in args.analysisStyle:
        ##qqH, non-VBF-topology
        AuxMergedSignalNames.append("qqH_NONVBFTOPO")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_0J_htt.*:r_qqH_NONVBFTOPO[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_1J_htt.*:r_qqH_NONVBFTOPO[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_0_60_htt.*:r_qqH_NONVBFTOPO[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_60_120_htt.*:r_qqH_NONVBFTOPO[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_120_350_htt.*:r_qqH_NONVBFTOPO[1,-25,25]' "
        #VBFTOPO_MJJ_350_700
        AuxMergedSignalNames.append("VBFTOPO_MJJ_350_700")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt.*:r_VBFTOPO_MJJ_350_700[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt.*:r_VBFTOPO_MJJ_350_700[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt.*:r_VBFTOPO_MJJ_350_700[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt.*:r_VBFTOPO_MJJ_350_700[1,-25,25]' " 
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt.*:r_VBFTOPO_MJJ_350_700[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt.*:r_VBFTOPO_MJJ_350_700[1,-25,25]' " 
        #VBFTOPO_MJJ_GE700
        AuxMergedSignalNames.append("VBFTOPO_MJJ_GE700")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt.*:r_VBFTOPO_MJJ_GE700[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt.*:r_VBFTOPO_MJJ_GE700[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt.*:r_VBFTOPO_MJJ_GE700[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt.*:r_VBFTOPO_MJJ_GE700[1,-25,25]' "             
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt.*:r_VBFTOPO_MJJ_GE700[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt.*:r_VBFTOPO_MJJ_GE700[1,-25,25]' "         
        #qqH ptH>200, BSM topo
        AuxMergedSignalNames.append("qqH_BSM")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*H_GE2J_MJJ_GE350_PTH_GE200_htt.*:r_qqH_BSM[1,-25,25]' "
        #ggH 2jets, non VBF like
        AuxMergedSignalNames.append("ggH_PTH_0_200_GE2J_MJJ_0_350")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt.*:r_ggH_PTH_0_200_GE2J_MJJ_0_350[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt.*:r_ggH_PTH_0_200_GE2J_MJJ_0_350[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt.*:r_ggH_PTH_0_200_GE2J_MJJ_0_350[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt.*:r_ggH_PTH_0_200_GE2J_MJJ_0_350[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt.*:r_ggH_PTH_0_200_GE2J_MJJ_0_350[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt.*:r_ggH_PTH_0_200_GE2J_MJJ_0_350[1,-25,25]' "
        #ggH, PTH 200+
        AuxMergedSignalNames.append("ggH_PTH_200_300")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_200_300_htt.*:r_ggH_PTH_200_300[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_200_300_htt.*:r_ggH_PTH_200_300[1,-25,25]' "
        AuxMergedSignalNames.append("ggH_PTH_GE300")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_300_450_htt.*:r_ggH_PTH_GE300[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_450_650_htt.*:r_ggH_PTH_GE300[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_GE650_htt.*:r_ggH_PTH_GE300[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_300_450_htt.*:r_ggH_PTH_GE300[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_450_650_htt.*:r_ggH_PTH_GE300[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_GE650_htt.*:r_ggH_PTH_GE300[1,-25,25]' "
        #0 jet general parameter
        AuxMergedSignalNames.append("ggH_0J")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_0J_PTH_0_10_htt.*:r_ggH_0J[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_0J_PTH_10_200_htt.*:r_ggH_0J[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_0J_PTH_0_10_htt.*:r_ggH_0J[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_0J_PTH_10_200_htt.*:r_ggH_0J[1,-25,25]' "
        #ggH, 0j low
        #AuxMergedSignalNames.append("ggH_0J_PTH_0_10")
        #PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_0J_PTH_0_10_htt125:r_ggH_0J_PTH_0_10[1,-25,25]' "
        #ggH, 0j high
        #AuxMergedSignalNames.append("ggH_0J_PTH_10_200")
        #PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_0J_PTH_10_200_htt125:r_ggH_0J_PTH_10_200[1,-25,25]' "
        #ggH, 1j low
        AuxMergedSignalNames.append("ggH_1J_PTH_0_60")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_1J_PTH_0_60_htt.*:r_ggH_1J_PTH_0_60[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_1J_PTH_0_60_htt.*:r_ggH_1J_PTH_0_60[1,-25,25]' "
        #ggH, 1j med
        AuxMergedSignalNames.append("ggH_1J_PTH_60_120")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_1J_PTH_60_120_htt.*:r_ggH_1J_PTH_60_120[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_1J_PTH_60_120_htt.*:r_ggH_1J_PTH_60_120[1,-25,25]' "
        #ggH, 1j high
        AuxMergedSignalNames.append("ggH_1J_PTH_120_200")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_1J_PTH_120_200_htt.*:r_ggH_1J_PTH_120_200[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/ggZH_PTH_0_200_1J_PTH_120_200_htt.*:r_ggH_1J_PTH_120_200[1,-25,25]' "
    if 'WH' in args.analysisStyle:
        AuxMergedSignalNames.append("WH_PTH_LT_150")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/WH_lep_PTV_0_75_htt.*:r_WH_PTH_LT_150[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/WH_lep_PTV_75_150_htt.*:r_WH_PTH_LT_150[1,-25,25]' "
        AuxMergedSignalNames.append("WH_PTH_GT_150")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/WH_lep_PTV_150_250_0J_htt.*:r_WH_PTH_GT_150[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/WH_lep_PTV_150_250_GE1J_htt.*:r_WH_PTH_GT_150[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/WH_lep_PTV_GT250_htt.*:r_WH_PTH_GT_150[1,-25,25]' "
    if 'ZH' in args.analysisStyle:
        AuxMergedSignalNames.append("ZH_PTH_LT_150")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*ZH_lep_PTV_0_75_htt.*:r_ZH_PTH_LT_150[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*ZH_lep_PTV_75_150_htt.*:r_ZH_PTH_LT_150[1,-25,25]' "
        AuxMergedSignalNames.append("ZH_PTH_GT_150")
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*ZH_lep_PTV_150_250_0J_htt.*:r_ZH_PTH_GT_150[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*ZH_lep_PTV_150_250_GE1J_htt.*:r_ZH_PTH_GT_150[1,-25,25]' "
        PerAuxMergedBinWorkSpaceCommand += "--PO 'map=.*/.*ZH_lep_PTV_GT250_htt.*:r_ZH_PTH_GT_150[1,-25,25]' "

    PerAuxMergedBinWorkSpaceCommand += CombinedCardName+" -o "+PerAuxMergedBinName+" -m 125"

    logging.info("Per Aux Merged Bin Work Space Command")
    logging.info('\n\n'+PerAuxMergedBinWorkSpaceCommand+'\n')
    os.system(PerAuxMergedBinWorkSpaceCommand+" | tee -a "+outputLoggingFile)

TextWorkspaceCommand = "text2workspace.py "+CombinedCardName+" -m 125"
logging.info("Text 2 Worskpace Command:")
logging.info('\n\n'+TextWorkspaceCommand+'\n')
os.system(TextWorkspaceCommand+" | tee -a "+outputLoggingFile)

if args.workspaceOnly:
    #move the log file into output
    os.system('mv '+outputLoggingFile+' '+OutputDir)
    #move anything we may have made in parallel, or that may be left over to the output
    os.system(" mv *"+DateTag+"* "+OutputDir)

    outputArea.PrintSessionInfo(DateTag)
    exit()

PhysModel = 'MultiDimFit'
if args.UseGrid:
    ExtraCombineOptions = '--robustFit=1 --X-rtd MINIMIZER_analytic --expectSignal=1 --cl=0.68 --algo=grid --points='+str(args.nGridPoints)
else:
    ExtraCombineOptions = '--robustFit=1 --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH --expectSignal=1 --cl=0.68 --algo=singles '
if args.ComputeSignificance:
    PhysModel = 'Significance'
    ExtraCombineOptions = '--X-rtd MINIMIZER_analytic  --cl=0.68 '
if args.StoreShapes:
    PhysModel = 'FitDiagnostics'
    ExtraCombineOptions = '--robustFit=1 --X-rtd MINIMIZER_analytic --expectSignal=1 --cl=0.68 --saveShapes '
if args.ExperimentalSpeedup:
    ExtraCombineOptions += ' --cminDefaultMinimizerStrategy 0 '
if args.ControlMode:
    ExtraCombineOptions += ' --cminDefaultMinimizerTolerance 100.0 ' 
    
#run the inclusive
CombinedWorkspaceName = CombinedCardName[:len(CombinedCardName)-3]+"root"
InclusiveCommand="combineTool.py -M "+PhysModel+" "+CombinedWorkspaceName+" "+ExtraCombineOptions+" " 
if not args.Unblind:
    InclusiveCommand+="--preFitValue=1. -t -1 "
InclusiveCommand+="-n "+DateTag+"_Inclusive"
    
if args.Timeout is True:
    InclusiveCommand = "timeout "+args.TimeoutTime+" "+InclusiveCommand
logging.info("Inclusive combine command:")
logging.info('\n\n'+InclusiveCommand+'\n')
if args.RunParallel:
    ThreadHandler.AddNewFit(InclusiveCommand,"r",OutputDir)    
elif args.DontPrintResults:
    os.system(InclusiveCommand+" > /dev/null")
else:
    os.system(InclusiveCommand+" | tee -a "+outputLoggingFile)
if args.UseGrid:
    outputScanName = "scan_Inclusive_"+DateTag
    outputScanFileName = outputScanName+".root"
    os.system("plot1DScan.py higgsCombine"+DateTag+"_Inclusive.MultiDimFit.mH120.root --output "+outputScanName)#let's draw the scans for the thing we just made

    theScanFile = ROOT.TFile(outputScanFileName)
    theResult = theScanFile.Get(outputScanName).GetXaxis().GetTitle()
    theResult = theResult.replace(" =",":")
    print(theResult)
    appendFile = open(outputLoggingFile,'a')
    appendFile.write(theResult+'\n')
    appendFile.close()
    theScanFile.Close()
if args.SplitUncertainties:
    Splitter.CreateGridMeasurement('r',OutputDir,CombinedWorkspaceName,DateTag,args.nGridPoints,logging)

os.system("mv *"+DateTag+"*.root "+OutputDir)

if not args.ComputeSignificance:
    #run the signal samples    
    stage0SignalNames = []
    if 'Standard' in args.analysisStyle:
        stage0SignalNames.append("r_ggH")
        stage0SignalNames.append("r_qqH")
    if 'WH' in args.analysisStyle and not 'ZH' in args.analysisStyle:
        stage0SignalNames.append('r_WH')
    if 'ZH' in args.analysisStyle and not 'WH' in args.analysisStyle:
        stage0SignalNames.append('r_ZH')
    if 'WH' in args.analysisStyle and 'ZH' in args.analysisStyle:
        stage0SignalNames.append('r_VH')
    for SignalName in stage0SignalNames:
        
        CombineCommand = "combineTool.py -M "+PhysModel+" "+PerSignalName+" "+ExtraCombineOptions
        if not args.Unblind:
            CombineCommand+=" --preFitValue=1. -t -1"
        CombineCommand+=" --setParameters "
        for parameter in stage0SignalNames:
            CombineCommand+=parameter+"=1,"
        CombineCommand+=" -P "+SignalName+" --floatOtherPOIs=1  -n "+DateTag+"_"+SignalName

        if args.Timeout is True:
            CombineCommand = "timeout "+args.TimeoutTime+" " + CombineCommand
        logging.info("Signal Sample Signal Command: ")
        logging.info('\n\n'+CombineCommand+'\n')
        
        if args.RunParallel:
            ThreadHandler.AddNewFit(CombineCommand,SignalName,OutputDir)
        elif args.DontPrintResults:
            os.system(CombineCommand+" > /dev/null")
        else:            
            os.system(CombineCommand+" | tee -a "+outputLoggingFile)

        if args.UseGrid:
            outputScanName = "scan_"+SignalName+"_"+DateTag
            outputScanFileName = outputScanName+".root"
            os.system("plot1DScan.py higgsCombine"+DateTag+"_"+SignalName+".MultiDimFit.mH120.root --output "+outputScanName+" --POI "+SignalName)#let's draw the scans for the thing we just made
            
            theScanFile = ROOT.TFile(outputScanFileName)
            theResult = theScanFile.Get(outputScanName).GetXaxis().GetTitle()
            theResult = theResult.replace(" =",":")
            print(theResult)
            appendFile = open(outputLoggingFile,'a')
            appendFile.write(theResult+'\n')
            appendFile.close()
            theScanFile.Close()
        if args.SplitUncertainties:            
            Splitter.CreateGridMeasurement(SignalName,OutputDir,PerSignalName,DateTag,args.nGridPoints,logging)
            
        os.system("mv *"+DateTag+"*.root "+OutputDir)
    
        #we need to remember to move and save the results file to something relevant           

# run the STXS bins
#if not (args.RunInclusiveggH or args.RunInclusiveqqH or args.ComputeSignificance):
if args.RunSTXS:    
    #run the merged bins
    for MergedBin in MergedSignalNames:
        CombineCommand = "combineTool.py -M "+PhysModel+" "+PerMergedBinName+" "+ExtraCombineOptions
        if not args.Unblind:
            CombineCommand+=" --preFitValue=1. -t -1"
        CombineCommand+=" -n "+DateTag+"_"+MergedBin+"_Merged --setParameters "
        
        for BinName in MergedSignalNames:
            CombineCommand+=("r_"+BinName+"=1,")
        if args.Timeout is True:
            CombineCommand = "timeout "+args.TimeoutTime+" " + CombineCommand        
        CombineCommand += " -P r_"+MergedBin+" --floatOtherPOIs=1"
        logging.info("Merged Bin Combine Command:")
        logging.info('\n\n'+CombineCommand+'\n')
        if args.RunParallel:
            ThreadHandler.AddNewFit(CombineCommand,"MergedScheme_"+MergedBin,OutputDir)
        elif args.DontPrintResults:
            os.system(CombineCommand+" > /dev/null")
        else:            
            os.system(CombineCommand+" | tee -a "+outputLoggingFile)
        if args.UseGrid:
            outputScanName = "scan_"+BinName+"_"+DateTag
            outputScanFileName = outputScanName+".root"
            os.system("plot1DScan.py higgsCombine"+DateTag+"_"+STXSBin+".MultiDimFit.mH120.root --output "+outputScanName+' --POI r_'+BinName)#let's draw the scans for the thing we just made
            
            theScanFile = ROOT.TFile(outputScanFileName)
            theResult = theScanFile.Get(outputScanName).GetXaxis().GetTitle()
            theResult = theResult.replace(" =",":")
            print(theResult)
            appendFile = open(outputLoggingFile,'a')
            appendFile.write(theResult+'\n')
            appendFile.close()
            theScanFile.Close()
        if args.SplitUncertainties:            
            Splitter.CreateGridMeasurement('r_'+BinName,OutputDir,PerMergedBinName,DateTag,args.nGridPoints,logging)
        os.system(" mv *"+DateTag+"*.root "+OutputDir)

    if args.CorrelationMatrix:
        supplementaryCombineCommand = "combineTool.py -M FitDiagnostics "+PerMergedBinName+" --robustFit=1 --preFitValue=1. --X-rtd MINIMIZER_analytic --cl=0.68 --saveShapes --plots --expectSignal=1 -t -1 -n "+DateTag+"_Merged_Correlation --setParameters "
        for BinName in MergedSignalNames:
            supplementaryCombineCommand += ("r_"+BinName+"=1,")
        logging.info("Merged POI Correlation matrix command:")
        logging.info('\n\n'+supplementaryCombineCommand+'\n')
        if args.DontPrintResults:
            os.system(CombineCommand+" > /dev/null")
        else:
            os.system(supplementaryCombineCommand+" | tee -a "+outputLoggingFile)
        os.system(" mv *"+DateTag+"*.root "+OutputDir)

    # same thing for the auxiliary merged scheme
    for AuxMergedBin in AuxMergedSignalNames:
        CombineCommand = "combineTool.py -M "+PhysModel+" "+PerAuxMergedBinName+" "+ExtraCombineOptions
        if not args.Unblind:
            CombineCommand+=" --preFitValue=1. -t -1"
        CombineCommand+=" -n "+DateTag+"_"+AuxMergedBin+"_AuxMerged --setParameters "
        
        for AuxBinName in AuxMergedSignalNames:
            CombineCommand+=("r_"+AuxBinName+"=1,")
        if args.Timeout is True:
            CombineCommand = "timeout "+args.TimeoutTime+" " + CombineCommand        
        CombineCommand += " -P r_"+AuxMergedBin+" --floatOtherPOIs=1"
        logging.info("Merged Bin Combine Command:")
        logging.info('\n\n'+CombineCommand+'\n')
        if args.RunParallel:
            ThreadHandler.AddNewFit(CombineCommand,"AuxMergedScheme_"+AuxMergedBin,OutputDir)
        elif args.DontPrintResults:
            os.system(CombineCommand+" > /dev/null")
        else:            
            os.system(CombineCommand+" | tee -a "+outputLoggingFile)
        if args.UseGrid:
            outputScanName = "scan_"+AuxBinName+"_"+DateTag
            outputScanFileName = outputScanName+".root"
            os.system("plot1DScan.py higgsCombine"+DateTag+"_"+STXSBin+".MultiDimFit.mH120.root --output "+outputScanName+' --POI r_'+AuxBinName)#let's draw the scans for the thing we just made
            
            theScanFile = ROOT.TFile(outputScanFileName)
            theResult = theScanFile.Get(outputScanName).GetXaxis().GetTitle()
            theResult = theResult.replace(" =",":")
            print(theResult)
            appendFile = open(outputLoggingFile,'a')
            appendFile.write(theResult+'\n')
            appendFile.close()
            theScanFile.Close()
        if args.SplitUncertainties:            
            Splitter.CreateGridMeasurement('r_'+AuxBinName,OutputDir,PerAuxMergedBinName,DateTag,args.nGridPoints,logging)
        os.system(" mv *"+DateTag+"*.root "+OutputDir)

    if args.CorrelationMatrix:
        supplementaryCombineCommand = "combineTool.py -M FitDiagnostics "+PerMergedBinName+" --robustFit=1 --preFitValue=1. --X-rtd MINIMIZER_analytic --cl=0.68 --saveShapes --plots --expectSignal=1 -t -1 -n "+DateTag+"_Merged_Correlation --setParameters "
        for BinName in MergedSignalNames:
            supplementaryCombineCommand += ("r_"+BinName+"=1,")
        logging.info("Merged POI Correlation matrix command:")
        logging.info('\n\n'+supplementaryCombineCommand+'\n')
        if args.DontPrintResults:
            os.system(CombineCommand+" > /dev/null")
        else:
            os.system(supplementaryCombineCommand+" | tee -a "+outputLoggingFile)
        os.system(" mv *"+DateTag+"*.root "+OutputDir)

#run impact fitting
if args.ComputeImpacts:
    os.chdir(OutputDir)
    print("\nCalculating Impacts, this may take a while...\n")
    print("Initial fit")
    ImpactCommand = "combineTool.py -M Impacts -d "+CombinedWorkspaceName+" -m 125 --doInitialFit --robustFit 1 --expectSignal=1" 
    if not args.Unblind:
        ImpactCommand+=" -t -1"
    ImpactCommand+= " --parallel 8 --X-rtd MINIMIZER_analytic"

    if args.ExperimentalSpeedup:
        ImpactCommand += ' --X-rtd FAST_VERTICAL_MORPH --cminDefaultMinimizerStrategy 0 '
    logging.info("Initial Fit Impact Command:")
    logging.info('\n\n'+ImpactCommand+'\n')
    if args.DontPrintResults:
        os.system(ImpactCommand+" > /dev/null")
    else:
        os.system(ImpactCommand+" | tee -a "+outputLoggingFile)        
        
    print("Full fit")
    ImpactCommand = "combineTool.py -M Impacts -d "+CombinedWorkspaceName+" -m 125 --robustFit 1 --doFits --expectSignal=1"
    if not args.Unblind:
        ImpactCommand += " -t -1"
    ImpactCommand+=" --parallel 8 --X-rtd MINIMIZER_analytic "

    if args.ExperimentalSpeedup:
        ImpactCommand += ' --X-rtd FAST_VERTICAL_MORPH --cminDefaultMinimizerStrategy 0 '
    logging.info("Full Fit Impact Command:")
    logging.info('\n\n'+ImpactCommand+'\n')
    if args.DontPrintResults:
        os.system(ImpactCommand+" > /dev/null")
    else:
        os.system(ImpactCommand+" | tee -a "+outputLoggingFile)

    print("json-ifying")
    ImpactJsonName = "impacts_final_"+DateTag+".json"
    ImpactCommand = "combineTool.py -M Impacts -d "+CombinedWorkspaceName+" -m 125 -o "+ImpactJsonName
    logging.info("JSON Output Impact Command:")
    logging.info('\n\n'+ImpactCommand+'\n')
    if args.DontPrintResults:
        os.system(ImpactCommand+" > /dev/null")
    else:
        os.system(ImpactCommand+" | tee -a "+outputLoggingFile)

    print("final impact plot")
    FinalImpactName = "impacts_final_"+DateTag
    ImpactCommand = "plotImpacts.py -i "+ImpactJsonName+" -o "+FinalImpactName
    if args.DontPrintResults:
        ImpactCommand += ' --blind'
    logging.info("Plotting Impact Command:")
    logging.info('\n\n'+ImpactCommand+'\n')
    if args.DontPrintResults:
        os.system(ImpactCommand+" > /dev/null")
    else:
        os.system(ImpactCommand+" | tee -a "+outputLoggingFile)

    os.chdir("../../")

if args.ComputeGOF:
    os.chdir(OutputDir)
    GOFJsonName = "gof_final_"+DateTag+".json"
    ImpactCommand = "combineTool.py -M GoodnessOfFit --algorithm saturated -m 125 --there -d " + CombinedWorkspaceName+" -n '.saturated.toys'  -t 25 -s 0:19:1 --parallel 12"
    if args.DontPrintResults:
        os.system(ImpactCommand+" > /dev/null")
    else:
        os.system(ImpactCommand+" | tee -a "+outputLoggingFile)

    ImpactCommand = "combineTool.py -M GoodnessOfFit --algorithm saturated -m 125 --there -d " + CombinedWorkspaceName+" -n '.saturated'"
    if args.DontPrintResults:
        os.system(ImpactCommand+" > /dev/null")
    else:
        os.system(ImpactCommand+" | tee -a "+outputLoggingFile)

    ImpactCommand = "combineTool.py -M CollectGoodnessOfFit --input higgsCombine.saturated.GoodnessOfFit.mH125.root higgsCombine.saturated.toys.GoodnessOfFit.mH125.*.root -o "+GOFJsonName
    if args.DontPrintResults:
        os.system(ImpactCommand+" > /dev/null")
    else:
        os.system(ImpactCommand+" | tee -a "+outputLoggingFile)

    ImpactCommand = "python ../../../CombineTools/scripts/plotGof.py --statistic saturated --mass 125.0 "+GOFJsonName+" --title-right='' --output='saturated' --title-left='All GoF'"
    if args.DontPrintResults:
        os.system(ImpactCommand+" > /dev/null")
    else:
        os.system(ImpactCommand+" | tee -a "+outputLoggingFile)

    for year in args.years:
        for channel in args.channels:
            if channel=="mt":
               channelTitle = "#mu#tau"
            if channel=="et":
                channelTitle = "e#tau"
            if channel=="tt":
                channelTitle = "#tau#tau"
            if channel=="em":
                channelTitle = "e#mu"
            CardNum = 1
            if args.Unblind:
                TheFile = ROOT.TFile(os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+".root")
            else:
                TheFile = ROOT.TFile(os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+"_GOF.root")
                print "Working on GOF with data outside signal region ",os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+"_GOF.root"
            for Directory in TheFile.GetListOfKeys():
                if Directory.GetName() in cfg.Categories[channel]:
                    ImpactCommand = "text2workspace.py -m 125 smh"+year+"_"+channel+"_"+str(CardNum)+"_13TeV_.txt "
                if args.DontPrintResults:
                    os.system(ImpactCommand+" > /dev/null")
                else:
                    os.system(ImpactCommand+" | tee -a "+outputLoggingFile)
                GOFJsonName = "gof_"+channel+"_"+year+"_"+str(CardNum)+"_"+DateTag+".json"
                ImpactCommand = "combineTool.py -M GoodnessOfFit --algorithm saturated -m 125 --there -d smh"+year+"_"+channel+"_"+str(CardNum)+"_13TeV_.root -n '.saturated."+year+"_"+channel+"_"+str(CardNum)+".toys'  -t 25 -s 0:19:1 --parallel 12"
                if args.DontPrintResults:
                    os.system(ImpactCommand+" > /dev/null")
                else:
                    os.system(ImpactCommand+" | tee -a "+outputLoggingFile)

                ImpactCommand = "combineTool.py -M GoodnessOfFit --algorithm saturated -m 125 --there -d smh"+year+"_"+channel+"_"+str(CardNum)+"_13TeV_.root -n '.saturated."+year+"_"+channel+"_"+str(CardNum)+"'"
                if args.DontPrintResults:
                    os.system(ImpactCommand+" > /dev/null")
                else:
                    os.system(ImpactCommand+" | tee -a "+outputLoggingFile)

                ImpactCommand = "combineTool.py -M CollectGoodnessOfFit --input higgsCombine.saturated."+year+"_"+channel+"_"+str(CardNum)+".GoodnessOfFit.mH125.root higgsCombine.saturated."+year+"_"+channel+"_"+str(CardNum)+".toys.GoodnessOfFit.mH125.*.root -o "+GOFJsonName
                os.system(ImpactCommand+" | tee -a "+outputLoggingFile)

                ImpactCommand = "python ../../../CombineTools/scripts/plotGof.py --statistic saturated --mass 125.0 "+GOFJsonName+" --title-right='' --output='saturated_"+year+"_"+channel+"_"+str(CardNum)+"' --title-left='"+year+" "+channelTitle+"' --title-right='"+CategoryMaps.mapTDir[Directory.GetName()]+"'"
                if args.DontPrintResults:
                    os.system(ImpactCommand+" > /dev/null")
                else:
                    os.system(ImpactCommand+" | tee -a "+outputLoggingFile)

                CardNum+=1

    os.chdir("../../")
#Run kappaV kappaF scan using the Asimov dataset please see below for details
if (args.RunKappaVKappaF and not args.RealData):
    os.chdir(OutputDir)

    #Create Workspace
    KappaVKappaFcmd = "text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.HiggsCouplings:cVcF --PO BRU=0 "+OutputDir+"FinalCard_"+DateTag+".txt"+"-o comb_htt_kvkf.root"
    logging.info("Text to workspace kappaV kappaF:")
    logging.info('\n\n'+KappaVKappaFcmd+'\n')
    os.system(KappaVKappaFcmd)
    #using kappav kappaf physics parameters here:/HiggsAnalysis/CombinedLimit/python/HiggsCouplings.py (and LHCHCGModels line 385 etc) 
    #the multidim fit fines the best fit value at a single point using 1000 toys spanning ranges of the coupling (k_v 0 to 5 k_f 0 to 5) - SM physics>0!
    KappaVKappaFcmd = "combine -M MultiDimFit -m 125 -n htt -t -1000 --setParameterRanges kappa_V=0.0,5.0:kappa_F=0.0,5.0 comb_htt_kvkf.root --algo=singles --robustFit=1" 
    logging.info("MultiDim Fit for kappaV kappaF central value:")
    logging.info('\n\n'+KappaVKappaFcmd+'\n')
    os.system(KappaVKappaFcmd)
    
    #Now that we have the best fit point we should draw a grid that represents the 1 sigma (standard deviation) around the best fit point. 
    #Here we use 1000 point to set up the grid with a kappa range  coupling (k_v 0 to 5 k_f 0 to 2) - SM physics>0!
    KappaVKappaFcmd = "combine -n KvKfgrid_tt -M MultiDimFit -m 125 -t -1000 --setParameterRanges kappa_V=0.0,5.0:kappa_F=0.0,2.0 comb_htt_kvkf.root --algo=grid --points=1000"   #  now dance around the central point - change the points for granularity
    logging.info("MultiDim Fit for Grid in the kappaV kappaF scan:")
    logging.info('\n\n'+KappaVKappaFcmd+'\n')
    os.system(KappaVKappaFcmd)

    #Plot the result -f points to the workspace file, order is just the order of computation for more than one input file 
    #- for example want to do Higgs gamma gamma and Higgs tau tau 
    #Layout is the location of the legend and with x and y ranges the range on the plot (similar to the scan above please) 
    #the axis hist is the same, it inherits from TH2D so this should be compatible with the number of points that we used to make the grid
    KappaVKappaFcmd = "plotKVKF.py -o plot_kVkF -f tau=higgsCombineKvKfgrid_tt.MultiDimFit.mH125.root --order=\"tau\" --legend-order=\"tau\" --layout 1 --x-range 0.0,5.0 --y-range 0.0,3.0 --axis-hist 200,0.0,5.0,200,0.0,3.0"
    logging.info("Plotting for kappaV kappaF scan:")
    logging.info('\n\n'+KappaVKappaFcmd+'\n')
    os.system(KappaVKappaFcmd)

#Run kappaV kappaF scan using the Real dataset please see below for details
if (args.RunKappaVKappaF and args.RealData):
    os.chdir(OutputDir)

    #Create Workspace
    KappaVKappaFcmd = "text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.HiggsCouplings:cVcF --PO BRU=0 "+OutputDir+"FinalCard_"+DateTag+".txt"+"-o comb_htt_kvkf.root"
    logging.info("Text to workspace kappaV kappaF:")
    logging.info('\n\n'+KappaVKappaFcmd+'\n')
    os.system(KappaVKappaFcmd)

    #using kappav kappaf physics parameters here:/HiggsAnalysis/CombinedLimit/python/HiggsCouplings.py (and LHCHCGModels line 385 etc) 
    #the multidim fit fines the best fit value at a single point using 1000 toys spanning ranges of the coupling (k_v 0 to 5 k_f 0 to 5) - SM physics>0!
    KappaVKappaFcmd = "combine -M MultiDimFit -m 125 -n htt --setParameterRanges kappa_V=0.0,5.0:kappa_F=0.0,5.0 comb_htt_kvkf.root --algo=singles --robustFit=1" # get the central point!  
    logging.info("MultiDim Fit for kappaV kappaF central value:")
    logging.info('\n\n'+KappaVKappaFcmd+'\n')
    os.system(KappaVKappaFcmd)
    
    #Now that we have the best fit point we should draw a grid that represents the 1 sigma (standard deviation) around the best fit point. 
    #Here we use 1000 point to set up the grid with a kappa range  coupling (k_v 0 to 5 k_f 0 to 2) - SM physics>0!
    KappaVKappaFcmd = "combine -n KvKfgrid_tt -M MultiDimFit -m 125 --setParameterRanges kappa_V=0.0,5.0:kappa_F=0.0,2.0 comb_htt_kvkf.root --algo=grid --points=1000"   #  now dance around the central point
    logging.info("MultiDim Fit for Grid in the kappaV kappaF scan:")
    logging.info('\n\n'+KappaVKappaFcmd+'\n')
    os.system(KappaVKappaFcmd)

    #Plot the result -f points to the workspace file, order is just the order of computation for more than one input file 
    #- for example want to do Higgs gamma gamma and Higgs tau tau 
    #Layout is the location of the legend and with x and y ranges the range on the plot (similar to the scan above please) 
    #the axis hist is the same, it inherits from TH2D so this should be compatible with the number of points that we used to make the grid
    KappaVKappaFcmd = "plotKVKF.py -o plot_kVkF -f tau=higgsCombineKvKfgrid_tt.MultiDimFit.mH125.root --order=\"tau\" --legend-order=\"tau\" --layout 1 --x-range 0.0,5.0 --y-range 0.0,3.0 --axis-hist 200,0.0,5.0,200,0.0,3.0"
    logging.info("Plotting for kappaV kappaF scan:")
    logging.info('\n\n'+KappaVKappaFcmd+'\n')
    os.system(KappaVKappaFcmd)

if args.RunParallel:
    ThreadHandler.BeginFits()
    ThreadHandler.WaitForAllThreadsToFinish()

#move the log file into output
os.system('mv '+outputLoggingFile+' '+OutputDir)
#move anything we may have made in parallel, or that may be left over to the output
os.system(" mv *"+DateTag+"* "+OutputDir)

outputArea.PrintSessionInfo(DateTag)
