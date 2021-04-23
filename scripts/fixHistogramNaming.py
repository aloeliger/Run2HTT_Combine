#!/usr/bin/env python
import ROOT
import argparse
import string

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update cards to fix histograms with bad naming conventions")
    parser.add_argument("--inputFile","-i",help="Input root file",required=True)
    parser.add_argument("--toReplace","-r",help="String to replace in cards",required=True)
    parser.add_argument("--replaceWith","-w",help="String to add instead in cards",required=True)

    args = parser.parse_args()

    dataCardFile = ROOT.TFile(args.inputFile,"UPDATE")
    
    for directoryKey in dataCardFile.GetListOfKeys():
        theDirectory  = dataCardFile.Get(directoryKey.GetName())
        try:
            theDirectory.cd()
        except AttributeError:
            continue #not a directory for whatever reason
        for histogramKey in theDirectory.GetListOfKeys():
            theHistogram = theDirectory.Get(histogramKey.GetName())

            if args.toReplace in theHistogram.GetName():
                theHistogram.SetNameTitle(
                    theHistogram.GetName().replace(args.toReplace,args.replaceWith),
                    theHistogram.GetTitle().replace(args.toReplace,args.replaceWith)
                )
                theHistogram.Write()
            else:
                continue
    dataCardFile.Write()
    dataCardFile.Close()
