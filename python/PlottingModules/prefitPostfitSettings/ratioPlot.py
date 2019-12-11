import ROOT
from .. import Utilities
from array import array

YBounds = (0.7,1.3)

ratioMarkerStyle = 20
ratioYAxisTitle = 'Obs / H#rightarrow#tau#tau + Bkg.'
ratioYAxisTitleSize = 0.1
ratioYAxisTitleOffset = 0.62
ratioYAxisLabelSize = 0.10
ratioYAxisNDivisions = (6,0,0)

errorFillStyle = 3001
errorFillColor = 15

def poisson_errors(N,coverage=0.6827):
    alpha = 1.0-coverage 
    L,U = 0,0
    if N>0:
        L = ROOT.Math.gamma_quantile(alpha/2, N, 1.)
    U = ROOT.Math.gamma_quantile_c(alpha/2,N+1,1)
    return L,U

def convert(histogram):
    output = ROOT.TGraphAsymmErrors(histogram)
    
    for i in range(0,histogram.GetSize()-2):
        yield_in_bin = output.GetY()[i]
        if yield_in_bin<0:
            yield_in_bin = 0
        N=int(yield_in_bin)

        L,U = poisson_errors(N)

        output.SetPointEYlow(i,N-L)
        output.SetPointEYhigh(i,U-N)
    return output

def setRatioErrors(ratio,theData):
    output = ROOT.TGraphAsymmErrors(ratio)
    for i in range(1,ratio.GetNbinsX()+1):
        try:
            print ''
            print("bin #"+str(i))
            print("Data: +"+str(theData.GetBinErrorUp(i))+"/-"+str(theData.GetBinErrorLow(i)))
            print("Ratio: "+str(ratio.GetBinContent(i))+" Error:"+str(theData.GetBinErrorUp(i)/theData.GetBinContent(i)*ratio.GetBinContent(i))+'/-'+str(theData.GetBinErrorLow(i)/theData.GetBinContent(i)*ratio.GetBinContent(i)))            
            output.SetPointEYlow(i-1,theData.GetBinErrorLow(i)/theData.GetBinContent(i)*ratio.GetBinContent(i))
            output.SetPointEYhigh(i-1,theData.GetBinErrorUp(i)/theData.GetBinContent(i)*ratio.GetBinContent(i))
        except ZeroDivisionError:
            output.SetPointEYlow(i,0)
            output.SetPointEYhigh(i,0)
    return output

def MakeRatioPlot(theStack,theData):    
    
    nBins,binBoundaries = Utilities.GetHistogramAxisInfo(theData)
    binBoundaryArray = array('f',binBoundaries)    

    ratioHist = ROOT.TH1F('Ratio',
                          'Ratio',
                          nBins,
                          binBoundaryArray)

    ratioHist.Sumw2()
    ratioHist.Add(theData)    
    #ratioHist = theData.Clone()
    #ratioHist.SetNameTitle('Ratio','Ratio')
    #ratioHist.SetBinErrorOption(ROOT.TH1.kPoisson)

    denominatorHistos = ROOT.TH1F('denominatorHistos',
                                  'denominatorHistos',
                                  nBins,
                                  binBoundaryArray)
    listOfStackHistograms = theStack.GetHists()
    for i in range(theStack.GetNhists()):        
        denominatorHistos.Add(theStack.GetHists().At(i))        
                    
    ratioHist.Divide(denominatorHistos)    

    """
    for i in range(1,ratioHist.GetNbinsX()+1):
        try:
            ratioHist.SetBinError(i,(theData.GetBinError(i)/theData.GetBinContent(i))*ratioHist.GetBinContent(i))
        except ZeroDivisionError:
            ratioHist.SetBinError(i,0)
    """
        
    #ratioHist = convert(ratioHist)
    
    ratioHist = setRatioErrors(ratioHist,theData)

    ratioHist.SetMarkerStyle(ratioMarkerStyle)
    #ratioHist.GetXaxis().SetRangeUser(theData.GetXaxis().GetXmin(),theData.GetXaxis().GetXmax())     

    MCErrors = ROOT.TH1F("MCErrors","MCErrors",
                         nBins,
                         binBoundaryArray)
    for i in range (1,MCErrors.GetNbinsX()+1):
        MCErrors.SetBinContent(i,1.0)
        try:
            MCErrors.SetBinError(i,denominatorHistos.GetBinError(i)/denominatorHistos.GetBinContent(i))
        except:
            MCErrors.SetBinError(i,0)
    MCErrors.SetFillStyle(errorFillStyle)
    MCErrors.SetFillColor(errorFillColor)
    MCErrors.SetMarkerStyle(1)

    MCErrors.GetYaxis().SetTitle(ratioYAxisTitle)
    MCErrors.GetYaxis().SetTitleSize(ratioYAxisTitleSize)
    MCErrors.GetYaxis().SetTitleOffset(ratioYAxisTitleOffset)
    MCErrors.GetYaxis().CenterTitle()
    MCErrors.GetYaxis().SetLabelSize(ratioYAxisLabelSize)
    MCErrors.GetYaxis().SetNdivisions(ratioYAxisNDivisions[0],
                                       ratioYAxisNDivisions[1],
                                       ratioYAxisNDivisions[2])
    MCErrors.GetYaxis().SetRangeUser(YBounds[0],YBounds[1])       

    return ratioHist,MCErrors
