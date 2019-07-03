//Andrew Loeliger
//Input options: 
// -s disables shape uncertainties
// -e disables embedded
// -b disables bin-by-bin uncertainties
// -g uses the inclusive ggH process (No STXS bins)
// -q uses the inclusive qqH process (No STXS bins)
#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/Run2HTT_Combine/interface/InputParserUtility.h"
#include "CombineHarvester/Run2HTT_Combine/interface/UtilityFunctions.h"

using namespace std;

int main(int argc, char **argv) {
  InputParserUtility Input(argc,argv);

  //! [part1]
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  cout<<"test"<<endl;
  string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/shapes/";
  
  //Dynamic Category Loading
  TFile* TheFile = new TFile((aux_shapes+"smh2018mt.root").c_str());
  std::vector<std::pair<int,std::string>> cats = {};
  for(int i = 0; i < TheFile->GetListOfKeys()->GetEntries(); ++i)
    {
      std::cout<<"Making category for: "<<i<<" "<<TheFile->GetListOfKeys()->At(i)->GetName()<<std::endl;
      cats.push_back({i+1,TheFile->GetListOfKeys()->At(i)->GetName()});
    }  

  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.  
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  vector<string> masses = {""};;
  //! [part3]
  cb.AddObservations({"*"}, {"smh2018"}, {"13TeV"}, {"mt"}, cats);

  vector<string> bkg_procs = {"ZT","VVT","TTT","jetFakes","ZL","VVL","TTL"};
  cb.AddProcesses({"*"}, {"smh2018"}, {"13TeV"}, {"mt"}, bkg_procs, cats, false);

  vector<string> ggH_STXS;
  if (Input.OptionExists("-g")) ggH_STXS = {"ggH_htt125"};
  else ggH_STXS = {"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125",
		   "ggH_PTH_0_200_1J_PTH_120_200_htt125",
		   "ggH_PTH_0_200_1J_PTH_60_120_htt125",
		   "ggH_PTH_0_200_1J_PTH_0_60_htt125",
		   "ggH_PTH_0_200_0J_PTH_10_200_htt125",
		   "ggH_PTH_0_200_0J_PTH_0_10_htt125",
		   "ggH_PTH_GE200_htt125"};
  
  vector<string> qqH_STXS; 
  if(Input.OptionExists("-q")) qqH_STXS = {"qqH_htt125"};
  else qqH_STXS = {"qqH_0J_htt125",
		   "qqH_1J_htt125",
		   "qqH_GE2J_MJJ_0_60_htt125",
		   "qqH_GE2J_MJJ_60_120_htt125",
		   "qqH_GE2J_MJJ_120_350_htt125",
		   "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125",
		   "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125",
		   "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125",
		   "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125",
		   "qqH_GE2J_MJJ_GE350_PTH_GE200_htt125"};

  vector<string> sig_procs = ch::JoinStr({ggH_STXS,qqH_STXS,{"ZH_htt125","WH_htt125"}});
  
  cb.AddProcesses(masses, {"smh2018"}, {"13TeV"}, {"mt"}, sig_procs, cats, true);    

  //! [part4]

  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;
  using ch::JoinStr;

  //start with lnN errors
  //********************************************************************************************************************************
  
  //What are these: Present in 18-032 Data cards.
  cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_PU_alphas", "lnN", SystMap<>::init(1.0062));
  cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_PU_mq", "lnN", SystMap<>::init(1.0099));
  cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_THU", "lnN", SystMap<>::init(1.017));  
  
  //Tau ID uncertainty: applied to genuine tau contributions.
  cb.cp().process(JoinStr({{"ZT","TTT","VVT"},sig_procs})).AddSyst(cb,"CMS_t_ID_eff","lnN",SystMap<>::init(1.02));

  //Muon ID efficiency: Decorollated in 18-032 datacards.  
  cb.cp().process(JoinStr({{"ZT","TTT","VVT","ZL","TTL","VVL"},sig_procs})).AddSyst(cb,"CMS_eff_m","lnN",SystMap<>::init(1.02));

  //lnN Fake Factor Uncertainties: Values from 18-032 data cards.
  // 28/5/19 Update: Decision is to pull all FF lnN uncertainties and simply proceed with un-renormalized shapes for now
  // so to avoid artificial reduction of errors.
  // Left commented out
  //cb.cp().process({"jetFakes"}).AddSyst(cb, "CMS_ff_norm_stat_mt_mt_qqh_unrolled_Run2018","lnN",SystMap<>::init(1.048));
  //Quadrature addition of CMS_ff_norm_syst_mt and CMS_ff_norm_syst_mt_Run2018
  //cb.cp().process({"jetFakes"}).AddSyst(cb, "CMS_ff_norm_syst_mt","lnN",SystMap<>::init(1.058));
  //Quadrature addition of CMS_ff_sub_syst_mt_mt_qqh_unrolled and CMS_ff_sub_syst_mt_mt_qqh_unrolled_Run2018
  //cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_sub_syst_mt_mt_qqh_unrolled", "lnN",SystMap<>::init(1.04));

  // b-tagging efficiency: Changed into lnN.
  //5% in ttbar and 0.5% otherwise.
  cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_htt_eff_b_TTL","lnN",SystMap<>::init(1.05));
  cb.cp().process(JoinStr({{"ZT","VVT","ZL","VVL"},sig_procs})).AddSyst(cb,"CMS_htt_eff_b","lnN",SystMap<>::init(1.005));

  // TTbar XSection Uncertainty
  cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_htt_tjXsec", "lnN", SystMap<>::init(1.06));

  // Diboson XSection Uncertainty
  cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_htt_vvXsec", "lnN", SystMap<>::init(1.05));
  //DY XSection Uncertainty
  cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_htt_zjXsec", "lnN", SystMap<>::init(1.04));
  //Muon Fake Rate Uncertainty
  cb.cp().process({"ZL"}).AddSyst(cb, "CMS_mFakeTau", "lnN",SystMap<>::init(1.26));    
  
  cb.cp().process({"WH_htt125"}).AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.008));
  cb.cp().process({"ZH_htt125"}).AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.009));
  cb.cp().process(qqH_STXS).AddSyst(cb, "QCDScale_qqH", "lnN", SystMap<>::init(1.005));

  //Luminosity Uncertainty
  cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","ZL","ZT","TTL","TTT"}})).AddSyst(cb, "lumi_Run2018", "lnN", SystMap<>::init(1.023));

  //??? present in HIG 18-032
  cb.cp().process({"WH_htt125"}).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.018));
  cb.cp().process({"ZH_htt125"}).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.013));
  cb.cp().process(ggH_STXS).AddSyst(cb, "pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));
  cb.cp().process(qqH_STXS).AddSyst(cb, "pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));  
  //********************************************************************************************************************************

  //shape uncertainties
  //********************************************************************************************************************************
  if(not Input.OptionExists("-s"))
    {
      //uses custom defined utility function that only adds the shape if at least one shape inside is not empty.
      
      //Mu to tau fake energy scale and e to tau energy fake scale            
      AddShapesIfNotEmpty({"CMS_ZLShape_mt_1prong","CMS_ZLShape_mt_1prong1pizero"},
			  {"ZL"},
			  &cb,
			  TheFile);
      
      //Fake factor shapes: taken from 18-032 data cards.      
      AddShapesIfNotEmpty({"CMS_ff_qcd_mt_syst", "CMS_ff_qcd_njet0_mt_stat", "CMS_ff_qcd_njet1_mt_stat",
	    "CMS_ff_tt_njet1_stat", "CMS_ff_tt_syst", "CMS_ff_w_njet0_mt_stat", "CMS_ff_w_njet1_mt_stat", 
	    "CMS_ff_w_syst"},
	{"jetFakes"},
	&cb,
	TheFile);
      
      //MET Unclustered Energy Scale      
      AddShapesIfNotEmpty({"CMS_scale_met_unclustered"},
			  {"TTT","TTL","VVT","VVL"},
			  &cb,
			  TheFile);

      //Recoil Shapes:                  
      //check which signal processes this should be applied to. If any.
      AddShapesIfNotEmpty({"CMS_htt_boson_reso_met","CMS_htt_boson_scale_met"},
			  JoinStr({ggH_STXS,qqH_STXS,{"ZT","ZL"}}),
			  &cb,
			  TheFile);

      //ZPT Reweighting Shapes:      
      AddShapesIfNotEmpty({"CMS_htt_dyShape"},
			  {"ZT","ZL"},
			  &cb,
			  TheFile);

      //Top Pt Reweighting      
      AddShapesIfNotEmpty({"CMS_htt_ttbarShape"},
			  {"TTL","TTT"},
			  &cb,
			  TheFile);
  
      //TES Uncertainty                  
      AddShapesIfNotEmpty({"CMS_scale_t_1prong","CMS_scale_t_3prong","CMS_scale_t_1prong1pizero"},
			  JoinStr({ggH_STXS,qqH_STXS,{"VVT","ZT","TTT","WH_htt125","ZH_htt125"}}),
			  &cb,
			  TheFile);

      // Jet Energy Scale Uncertainties            
      AddShapesIfNotEmpty({"CMS_JetRelativeBal","CMS_JetEta3to5","CMS_JetEta0to5",
	    "CMS_JetEta0to3","CMS_JetRelativeSample","CMS_JetEC2"},
	JoinStr({ggH_STXS,qqH_STXS,{"ZT","WH_htt125","ZH_htt125","VVL","ZL","TTL"}}),
	&cb,
	TheFile);

      //ggH Theory Uncertainties
      AddShapesIfNotEmpty({"THU_ggH_Mu","THU_ggH_Res","THU_ggH_Mig01","THU_ggH_Mig12","THU_ggH_VBF2j",
	    "THU_ggH_VBF3j","THU_ggH_qmtop","THU_ggH_PT60","THU_ggH_PT120"},
	ggH_STXS,
	&cb,
	TheFile);            

      //Muon Energy scale uncertainties      
      AddShapesIfNotEmpty({"CMS_scale_m_etam2p4tom2p1","CMS_scale_m_etam2p1tom1p2",
	    "CMS_scale_m_etam1p2to1p2","CMS_scale_m_eta1p2to2p1","CMS_scale_m_eta2p1to2p4"},
	JoinStr({ggH_STXS,qqH_STXS,{"ZT","VVT","TTT","ZL","VVL","TTL","WH_htt125","ZH_htt125"}}),
	&cb,
	TheFile);
    }
  //********************************************************************************************************************************


  //embedded uncertainties. No embedded avaialable for 2018 yet.
  //********************************************************************************************************************************
  if(not Input.OptionExists("-e"))
    {
      //Quadrature addition of CMS_eff_emb_t and CMS_eff_emb_t_Run2018
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_emb_t", "lnN", SystMap<>::init(1.019));
  
      //Quadrature addition of CMS_eff_emb_t_mt and CMS_eff_emt_t_mt_Run2018
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_emb_t_mt","lnN",SystMap<>::init(1.0084));

      //These were changed from shapes to lnN
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_1ProngPi0Eff","lnN",ch::syst::SystMapAsymm<>::init(0.9934,1.011));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_3ProngEff","lnN",ch::syst::SystMapAsymm<>::init(0.969,1.005));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_emb_m","lnN",SystMap<>::init(1.014));

      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_htt_doublemutrg", "lnN", SystMap<>::init(1.04));

      // TTBar Contamination
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_htt_emb_ttbar", "shape", SystMap<>::init(1.00));

      //TES uncertainty
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_1prong", "shape", SystMap<>::init(1.00));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_1prong1pizero", "shape", SystMap<>::init(1.00));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_3prong", "shape", SystMap<>::init(1.00));
    }
  //********************************************************************************************************************************                          

  cb.cp().backgrounds().ExtractShapes(
      aux_shapes + "smh2018mt.root",
      "$BIN/$PROCESS",
      "$BIN/$PROCESS_$SYSTEMATIC");
  cb.cp().signals().ExtractShapes(
      aux_shapes + "smh2018mt.root",
      "$BIN/$PROCESS$MASS",
      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
  //! [part7]

  //! [part8]

  //TODO: Ongoing effort to move to autoMCstats instead of combineharvester bin-by-bin.
  if (not Input.OptionExists("-b"))
    {
      auto bbb = ch::BinByBinFactory()
	.SetAddThreshold(0.05)
	.SetMergeThreshold(0.5)
	.SetFixNorm(false);
      bbb.MergeBinErrors(cb.cp().backgrounds());
      bbb.AddBinByBin(cb.cp().backgrounds(), cb);
      bbb.AddBinByBin(cb.cp().signals(), cb);
    }  
   
  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]

  //! [part9]
  // First we generate a set of bin names:
  set<string> bins = cb.bin_set();
  // This method will produce a set of unique bin names by considering all
  // Observation, Process and Systematic entries in the CombineHarvester
  // instance.

  // We create the output root file that will contain all the shapes.
  TFile output("smh2018_mt.input.root", "RECREATE");

  // Finally we iterate through each bin,mass combination and write a
  // datacard.
  for (auto b : bins) {
    for (auto m : masses) {
      cout << ">> Writing datacard for bin: " << b << " and mass: " << m
           << "\n";
      // We need to filter on both the mass and the mass hypothesis,
      // where we must remember to include the "*" mass entry to get
      // all the data and backgrounds.
      cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(
          b + "_" + m + ".txt", output);
    }
  }
  //! [part9]

}
