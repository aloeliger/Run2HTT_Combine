import ROOT
import argparse

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptStat(0)

is_topology=0

def add_lumi():
    lowX=0.70
    lowY=0.9
    lumi  = ROOT.TPaveText(lowX, lowY+0.0, lowX+0.30, lowY+0.1, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.04)
    lumi.SetTextFont (   42 )
    lumi.AddText("137 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.02
    lowY=0.9
    lumi  = ROOT.TPaveText(lowX, lowY+0.0, lowX+0.15, lowY+0.1, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.04)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi

def add_Preliminary():
    lowX=0.12
    lowY=0.895
    lumi  = ROOT.TPaveText(lowX, lowY+0.0, lowX+0.15, lowY+0.1, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.04)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Preliminary")
    return lumi

def add_Scheme(scheme):
    lowX=0.36
    lowY=0.895
    lumi  = ROOT.TPaveText(lowX, lowY+0.0, lowX+0.15, lowY+0.1, "NDC")
    lumi.SetTextFont(42)
    lumi.SetTextSize(0.04)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText(scheme)
    return lumi

def make_legend():
        output = ROOT.TLegend(0.25, 0.88, 1.00, 0.92, "", "brNDC")
 	output.SetTextSize(0.05)
        output.SetNColumns(3)
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        output.SetFillStyle(0)
        output.SetBorderSize(0)
        output.SetTextFont(62)
        return output


# Canvas and pads
canv = ROOT.TCanvas("canv","canv",800,1600)
canv.cd()
canv.SetRightMargin(0.05)
canv.SetLeftMargin(0.25)
canv.SetTopMargin(0.08)

nlines=11+4

axis = ROOT.TH2F('axis', '', 1, -4.0, 28, nlines, 0.01, nlines)
axis.GetXaxis().SetTitle("Parameter value")
axis.GetXaxis().SetTitleOffset(0.7)
axis.GetXaxis().SetTitleSize(0.07)
axis.GetYaxis().SetLabelSize(0)
axis.GetYaxis().SetTickLength(0)
axis.Draw()

y_pos = float(nlines)-0.5
x_text = 1.85

gr = ROOT.TGraphAsymmErrors(nlines-1)
gr.SetMarkerStyle(20)
#gr.SetLineWidth(3)

gr_ggH = ROOT.TGraphAsymmErrors(nlines-1)
gr_ggH.SetMarkerStyle(20)
#gr_ggH.SetMarkerColor(ROOT.kAzure+7)
#gr_ggH.SetLineColor(ROOT.kAzure+7)
#gr_ggH.SetLineWidth(3)

gr_qqH = ROOT.TGraphAsymmErrors(nlines-1)
gr_qqH.SetMarkerStyle(20)
#gr_qqH.SetMarkerColor(ROOT.kOrange-3)
#gr_qqH.SetLineColor(ROOT.kOrange-3)
#gr_qqH.SetLineWidth(3)

gr_VH = ROOT.TGraphAsymmErrors(nlines-1)
gr_VH.SetMarkerStyle(20)

gr_mix = ROOT.TGraphAsymmErrors(nlines-1)
gr_mix.SetMarkerStyle(20)
#gr_mix.SetMarkerColor(ROOT.kGreen+1)
#gr_mix.SetLineColor(ROOT.kGreen+1)
#gr_mix.SetLineWidth(3)

colors=[ROOT.kOrange-3,ROOT.kOrange-3,ROOT.kOrange-3,ROOT.kOrange-3,ROOT.kAzure+7,ROOT.kAzure+7,ROOT.kAzure+7,ROOT.kAzure+7,ROOT.kAzure+7,ROOT.kAzure+7,ROOT.kAzure+7,ROOT.kGreen+1,ROOT.kGreen+1,ROOT.kGreen+1,ROOT.kGreen+1]

if is_topology:
  colors=[ROOT.kOrange-3,ROOT.kGreen+1,ROOT.kGreen+1,ROOT.kOrange-3,ROOT.kAzure+7,ROOT.kAzure+7,ROOT.kAzure+7,ROOT.kAzure+7,ROOT.kAzure+7,ROOT.kAzure+7,ROOT.kAzure+7]

combineMu=0
lowBnad=0
highBand=0
i=0
ii=0

boxes=[]
myresult=["","","","","","","","","","","","","","",""]
myresultth=["","","","","","","","","","","","","","",""]
myresultbbb=["","","","","","","","","","","","","","",""]
myresultstat=["","","","","","","","","","","","","","",""]
myresultsyst=["","","","","","","","","","","","","","",""]

### Default scheme
mycat=["#mu_{qqH non-VBF topo.}",
       "#mu_{qqH/mJJ[350-700]}",
       "#mu_{qqH/mJJ>700}",
       "#mu_{qqH-2j/pT>200}",
       "#mu_{ggH-2j/pT<200}",
       "#mu_{ggH/pT[200-300]}",
       "#mu_{ggH/pT>300}",
       "#mu_{ggH-0j/pT<200}",
       "#mu_{ggH-1j/pT[0-60]}",
       "#mu_{ggH-1j/pT[60-120]}",
       "#mu_{ggH-1j/pT[120-200]}",
       "#mu_{WH/pT<150}",
       "#mu_{WH/pT>150}",
       "#mu_{ZH/pT<150}",
       "#mu_{ZH/pT>150}",]

mean=[round(1.942, 2),
      round(-0.294, 2),
      round(0.677, 2),
      round(0.691, 2),
      round(0.047, 2),
      round(0.701, 2),
      round(1.647, 2),
      round(-0.178, 2),
      round(-0.872, 2),
      round(3.366, 2),
      round(1.944, 2),
      #VH ones here
      round(0.771,2),
      round(2.650,2),
      round(1.974,2),
      round(2.227,2),]

up=[round(4.550, 2),
    round(1.771, 2),
    round(0.392, 2),
    round(0.582, 2),
    round(0.877, 2),
    round(0.889, 2),
    round(1.279, 2),
    round(0.464, 2),
    round(1.210, 2),
    round(1.229, 2),
    round(1.212, 2),
    #VH ones here
    round(0.950,2),
    round(1.377,2),
    round(0.904,2),
    round(1.009,2),]
down=[
    round(2.928, 2),
    round(1.442, 2),
    round(0.384, 2),
    round(0.449, 2),
    round(1.530, 2),
    round(1.290, 2),
    round(1.462, 2),
    round(0.463, 2),
    round(1.206, 2),
    round(1.133, 2),
    round(1.244, 2),
    #VH ones here
    round(0.911,2),
    round(1.259,2),
    round(0.807,2),
    round(0.825,2),]

stat_up=[round(0.525, 2),
         round(0.984, 2),
         round(0.318, 2),
         round(0.318, 2),
         round(0.252, 2),
         round(0.338, 2),
         round(0.455, 2),
         round(0.163, 2),
         round(0.498, 2),
         round(0.493, 2),
         round(0.601, 2),
         #VH ones here
         round(0.768,2),
         round(1.208,2),
         round(0.799,2),
         round(0.885,2),]
stat_down=[
    round(0.522, 2),
    round(0.972, 2),
    round(0.309, 2),
    round(0.305, 2),
    round(0.251, 2),
    round(0.334, 2),
    round(0.447, 2),
    round(0.163, 2),
    round(0.498, 2),
    round(0.491, 2),
    round(0.598, 2),
    #VH ones here
    round(0.732,2),
    round(1.110,2),
    round(0.741,2),
    round(0.769,2),]

syst_up=[round(2.333, 2),
         round(0.765, 2),
         round(0.164, 2),
         round(0.281, 2),
         round(0.609, 2),
         round(0.604, 2),
         round(0.716, 2),
         round(0.386, 2),
         round(0.875, 2),
         round(0.666, 2),
         round(0.656, 2),
         #VH ones here
         round(0.514,2),
         round(0.568,2),
         round(0.342,2),
         round(0.223,2),]
syst_down=[
    round(2.146, 2),
    round(0.723, 2),
    round(0.163, 2),
    round(0.244, 2),
    round(0.660, 2),
    round(0.635, 2),
    round(0.760, 2),
    round(0.383, 2),
    round(0.886, 2),
    round(0.663, 2),
    round(0.672, 2),
    #VH ones here
    round(0.488,2),
    round(0.531,2),
    round(0.287,2),
    round(0.160,2),]

th_up=[round(3.490, 2),
       round(1.073, 2),
       round(0.062, 2),
       round(0.333, 2),
       round(0.453, 2),
       round(0.406, 2),
       round(0.838, 2),
       round(0.033, 2),
       round(0.436, 2),
       round(0.799, 2),
       round(0.688, 2),
       #VH ones here
       round(0.045,2),
       round(0.230,2),
       round(0.229,2),
       round(0.410,2),]
th_down=[
    round(1.432, 2),
    round(0.494, 2),
    round(0.059, 2),
    round(0.118, 2),
    round(1.275, 2),
    round(0.969, 2),
    round(1.024, 2),
    round(0.052, 2),
    round(0.361, 2),
    round(0.642, 2),
    round(0.696, 2),
    #VH ones here
    round(0.055,2),
    round(0.099,2),
    round(0.104,2),
    round(0.212,2),]

bbb_up=[round(1.673, 2),
        round(0.657, 2),
        round(0.146, 2),
        round(0.217, 2),
        round(0.359, 2),
        round(0.381, 2),
        round(0.462, 2),
        round(0.197, 2),
        round(0.511, 2),
        round(0.431, 2),
        round(0.453, 2),
        #VH ones here
        round(0.216,2),
        round(0.248,2),
        round(0.090,2),
        round(0.130,2),]

bbb_down=[
    round(1.283, 2),
    round(0.608, 2),
    round(0.148, 2),
    round(0.187, 2),
    round(0.464, 2),
    round(0.459, 2),
    round(0.560, 2),
    round(0.196, 2),
    round(0.538, 2),
    round(0.436, 2),
    round(0.503, 2),
    #VH ones here
    round(0.230,2),
    round(0.251,2),
    round(0.096,2),
    round(0.137,2),]


##Alternative scheme
if is_topology:
  mycat=["#mu_{qqH non-VBF topo.}",
  "#mu_{mJJ[350-700]}",
  "#mu_{mJJ>700}",
  "#mu_{qqH-2j/pT>200}",
  "#mu_{ggH-2j/mJJ<350}",
  "#mu_{ggH/pT[200-300]}",
  "#mu_{ggH/pT>300}",
  "#mu_{ggH-0j/pT<200}",
  "#mu_{ggH-1j/pT[0-60]}",
  "#mu_{ggH-1j/pT[60-120]}",
  "#mu_{ggH-1j/pT[120-200]}"]

  mean=[round(0.16, 2),
  round(-0.04, 2),
  round(0.65, 2),
  round(0.57, 2),
  round(0.64, 2),
  round(1.09, 2),
  round(1.98, 2),
  round(0.03, 2),
  round(-1.53, 2),
  round(3.86, 2),
  round(2.06, 2)]

  up=[round(3.22, 2),
  round(0.54, 2),
  round(0.49, 2),
  round(0.44, 2),
  round(1.31, 2),
  round(0.88, 2),
  round(1.34, 2),
  round(0.45, 2),
  round(1.32, 2),
  round(1.25, 2),
  round(1.61, 2)]

  down=[round(3.91, 2),
  round(0.56, 2),
  round(0.38, 2),
  round(0.42, 2),
  round(0.99, 2),
  round(0.80, 2),
  round(1.08, 2),
  round(0.50, 2),
  round(1.33, 2),
  round(1.21, 2),
  round(0.94, 2)]

  th_up=[round(1.63, 2),
  round(0.10, 2),
  round(0.15, 2),
  round(0.09, 2),
  round(1.10, 2),
  round(0.51, 2),
  round(0.36, 2),
  round(0.04, 2),
  round(0.33, 2),
  round(0.83, 2),
  round(0.94, 2)]
  th_down=[
  round(1.86, 2),
  round(0.10, 2),
  round(0.16, 2),
  round(0.09, 2),
  round(0.53, 2),
  round(0.31, 2),
  round(0.40, 2),
  round(0.04, 2),
  round(0.45, 2),
  round(0.61, 2),
  round(0.23, 2)]

  bbb_up=[round(1.74, 2),
  round(0.23, 2),
  round(0.31, 2),
  round(0.18, 2),
  round(0.33, 2),
  round(0.33, 2),
  round(1.00, 2),
  round(0.19, 2),
  round(0.61, 2),
  round(0.43, 2),
  round(0.75, 2)]
  bbb_down=[
  round(2.13, 2),
  round(0.24, 2),
  round(0.18, 2),
  round(0.18, 2),
  round(0.51, 2),
  round(0.36, 2),
  round(0.61, 2),
  round(0.29, 2),
  round(0.59, 2),
  round(0.52, 2),
  round(0.41, 2)]

  stat_up=[round(1.91, 2),
  round(0.48, 2),
  round(0.30, 2),
  round(0.38, 2),
  round(0.58, 2),
  round(0.58, 2),
  round(0.75, 2),
  round(0.17, 2),
  round(0.72, 2),
  round(0.74, 2),
  round(0.77, 2)]
  stat_down=[
  round(1.92, 2),
  round(0.48, 2),
  round(0.29, 2),
  round(0.36, 2),
  round(0.58, 2),
  round(0.58, 2),
  round(0.74, 2),
  round(0.17, 2),
  round(0.71, 2),
  round(0.74, 2),
  round(0.76, 2)]

  syst_up=[round(1.00, 2),
  round(0.14, 2),
  round(0.18, 2),
  round(0.11, 2),
  round(0.27, 2),
  round(0.25, 2),
  round(0.29, 2),
  round(0.37, 2),
  round(0.87, 2),
  round(0.38, 2),
  round(0.75, 2)]
  syst_down=[
  round(1.88, 2),
  round(0.15, 2),
  round(0.09, 2),
  round(0.08, 2),
  round(0.31, 2),
  round(0.29, 2),
  round(0.30, 2),
  round(0.37, 2),
  round(0.84, 2),
  round(0.51, 2),
  round(0.28, 2)]

  
categ=[]
result=[]
resultsyst=[]
resultstat=[]
resultth=[]
resultbbb=[]

for i in range(0,nlines):
   y_pos=float(nlines)-1.7-i*0.91
   myresult[i]="%.2f^{+%.2f}_{#minus%.2f}"%(mean[i],up[i],down[i])
   myresultth[i]="{}^{+%.2f}_{#minus%.2f}"%(th_up[i],th_down[i])
   myresultstat[i]="{}^{+%.2f}_{#minus%.2f}"%(stat_up[i],stat_down[i])
   myresultsyst[i]="{}^{+%.2f}_{#minus%.2f}"%(syst_up[i],syst_down[i])
   myresultbbb[i]="{}^{+%.2f}_{#minus%.2f}"%(bbb_up[i],bbb_down[i])
   if is_topology:
      if i==1 or i>6:
        gr_ggH.SetPoint(i+1, mean[i], y_pos)
        gr_ggH.SetPointError(i+1,down[i] ,up[i], 0, 0)
      elif i==2 or i==3 or i==6:
        gr_qqH.SetPoint(i+1, mean[i], y_pos)
        gr_qqH.SetPointError(i+1,down[i] ,up[i], 0, 0)
      elif i==4 or i==5:
        gr_mix.SetPoint(i+1, mean[i], y_pos)
        gr_mix.SetPointError(i+1,down[i] ,up[i], 0, 0)
      else:
        gr.SetPoint(i+1, mean[i], y_pos)
        gr.SetPointError(i+1,down[i] ,up[i], 0, 0)
   else: 
       if i<4:
           gr_qqH.SetPoint(i+1, mean[i], y_pos)
           gr_qqH.SetPointError(i+1,down[i] ,up[i], 0, 0)
       elif i >= 4 and i <11:
           gr_ggH.SetPoint(i+1, mean[i], y_pos)
           gr_ggH.SetPointError(i+1,down[i] ,up[i], 0, 0)
       elif i >= 11:
           gr_VH.SetPoint(i+1, mean[i], y_pos)
           gr_VH.SetPointError(i+1,down[i] ,up[i], 0, 0)
       else:
           gr.SetPoint(i+1, mean[i], y_pos)
           gr.SetPointError(i+1,down[i] ,up[i], 0, 0)
       """
      if i>3:
        gr_ggH.SetPoint(i+1, mean[i], y_pos)
        gr_ggH.SetPointError(i+1,down[i] ,up[i], 0, 0)
      elif i<4:
        gr_qqH.SetPoint(i+1, mean[i], y_pos)
        gr_qqH.SetPointError(i+1,down[i] ,up[i], 0, 0)
      else:
        gr.SetPoint(i+1, mean[i], y_pos)
        gr.SetPointError(i+1,down[i] ,up[i], 0, 0)
       """



   categ.append( ROOT.TPaveText(0.00, 0.85-(i+1)*(0.855-0.105)/nlines+0.5*(0.855-0.105)/nlines, 0.24, 0.85+0.01-(i+1)*(0.855-0.105)/nlines+0.5*(0.855-0.105)/nlines, "NDC"))
   categ[i].SetBorderSize(   0 )
   categ[i].SetFillStyle(    0 )
   categ[i].SetTextAlign(   32 )
   categ[i].SetTextSize ( 0.038 )
   categ[i].SetTextColor(    1 )
   categ[i].SetTextFont (   42 )
   categ[i].AddText(mycat[i])
   categ[i].Draw("same")

   result.append( ROOT.TPaveText(0.45, 0.85-(i+1)*(0.855-0.105)/nlines+0.5*(0.855-0.105)/nlines, 0.55, 0.85+0.01-(i+1)*(0.855-0.105)/nlines+0.5*(0.855-0.105)/nlines, "NDC"))
   result[i].SetBorderSize(   0 )
   result[i].SetFillStyle(    0 )
   result[i].SetTextAlign(   12 )
   result[i].SetTextSize ( 0.04 )
   result[i].SetTextColor(    1 )
   result[i].SetTextFont (   42 )
   result[i].AddText(myresult[i])
   result[i].Draw("same")

   resultth.append( ROOT.TPaveText(0.60, 0.85-(i+1)*(0.855-0.105)/nlines+0.5*(0.855-0.105)/nlines, 0.68, 0.85+0.01-(i+1)*(0.855-0.105)/nlines+0.5*(0.855-0.105)/nlines, "NDC"))
   resultth[i].SetBorderSize(   0 )
   resultth[i].SetFillStyle(    0 )
   resultth[i].SetTextAlign(   12 )
   resultth[i].SetTextSize ( 0.04 )
   resultth[i].SetTextColor(    1 )
   resultth[i].SetTextFont (   42 )
   resultth[i].AddText(myresultth[i])
   resultth[i].Draw("same")

   resultstat.append( ROOT.TPaveText(0.68, 0.85-(i+1)*(0.855-0.105)/nlines+0.5*(0.855-0.105)/nlines, 0.76, 0.85+0.01-(i+1)*(0.855-0.105)/nlines+0.5*(0.855-0.105)/nlines, "NDC"))
   resultstat[i].SetBorderSize(   0 )
   resultstat[i].SetFillStyle(    0 )
   resultstat[i].SetTextAlign(   12 )
   resultstat[i].SetTextSize ( 0.04 )
   resultstat[i].SetTextColor(    1 )
   resultstat[i].SetTextFont (   42 )
   resultstat[i].AddText(myresultstat[i])
   resultstat[i].Draw("same")

   resultsyst.append( ROOT.TPaveText(0.76, 0.85-(i+1)*(0.855-0.105)/nlines+0.5*(0.855-0.105)/nlines, 0.84, 0.85+0.01-(i+1)*(0.855-0.105)/nlines+0.5*(0.855-0.105)/nlines, "NDC"))
   resultsyst[i].SetBorderSize(   0 )
   resultsyst[i].SetFillStyle(    0 )
   resultsyst[i].SetTextAlign(   12 )
   resultsyst[i].SetTextSize ( 0.04 )
   resultsyst[i].SetTextColor(    1 )
   resultsyst[i].SetTextFont (   42 )
   resultsyst[i].AddText(myresultsyst[i])
   resultsyst[i].Draw("same")

   resultbbb.append( ROOT.TPaveText(0.84, 0.85-(i+1)*(0.855-0.105)/nlines+0.5*(0.855-0.105)/nlines, 0.92, 0.85+0.01-(i+1)*(0.855-0.105)/nlines+0.5*(0.855-0.105)/nlines, "NDC"))
   resultbbb[i].SetBorderSize(   0 )
   resultbbb[i].SetFillStyle(    0 )
   resultbbb[i].SetTextAlign(   12 )
   resultbbb[i].SetTextSize ( 0.04 )
   resultbbb[i].SetTextColor(    1 )
   resultbbb[i].SetTextFont (   42 )
   resultbbb[i].AddText(myresultbbb[i])
   resultbbb[i].Draw("same")

   boxes.append(ROOT.TBox(mean[i]-stat_down[i], y_pos-0.08,mean[i]+stat_up[i], y_pos+0.08))
   boxes[i].SetFillColor(colors[i])
   boxes[i].SetLineColor(colors[i])
   boxes[i].Draw("same")


th_text= ROOT.TPaveText(0.63, 0.85, 0.68, 0.87, "NDC")
th_text.SetBorderSize(   0 )
th_text.SetFillStyle(    0 )
th_text.SetTextAlign(   12 )
th_text.SetTextSize ( 0.035 )
th_text.SetTextColor(    1 )
th_text.SetTextFont (   62 )
th_text.AddText("th.")
th_text.Draw("same")

stat_text= ROOT.TPaveText(0.69, 0.85, 0.76, 0.87, "NDC")
stat_text.SetBorderSize(   0 )
stat_text.SetFillStyle(    0 )
stat_text.SetTextAlign(   12 )
stat_text.SetTextSize ( 0.035 )
stat_text.SetTextColor(    1 )
stat_text.SetTextFont (   62 )
stat_text.AddText("stat.")
stat_text.Draw("same")


syst_text= ROOT.TPaveText(0.77, 0.848, 0.84, 0.868, "NDC")
syst_text.SetBorderSize(   0 )
syst_text.SetFillStyle(    0 )
syst_text.SetTextAlign(   12 )
syst_text.SetTextSize ( 0.035 )
syst_text.SetTextColor(    1 )
syst_text.SetTextFont (   62 )
syst_text.AddText("syst.")
syst_text.Draw("same")


bbb_text= ROOT.TPaveText(0.86, 0.85, 0.92, 0.87, "NDC")
bbb_text.SetBorderSize(   0 )
bbb_text.SetFillStyle(    0 )
bbb_text.SetTextAlign(   12 )
bbb_text.SetTextSize ( 0.035 )
bbb_text.SetTextColor(    1 )
bbb_text.SetTextFont (   62 )
bbb_text.AddText("bbb")
bbb_text.Draw("same")


gr.Draw('P0')


theory_band = ROOT.TBox(mean[0]-down[0],0,mean[0]+up[0],nlines-0.1)
theory_band.SetFillColor(ROOT.kYellow)
#theory_band.Draw('same')

l3=ROOT.TLine(1.0,0,1.0,13.5)
l3.SetLineStyle(2)
l3.SetLineColor(1)
l3.Draw('sameL')

l4=ROOT.TLine(0.0,0,0.0,13.5)
l4.SetLineStyle(3)
l4.SetLineColor(ROOT.kGray)
l4.Draw('sameL')

l5=ROOT.TLine(2.0,0,2.0,13.5)
l5.SetLineStyle(3)
l5.SetLineColor(ROOT.kGray)
l5.Draw('sameL')

l6=ROOT.TLine(3.0,0,3.0,13.5)
l6.SetLineStyle(3)
l6.SetLineColor(ROOT.kGray)
l6.Draw('sameL')

l7=ROOT.TLine(-1.0,0,-1.0,13.5)
l7.SetLineStyle(3)
l7.SetLineColor(ROOT.kGray)
l7.Draw('sameL')

l8=ROOT.TLine(4.0,0,4.0,13.5)
l8.SetLineStyle(3)
l8.SetLineColor(ROOT.kGray)
l8.Draw('sameL')

l9=ROOT.TLine(-2.0,0,-2.0,13.5)
l9.SetLineStyle(3)
l9.SetLineColor(ROOT.kGray)
l9.Draw('sameL')

l10=ROOT.TLine(0.5,0,0.5,13.5)
l10.SetLineStyle(3)
l10.SetLineColor(ROOT.kGray)
#l10.Draw('sameL')

l11=ROOT.TLine(1.5,0,1.5,13.5)
l11.SetLineStyle(3)
l11.SetLineColor(ROOT.kGray)
#l11.Draw('sameL')

gr.Draw('SAMEP')
gr_ggH.Draw('SAMEP')
gr_qqH.Draw('SAMEP')
gr_VH.Draw('SAMEP')
if is_topology:
  gr_mix.Draw('SAMEP')

lumi1=add_Preliminary()
lumi1.Draw("same")
lumi2=add_CMS()
lumi2.Draw("same")
lumi3=add_lumi()
lumi3.Draw("same")
lumi4=add_Scheme("Process-based")
if is_topology:
  lumi4=add_Scheme("Topology-based")
lumi4.Draw("same")

legend=make_legend()
legend.AddEntry(gr,"Obs.","p")
legend.AddEntry(gr,"#pm1#sigma","l")
legend.AddEntry(boxes[0],"#pm1#sigma stat.","f")
legend.Draw("same")

canv.cd()
canv.RedrawAxis()

if is_topology:
  canv.Print('muvalue_alternative.png')
  canv.Print('muvalue_alternative.pdf')
else:
  canv.Print('muvalue.png')
  canv.Print('muvalue.pdf')

