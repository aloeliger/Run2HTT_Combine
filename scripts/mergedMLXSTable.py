#!/usr/bin/env python
import ROOT
import argparse
import CombineHarvester.Run2HTT_Combine.PlottingModules.globalSettings as globalSettings
import math
from ROOT import gROOT
from array import array
gROOT.SetBatch(ROOT.kTRUE)

def roundToSigDigits(number,sigDigits):    
    return round(number,sigDigits-int(math.floor(math.log10(abs(number))))-1)

parameters_STXS = {
    'r':{
        'SMXS': 3422.279, #higgs XS is 54.257 pb, scale to fb, and use tau BR
        'mu_value':1.006, #+0.865   -0.108/+0.115
        'uncert_down':0.101,
        'uncert_up':0.100,
        'color':ROOT.kBlack,
        'axis':'H#rightarrow#tau#tau',
        'SMXS_mu_up': 0.0503,
        'SMXS_mu_down': 0.0503,        
    },
    'r_ML':{
        'SMXS': 3422.279, #higgs XS is 54.257 pb, scale to fb, and use tau BR
        'mu_value':0.7527, #+0.865   -0.108/+0.115
        'uncert_down':0.0920,
        'uncert_up':0.09847,
        'color':ROOT.kBlack,
        'axis':'H#rightarrow#tau#tau',
        'SMXS_mu_up': 0.0503,
        'SMXS_mu_down': 0.0503,        

    },
    'r_ggH':{
        'SMXS': 3051.344, #ggH XS is 48.68 pb, scale to fb and use tau BR (+ggZH)
        'mu_value':1.0088, #+1.002   -0.181/+0.194
        'uncert_down':0.318,
        'uncert_up':0.191,
        'color':ROOT.kAzure+7,
        'axis':'ggH#rightarrow#tau#tau',
        'SMXS_mu_up': 0.0523,
        'SMXS_mu_down':0.0523,
        },
    'r_ggH_ML':{
        'SMXS': 3051.344, #ggH XS is 48.68 pb, scale to fb and use tau BR (+ggZH)
        'mu_value':1.0088, #+1.002   -0.181/+0.194
        'uncert_down':0.318,
        'uncert_up':0.191,
        'color':ROOT.kAzure+7,
        'axis':'ggH#rightarrow#tau#tau',
        'SMXS_mu_up': 0.0523,
        'SMXS_mu_down':0.0523,
        },
    'r_qqH':{
        'SMXS': 328.6833, #total qqH cross section as we consider it
        'mu_value': 0.801, #+0.672   -0.223/+0.229
        'uncert_down': 0.219,
        'uncert_up': 0.230,
        'color':ROOT.kOrange-3,
        'axis':'qqH#rightarrow#tau#tau',
        'SMXS_mu_up': 0.0294,
        'SMXS_mu_down':0.0294,
        },
    'r_qqH_ML':{
        'SMXS': 328.6833, #total qqH cross section as we consider it
        'mu_value': 0.801, #+0.672   -0.223/+0.229
        'uncert_down': 0.219,
        'uncert_up': 0.230,
        'color':ROOT.kOrange-3,
        'axis':'qqH#rightarrow#tau#tau',
        'SMXS_mu_up': 0.0294,
        'SMXS_mu_down':0.0294,
        },
    'r_VH':{
        'SMXS':44.19176,
        'mu_value':1.800,
        'uncert_down':0.414,
        'uncert_up':0.444,
        'color': ROOT.kGreen+1,
        'axis':'VH#rightarrow#tau#tau',
        'SMXS_mu_up': 0.031,
        'SMXS_mu_down': 0.034,
    },
    'r_VH_ML':{
        'SMXS':44.19176,
        'mu_value':1.800,
        'uncert_down':0.414,
        'uncert_up':0.444,
        'color': ROOT.kGreen+1,
        'axis':'VH#rightarrow#tau#tau',
        'SMXS_mu_up': 0.031,
        'SMXS_mu_down': 0.034,
    },
    'r_ggH_0J':{
        'SMXS': 1752.942,
        'mu_value':-0.339,
        'uncert_down':0.438,
        'uncert_up':0.437,
        'color':ROOT.kAzure+7,
        'axis':'ggH: 0 Jet',
        'SMXS_mu_up': 0.09125,
        'SMXS_mu_down': 0.09125,        
    },
    'r_ggH_0J_PTH_0_10_ML':{
        'SMXS': 1752.942,
        'mu_value':-0.339,
        'uncert_down':0.438,
        'uncert_up':0.437,
        'color':ROOT.kAzure+7,
        'axis':'ggH: 0 Jet p_{T}^{H}[0,10]',
        'SMXS_mu_up': 0.09125,
        'SMXS_mu_down': 0.09125,        
    },
    'r_ggH_0J_PTH_10_200_ML':{
        'SMXS': 1752.942,
        'mu_value':-0.339,
        'uncert_down':0.438,
        'uncert_up':0.437,
        'color':ROOT.kAzure+7,
        'axis':'ggH: 0 Jet p_{T}^{H}[10,200]',
        'SMXS_mu_up': 0.09125,
        'SMXS_mu_down': 0.09125,        
    },
    'r_ggH_1J_PTH_0_60':{
        'SMXS': 451.0862,
        'mu_value':-0.301,
        'uncert_down':0.983,
        'uncert_up':0.987,
        'color':ROOT.kAzure+7,
        'axis':'ggH: 1 Jet, p_{T}^{H}[0,60]',
        'SMXS_mu_up': 0.140,
        'SMXS_mu_down': 0.140,        
    },
    'r_ggH_1J_PTH_0_60_ML':{
        'SMXS': 451.0862,
        'mu_value':-0.301,
        'uncert_down':0.983,
        'uncert_up':0.987,
        'color':ROOT.kAzure+7,
        'axis':'ggH: 1 Jet, p_{T}^{H}[0,60]',
        'SMXS_mu_up': 0.140,
        'SMXS_mu_down': 0.140,        
    },
    'r_ggH_1J_PTH_60_120':{
        'SMXS': 287.6776,
        'mu_value':2.663,
        'uncert_down':0.861,
        'uncert_up':0.854,
        'color':ROOT.kAzure+7,
        'axis':'ggH: 1 Jet, p_{T}^{H}[60,120]',
        'SMXS_mu_up': 0.142,
        'SMXS_mu_down': 0.142,        
    },
    'r_ggH_1J_PTH_60_120_ML':{
        'SMXS': 287.6776,
        'mu_value':2.663,
        'uncert_down':0.861,
        'uncert_up':0.854,
        'color':ROOT.kAzure+7,
        'axis':'ggH: 1 Jet, p_{T}^{H}[60,120]',
        'SMXS_mu_up': 0.142,
        'SMXS_mu_down': 0.142,        
    },
    'r_ggH_1J_PTH_120_200':{
        'SMXS': 50.04276,
        'mu_value':1.520,
        'uncert_down':0.952,
        'uncert_up':0.964,
        'color':ROOT.kAzure+7,
        'axis':'ggH: 1 Jet, p_{T}^{H}[120,200]',
        'SMXS_mu_up': 0.193,
        'SMXS_mu_down': 0.193,        
    },
    'r_ggH_1J_PTH_120_200_ML':{
        'SMXS': 50.04276,
        'mu_value':1.520,
        'uncert_down':0.952,
        'uncert_up':0.964,
        'color':ROOT.kAzure+7,
        'axis':'ggH: 1 Jet, p_{T}^{H}[120,200]',
        'SMXS_mu_up': 0.193,
        'SMXS_mu_down': 0.193,        
    },
    'r_ggH_PTH_0_200_GE2J':{
        'SMXS': 306.2587,
        'mu_value':-0.202,
        'uncert_down':0.759,
        'uncert_up':0.771,
        'color':ROOT.kAzure+7,
        'axis':'ggH: #geq 2 Jet',
        'SMXS_mu_up': 0.2296,
        'SMXS_mu_down': 0.2296,        
    },
    'r_ggH_PTH_0_200_GE2J_ML':{
        'SMXS': 306.2587,
        'mu_value':-0.202,
        'uncert_down':0.759,
        'uncert_up':0.771,
        'color':ROOT.kAzure+7,
        'axis':'ggH: #geq 2 Jet',
        'SMXS_mu_up': 0.2296,
        'SMXS_mu_down': 0.2296,        
    },
    'r_ggH_PTH_200_300':{
        'SMXS': 27.51224,
        'mu_value':0.489,
        'uncert_down':0.804,
        'uncert_up':0.817,
        'color':ROOT.kAzure+7,
        'axis':'ggH: p_{T}^{H}[200,300]',
        'SMXS_mu_up': 0.41885,
        'SMXS_mu_down': 0.41885,        
    },
    'r_ggH_PTH_200_300_ML':{
        'SMXS': 27.51224,
        'mu_value':0.489,
        'uncert_down':0.804,
        'uncert_up':0.817,
        'color':ROOT.kAzure+7,
        'axis':'ggH: p_{T}^{H}[200,300]',
        'SMXS_mu_up': 0.41885,
        'SMXS_mu_down': 0.41885,        
    },
    'r_ggH_PTH_GE300':{
        'SMXS': 7.188811,
        'mu_value':1.029,
        'uncert_down':1.007,
        'uncert_up':1.026,
        'color':ROOT.kAzure+7,
        'axis':'ggH: p_{T}^{H} > 300',
        'SMXS_mu_up': 0.467,
        'SMXS_mu_down': 0.467,        
    },
    'r_ggH_PTH_GE300_ML':{
        'SMXS': 7.188811,
        'mu_value':1.029,
        'uncert_down':1.007,
        'uncert_up':1.026,
        'color':ROOT.kAzure+7,
        'axis':'ggH: p_{T}^{H} > 300',
        'SMXS_mu_up': 0.467,
        'SMXS_mu_down': 0.467,        
    },
    'r_qqH_NONVBFTOPO':{
        'SMXS': 209.42,
        'mu_value':3.468,
        'uncert_down':2.373,
        'uncert_up':2.333,
        'color':ROOT.kOrange-3,
        'axis':'qqH: Non-VBF Topology',
        'SMXS_mu_up': 0.02919,
        'SMXS_mu_down': 0.02919,        
    },
    'r_qqH_NONVBFTOPO_ML':{
        'SMXS': 209.42,
        'mu_value':3.468,
        'uncert_down':2.373,
        'uncert_up':2.333,
        'color':ROOT.kOrange-3,
        'axis':'qqH: Non-VBF Topology',
        'SMXS_mu_up': 0.02919,
        'SMXS_mu_down': 0.02919,        
    },
    'r_qqH_GE2J_MJJ_350_700_PTH_0_200':{
        'SMXS': 34.430,
        'mu_value':0.053,
        'uncert_down':1.294,
        'uncert_up':1.295,
        'color':ROOT.kOrange-3,
        'axis':'qqH: #geq  2 Jets, m_{jj}[350,700]',
        'SMXS_mu_up': 0.03639,
        'SMXS_mu_down': 0.03639,        
    },
    'r_qqH_GE2J_MJJ_350_700_PTH_0_200_ML':{
        'SMXS': 34.430,
        'mu_value':0.053,
        'uncert_down':1.294,
        'uncert_up':1.295,
        'color':ROOT.kOrange-3,
        'axis':'qqH: #geq  2 Jets, m_{jj}[350,700]',
        'SMXS_mu_up': 0.03639,
        'SMXS_mu_down': 0.03639,        
    },
    'r_qqH_GE2J_MJJ_GE700_PTH_0_200':{
        'SMXS': 47.481,
        'mu_value':0.606,
        'uncert_down':0.362,
        'uncert_up':0.371,
        'color':ROOT.kOrange-3,
        'axis':'qqH: #geq 2 Jets, m_{jj} > 700',
        'SMXS_mu_up': 0.0379,
        'SMXS_mu_down': 0.0379,        
    },    
    'r_qqH_GE2J_MJJ_GE700_PTH_0_200_ML':{
        'SMXS': 47.481,
        'mu_value':0.606,
        'uncert_down':0.362,
        'uncert_up':0.371,
        'color':ROOT.kOrange-3,
        'axis':'qqH: #geq 2 Jets, m_{jj} > 700',
        'SMXS_mu_up': 0.0379,
        'SMXS_mu_down': 0.0379,        
    },    
    'r_qqH_BSM':{
        'SMXS': 9.8996,
        'mu_value':0.894,
        'uncert_down':0.428,
        'uncert_up':0.441,
        'color':ROOT.kOrange-3,
        'axis':'qqH: p_{T}^{H} > 200',
        'SMXS_mu_up': 0.03426,
        'SMXS_mu_down': 0.03426,        
    },    
    'r_qqH_BSM_ML':{
        'SMXS': 9.8996,
        'mu_value':0.894,
        'uncert_down':0.428,
        'uncert_up':0.441,
        'color':ROOT.kOrange-3,
        'axis':'qqH: p_{T}^{H} > 200',
        'SMXS_mu_up': 0.03426,
        'SMXS_mu_down': 0.03426,        
    },    
    'r_WH_LowPt':{
        'SMXS':20.5715,
        'mu_value':0.765,
        'uncert_down':0.908,
        'uncert_up':0.944,
        'color':ROOT.kGreen+1,
        'axis':'WH: p_{T}^{H} < 150',
        'SMXS_mu_up': 0.029,
        'SMXS_mu_down':0.029,
    },
    'r_WH_LowPt_ML':{
        'SMXS':20.5715,
        'mu_value':0.765,
        'uncert_down':0.908,
        'uncert_up':0.944,
        'color':ROOT.kGreen+1,
        'axis':'WH: p_{T}^{H} < 150',
        'SMXS_mu_up': 0.029,
        'SMXS_mu_down':0.029,
    },
    'r_WH_HighPt':{
        'SMXS':3.30085,
        'mu_value':2.621,
        'uncert_down':1.252,
        'uncert_up':1.366,
        'color':ROOT.kGreen+1,
        'axis':'WH: p_{T}^{H} > 150',
        'SMXS_mu_up':0.05,
        'SMXS_mu_down':0.05,
    },
    'r_WH_HighPt_ML':{
        'SMXS':3.30085,
        'mu_value':2.621,
        'uncert_down':1.252,
        'uncert_up':1.366,
        'color':ROOT.kGreen+1,
        'axis':'WH: p_{T}^{H} > 150',
        'SMXS_mu_up':0.05,
        'SMXS_mu_down':0.05,
    },
    'r_ZH_LowPt':{
        'SMXS':11.99453,
        'mu_value': 2.225,
        'uncert_down':1.021,
        'uncert_up':1.126,
        'color':ROOT.kGreen+1,
        'axis':'ZH: p_{T}^{H} < 150',
        'SMXS_mu_up':0.061,
        'SMXS_mu_down':0.054,
    },
    'r_ZH_LowPt_ML':{
        'SMXS':11.99453,
        'mu_value': 2.225,
        'uncert_down':1.021,
        'uncert_up':1.126,
        'color':ROOT.kGreen+1,
        'axis':'ZH: p_{T}^{H} < 150',
        'SMXS_mu_up':0.061,
        'SMXS_mu_down':0.054,
    },
    'r_ZH_HighPt':{
        'SMXS':2.55471,
        'mu_value':3.020,
        'uncert_down':1.266,
        'uncert_up':1.484,
        'color':ROOT.kGreen+1,
        'axis':'ZH: p_{T}^{H} > 150',
        'SMXS_mu_up':0.097,
        'SMXS_mu_down':0.092,
    },
    'r_ZH_HighPt_ML':{
        'SMXS':2.55471,
        'mu_value':3.020,
        'uncert_down':1.266,
        'uncert_up':1.484,
        'color':ROOT.kGreen+1,
        'axis':'ZH: p_{T}^{H} > 150',
        'SMXS_mu_up':0.097,
        'SMXS_mu_down':0.092,
    },
}

parameterOrder = ['r', 'r_ML',
                  'r_ggH', 'r_ggH_ML',
                  'r_qqH', 'r_qqH_ML',
                  'r_VH', 'r_VH_ML',
                  'r_ggH_0J', 'r_ggH_0J_PTH_0_10_ML', 'r_ggH_0J_PTH_10_200_ML',
                  'r_ggH_1J_PTH_0_60', 'r_ggH_1J_PTH_0_60_ML',
                  'r_ggH_1J_PTH_60_120', 'r_ggH_1J_PTH_60_120_ML',
                  'r_ggH_1J_PTH_120_200', 'r_ggH_1J_PTH_120_200_ML',
                  'r_ggH_PTH_0_200_GE2J', 'r_ggH_PTH_0_200_GE2J_ML',
                  'r_ggH_PTH_200_300', 'r_ggH_PTH_200_300_ML',
                  'r_ggH_PTH_GE300', 'r_ggH_PTH_GE300_ML',
                  'r_qqH_NONVBFTOPO', 'r_qqH_NONVBFTOPO_ML',
                  'r_qqH_GE2J_MJJ_350_700_PTH_0_200', 'r_qqH_GE2J_MJJ_350_700_PTH_0_200_ML',
                  'r_qqH_GE2J_MJJ_GE700_PTH_0_200', 'r_qqH_GE2J_MJJ_GE700_PTH_0_200_ML', 
                  'r_qqH_BSM', 'r_qqH_BSM_ML',
                  'r_WH_LowPt', 'r_WH_LowPt_ML',
                  'r_WH_HighPt', 'r_WH_HighPt_ML',
                  'r_ZH_LowPt', 'r_ZH_LowPt_ML',
                  'r_ZH_HighPt','r_ZH_HighPt_ML',]

latexAlignments = [40000, 40000, #inclusive: CB and ML
                   40000, 40000, #ggH: CB and ML
                   2000, 2000, #qqH: CB and ML
                   600, 600, #VH: CB and ML
                   9000, 9000, 9000, #ggH 0J: CB and 2 ggH_0J parameters: ML
                   2500, 2500,
                   5000, 5000,
                   600, 600,
                   2000, 2000,
                   300, 300,
                   90, 90,
                   5000, 5000,
                   250, 250,
                   250, 250,
                   70, 70,
                   180, 180,
                   80, 80,
                   180, 180,
                   60, 60,]


ggHZeroJetParameters = ['r_ggH_0J','r_ggH_0J_PTH_0_10_ML','r_ggH_0J_PTH_10_200_ML']

ggHNonZeroJetParameters = [
    'r_ggH_1J_PTH_0_60',
    'r_ggH_1J_PTH_60_120',
    'r_ggH_1J_PTH_120_200',
    'r_ggH_PTH_0_200_GE2J',
    'r_ggH_PTH_200_300',
    'r_ggH_PTH_GE300',
]

ggHNonZeroJetParameters_ML = [
    'r_ggH_1J_PTH_0_60_ML',
    'r_ggH_1J_PTH_60_120_ML',
    'r_ggH_1J_PTH_120_200_ML',
    'r_ggH_PTH_0_200_GE2J_ML',
    'r_ggH_PTH_200_300_ML',
    'r_ggH_PTH_GE300_ML',
]

qqHParameters= [
    'r_qqH_NONVBFTOPO',
    'r_qqH_GE2J_MJJ_350_700_PTH_0_200',
    'r_qqH_GE2J_MJJ_GE700_PTH_0_200', 
    'r_qqH_BSM',
]
qqHParameters_ML= [
    'r_qqH_NONVBFTOPO_ML',
    'r_qqH_GE2J_MJJ_350_700_PTH_0_200_ML',
    'r_qqH_GE2J_MJJ_GE700_PTH_0_200_ML', 
    'r_qqH_BSM_ML',
]

VHParameters = [
    'r_WH_LowPt',
    'r_WH_HighPt',
    'r_ZH_LowPt',
    'r_ZH_HighPt',]

VHParameters_ML = [
    'r_WH_LowPt_ML',
    'r_WH_HighPt_ML',
    'r_ZH_LowPt_ML',
    'r_ZH_HighPt_ML',]

#parser = argparse.ArgumentParser(description = 'Create a fancy cross section plot table ')
#args = parser.parse_args()

globalSettings.style.setPASStyle()
ROOT.gROOT.SetStyle('pasStyle')

#okay, let's start by creating the canvas
theCanvas = ROOT.TCanvas("crossSectionCanvas","crossSectionCanvas")
theCanvas.SetCanvasSize(1800,650)
theCanvas.Divide(1,2)
plotPad = theCanvas.GetPrimitive(theCanvas.GetName()+'_1')
ratioPad = theCanvas.GetPrimitive(theCanvas.GetName()+'_2')
plotPad.SetPad(0.0,0.45,1.,1.) 
ratioPad.SetPad(0.0,0.0,1.0,0.52) 
plotPad.SetTopMargin(1)
plotPad.SetLeftMargin(1.0)


plotPad.SetLogy()
plotPad.SetLogy()
plotPad.SetTickx()
plotPad.SetTicky()
plotPad.SetGridx()

plotGridHisto = ROOT.TH1F("XSGraphFrame","XSGraphFrame",len(parameters_STXS)-1,0.0,float(len(parameters_STXS)-1))
plotGridHisto.GetXaxis().SetNdivisions((len(parameters_STXS)-1)/2,0,0)
plotGridHisto.GetXaxis().SetTickLength(0)
#plotGridHisto.GetYaxis().SetTickLength(0)

ratioPad.SetTickx()
ratioPad.SetTicky()
ratioPad.SetGridy()
ratioPad.SetGridx()
ratioPad.SetTopMargin(0.04)
ratioPad.SetBottomMargin(0.5)
ratioPad.SetLeftMargin(1)

#ratioGridHisto = ROOT.TH1F("RatioGraphFrame","RatioGraphFrame",len(parameters_STXS)-1,0.0,float(len(parameters_STXS)-1))
ratioGridHisto = ROOT.TH1F("RatioGraphFrame","RatioGraphFrame",len(parameters_STXS)-1,0.0,float(len(parameters_STXS)-1))
ratioGridHisto.GetXaxis().SetNdivisions((len(parameters_STXS)-1)/2,0,0)
ratioGridHisto.GetXaxis().SetTickLength(0)

axisLabelHisto = ROOT.TH1F("AxisLabelHisto",
                           "AxisLabelHisto",
                           21,
                           array('f', [0.0,
                                       2.0, #inclusive bins
                                       4.0, #right edge: ggH bins
                                       6.0, #right edge: qqH bins
                                       8.0, #right edge: VH bins
                                       9.0, #ggH_0 CB 
                                       9.5, 
                                       10.0, #ggH-0 ML,
                                       12.0,
                                       14.0,
                                       16.0,
                                       18.0,
                                       20.0,
                                       22.0,
                                       24.0,
                                       26.0,
                                       28.0,
                                       30.0,
                                       32.0,
                                       34.0,
                                       36.0,
                                       38.0]))

#okay, now, let's create a multi graph that contains the points

inclusiveGraph = ROOT.TGraphAsymmErrors(1)
inclusiveGraph.SetPoint(0,0.5,parameters_STXS['r']['SMXS']*parameters_STXS['r']['mu_value'])
inclusiveGraph.SetPointEYlow(0,parameters_STXS['r']['SMXS']*parameters_STXS['r']['uncert_down'])
inclusiveGraph.SetPointEYhigh(0,parameters_STXS['r']['SMXS']*parameters_STXS['r']['uncert_up'])
inclusiveGraph.SetMarkerColor(parameters_STXS['r']['color'])
inclusiveGraph.SetLineColor(parameters_STXS['r']['color'])
inclusiveGraph.SetMarkerStyle(21)
inclusiveGraph.SetLineWidth(2)
inclusiveGraph.SetMarkerSize(1.5)

inclusiveGraph_ML = ROOT.TGraphAsymmErrors(1)
inclusiveGraph_ML.SetPoint(0,1.5,parameters_STXS['r_ML']['SMXS']*parameters_STXS['r_ML']['mu_value'])
inclusiveGraph_ML.SetPointEYlow(0,parameters_STXS['r_ML']['SMXS']*parameters_STXS['r_ML']['uncert_down'])
inclusiveGraph_ML.SetPointEYhigh(0,parameters_STXS['r_ML']['SMXS']*parameters_STXS['r_ML']['uncert_up'])
inclusiveGraph_ML.SetMarkerColor(parameters_STXS['r_ML']['color'])
inclusiveGraph_ML.SetLineColor(parameters_STXS['r_ML']['color'])
inclusiveGraph_ML.SetMarkerStyle(22)
inclusiveGraph_ML.SetLineWidth(2)
inclusiveGraph_ML.SetMarkerSize(1.5)

ggHGraph = ROOT.TGraphAsymmErrors(1)
ggHGraph.SetPoint(0,2.5,parameters_STXS['r_ggH']['SMXS']*parameters_STXS['r_ggH']['mu_value'])
ggHGraph.SetPointEYlow(0,parameters_STXS['r_ggH']['SMXS']*parameters_STXS['r_ggH']['uncert_down'])
ggHGraph.SetPointEYhigh(0,parameters_STXS['r_ggH']['SMXS']*parameters_STXS['r_ggH']['uncert_up'])
ggHGraph.SetMarkerColor(parameters_STXS['r_ggH']['color'])
ggHGraph.SetLineColor(parameters_STXS['r_ggH']['color'])
ggHGraph.SetMarkerStyle(21)
ggHGraph.SetLineWidth(2)
ggHGraph.SetMarkerSize(1.5)

ggHGraph_ML = ROOT.TGraphAsymmErrors(1)
ggHGraph_ML.SetPoint(0,3.5,parameters_STXS['r_ggH_ML']['SMXS']*parameters_STXS['r_ggH_ML']['mu_value'])
ggHGraph_ML.SetPointEYlow(0,parameters_STXS['r_ggH_ML']['SMXS']*parameters_STXS['r_ggH_ML']['uncert_down'])
ggHGraph_ML.SetPointEYhigh(0,parameters_STXS['r_ggH_ML']['SMXS']*parameters_STXS['r_ggH_ML']['uncert_up'])
ggHGraph_ML.SetMarkerColor(parameters_STXS['r_ggH_ML']['color'])
ggHGraph_ML.SetLineColor(parameters_STXS['r_ggH_ML']['color'])
ggHGraph_ML.SetMarkerStyle(22)
ggHGraph_ML.SetLineWidth(2)
ggHGraph_ML.SetMarkerSize(1.5)

qqHGraph = ROOT.TGraphAsymmErrors(1)
qqHGraph.SetPoint(0,4.5,parameters_STXS['r_qqH']['SMXS']*parameters_STXS['r_qqH']['mu_value'])
qqHGraph.SetPointEYlow(0,parameters_STXS['r_qqH']['SMXS']*parameters_STXS['r_qqH']['uncert_down'])
qqHGraph.SetPointEYhigh(0,parameters_STXS['r_qqH']['SMXS']*parameters_STXS['r_qqH']['uncert_up'])
qqHGraph.SetMarkerColor(parameters_STXS['r_qqH']['color'])
qqHGraph.SetLineColor(parameters_STXS['r_qqH']['color'])
qqHGraph.SetMarkerStyle(21)
qqHGraph.SetLineWidth(2)
qqHGraph.SetMarkerSize(1.5)

qqHGraph_ML = ROOT.TGraphAsymmErrors(1)
qqHGraph_ML.SetPoint(0,5.5,parameters_STXS['r_qqH_ML']['SMXS']*parameters_STXS['r_qqH_ML']['mu_value'])
qqHGraph_ML.SetPointEYlow(0,parameters_STXS['r_qqH_ML']['SMXS']*parameters_STXS['r_qqH_ML']['uncert_down'])
qqHGraph_ML.SetPointEYhigh(0,parameters_STXS['r_qqH_ML']['SMXS']*parameters_STXS['r_qqH_ML']['uncert_up'])
qqHGraph_ML.SetMarkerColor(parameters_STXS['r_qqH_ML']['color'])
qqHGraph_ML.SetLineColor(parameters_STXS['r_qqH_ML']['color'])
qqHGraph_ML.SetMarkerStyle(22)
qqHGraph_ML.SetLineWidth(2)
qqHGraph_ML.SetMarkerSize(1.5)

VHGraph = ROOT.TGraphAsymmErrors(1)
VHGraph.SetPoint(0,6.5,parameters_STXS['r_VH']['SMXS']*parameters_STXS['r_VH']['mu_value'])
VHGraph.SetPointEYlow(0,parameters_STXS['r_VH']['SMXS']*parameters_STXS['r_VH']['uncert_down'])
VHGraph.SetPointEYhigh(0,parameters_STXS['r_VH']['SMXS']*parameters_STXS['r_VH']['uncert_up'])
VHGraph.SetMarkerColor(parameters_STXS['r_VH']['color'])
VHGraph.SetLineColor(parameters_STXS['r_VH']['color'])
VHGraph.SetMarkerStyle(21)
VHGraph.SetLineWidth(2)
VHGraph.SetMarkerSize(1.5)

VHGraph_ML = ROOT.TGraphAsymmErrors(1)
VHGraph_ML.SetPoint(0,7.5,parameters_STXS['r_VH_ML']['SMXS']*parameters_STXS['r_VH_ML']['mu_value'])
VHGraph_ML.SetPointEYlow(0,parameters_STXS['r_VH_ML']['SMXS']*parameters_STXS['r_VH_ML']['uncert_down'])
VHGraph_ML.SetPointEYhigh(0,parameters_STXS['r_VH_ML']['SMXS']*parameters_STXS['r_VH_ML']['uncert_up'])
VHGraph_ML.SetMarkerColor(parameters_STXS['r_VH_ML']['color'])
VHGraph_ML.SetLineColor(parameters_STXS['r_VH_ML']['color'])
VHGraph_ML.SetMarkerStyle(22)
VHGraph_ML.SetLineWidth(2)
VHGraph_ML.SetMarkerSize(1.5)

ggHZeroJetGraphCB = ROOT.TGraphAsymmErrors(1)
ggHZeroJetGraphCB.SetPoint(0,8.5,parameters_STXS['r_ggH_0J']['SMXS']*parameters_STXS['r_ggH_0J']['mu_value'])
ggHZeroJetGraphCB.SetPointEYlow(0,parameters_STXS['r_ggH_0J']['SMXS']*parameters_STXS['r_ggH_0J']['uncert_down'])
ggHZeroJetGraphCB.SetPointEYhigh(0,parameters_STXS['r_ggH_0J']['SMXS']*parameters_STXS['r_ggH_0J']['uncert_up'])
ggHZeroJetGraphCB.SetMarkerColor(parameters_STXS['r_ggH_0J']['color'])
ggHZeroJetGraphCB.SetLineColor(parameters_STXS['r_ggH_0J']['color'])
ggHZeroJetGraphCB.SetMarkerStyle(21)
ggHZeroJetGraphCB.SetLineWidth(2)
ggHZeroJetGraphCB.SetMarkerSize(1.5)


ggHZeroJetGraphML = ROOT.TGraphAsymmErrors(2)

ggHZeroJetGraphML.SetPoint(0,9.25,parameters_STXS['r_ggH_0J_PTH_0_10_ML']['SMXS']*parameters_STXS['r_ggH_0J_PTH_0_10_ML']['mu_value'])
ggHZeroJetGraphML.SetPointEYlow(0,parameters_STXS['r_ggH_0J_PTH_0_10_ML']['SMXS']*parameters_STXS['r_ggH_0J_PTH_0_10_ML']['uncert_down'])
ggHZeroJetGraphML.SetPointEYhigh(0,parameters_STXS['r_ggH_0J_PTH_0_10_ML']['SMXS']*parameters_STXS['r_ggH_0J_PTH_0_10_ML']['uncert_up'])

ggHZeroJetGraphML.SetPoint(1,9.75,parameters_STXS['r_ggH_0J_PTH_10_200_ML']['SMXS']*parameters_STXS['r_ggH_0J_PTH_10_200_ML']['mu_value'])
ggHZeroJetGraphML.SetPointEYlow(1,parameters_STXS['r_ggH_0J_PTH_10_200_ML']['SMXS']*parameters_STXS['r_ggH_0J_PTH_10_200_ML']['uncert_down'])
ggHZeroJetGraphML.SetPointEYhigh(1,parameters_STXS['r_ggH_0J_PTH_10_200_ML']['SMXS']*parameters_STXS['r_ggH_0J_PTH_10_200_ML']['uncert_up'])

ggHZeroJetGraphML.SetMarkerColor(parameters_STXS['r_ggH_0J']['color'])
ggHZeroJetGraphML.SetLineColor(parameters_STXS['r_ggH_0J']['color'])
ggHZeroJetGraphML.SetMarkerStyle(22)
ggHZeroJetGraphML.SetLineWidth(2)
ggHZeroJetGraphML.SetMarkerSize(1.5)

ggHSTXSCB = ROOT.TGraphAsymmErrors(len(ggHNonZeroJetParameters))
for ggHParameterIndex in range(len(ggHNonZeroJetParameters)):
    ggHSTXSCB.SetPoint(ggHParameterIndex,
                       2*ggHParameterIndex+10.5,
                       parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['SMXS']*parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['mu_value'])
    ggHSTXSCB.SetPointEYlow(ggHParameterIndex,
                            parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['SMXS']*parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['uncert_down'])
    ggHSTXSCB.SetPointEYhigh(ggHParameterIndex,
                             parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['SMXS']*parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['uncert_up'])
    ggHSTXSCB.SetMarkerColor(parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['color'])
    ggHSTXSCB.SetLineColor(parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['color'])
ggHSTXSCB.SetMarkerStyle(21)
ggHSTXSCB.SetLineWidth(2)
ggHSTXSCB.SetMarkerSize(1.5)

ggHSTXSML = ROOT.TGraphAsymmErrors(len(ggHNonZeroJetParameters_ML))
for ggHParameterIndex in range(len(ggHNonZeroJetParameters_ML)):
    ggHSTXSML.SetPoint(ggHParameterIndex,
                       (2*ggHParameterIndex+1)+10.5,
                       parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['SMXS']*parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['mu_value'])
    ggHSTXSML.SetPointEYlow(ggHParameterIndex,
                            parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['SMXS']*parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['uncert_down'])
    ggHSTXSML.SetPointEYhigh(ggHParameterIndex,
                             parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['SMXS']*parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['uncert_up'])
    ggHSTXSML.SetMarkerColor(parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['color'])
    ggHSTXSML.SetLineColor(parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['color'])
ggHSTXSML.SetMarkerStyle(22)
ggHSTXSML.SetLineWidth(2)
ggHSTXSML.SetMarkerSize(1.5)

qqHSTXSCB = ROOT.TGraphAsymmErrors(len(qqHParameters))
for qqHParameterIndex in range(len(qqHParameters)):
    qqHSTXSCB.SetPoint(qqHParameterIndex,
                       2*qqHParameterIndex+10.5+len(ggHNonZeroJetParameters)+len(ggHNonZeroJetParameters_ML),
                     parameters_STXS[qqHParameters[qqHParameterIndex]]['SMXS']*parameters_STXS[qqHParameters[qqHParameterIndex]]['mu_value'])
    qqHSTXSCB.SetPointEYlow(qqHParameterIndex,
                          parameters_STXS[qqHParameters[qqHParameterIndex]]['SMXS']*parameters_STXS[qqHParameters[qqHParameterIndex]]['uncert_down'])
    qqHSTXSCB.SetPointEYhigh(qqHParameterIndex,
                           parameters_STXS[qqHParameters[qqHParameterIndex]]['SMXS']*parameters_STXS[qqHParameters[qqHParameterIndex]]['uncert_up'])
    qqHSTXSCB.SetMarkerColor(parameters_STXS[qqHParameters[qqHParameterIndex]]['color'])
    qqHSTXSCB.SetLineColor(parameters_STXS[qqHParameters[qqHParameterIndex]]['color'])
qqHSTXSCB.SetMarkerStyle(21)
qqHSTXSCB.SetLineWidth(2)
qqHSTXSCB.SetMarkerSize(1.5)

qqHSTXSML = ROOT.TGraphAsymmErrors(len(qqHParameters_ML))
for qqHParameterIndex in range(len(qqHParameters_ML)):
    qqHSTXSML.SetPoint(qqHParameterIndex,
                       (2*qqHParameterIndex+1)+10.5+len(ggHNonZeroJetParameters)+len(ggHNonZeroJetParameters_ML),
                       parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['SMXS']*parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['mu_value'])
    qqHSTXSML.SetPointEYlow(qqHParameterIndex,
                            parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['SMXS']*parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['uncert_down'])
    qqHSTXSML.SetPointEYhigh(qqHParameterIndex,
                             parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['SMXS']*parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['uncert_up'])
    qqHSTXSML.SetMarkerColor(parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['color'])
    qqHSTXSML.SetLineColor(parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['color'])
qqHSTXSML.SetMarkerStyle(22)
qqHSTXSML.SetLineWidth(2)
qqHSTXSML.SetMarkerSize(1.5)

VHSTXSCB = ROOT.TGraphAsymmErrors(len(VHParameters))
for VHParameterIndex in range(len(VHParameters)):
    VHSTXSCB.SetPoint(VHParameterIndex,
                      2*VHParameterIndex+10.5+len(ggHNonZeroJetParameters)+len(ggHNonZeroJetParameters_ML)+len(qqHParameters)+len(qqHParameters_ML),
                    parameters_STXS[VHParameters[VHParameterIndex]]['SMXS']*parameters_STXS[VHParameters[VHParameterIndex]]['mu_value'])
    VHSTXSCB.SetPointEYlow(VHParameterIndex,
                         parameters_STXS[VHParameters[VHParameterIndex]]['SMXS']*parameters_STXS[VHParameters[VHParameterIndex]]['uncert_down'])
    VHSTXSCB.SetPointEYhigh(VHParameterIndex,
                          parameters_STXS[VHParameters[VHParameterIndex]]['SMXS']*parameters_STXS[VHParameters[VHParameterIndex]]['uncert_up'])
    VHSTXSCB.SetMarkerColor(parameters_STXS[VHParameters[VHParameterIndex]]['color'])
    VHSTXSCB.SetLineColor(parameters_STXS[VHParameters[VHParameterIndex]]['color'])
VHSTXSCB.SetMarkerStyle(21)
VHSTXSCB.SetLineWidth(2)
VHSTXSCB.SetMarkerSize(1.5)

VHSTXSML = ROOT.TGraphAsymmErrors(len(VHParameters_ML))
for VHParameterIndex in range(len(VHParameters_ML)):
    VHSTXSML.SetPoint(VHParameterIndex,
                      (2*VHParameterIndex+1)+10.5+len(ggHNonZeroJetParameters)+len(ggHNonZeroJetParameters_ML)+len(qqHParameters)+len(qqHParameters_ML),
                    parameters_STXS[VHParameters_ML[VHParameterIndex]]['SMXS']*parameters_STXS[VHParameters_ML[VHParameterIndex]]['mu_value'])
    VHSTXSML.SetPointEYlow(VHParameterIndex,
                         parameters_STXS[VHParameters_ML[VHParameterIndex]]['SMXS']*parameters_STXS[VHParameters_ML[VHParameterIndex]]['uncert_down'])
    VHSTXSML.SetPointEYhigh(VHParameterIndex,
                          parameters_STXS[VHParameters_ML[VHParameterIndex]]['SMXS']*parameters_STXS[VHParameters_ML[VHParameterIndex]]['uncert_up'])
    VHSTXSML.SetMarkerColor(parameters_STXS[VHParameters_ML[VHParameterIndex]]['color'])
    VHSTXSML.SetLineColor(parameters_STXS[VHParameters_ML[VHParameterIndex]]['color'])
VHSTXSML.SetMarkerStyle(22)
VHSTXSML.SetLineWidth(2)
VHSTXSML.SetMarkerSize(1.5)

overallXSGraph = ROOT.TMultiGraph()
overallXSGraph.Add(inclusiveGraph)
overallXSGraph.Add(inclusiveGraph_ML)
overallXSGraph.Add(ggHGraph)
overallXSGraph.Add(ggHGraph_ML)
overallXSGraph.Add(qqHGraph)
overallXSGraph.Add(qqHGraph_ML)
overallXSGraph.Add(VHGraph)
overallXSGraph.Add(VHGraph_ML)
overallXSGraph.Add(ggHZeroJetGraphCB)
overallXSGraph.Add(ggHZeroJetGraphML)
overallXSGraph.Add(ggHSTXSCB)
overallXSGraph.Add(ggHSTXSML)
overallXSGraph.Add(qqHSTXSCB)
overallXSGraph.Add(qqHSTXSML)
overallXSGraph.Add(VHSTXSCB)
overallXSGraph.Add(VHSTXSML)

SMXSErrorHisto = ROOT.TGraphAsymmErrors(len(parameterOrder))
for parameterIndex in range(len(parameters_STXS)):
    if parameterIndex < 9:
        SMXSErrorHisto.SetPoint(parameterIndex,parameterIndex+0.5,parameters_STXS[parameterOrder[parameterIndex]]['SMXS'])
    elif parameterIndex == 9: 
        SMXSErrorHisto.SetPoint(parameterIndex,9.25,parameters_STXS[parameterOrder[parameterIndex]]['SMXS'])
    elif parameterIndex == 10: #ggH_0J_ML stuff
        SMXSErrorHisto.SetPoint(parameterIndex,9.75,parameters_STXS[parameterOrder[parameterIndex]]['SMXS'])
    else:
        SMXSErrorHisto.SetPoint(parameterIndex,parameterIndex-0.5,parameters_STXS[parameterOrder[parameterIndex]]['SMXS'])
    SMXSErrorHisto.SetPointEYlow(parameterIndex,parameters_STXS[parameterOrder[parameterIndex]]['SMXS_mu_down']*parameters_STXS[parameterOrder[parameterIndex]]['SMXS'])
    SMXSErrorHisto.SetPointEYhigh(parameterIndex,parameters_STXS[parameterOrder[parameterIndex]]['SMXS_mu_up']*parameters_STXS[parameterOrder[parameterIndex]]['SMXS'])
    SMXSErrorHisto.SetPointEXlow(parameterIndex,0.25)
    SMXSErrorHisto.SetPointEXhigh(parameterIndex,0.25)
SMXSErrorHisto.SetFillStyle(3001)
SMXSErrorHisto.SetFillColor(15)

#let's also create the ratio plot
inclusiveRatioGraph = ROOT.TGraphAsymmErrors(1)
inclusiveRatioGraph.SetPoint(0,0.5,parameters_STXS['r']['mu_value'])
inclusiveRatioGraph.SetPointEYlow(0,parameters_STXS['r']['uncert_down'])
inclusiveRatioGraph.SetPointEYhigh(0,parameters_STXS['r']['uncert_up'])
inclusiveRatioGraph.SetMarkerColor(parameters_STXS['r']['color'])
inclusiveRatioGraph.SetLineColor(parameters_STXS['r']['color'])
inclusiveRatioGraph.SetMarkerStyle(21)
inclusiveRatioGraph.SetLineWidth(2)
inclusiveRatioGraph.SetMarkerSize(1.5)

inclusiveRatioGraph_ML = ROOT.TGraphAsymmErrors(1)
inclusiveRatioGraph_ML.SetPoint(0,1.5,parameters_STXS['r_ML']['mu_value'])
inclusiveRatioGraph_ML.SetPointEYlow(0,parameters_STXS['r_ML']['uncert_down'])
inclusiveRatioGraph_ML.SetPointEYhigh(0,parameters_STXS['r_ML']['uncert_up'])
inclusiveRatioGraph_ML.SetMarkerColor(parameters_STXS['r_ML']['color'])
inclusiveRatioGraph_ML.SetLineColor(parameters_STXS['r_ML']['color'])
inclusiveRatioGraph_ML.SetMarkerStyle(22)
inclusiveRatioGraph_ML.SetLineWidth(2)
inclusiveRatioGraph_ML.SetMarkerSize(1.5)

ggHRatioGraph = ROOT.TGraphAsymmErrors(1)
ggHRatioGraph.SetPoint(0,2.5,parameters_STXS['r_ggH']['mu_value'])
ggHRatioGraph.SetPointEYlow(0,parameters_STXS['r_ggH']['uncert_down'])
ggHRatioGraph.SetPointEYhigh(0,parameters_STXS['r_ggH']['uncert_up'])
ggHRatioGraph.SetMarkerColor(parameters_STXS['r_ggH']['color'])
ggHRatioGraph.SetLineColor(parameters_STXS['r_ggH']['color'])
ggHRatioGraph.SetMarkerStyle(21)
ggHRatioGraph.SetLineWidth(2)
ggHRatioGraph.SetMarkerSize(1.5)

ggHRatioGraph_ML = ROOT.TGraphAsymmErrors(1)
ggHRatioGraph_ML.SetPoint(0,3.5,parameters_STXS['r_ggH_ML']['mu_value'])
ggHRatioGraph_ML.SetPointEYlow(0,parameters_STXS['r_ggH_ML']['uncert_down'])
ggHRatioGraph_ML.SetPointEYhigh(0,parameters_STXS['r_ggH_ML']['uncert_up'])
ggHRatioGraph_ML.SetMarkerColor(parameters_STXS['r_ggH_ML']['color'])
ggHRatioGraph_ML.SetLineColor(parameters_STXS['r_ggH_ML']['color'])
ggHRatioGraph_ML.SetMarkerStyle(22)
ggHRatioGraph_ML.SetLineWidth(2)
ggHRatioGraph_ML.SetMarkerSize(1.5)

qqHRatioGraph = ROOT.TGraphAsymmErrors(1)
qqHRatioGraph.SetPoint(0,4.5,parameters_STXS['r_qqH']['mu_value'])
qqHRatioGraph.SetPointEYlow(0,parameters_STXS['r_qqH']['uncert_down'])
qqHRatioGraph.SetPointEYhigh(0,parameters_STXS['r_qqH']['uncert_up'])
qqHRatioGraph.SetMarkerColor(parameters_STXS['r_qqH']['color'])
qqHRatioGraph.SetLineColor(parameters_STXS['r_qqH']['color'])
qqHRatioGraph.SetMarkerStyle(21)
qqHRatioGraph.SetLineWidth(2)
qqHRatioGraph.SetMarkerSize(1.5)

qqHRatioGraph_ML = ROOT.TGraphAsymmErrors(1)
qqHRatioGraph_ML.SetPoint(0,5.5,parameters_STXS['r_qqH_ML']['mu_value'])
qqHRatioGraph_ML.SetPointEYlow(0,parameters_STXS['r_qqH_ML']['uncert_down'])
qqHRatioGraph_ML.SetPointEYhigh(0,parameters_STXS['r_qqH_ML']['uncert_up'])
qqHRatioGraph_ML.SetMarkerColor(parameters_STXS['r_qqH_ML']['color'])
qqHRatioGraph_ML.SetLineColor(parameters_STXS['r_qqH_ML']['color'])
qqHRatioGraph_ML.SetMarkerStyle(22)
qqHRatioGraph_ML.SetLineWidth(2)
qqHRatioGraph_ML.SetMarkerSize(1.5)

VHRatioGraph = ROOT.TGraphAsymmErrors(1)
VHRatioGraph.SetPoint(0,6.5,parameters_STXS['r_VH']['mu_value'])
VHRatioGraph.SetPointEYlow(0,parameters_STXS['r_VH']['uncert_down'])
VHRatioGraph.SetPointEYhigh(0,parameters_STXS['r_VH']['uncert_up'])
VHRatioGraph.SetMarkerColor(parameters_STXS['r_VH']['color'])
VHRatioGraph.SetLineColor(parameters_STXS['r_VH']['color'])
VHRatioGraph.SetMarkerStyle(21)
VHRatioGraph.SetLineWidth(2)
VHRatioGraph.SetMarkerSize(1.5)

VHRatioGraph_ML = ROOT.TGraphAsymmErrors(1)
VHRatioGraph_ML.SetPoint(0,7.5,parameters_STXS['r_VH_ML']['mu_value'])
VHRatioGraph_ML.SetPointEYlow(0,parameters_STXS['r_VH_ML']['uncert_down'])
VHRatioGraph_ML.SetPointEYhigh(0,parameters_STXS['r_VH_ML']['uncert_up'])
VHRatioGraph_ML.SetMarkerColor(parameters_STXS['r_VH_ML']['color'])
VHRatioGraph_ML.SetLineColor(parameters_STXS['r_VH_ML']['color'])
VHRatioGraph_ML.SetMarkerStyle(22)
VHRatioGraph_ML.SetLineWidth(2)
VHRatioGraph_ML.SetMarkerSize(1.5)

ggHZeroJetRatioGraphCB = ROOT.TGraphAsymmErrors(1)
ggHZeroJetRatioGraphCB.SetPoint(0,8.5,parameters_STXS['r_ggH_0J']['mu_value'])
ggHZeroJetRatioGraphCB.SetPointEYlow(0,parameters_STXS['r_ggH_0J']['uncert_down'])
ggHZeroJetRatioGraphCB.SetPointEYhigh(0,parameters_STXS['r_ggH_0J']['uncert_up'])
ggHZeroJetRatioGraphCB.SetMarkerColor(parameters_STXS['r_ggH_0J']['color'])
ggHZeroJetRatioGraphCB.SetLineColor(parameters_STXS['r_ggH_0J']['color'])
ggHZeroJetRatioGraphCB.SetMarkerStyle(21)
ggHZeroJetRatioGraphCB.SetLineWidth(2)
ggHZeroJetRatioGraphCB.SetMarkerSize(1.5)

ggHZeroJetRatioGraphML = ROOT.TGraphAsymmErrors(2)

ggHZeroJetRatioGraphML.SetPoint(0,9.25,parameters_STXS['r_ggH_0J_PTH_0_10_ML']['mu_value'])
ggHZeroJetRatioGraphML.SetPointEYlow(0,parameters_STXS['r_ggH_0J_PTH_0_10_ML']['uncert_down'])
ggHZeroJetRatioGraphML.SetPointEYhigh(0,parameters_STXS['r_ggH_0J_PTH_0_10_ML']['uncert_up'])

ggHZeroJetRatioGraphML.SetPoint(1,9.75,parameters_STXS['r_ggH_0J_PTH_10_200_ML']['mu_value'])
ggHZeroJetRatioGraphML.SetPointEYlow(0,parameters_STXS['r_ggH_0J_PTH_10_200_ML']['uncert_down'])
ggHZeroJetRatioGraphML.SetPointEYhigh(0,parameters_STXS['r_ggH_0J_PTH_10_200_ML']['uncert_up'])

ggHZeroJetRatioGraphML.SetMarkerColor(parameters_STXS['r_ggH_0J']['color'])
ggHZeroJetRatioGraphML.SetLineColor(parameters_STXS['r_ggH_0J']['color'])
ggHZeroJetRatioGraphML.SetMarkerStyle(22)
ggHZeroJetRatioGraphML.SetLineWidth(2)
ggHZeroJetRatioGraphML.SetMarkerSize(1.5)


ggHRatioSTXSCB = ROOT.TGraphAsymmErrors(len(ggHNonZeroJetParameters))
for ggHParameterIndex in range(len(ggHNonZeroJetParameters)):
    ggHRatioSTXSCB.SetPoint(ggHParameterIndex,
                          (2*ggHParameterIndex)+10.5,
                          parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['mu_value'])
    ggHRatioSTXSCB.SetPointEYlow(ggHParameterIndex,
                               parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['uncert_down'])
    ggHRatioSTXSCB.SetPointEYhigh(ggHParameterIndex,
                                parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['uncert_up'])
    ggHRatioSTXSCB.SetMarkerColor(parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['color'])
    ggHRatioSTXSCB.SetLineColor(parameters_STXS[ggHNonZeroJetParameters[ggHParameterIndex]]['color'])
ggHRatioSTXSCB.SetMarkerStyle(21)
ggHRatioSTXSCB.SetLineWidth(2)
ggHRatioSTXSCB.SetMarkerSize(1.5)

ggHRatioSTXSML = ROOT.TGraphAsymmErrors(len(ggHNonZeroJetParameters_ML))
for ggHParameterIndex in range(len(ggHNonZeroJetParameters_ML)):
    ggHRatioSTXSML.SetPoint(ggHParameterIndex,
                            (2*ggHParameterIndex+1)+10.5,
                          parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['mu_value'])
    ggHRatioSTXSML.SetPointEYlow(ggHParameterIndex,
                               parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['uncert_down'])
    ggHRatioSTXSML.SetPointEYhigh(ggHParameterIndex,
                                parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['uncert_up'])
    ggHRatioSTXSML.SetMarkerColor(parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['color'])
    ggHRatioSTXSML.SetLineColor(parameters_STXS[ggHNonZeroJetParameters_ML[ggHParameterIndex]]['color'])
ggHRatioSTXSML.SetMarkerStyle(22)
ggHRatioSTXSML.SetLineWidth(2)
ggHRatioSTXSML.SetMarkerSize(1.5)

qqHRatioSTXSCB = ROOT.TGraphAsymmErrors(len(qqHParameters))
for qqHParameterIndex in range(len(qqHParameters)):
    qqHRatioSTXSCB.SetPoint(qqHParameterIndex,
                            (2*qqHParameterIndex)+10.5+len(ggHNonZeroJetParameters)+len(ggHNonZeroJetParameters_ML),
                          parameters_STXS[qqHParameters[qqHParameterIndex]]['mu_value'])
    qqHRatioSTXSCB.SetPointEYlow(qqHParameterIndex,
                               parameters_STXS[qqHParameters[qqHParameterIndex]]['uncert_down'])
    qqHRatioSTXSCB.SetPointEYhigh(qqHParameterIndex,
                                parameters_STXS[qqHParameters[qqHParameterIndex]]['uncert_up'])
    qqHRatioSTXSCB.SetMarkerColor(parameters_STXS[qqHParameters[qqHParameterIndex]]['color'])
    qqHRatioSTXSCB.SetLineColor(parameters_STXS[qqHParameters[qqHParameterIndex]]['color'])
qqHRatioSTXSCB.SetMarkerStyle(21)
qqHRatioSTXSCB.SetLineWidth(2)
qqHRatioSTXSCB.SetMarkerSize(1.5)

qqHRatioSTXSML = ROOT.TGraphAsymmErrors(len(qqHParameters_ML))
for qqHParameterIndex in range(len(qqHParameters_ML)):
    qqHRatioSTXSML.SetPoint(qqHParameterIndex,
                            (2*qqHParameterIndex+1)+10.5+len(ggHNonZeroJetParameters)+len(ggHNonZeroJetParameters_ML),
                          parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['mu_value'])
    qqHRatioSTXSML.SetPointEYlow(qqHParameterIndex,
                               parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['uncert_down'])
    qqHRatioSTXSML.SetPointEYhigh(qqHParameterIndex,
                                parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['uncert_up'])
    qqHRatioSTXSML.SetMarkerColor(parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['color'])
    qqHRatioSTXSML.SetLineColor(parameters_STXS[qqHParameters_ML[qqHParameterIndex]]['color'])
qqHRatioSTXSML.SetMarkerStyle(22)
qqHRatioSTXSML.SetLineWidth(2)
qqHRatioSTXSML.SetMarkerSize(1.5)

VHRatioSTXSCB = ROOT.TGraphAsymmErrors(len(VHParameters))
for VHParameterIndex in range(len(VHParameters)):
    VHRatioSTXSCB.SetPoint(VHParameterIndex,
                         (2*VHParameterIndex)+10.5+len(ggHNonZeroJetParameters)+len(ggHNonZeroJetParameters_ML)+len(qqHParameters)+len(qqHParameters_ML),
                         parameters_STXS[VHParameters[VHParameterIndex]]['mu_value'])
    VHRatioSTXSCB.SetPointEYlow(VHParameterIndex,
                              parameters_STXS[VHParameters[VHParameterIndex]]['uncert_down'])
    VHRatioSTXSCB.SetPointEYhigh(VHParameterIndex,
                               parameters_STXS[VHParameters[VHParameterIndex]]['uncert_up'])
    VHRatioSTXSCB.SetMarkerColor(parameters_STXS[VHParameters[VHParameterIndex]]['color'])
    VHRatioSTXSCB.SetLineColor(parameters_STXS[VHParameters[VHParameterIndex]]['color'])
VHRatioSTXSCB.SetMarkerStyle(21)
VHRatioSTXSCB.SetLineWidth(2)
VHRatioSTXSCB.SetMarkerSize(1.5)

VHRatioSTXSML = ROOT.TGraphAsymmErrors(len(VHParameters_ML))
for VHParameterIndex in range(len(VHParameters_ML)):
    VHRatioSTXSML.SetPoint(VHParameterIndex,
                           (2*VHParameterIndex+1)+10.5+len(ggHNonZeroJetParameters)+len(ggHNonZeroJetParameters_ML)+len(qqHParameters)+len(qqHParameters_ML),
                         parameters_STXS[VHParameters_ML[VHParameterIndex]]['mu_value'])
    VHRatioSTXSML.SetPointEYlow(VHParameterIndex,
                              parameters_STXS[VHParameters_ML[VHParameterIndex]]['uncert_down'])
    VHRatioSTXSML.SetPointEYhigh(VHParameterIndex,
                               parameters_STXS[VHParameters_ML[VHParameterIndex]]['uncert_up'])
    VHRatioSTXSML.SetMarkerColor(parameters_STXS[VHParameters_ML[VHParameterIndex]]['color'])
    VHRatioSTXSML.SetLineColor(parameters_STXS[VHParameters_ML[VHParameterIndex]]['color'])
VHRatioSTXSML.SetMarkerStyle(22)
VHRatioSTXSML.SetLineWidth(2)
VHRatioSTXSML.SetMarkerSize(1.5)

ratioGraph = ROOT.TMultiGraph()
ratioGraph.Add(inclusiveRatioGraph)
ratioGraph.Add(inclusiveRatioGraph_ML)
ratioGraph.Add(ggHRatioGraph)
ratioGraph.Add(ggHRatioGraph_ML)
ratioGraph.Add(qqHRatioGraph)
ratioGraph.Add(qqHRatioGraph_ML)
ratioGraph.Add(VHRatioGraph)
ratioGraph.Add(VHRatioGraph_ML)
ratioGraph.Add(ggHZeroJetRatioGraphCB)
ratioGraph.Add(ggHZeroJetRatioGraphML)
ratioGraph.Add(ggHRatioSTXSCB)
ratioGraph.Add(ggHRatioSTXSML)
ratioGraph.Add(qqHRatioSTXSCB)
ratioGraph.Add(qqHRatioSTXSML)
ratioGraph.Add(VHRatioSTXSCB)
ratioGraph.Add(VHRatioSTXSML)

SMXSRatioErrorHisto = ROOT.TGraphAsymmErrors(len(parameterOrder))
for parameterIndex in range(len(parameters_STXS)):
    if parameterIndex < 9: #ggH_0J_ML
        SMXSRatioErrorHisto.SetPoint(parameterIndex,parameterIndex+0.5,1)
    elif parameterIndex == 9:
        SMXSRatioErrorHisto.SetPoint(parameterIndex,9.25,1)
    elif parameterIndex == 10:
        SMXSRatioErrorHisto.SetPoint(parameterIndex,9.75,1)
    else:
        SMXSRatioErrorHisto.SetPoint(parameterIndex,parameterIndex-0.5,1)
    SMXSRatioErrorHisto.SetPointEYlow(parameterIndex,parameters_STXS[parameterOrder[parameterIndex]]['SMXS_mu_down'])
    SMXSRatioErrorHisto.SetPointEYhigh(parameterIndex,parameters_STXS[parameterOrder[parameterIndex]]['SMXS_mu_up'])
    SMXSRatioErrorHisto.SetPointEXlow(parameterIndex,0.25)
    SMXSRatioErrorHisto.SetPointEXhigh(parameterIndex,0.25)
SMXSRatioErrorHisto.SetFillStyle(3001)
SMXSRatioErrorHisto.SetFillColor(15)

#okay, we need to set up our special axis labels here and now
axisLabelHisto.GetXaxis().SetBinLabel(1,'H#rightarrow#tau#tau')
axisLabelHisto.GetXaxis().SetBinLabel(2,'ggH#rightarrow#tau#tau')
axisLabelHisto.GetXaxis().SetBinLabel(3,'qqH#rightarrow#tau#tau')
axisLabelHisto.GetXaxis().SetBinLabel(4,'VH#rightarrow#tau#tau')
axisLabelHisto.GetXaxis().SetBinLabel(5,'ggH: 0 J')
axisLabelHisto.GetXaxis().SetBinLabel(6,'ggH: 0 J P_{T}^{H}[0,10]')
axisLabelHisto.GetXaxis().SetBinLabel(7,'ggH: 0 J P_{T}^{H}[10,200]')
axisLabelHisto.GetXaxis().SetBinLabel(8,'ggH: 1 J, p_{T}^{H}[0,60]')
axisLabelHisto.GetXaxis().SetBinLabel(9,'ggH: 1 J, p_{T}^{H}[60,120]')
axisLabelHisto.GetXaxis().SetBinLabel(10,'ggH: 1 J, p_{T}^{H}[120,200]')
axisLabelHisto.GetXaxis().SetBinLabel(11,'ggH: #geq 2 J')
axisLabelHisto.GetXaxis().SetBinLabel(12,'ggH: p_{T}^{H}[200,300]')
axisLabelHisto.GetXaxis().SetBinLabel(13,'ggH: p_{T}^{H} > 300')
axisLabelHisto.GetXaxis().SetBinLabel(14,'qqH: Non-VBF Topology')
axisLabelHisto.GetXaxis().SetBinLabel(15,'qqH: #geq  2 J, m_{jj}[350,700]')
axisLabelHisto.GetXaxis().SetBinLabel(16,'qqH: #geq 2 J, m_{jj} > 700')
axisLabelHisto.GetXaxis().SetBinLabel(17,'qqH: p_{T}^{H} > 200')
axisLabelHisto.GetXaxis().SetBinLabel(18,'WH: p_{T}^{V} < 150')
axisLabelHisto.GetXaxis().SetBinLabel(19,'WH: p_{T}^{V} > 150')
axisLabelHisto.GetXaxis().SetBinLabel(20,'ZH: p_{T}^{V} < 150')
axisLabelHisto.GetXaxis().SetBinLabel(21,'ZH: p_{T}^{V} > 150')
#for parameterIndex in range(len(parameterOrder)):
#    ratioGridHisto.GetXaxis().SetBinLabel(parameterIndex+1,parameters_STXS[parameterOrder[parameterIndex]]['axis'])

#

#draw the overall plot elements
plotPad.cd()
plotGridHisto.Draw()
plotGridHisto.SetMaximum(200000)
plotGridHisto.SetMinimum(0.5)
plotGridHisto.GetYaxis().SetTitle("#sigmaB (fb)")
plotGridHisto.GetYaxis().SetTitleSize(0.125)
plotGridHisto.GetYaxis().SetTitleOffset(0.35*(0.095/0.125))
plotGridHisto.GetYaxis().SetTickLength(0.01)
plotGridHisto.GetXaxis().SetLabelSize(0)
SMXSErrorHisto.Draw("2")
overallXSGraph.Draw("0PZ")

#let's draw a legend.
theLegend = ROOT.TLegend(0.35,0.8,0.98,0.87)
theLegend.SetNColumns(4)
theLegend.AddEntry(inclusiveGraph,"Observed: CB analysis","P")
theLegend.AddEntry(inclusiveGraph_ML,"Observed: ML analysis","P")
theLegend.AddEntry(inclusiveGraph,"#pm1#sigma","L")
theLegend.AddEntry(SMXSErrorHisto,"Uncertainty on SM prediction","F")
theLegend.SetBorderSize(0)
#theLegend.SetFillStyle(0)
theLegend.Draw()
    

#okay, let's draw the latex
latex = ROOT.TLatex()
latex.SetTextSize(0.050)
latex.SetTextAlign(23)
latex.SetTextFont(42)
latex.SetTextAngle(90)
for parameterIndex in range(len(parameterOrder)):
    try:
        quotedNominal = roundToSigDigits(parameters_STXS[parameterOrder[parameterIndex]]['mu_value']*parameters_STXS[parameterOrder[parameterIndex]]['SMXS'],3)
        if math.floor(math.log10(abs(quotedNominal))) >= 2 and quotedNominal%1 == 0:
            quotedNominal = int(quotedNominal)
    except ValueError:
        quotedNominal = 0
    try:
        quotedUp = roundToSigDigits(parameters_STXS[parameterOrder[parameterIndex]]['uncert_up']*parameters_STXS[parameterOrder[parameterIndex]]['SMXS'],3)
        if math.floor(math.log10(abs(quotedUp))) >= 2 and quotedUp%1 == 0:
            quotedUp = int(quotedUp)
    except:
        quotedUp = 0
    try:
        quotedDown = roundToSigDigits(parameters_STXS[parameterOrder[parameterIndex]]['uncert_down']*parameters_STXS[parameterOrder[parameterIndex]]['SMXS'],3)
        if math.floor(math.log10(abs(quotedDown))) >= 2 and quotedDown%1 == 0:
            quotedDown = int(quotedDown)
    except ValueError:
        quotedDown = 0        
    if parameterIndex < 9: #ggH_0J_ML
        latex.DrawLatex(parameterIndex+0.3,latexAlignments[parameterIndex],str(quotedNominal)+'^{+'+str(quotedUp)+'}_{-'+str(quotedDown)+'}')
    elif parameterIndex == 9:
        latex.DrawLatex(9.0,latexAlignments[parameterIndex],str(quotedNominal)+'^{+'+str(quotedUp)+'}_{-'+str(quotedDown)+'}')
    elif parameterIndex == 10:
        latex.DrawLatex(9.5,latexAlignments[parameterIndex],str(quotedNominal)+'^{+'+str(quotedUp)+'}_{-'+str(quotedDown)+'}')
    else:
        latex.DrawLatex(parameterIndex-0.7,latexAlignments[parameterIndex],str(quotedNominal)+'^{+'+str(quotedUp)+'}_{-'+str(quotedDown)+'}')
    
#let's draw the other text pieces.
cmsLatex = ROOT.TLatex()
cmsLatex.SetTextSize(0.09)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.DrawLatex(0.1,0.92,"CMS")
#cmsLatex.SetTextFont(52)
#cmsLatex.DrawLatex(0.1+0.09,0.92,"Preliminary")

cmsLatex.SetTextAlign(31)
cmsLatex.SetTextFont(42)
cmsLatex.DrawLatex(0.98,0.92,"137 fb^{-1} (13 TeV)")

#draw the ratio plot elements
ratioPad.cd()
ratioPad.SetTopMargin(0.025)
ratioPad.SetBottomMargin(0.55)

axisLabelHisto.Draw()
axisLabelHisto.GetYaxis().SetTitle("Ratio to SM")
axisLabelHisto.GetYaxis().CenterTitle()
axisLabelHisto.GetYaxis().SetTitleOffset(0.35)
axisLabelHisto.GetYaxis().SetTitleSize(0.095)
axisLabelHisto.GetYaxis().SetNdivisions(7,0,0)
axisLabelHisto.GetXaxis().LabelsOption("v")
axisLabelHisto.GetXaxis().SetLabelSize(0.078)
axisLabelHisto.SetMaximum(4)
axisLabelHisto.SetMinimum(-3)
ratioGridHisto.Draw("SAME")

#let's make a strike out plot?
strikeOutPlot = ROOT.TH1F("StikeOut","StirkeOut",len(parameters_STXS),0.0,float(len(parameters_STXS)))
for i in range(1,len(parameters_STXS)+1):
    strikeOutPlot.SetBinContent(i,-10)
strikeOutPlot.SetFillColor(ROOT.kBlack)
strikeOutPlot.SetFillStyle(3354)

SMXSRatioErrorHisto.Draw('2')
strikeOutPlot.Draw("SAME")
ratioGraph.Draw("P0Z")

theCanvas.SaveAs("finalCrossSectionTable.png")
theCanvas.SaveAs("finalCrossSectionTable.pdf")
raw_input("Press Enter To Continue...")
