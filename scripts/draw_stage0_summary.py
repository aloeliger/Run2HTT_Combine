import ROOT
import argparse

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptStat(0)

def add_lumi():
    lowX=0.60
    lowY=0.9
    lumi  = ROOT.TPaveText(lowX, lowY+0.0, lowX+0.30, lowY+0.1, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.06)
    lumi.SetTextFont (   42 )
    lumi.AddText("137 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.10
    lowY=0.9
    lumi  = ROOT.TPaveText(lowX, lowY+0.0, lowX+0.15, lowY+0.1, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi

def add_Preliminary():
    lowX=0.23
    lowY=0.895
    lumi  = ROOT.TPaveText(lowX, lowY+0.0, lowX+0.15, lowY+0.1, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Preliminary")
    return lumi

def make_legend():
        output = ROOT.TLegend(0.10, 0.75, 0.88, 0.85, "", "brNDC")
        output.SetNColumns(3)
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        output.SetFillStyle(0)
        output.SetBorderSize(0)
        output.SetTextFont(62)
        return output


# Canvas and pads
canv = ROOT.TCanvas("canv","canv",800,600)
canv.cd()
canv.SetRightMargin(0.05)

nlines=3+1

axis = ROOT.TH2F('axis', '', 1, 0.4, 5.0, nlines, 0.01, nlines)
axis.GetXaxis().SetTitle("Parameter value")
axis.GetYaxis().SetTitleSize(0.08)
axis.GetXaxis().SetTitleSize(0.06)
axis.GetYaxis().SetLabelSize(0)
axis.GetXaxis().SetTitleOffset(0.7)
axis.GetYaxis().SetTickLength(0.)
axis.Draw()

y_pos = float(nlines)-0.5
x_text = 1.85

gr = ROOT.TGraphAsymmErrors(nlines-1)
gr.SetMarkerStyle(20)
gr.GetXaxis().SetTitleSize(0.08)

combineMu=0
lowBnad=0
highBand=0
i=0
ii=0

myresult=["#mu","#mu_{ggH}","#mu_{qqH}","#mu_{VH}"]
mycat=["#mu","#mu_{ggH}","#mu_{qqH}","#mu_{VH}"]
mean=[round(0.941, 2),
      round(1.015, 2),
      round(0.638, 2),
      round(1.790,2)]
up=[round(0.125, 2),
    round(0.191, 2),
    round(0.225, 2),
    round(0.452,2)]
down=[round(0.116, 2),
      round(0.173, 2),
      round(0.217, 2),
      round(0.416,2)]
th_up=[round(0.074, 2),
       round(0.128, 2),
       round(0.099, 2),
       round(0.087,2)]
th_down=[round(0.066, 2),
         round(0.104, 2),
         round(0.097, 2),
         round(0.059,2)]
syst_up=[round(0.072, 2),
         round(0.105, 2),
         round(0.091, 2),
         round(0.242,2)]
syst_down=[round(0.065, 2),
           round(0.100, 2),
           round(0.080, 2),
           round(0.208,2)]
stat_up=[round(0.061, 2),
         round(0.079, 2),
         round(0.165, 2),
         round(0.364,2)]
stat_down=[round(0.060, 2),
           round(0.079, 2),
           round(0.162, 2),
           round(0.348,2)]
bbb_up=[round(0.036, 2),
        round(0.053, 2),
        round(0.074, 2),
        round(0.077,2)]
bbb_down=[round(0.034, 2),
          round(0.054, 2),
          round(0.073, 2),
          round(0.075,2)]

categ=[]
result=[]
bbb_result=[]
syst_result=[]

stat_result=[]
th_result=[]

boxes=[]
colors=[ROOT.kGray,ROOT.kAzure+7,ROOT.kOrange-3,ROOT.kGreen+1]

for i in range(0,nlines):
   y_pos=0.75*(float(nlines)-0.5-i)
   #myresult[i]=str(mean[i])+" -"+str(down[i])+"/+"+str(up[i])
   myresult[i]="%.2f^{+%.2f}_{#minus%.2f}"%(float(mean[i]),float(up[i]),float(down[i]))
   gr.SetPoint(i+1, mean[i], y_pos)
   gr.SetPointError(i+1,down[i] ,up[i], 0, 0)

   boxes.append(ROOT.TBox(mean[i]-stat_down[i], y_pos-0.05,mean[i]+stat_up[i], y_pos+0.05))
   boxes[i].SetFillColor(colors[i])
   boxes[i].SetLineColor(colors[i])
   boxes[i].Draw("same")

   categ.append( ROOT.TPaveText(0.01, 0.70-(i+1)*(0.705-0.105)/nlines+0.5*(0.705-0.105)/nlines, 0.10, 0.70+0.01-(i+1)*(0.705-0.105)/nlines+0.5*(0.705-0.105)/nlines, "NDC"))
   categ[i].SetBorderSize(   0 )
   categ[i].SetFillStyle(    0 )
   categ[i].SetTextAlign(   32 )
   categ[i].SetTextSize ( 0.05 )
   categ[i].SetTextColor(    1 )
   categ[i].SetTextFont (   42 )
   categ[i].AddText(mycat[i])
   categ[i].Draw("same")

   result.append( ROOT.TPaveText(0.45, 0.70-(i+1)*(0.705-0.105)/nlines+0.5*(0.705-0.105)/nlines, 0.55, 0.70+0.01-(i+1)*(0.705-0.105)/nlines+0.5*(0.705-0.105)/nlines, "NDC"))
   result[i].SetBorderSize(   0 )
   result[i].SetFillStyle(    0 )
   result[i].SetTextAlign(   12 )
   result[i].SetTextSize ( 0.05 )
   result[i].SetTextColor(    1 )
   result[i].SetTextFont (   42 )
   result[i].AddText(myresult[i])
   result[i].Draw("same")

   th_result.append( ROOT.TPaveText(0.60, 0.70-(i+1)*(0.705-0.105)/nlines+0.5*(0.705-0.105)/nlines, 0.68, 0.70+0.01-(i+1)*(0.705-0.105)/nlines+0.5*(0.705-0.105)/nlines, "NDC"))
   th_result[i].SetBorderSize(   0 )
   th_result[i].SetFillStyle(    0 )
   th_result[i].SetTextAlign(   12 )
   th_result[i].SetTextSize ( 0.05 )
   th_result[i].SetTextColor(    1 )
   th_result[i].SetTextFont (   42 )
   th_result[i].AddText("{}^{+%.2f}_{#minus%.2f}"%(float(th_up[i]),float(th_down[i])))
   th_result[i].Draw("same")

   stat_result.append( ROOT.TPaveText(0.68, 0.70-(i+1)*(0.705-0.105)/nlines+0.5*(0.705-0.105)/nlines, 0.76, 0.70+0.01-(i+1)*(0.705-0.105)/nlines+0.5*(0.705-0.105)/nlines, "NDC"))
   stat_result[i].SetBorderSize(   0 )
   stat_result[i].SetFillStyle(    0 )
   stat_result[i].SetTextAlign(   12 )
   stat_result[i].SetTextSize ( 0.05 )
   stat_result[i].SetTextColor(    1 )
   stat_result[i].SetTextFont (   42 )
   stat_result[i].AddText("{}^{+%.2f}_{#minus%.2f}"%(float(stat_up[i]),float(stat_down[i])))
   stat_result[i].Draw("same")

   syst_result.append( ROOT.TPaveText(0.76, 0.70-(i+1)*(0.705-0.105)/nlines+0.5*(0.705-0.105)/nlines, 0.84, 0.70+0.01-(i+1)*(0.705-0.105)/nlines+0.5*(0.705-0.105)/nlines, "NDC"))
   syst_result[i].SetBorderSize(   0 )
   syst_result[i].SetFillStyle(    0 )
   syst_result[i].SetTextAlign(   12 )
   syst_result[i].SetTextSize ( 0.05 )
   syst_result[i].SetTextColor(    1 )
   syst_result[i].SetTextFont (   42 )
   syst_result[i].AddText("{}^{+%.2f}_{#minus%.2f}"%(float(syst_up[i]),float(syst_down[i])))
   syst_result[i].Draw("same")

   bbb_result.append( ROOT.TPaveText(0.84, 0.70-(i+1)*(0.705-0.105)/nlines+0.5*(0.705-0.105)/nlines, 0.92, 0.70+0.01-(i+1)*(0.705-0.105)/nlines+0.5*(0.705-0.105)/nlines, "NDC"))
   bbb_result[i].SetBorderSize(   0 )
   bbb_result[i].SetFillStyle(    0 )
   bbb_result[i].SetTextAlign(   12 )
   bbb_result[i].SetTextSize ( 0.05 )
   bbb_result[i].SetTextColor(    1 )
   bbb_result[i].SetTextFont (   42 )
   bbb_result[i].AddText("{}^{+%.2f}_{#minus%.2f}"%(float(bbb_up[i]),float(bbb_down[i])))
   bbb_result[i].Draw("same")

th_text= ROOT.TPaveText(0.60, 0.67, 0.68, 0.72, "NDC")
th_text.SetBorderSize(   0 )
th_text.SetFillStyle(    0 )
th_text.SetTextAlign(   12 )
th_text.SetTextSize ( 0.04 )
th_text.SetTextColor(    1 )
th_text.SetTextFont (   62 )
th_text.AddText("th.")
th_text.Draw("same")

stat_text= ROOT.TPaveText(0.68, 0.67, 0.76, 0.72, "NDC")
stat_text.SetBorderSize(   0 )
stat_text.SetFillStyle(    0 )
stat_text.SetTextAlign(   12 )
stat_text.SetTextSize ( 0.04 )
stat_text.SetTextColor(    1 )
stat_text.SetTextFont (   62 )
stat_text.AddText("stat.")
stat_text.Draw("same")


syst_text= ROOT.TPaveText(0.76, 0.666, 0.84, 0.716, "NDC")
syst_text.SetBorderSize(   0 )
syst_text.SetFillStyle(    0 )
syst_text.SetTextAlign(   12 )
syst_text.SetTextSize ( 0.04 )
syst_text.SetTextColor(    1 )
syst_text.SetTextFont (   62 )
syst_text.AddText("syst.")
syst_text.Draw("same")


bbb_text= ROOT.TPaveText(0.84, 0.67, 0.92, 0.72, "NDC")
bbb_text.SetBorderSize(   0 )
bbb_text.SetFillStyle(    0 )
bbb_text.SetTextAlign(   12 )
bbb_text.SetTextSize ( 0.04 )
bbb_text.SetTextColor(    1 )
bbb_text.SetTextFont (   62 )
bbb_text.AddText("bbb")
bbb_text.Draw("same")


gr.Draw('P0')

l1=ROOT.TLine(1.0,0,1.0,4*0.75)
l1.SetLineStyle(1)
l1.SetLineColor(ROOT.kBlack)
l1.Draw('sameL')

l2=ROOT.TLine(0.5,0,0.5,4*0.75)
l2.SetLineStyle(2)
l2.SetLineColor(ROOT.kGray)
l2.Draw('sameL')

l3=ROOT.TLine(0.75,0,0.75,4*0.75)
l3.SetLineStyle(2)
l3.SetLineColor(ROOT.kGray)
l3.Draw('sameL')

l4=ROOT.TLine(1.25,0,1.25,4*0.75)
l4.SetLineStyle(2)
l4.SetLineColor(ROOT.kGray)
l4.Draw('sameL')



gr.Draw('SAMEP')

lumi1=add_Preliminary()
lumi1.Draw("same")
lumi2=add_CMS()
lumi2.Draw("same")
lumi3=add_lumi()
lumi3.Draw("same")

legend=make_legend()
legend.AddEntry(gr,"Obs.","p")
legend.AddEntry(gr,"#pm1#sigma","l")
legend.AddEntry(boxes[0],"#pm1#sigma stat.","f")
#legend.AddEntry(gr,"#pm1#sigma (stat. #oplus syst.)","e")
legend.Draw("same")

canv.cd()
canv.RedrawAxis()

canv.Print('stage0summary.png')
canv.Print('stage0summary.pdf')

