//Andrew Loeliger
//Input options: 
// -s disables shape uncertainties
// -e disables embedded
// -b disables bin-by-bin uncertainties
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
#include "CombineHarvester/CombineTools/interface/AutoRebin.h"

using namespace std;

int main(int argc, char **argv) 
{
  InputParserUtility Input(argc,argv);
  
  //! [part1]
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  cout<<"test"<<endl;
  string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/shapes/";

  //keep a handle on the file, we need it to check if shapes are empty.
  TFile* TheFile;
  if (Input.OptionExists("-c")) TheFile = new TFile((aux_shapes+"tt_controls_2017.root").c_str());
  else if (Input.OptionExists("-gf")) TheFile = new TFile((aux_shapes+"smh2017tt_GOF.root").c_str());
  else if (Input.OptionExists("-dp") or Input.OptionExists("-dn") or Input.OptionExists("-dm")||Input.OptionExists("-dljpt")) TheFile = new TFile((aux_shapes+"smh2017tt_Differential.root").c_str());
  else TheFile = new TFile((aux_shapes+"smh2017tt.root").c_str());

  //categories loaded from configurations
  std::vector<std::pair<int,std::string>> cats = {};
  std::vector<std::string> CategoryArgs = Input.GetAllArguments("--Categories");
  int CatNum=1;
  for (auto it = CategoryArgs.begin(); it != CategoryArgs.end(); ++it)
    {
      std::cout<<"Making category for: "<<CatNum<<" "<<*it<<std::endl;
      cats.push_back({CatNum,(std::string)*it});
      CatNum++;
    }

  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  vector<string> masses = {""};;
  //! [part3]
  cb.AddObservations({"*"}, {"smh2017"}, {"13TeV"}, {"tt"}, cats);

  
  vector<string> bkg_procs = {"embedded","jetFakes","VVL","STL","TTL","ZL"};
  if(Input.OptionExists("-e")) { // disable embed
    bkg_procs.erase(std::remove(bkg_procs.begin(), bkg_procs.end(), "embedded"), bkg_procs.end());
    bkg_procs.push_back("ZT");
    bkg_procs.push_back("VVT");
    bkg_procs.push_back("TTT");
    bkg_procs.push_back("STT");
  }
if (Input.OptionExists("-dp") || Input.OptionExists("-dn") || Input.OptionExists("-dm")||Input.OptionExists("-dljpt")) bkg_procs.push_back("OutsideAcceptance");      
 else
   {
     bkg_procs.push_back("ggH_hww125");
     bkg_procs.push_back("qqH_hww125");
     bkg_procs.push_back("WH_hww125");
     bkg_procs.push_back("ZH_hww125");
   } 
 
  cb.AddProcesses({"*"}, {"smh2017"}, {"13TeV"}, {"tt"}, bkg_procs, cats, false);

  vector<string> ggH_STXS;
  if (Input.OptionExists("-g")) ggH_STXS = {"ggH_htt125"};
  else if (Input.OptionExists("-dp")) 
    {
      ggH_STXS = {
	"ggH_PTH_0_45",
	"ggH_PTH_45_80",
	"ggH_PTH_80_120",
	"ggH_PTH_120_200",
	"ggH_PTH_200_350",
	"ggH_PTH_350_450",
	"ggH_PTH_GT450",
      };
      if (Input.OptionExists("-r")) ggH_STXS = {
	  "ggH_recoPTH_0_45",
	  "ggH_recoPTH_45_80",
	  "ggH_recoPTH_80_120",
	  "ggH_recoPTH_120_200",
	  "ggH_recoPTH_200_350",
	  "ggH_recoPTH_350_450",
	  "ggH_recoPTH_GT450",
	};
    }
  //NJets differential Option
  else if (Input.OptionExists("-dn")) 
    {
      ggH_STXS = {
	"ggH_NJ_0",
	"ggH_NJ_1",
	"ggH_NJ_2",
	"ggH_NJ_3",
	"ggH_NJ_GE4",
      };
      if (Input.OptionExists("-r")) ggH_STXS = {
	  "ggH_recoNJ_0",
	  "ggH_recoNJ_1",
	  "ggH_recoNJ_2",
	  "ggH_recoNJ_3",
	  "ggH_recoNJ_GE4",
	};
    }

  //mjj differential option
  else if (Input.OptionExists("-dm")) ggH_STXS = {
      "ggH_MJJ_0_150",
      "ggH_MJJ_150_300",
      "ggH_MJJ_300_450",
      "ggH_MJJ_450_600",
      "ggH_MJJ_600_1000",
      "ggH_MJJ_1000_1400",
      "ggH_MJJ_1400_1800",
      "ggH_MJJ_GE1800",
    };
  else if (Input.OptionExists("-dljpt"))
    {
      ggH_STXS = {
	"ggH_NJ_0",
	"ggH_J1PT_30_60",
	"ggH_J1PT_60_120",
	"ggH_J1PT_120_200",
	"ggH_J1PT_200_350",
	"ggH_J1PT_GT350",
      };
      if (Input.OptionExists("-r")) ggH_STXS = {
	  "ggH_recoNJ_0",
	  "ggH_recoJ1PT_30_60",
	  "ggH_recoJ1PT_60_120",
	  "ggH_recoJ1PT_120_200",
	  "ggH_recoJ1PT_200_350",
	  "ggH_recoJ1PT_GT350",
	};

    }
  else ggH_STXS = {"ggH_PTH_0_200_0J_PTH_10_200_htt125",
		   "ggH_PTH_0_200_0J_PTH_0_10_htt125",
		   "ggH_PTH_0_200_1J_PTH_0_60_htt125",
		   "ggH_PTH_0_200_1J_PTH_60_120_htt125",
		   "ggH_PTH_0_200_1J_PTH_120_200_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125",
		   "ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125",
		   "ggH_PTH_200_300_htt125",
		   "ggH_PTH_300_450_htt125",
		   "ggH_PTH_450_650_htt125",
		   "ggH_PTH_GE650_htt125"};

  vector<string> qqH_STXS; 
  if(Input.OptionExists("-q")) qqH_STXS = {"qqH_htt125"};
  else if (Input.OptionExists("-dp")) 
    {
      qqH_STXS = {
	"xH_PTH_0_45",
	"xH_PTH_45_80",
	"xH_PTH_80_120",
	"xH_PTH_120_200",
	"xH_PTH_200_350",
	"xH_PTH_350_450",
	"xH_PTH_GT450",
      };
      if (Input.OptionExists("-r")) qqH_STXS = {
	  "xH_recoPTH_0_45",
	  "xH_recoPTH_45_80",
	  "xH_recoPTH_80_120",
	  "xH_recoPTH_120_200",
	  "xH_recoPTH_200_350",
	  "xH_recoPTH_350_450",
	  "xH_recoPTH_GT450",
	};
    }

  //NJets differential Option
  else if (Input.OptionExists("-dn")) 
    {
      qqH_STXS = {
	"xH_NJ_0",
	"xH_NJ_1",
	"xH_NJ_2",
	"xH_NJ_3",
	"xH_NJ_GE4",
      };
      if(Input.OptionExists("-r")) qqH_STXS = {
	"xH_recoNJ_0",
	"xH_recoNJ_1",
	"xH_recoNJ_2",
	"xH_recoNJ_3",
	"xH_recoNJ_GE4",
      };
    }
  //mjj differential option
  else if (Input.OptionExists("-dm")) qqH_STXS = {
      "xH_MJJ_0_150",
      "xH_MJJ_150_300",
      "xH_MJJ_300_450",
      "xH_MJJ_450_600",
      "xH_MJJ_600_1000",
      "xH_MJJ_1000_1400",
      "xH_MJJ_1400_1800",
      "xH_MJJ_GE1800",
    };
  else if (Input.OptionExists("-dljpt")) 
    {
      qqH_STXS = {
	"xH_NJ_0",
	"xH_J1PT_30_60",
	"xH_J1PT_60_120",
	"xH_J1PT_120_200",
	"xH_J1PT_200_350",
	"xH_J1PT_GT350",
      };
      if(Input.OptionExists("-r")) qqH_STXS = {
	  "xH_recoNJ_0",
	  "xH_recoJ1PT_30_60",
	  "xH_recoJ1PT_60_120",
	  "xH_recoJ1PT_120_200",
	  "xH_recoJ1PT_200_350",
	  "xH_recoJ1PT_GT350",
	};
    }
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

  vector<string> WH_STXS;
  if (Input.OptionExists("-q")) WH_STXS = {"WH_lep_htt125","WH_had_htt125"};
  else if (Input.OptionExists("-dp")||Input.OptionExists("-dn")||Input.OptionExists("-dm")||Input.OptionExists("-dljpt")) WH_STXS = {};  
  else WH_STXS = {
      "WH_lep_htt125",
      "WH_0J_htt125",
      "WH_1J_htt125",
      "WH_GE2J_MJJ_0_60_htt125",
      "WH_GE2J_MJJ_60_120_htt125",
      "WH_GE2J_MJJ_120_350_htt125",
      "WH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125",
      "WH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125",
      "WH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125",
      "WH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125",
      "WH_GE2J_MJJ_GE350_PTH_GE200_htt125",
    };

  vector<string> ZH_STXS;
  if (Input.OptionExists("-q")) ZH_STXS = {"ZH_lep_htt125","ZH_had_htt125"};
  else if (Input.OptionExists("-dp")||Input.OptionExists("-dn")||Input.OptionExists("-dm")||Input.OptionExists("-dljpt")) ZH_STXS = {};  
  else ZH_STXS = {
      "ZH_lep_htt125",
      "ZH_0J_htt125",
      "ZH_1J_htt125",
      "ZH_GE2J_MJJ_0_60_htt125",
      "ZH_GE2J_MJJ_60_120_htt125",
      "ZH_GE2J_MJJ_120_350_htt125",
      "ZH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125",
      "ZH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125",
      "ZH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125",
      "ZH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125",
      "ZH_GE2J_MJJ_GE350_PTH_GE200_htt125",
    };

  vector<string> ggZH_STXS;
  if (Input.OptionExists("-g")) ggZH_STXS = {"ggZH_lep_htt125","ggZH_had_htt125"};
  else if (Input.OptionExists("-dm")||Input.OptionExists("-dp")||Input.OptionExists("-dn")||Input.OptionExists("-dljpt")) ggZH_STXS = {};
  else ggZH_STXS = {
      "ggZH_lep_htt125",
      "ggZH_PTH_0_200_0J_PTH_10_200_htt125",
      "ggZH_PTH_0_200_0J_PTH_0_10_htt125",
      "ggZH_PTH_0_200_1J_PTH_0_60_htt125",
      "ggZH_PTH_0_200_1J_PTH_60_120_htt125",
      "ggZH_PTH_0_200_1J_PTH_120_200_htt125",
      "ggZH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125",
      "ggZH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125",
      "ggZH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125",
      "ggZH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125",
      "ggZH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125",
      "ggZH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125",
      "ggZH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125",
      "ggZH_PTH_200_300_htt125",
      "ggZH_PTH_300_450_htt125",
      "ggZH_PTH_450_650_htt125",
      "ggZH_PTH_GE650_htt125"
    };

  vector<string> sig_procs = ch::JoinStr({ggH_STXS,
	qqH_STXS,
	WH_STXS,
	ZH_STXS,
	ggZH_STXS});
  cb.AddProcesses(masses, {"smh2017"}, {"13TeV"}, {"tt"}, sig_procs, cats, true);

  //! [part4]

  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;
  using ch::JoinStr;
  //**************************************************
  //start with lnN errors
  //**************************************************

  //Theory uncertainties
  //Theory uncerts
  if (not(Input.OptionExists("-x0")||Input.OptionExists("-x1")||Input.OptionExists("-dp")||Input.OptionExists("-dn")||Input.OptionExists("-dm")||Input.OptionExists("-dljpt")))
    {
      cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_PU_alphas", "lnN", SystMap<>::init(1.0062));
      cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_PU_mq", "lnN", SystMap<>::init(1.0099));
      cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_THU", "lnN", SystMap<>::init(1.017));
      //cb.cp().process(JoinStr({WH_STXS,{"WH_hww125","WH_htt_nonfid125"}})).AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.008));
      //cb.cp().process(JoinStr({ZH_STXS,{"ZH_hww125","ZH_htt_nonfid125"}})).AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.009));
      cb.cp().process(JoinStr({ggH_STXS,{"ggH_hww125"}})).AddSyst(cb, "pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));
      if(not(Input.OptionExists("-dp")||Input.OptionExists("-dn")||Input.OptionExists("-dm")||Input.OptionExists("-dljpt")))
	{
	  cb.cp().process(JoinStr({qqH_STXS,{"qqH_hww125"}})).AddSyst(cb, "pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));
	  cb.cp().process(JoinStr({WH_STXS,{"WH_hww125"}})).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.018));
	  cb.cp().process(JoinStr({ZH_STXS,{"ZH_hww125"}})).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.013));      
	}
    }
  cb.cp().process({"ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125"}).AddSyst(cb, "BR_hww_PU_alphas", "lnN", ch::syst::SystMapAsymm<>::init(1.0066,1.0063));
  cb.cp().process({"ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125"}).AddSyst(cb, "BR_hww_PU_mq", "lnN", ch::syst::SystMapAsymm<>::init(1.0099,1.0098));
  cb.cp().process({"ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125"}).AddSyst(cb, "BR_hww_THU", "lnN", SystMap<>::init(1.0099));  
  //cb.cp().process(JoinStr({qqH_STXS,{"qqH_hww125"}})).AddSyst(cb, "QCDScale_qqH", "lnN", SystMap<>::init(1.005));  

  cb.cp().process({"WH_had_htt125","WH_lep_htt125","WH_hww125","WH_lep_PTV_0_75_htt125","WH_lep_PTV_75_150_htt125","WH_lep_PTV_150_250_0J_htt125","WH_lep_PTV_PTV_150_250_GE1J_htt125","WH_lep_PTV_GT250_htt125"}).AddSyst(cb, "THU_WH_inc", "lnN", ch::syst::SystMapAsymm<>::init(0.993,1.005));
  cb.cp().process({"WH_lep_PTV_0_75_htt125"}).AddSyst(cb, "THU_WH_mig75", "lnN", SystMap<>::init(0.965));
  cb.cp().process({"WH_lep_PTV_75_150_htt125","WH_lep_PTV_150_250_0J_htt125","WH_lep_PTV_150_250_GE1J_htt125","WH_lep_PTV_GT250_htt125"}).AddSyst(cb, "THU_WH_mig75", "lnN", SystMap<>::init(1.039));
  cb.cp().process({"WH_lep_PTV_75_150_htt125"}).AddSyst(cb,"THU_WH_mig150","lnN", SystMap<>::init(0.995));
  cb.cp().process({"WH_lep_PTV_150_250_0J_htt125","WH_lep_PTV_150_250_GE1J_htt125","WH_lep_PTV_GT250_htt125"}).AddSyst(cb, "THU_WH_mig150", "lnN", SystMap<>::init(1.013));
  cb.cp().process({"WH_lep_PTV_150_250_0J","WH_lep_PTV_150_250_GE1J"}).AddSyst(cb, "THU_WH_mig250", "lnN", SystMap<>::init(0.9958));
  cb.cp().process({"WH_lep_PTV_GT250"}).AddSyst(cb, "THU_WH_mig250", "lnN", SystMap<>::init(1.014));
  cb.cp().process({"WH_lep_PTV_150_250_0J"}).AddSyst(cb, "THU_WH_mig01", "lnN", SystMap<>::init(0.961));
  cb.cp().process({"WH_lep_PTV_150_250_GE1J"}).AddSyst(cb, "THU_WH_mig01", "lnN", SystMap<>::init(1.053));

  cb.cp().process({"ZH_had_htt125","ZH_lep_htt125","ZH_hww125","ZH_lep_PTV_0_75_htt125","ZH_lep_PTV_75_150_htt125","ZH_lep_PTV_150_250_0J_htt125","ZH_lep_PTV_PTV_150_250_GE1J_htt125","ZH_lep_PTV_GT250_htt125"}).AddSyst(cb, "THU_ZH_inc", "lnN", ch::syst::SystMapAsymm<>::init(0.994,1.005));
  cb.cp().process({"ZH_lep_PTV_0_75_htt125"}).AddSyst(cb, "THU_ZH_mig75", "lnN", SystMap<>::init(0.963));
  cb.cp().process({"ZH_lep_PTV_75_150_htt125","ZH_lep_PTV_150_250_0J_htt125","ZH_lep_PTV_150_250_GE1J_htt125","ZH_lep_PTV_GT250_htt125"}).AddSyst(cb, "THU_ZH_mig75", "lnN", SystMap<>::init(1.04));
  cb.cp().process({"ZH_lep_PTV_75_150_htt125"}).AddSyst(cb,"THU_ZH_mig150","lnN", SystMap<>::init(0.995));
  cb.cp().process({"ZH_lep_PTV_150_250_0J_htt125","ZH_lep_PTV_150_250_GE1J_htt125","ZH_lep_PTV_GT250_htt125"}).AddSyst(cb, "THU_ZH_mig150", "lnN", SystMap<>::init(1.013));
  cb.cp().process({"ZH_lep_PTV_150_250_0J","ZH_lep_PTV_150_250_GE1J"}).AddSyst(cb, "THU_ZH_mig250", "lnN", SystMap<>::init(0.9958));
  cb.cp().process({"ZH_lep_PTV_GT250"}).AddSyst(cb, "THU_ZH_mig250", "lnN", SystMap<>::init(1.014));
  cb.cp().process({"ZH_lep_PTV_150_250_0J"}).AddSyst(cb, "THU_ZH_mig01", "lnN", SystMap<>::init(0.956));
  cb.cp().process({"ZH_lep_PTV_150_250_GE1J"}).AddSyst(cb, "THU_ZH_mig01", "lnN", SystMap<>::init(1.053));

  cb.cp().process({"ggZH_had_htt125","ggZH_lep_htt125","ggZH_lep_PTV_0_75_htt125","ggZH_lep_PTV_75_150_htt125","ggZH_lep_PTV_150_250_0J_htt125","ggZH_lep_PTV_PTV_150_250_GE1J_htt125","ggZH_lep_PTV_GT250_htt125"}).AddSyst(cb, "THU_ggZH_inc", "lnN", ch::syst::SystMapAsymm<>::init(0.811,1.251));
  cb.cp().process({"ggZH_lep_PTV_0_75_htt125"}).AddSyst(cb, "THU_ggZH_mig75", "lnN", ch::syst::SystMapAsymm<>::init(1.9,0.1));
  cb.cp().process({"ggZH_lep_PTV_75_150_htt125","ggZH_lep_PTV_150_250_0J_htt125","ggZH_lep_PTV_150_250_GE1J_htt125","ggZH_lep_PTV_GT250_htt125"}).AddSyst(cb, "THU_ggZH_mig75", "lnN", SystMap<>::init(1.27));
  cb.cp().process({"ggZH_lep_PTV_75_150_htt125"}).AddSyst(cb,"THU_ggZH_mig150","lnN", SystMap<>::init(0.882));
  cb.cp().process({"ggZH_lep_PTV_150_250_0J_htt125","ggZH_lep_PTV_150_250_GE1J_htt125","ggZH_lep_PTV_GT250_htt125"}).AddSyst(cb, "THU_ggZH_mig150", "lnN", SystMap<>::init(1.142));
  cb.cp().process({"ggZH_lep_PTV_150_250_0J","ggZH_lep_PTV_150_250_GE1J"}).AddSyst(cb, "THU_ggZH_mig250", "lnN", SystMap<>::init(0.963));
  cb.cp().process({"ggZH_lep_PTV_GT250"}).AddSyst(cb, "THU_ggZH_mig250", "lnN", SystMap<>::init(1.154));
  cb.cp().process({"ggZH_lep_PTV_150_250_0J"}).AddSyst(cb, "THU_ggZH_mig01", "lnN", ch::syst::SystMapAsymm<>::init(1.6,0.393));
  cb.cp().process({"ggZH_lep_PTV_150_250_GE1J"}).AddSyst(cb, "THU_ggZH_mig01", "lnN", SystMap<>::init(1.277));

  if(not (Input.OptionExists("-x1")))
    {
      cb.cp().process({"ggH_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.97,1.024));
      cb.cp().process({"ggH_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.879,1.061));
      cb.cp().process({"ggH_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.067,0.972));
      cb.cp().process({"ggH_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.055,0.944));
      cb.cp().process({"ggH_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.973,1.023));
      cb.cp().process({"qqH_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.011,0.999));
      cb.cp().process({"qqH_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.985,1.016));
      cb.cp().process({"qqH_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.003,1.022));
      cb.cp().process({"qqH_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.024,0.988));
      cb.cp().process({"qqH_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.988,1.003));
      cb.cp().process({"ggH_PTH_450_650_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_450_650_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.947,1.001));
      cb.cp().process({"ggH_PTH_450_650_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.842,1.046));
      cb.cp().process({"ggH_PTH_450_650_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_450_650_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.139,0.915));
      cb.cp().process({"ggH_PTH_GE650_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_GE650_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_GE650_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.938,0.954));
      cb.cp().process({"ggH_PTH_GE650_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_GE650_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.357,0.691));
      cb.cp().process({"qqH_GE2J_MJJ_0_60_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.923,0.95));
      cb.cp().process({"qqH_GE2J_MJJ_0_60_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.47,0.904));
      cb.cp().process({"qqH_GE2J_MJJ_0_60_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.956,1.01));
      cb.cp().process({"qqH_GE2J_MJJ_0_60_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.986,0.891));
      cb.cp().process({"qqH_GE2J_MJJ_0_60_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.033,0.973));
      cb.cp().process({"qqH_GE2J_MJJ_60_120_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.628,1.147));
      cb.cp().process({"qqH_GE2J_MJJ_60_120_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.953,0.997));
      cb.cp().process({"qqH_GE2J_MJJ_60_120_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.009,0.99));
      cb.cp().process({"qqH_GE2J_MJJ_60_120_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.918,1.007));
      cb.cp().process({"qqH_GE2J_MJJ_60_120_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.998,1.011));
      cb.cp().process({"qqH_GE2J_MJJ_120_350_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.948,1.008));
      cb.cp().process({"qqH_GE2J_MJJ_120_350_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.96,1.008));
      cb.cp().process({"qqH_GE2J_MJJ_120_350_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.966,1.024));
      cb.cp().process({"qqH_GE2J_MJJ_120_350_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.008,1.035));
      cb.cp().process({"qqH_GE2J_MJJ_120_350_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.918,1.027));
      cb.cp().process({"qqH_1J_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.01,0.996));
      cb.cp().process({"qqH_1J_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.985,1.014));
      cb.cp().process({"qqH_1J_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.94,1.025));
      cb.cp().process({"qqH_1J_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.937,1.021));
      cb.cp().process({"qqH_1J_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.043,0.988));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_0_10_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.994,1.021));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_0_10_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.974,1.002));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_0_10_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.905,1.003));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_0_10_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.654,1.074));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_0_10_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_10_200_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.003,0.993));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_10_200_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.008,0.984));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_10_200_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.152,0.944));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_10_200_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.876,0.931));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_10_200_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_0_10_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.994,1.021));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_0_10_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.974,1.002));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_0_10_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.905,1.003));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_0_10_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.654,1.074));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_0_10_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_10_200_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.003,0.993));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_10_200_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.008,0.984));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_10_200_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.152,0.944));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_10_200_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.876,0.931));
      cb.cp().process({"ggH_PTH_0_200_0J_PTH_10_200_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_GE200_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.84,1.046));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_GE200_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.917,1.046));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_GE200_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.97,1.051));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_GE200_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.017,0.977));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_GE200_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.99,1.008));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_0_60_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.969,1.027));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_0_60_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.835,1.118));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_0_60_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.934,1.025));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_0_60_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.751,1.056));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_0_60_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_60_120_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.013,0.962));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_60_120_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.9,1.071));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_60_120_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.103,0.964));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_60_120_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.125,0.93));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_60_120_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_120_200_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.817,1.077));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_120_200_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.882,1.062));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_120_200_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.024,0.998));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_120_200_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.935,1.014));
      cb.cp().process({"ggH_PTH_0_200_1J_PTH_120_200_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.699,1.204));
      cb.cp().process({"ggH_PTH_200_300_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.119,0.898));
      cb.cp().process({"ggH_PTH_200_300_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.904,1.037));
      cb.cp().process({"ggH_PTH_200_300_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.019,0.97));
      cb.cp().process({"ggH_PTH_200_300_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.119,0.951));
      cb.cp().process({"ggH_PTH_200_300_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.006,0.964));
      cb.cp().process({"ggH_PTH_300_450_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.789,1.003));
      cb.cp().process({"ggH_PTH_300_450_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.922,1.028));
      cb.cp().process({"ggH_PTH_300_450_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.062,0.936));
      cb.cp().process({"ggH_PTH_300_450_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.935,1.008));
      cb.cp().process({"ggH_PTH_300_450_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.948,1.123));
      cb.cp().process({"qqH_0J_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.116,0.966));
      cb.cp().process({"qqH_0J_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.062,0.951));
      cb.cp().process({"qqH_0J_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.231,0.951));
      cb.cp().process({"qqH_0J_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.468,1.201));
      cb.cp().process({"qqH_0J_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.478,0.809));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.902,1.063));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.946,1.043));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.907,1.047));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.928,1.043));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.246,0.772));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.902,1.016));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.868,1.111));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.035,0.952));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.919,0.944));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.023,1.019));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.911,1.05));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.041,1.033));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.038,1.005));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.896,1.032));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.404,0.72));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.979,0.984));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.038,0.991));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.987,0.998));
      cb.cp().process({"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.147,0.906));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.012,0.787));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.858,1.072));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.02,0.999));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.877,1.044));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.589,1.352));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.433,0.707));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.755,1.101));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.049,0.964));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.147,0.863));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.922,0.903));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.962,0.895));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.95,1.009));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.889,1.008));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.985,0.955));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.514,1.343));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.417,0.83));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(2.069,0.917));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.125,0.912));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.455,0.708));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.903,1.08));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.19,0.872));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.939,0.946));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.896,1.083));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.13,0.893));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.911,1.046));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.421,0.921));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.962,0.926));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",SystMap<>::init(1.0));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(0.857,1.067));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.261,0.936));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.2,0.92));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.01,0.98));
      cb.cp().process({"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_pythia_scale","lnN",ch::syst::SystMapAsymm<>::init(1.138,0.85));
    }

  //pdf acceptance uncertainties
    cb.cp().process({ggH_STXS}).bin({"tt_0jet"}).AddSyst(cb,"pdf_Higgs_gg_ACCEPT","lnN",SystMap<>::init(1.009));
  cb.cp().process({ggH_STXS}).bin({"tt_boosted_onejet"}).AddSyst(cb,"pdf_Higgs_gg_ACCEPT","lnN",SystMap<>::init(1.010));
  cb.cp().process({ggH_STXS}).bin({"tt_boosted_multijet"}).AddSyst(cb,"pdf_Higgs_gg_ACCEPT","lnN",SystMap<>::init(1.004));
  cb.cp().process({ggH_STXS}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"pdf_Higgs_gg_ACCEPT","lnN",SystMap<>::init(1.013));
  cb.cp().process({ggH_STXS}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"pdf_Higgs_gg_ACCEPT","lnN",SystMap<>::init(1.013));

  cb.cp().process({qqH_STXS}).bin({"tt_0jet"}).AddSyst(cb,"pdf_Higgs_qq_ACCEPT","lnN",SystMap<>::init(1.008));
  cb.cp().process({qqH_STXS}).bin({"tt_boosted_onejet"}).AddSyst(cb,"pdf_Higgs_qq_ACCEPT","lnN",SystMap<>::init(1.005));
  cb.cp().process({qqH_STXS}).bin({"tt_boosted_multijet"}).AddSyst(cb,"pdf_Higgs_qq_ACCEPT","lnN",SystMap<>::init(1.004));
  cb.cp().process({qqH_STXS}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"pdf_Higgs_qq_ACCEPT","lnN",SystMap<>::init(1.006));
  cb.cp().process({qqH_STXS}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"pdf_Higgs_qq_ACCEPT","lnN",SystMap<>::init(1.006));
  
  // XSection Uncertainties
  cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_htt_tjXsec", "lnN", SystMap<>::init(1.042));
  cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_htt_vvXsec", "lnN", SystMap<>::init(1.05));
  cb.cp().process({"STT","STL"}).AddSyst(cb,"CMS_htt_stXsec", "lnN", SystMap<>::init(1.05));
  cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_htt_zjXsec", "lnN", SystMap<>::init(1.02));
  
  
  //Luminosity Uncertainty
  cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZT","TTL","TTT","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","OutsideAcceptance"}})).AddSyst(cb, "lumi_13TeV_2017", "lnN", SystMap<>::init(1.020));
  cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZT","TTL","TTT","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","OutsideAcceptance"}})).AddSyst(cb, "lumi_13TeV_correlated", "lnN", SystMap<>::init(1.009));
  cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","ZL","ZT","TTL","TTT","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","OutsideAcceptance"}})).AddSyst(cb, "lumi_13TeV_1718", "lnN", SystMap<>::init(1.006));


  cb.cp().process({"jetFakes"}).bin({"tt_0jet"}).AddSyst(cb,"CMS_jetFakesNorm_0jet_tt_2017","lnN",SystMap<>::init(1.05));
  cb.cp().process({"jetFakes"}).bin({"tt_boosted_onejet"}).AddSyst(cb,"CMS_jetFakesNorm_1jet_tt_2017","lnN",SystMap<>::init(1.05));
  cb.cp().process({"jetFakes"}).bin({"tt_boosted_multijet"}).AddSyst(cb,"CMS_jetFakesNorm_2jet_tt_2017","lnN",SystMap<>::init(1.05));
  cb.cp().process({"jetFakes"}).bin({"tt_vbf_highHpT"}).AddSyst(cb,"CMS_jetFakesNorm_2jet_tt_2017","lnN",SystMap<>::init(1.05));
  cb.cp().process({"jetFakes"}).bin({"tt_vbf_lowHpT"}).AddSyst(cb,"CMS_jetFakesNorm_2jet_tt_2017","lnN",SystMap<>::init(1.05));

  cb.cp().process({"jetFakes"}).bin({"htt_PTH_tt_HighTauPt","htt_NJ_tt_HighTauPt","htt_J1PT_tt_HighTauPt"}).AddSyst(cb,"CMS_jetFakesNorm_HighTauPt_tt_2017","lnN",SystMap<>::init(1.05));

  //***********************************************************************
  //shape uncertainties
  //***********************************************************************
  if(not Input.OptionExists("-s"))
    {
      std::cout<<"Adding Shapes..."<<std::endl;
      //uses custom defined utility function that only adds the shape if at least one shape inside is not empty.

      // Prefiring
      AddShapesIfNotEmpty({"CMS_prefiring"},
                          JoinStr({sig_procs,{"VVL","STL","ZL","TTL","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","OutsideAcceptance"}}),
                          &cb,
                          1.00,
                          TheFile,CategoryArgs);

      // Tau ID eff in DM bins
      std::cout<<"Tau ID eff"<<std::endl;
      AddShapesIfNotEmpty({"CMS_tauideff_dm0_2017","CMS_tauideff_dm1_2017","CMS_tauideff_dm10_2017","CMS_tauideff_dm11_2017"},
                          JoinStr({sig_procs,{"ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","OutsideAcceptance"}}),
                          &cb,
                          1.00,
                          TheFile,CategoryArgs);

      // Shape for looser Deep tau ID vsLep than recommanded WP
      if(Input.OptionExists("-dp")||Input.OptionExists("-dn")||Input.OptionExists("-dm")||Input.OptionExists("-dljpt"))
	cb.cp().process({"embedded","ZL","VVL","STL","TTL","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125"}).AddSyst(cb,"CMS_looser_lep_wp", "shape", SystMap<>::init(1.00));

      // Trg eff. 
      std::cout<<"Trigger eff"<<std::endl;
      AddShapesIfNotEmpty({"CMS_doubletautrg_dm0_2017","CMS_doubletautrg_dm1_2017","CMS_doubletautrg_dm10_2017","CMS_doubletautrg_dm11_2017"},
                          JoinStr({sig_procs,{"VVL","STL","TTL","ZL","ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","OutsideAcceptance"}}),
                          &cb,
                          1.00,
                          TheFile,CategoryArgs);


      //Fake factors
      std::cout<<"Fake factors"<<std::endl;
      if (Input.OptionExists("-c"))
	{
	  AddShapesIfNotEmpty({"CMS_rawFF_tt_qcd_0jet_2017",
		"CMS_rawFF_tt_qcd_1jet_2017",
		"CMS_rawFF_tt_qcd_2jet_2017",
		"CMS_FF_closure_tau2pt_tt_qcd_0jet",
		"CMS_FF_closure_tau2pt_tt_qcd_1jet",
		"CMS_FF_closure_tau2pt_tt_qcd_2jet",
		"CMS_FF_closure_tt_qcd_osss_2017",},
	    {"jetFakes"},
	    &cb,
	    1.00,
	    TheFile,CategoryArgs);
	}
      else if (Input.OptionExists("-dp") || Input.OptionExists("-dn") || Input.OptionExists("-dm")||Input.OptionExists("-dljpt"))
       {
	 AddShapesIfNotEmpty({
	      "CMS_rawFF_tt_qcd_0jet_barrel_2017",
		"CMS_rawFF_tt_qcd_1jet_barrel_2017",
		"CMS_rawFF_tt_qcd_2jet_barrel_2017",

		"CMS_rawFF_tt_qcd_0jet_endcap_2017",
		"CMS_rawFF_tt_qcd_1jet_endcap_2017",
		"CMS_rawFF_tt_qcd_2jet_endcap_2017",

		
		"CMS_FF_closure_tau2pt_tt_qcd",

		//"CMS_FF_closure_jet1pt_tt_qcd",
		//"CMS_FF_closure_pth_tt_0jet_qcd",
		"CMS_FF_closure_jet1pt_pth0to45_tt_qcd",
		"CMS_FF_closure_jet1pt_pth45to80_tt_qcd",
		"CMS_FF_closure_jet1pt_pth80to120_tt_qcd",
		"CMS_FF_closure_jet1pt_pth120to200_tt_qcd",
		"CMS_FF_closure_jet1pt_pthgt200_tt_qcd",

		"CMS_FF_norm_tt_0jet_2017",
		"CMS_FF_norm_tt_1jet_2017",
		"CMS_FF_norm_tt_2jet_2017",
		"CMS_FF_norm_tt_3jet_2017",
		"CMS_FF_norm_tt_4jet_2017",
		"CMS_FF_closure_tt_qcd_osss_2017",
	       },
	    {"jetFakes"},
	    &cb,
	    1.00,
	    TheFile,CategoryArgs);
       }
      else
	{
	  AddShapesIfNotEmpty({"CMS_rawFF_tt_qcd_0jet_2017",	    
		"CMS_FF_closure_tau2pt_tt_qcd_0jet",
		"CMS_FF_closure_tt_qcd_osss_2017",},
	    {"jetFakes"},
	    &cb,
	    1.00,
	    TheFile,
	    {"tt_0jet"});

	  AddShapesIfNotEmpty({"CMS_rawFF_tt_qcd_1jet_2017",	    
		"CMS_FF_closure_tau2pt_tt_qcd_1jet",
		"CMS_FF_closure_tt_qcd_osss_2017",},
	    {"jetFakes"},
	    &cb,
	    1.00,
	    TheFile,
	    {"tt_boosted_onejet"});

	  AddShapesIfNotEmpty({"CMS_rawFF_tt_qcd_2jet_2017",	    
		"CMS_FF_closure_tau2pt_tt_qcd_2jet",
		"CMS_FF_closure_tt_qcd_osss_2017",},
	    {"jetFakes"},
	    &cb,
	    1.00,
	    TheFile,
	    {"tt_boosted_multijet","tt_vbf_highHpT","tt_vbf_lowHpT"});
	}

      //MET Unclustered Energy Scale      
      std::cout<<"MET UES"<<std::endl;
      AddShapesIfNotEmpty({"CMS_scale_met_unclustered_2017"},
                          {"TTL","VVL","STL"},
                          &cb,
                          1.00,
                          TheFile,CategoryArgs);

      //Recoil Shapes:                  
      std::cout<<"Recoil shapes"<<std::endl;
      if (Input.OptionExists("-c"))
	{
	  AddShapesIfNotEmpty({"CMS_htt_boson_reso_met_0jet_2017","CMS_htt_boson_scale_met_0jet_2017",
		"CMS_htt_boson_reso_met_1jet_2017","CMS_htt_boson_scale_met_1jet_2017",
		"CMS_htt_boson_reso_met_2jet_2017","CMS_htt_boson_scale_met_2jet_2017"},
	    JoinStr({ggH_STXS,qqH_STXS,{"ZL","ggH_hww125","qqH_hww125"}}),
	    &cb,
	    1.00,
	    TheFile,CategoryArgs);
	}
      else if (Input.OptionExists("-dp") || Input.OptionExists("-dn") || Input.OptionExists("-dm")||Input.OptionExists("-dljpt"))
	{
	  AddShapesIfNotEmpty({"CMS_htt_boson_reso_met_0jet_2017","CMS_htt_boson_scale_met_0jet_2017",
		"CMS_htt_boson_reso_met_1jet_2017","CMS_htt_boson_scale_met_1jet_2017",
		"CMS_htt_boson_reso_met_2jet_2017","CMS_htt_boson_scale_met_2jet_2017"},
	    JoinStr({ggH_STXS,qqH_STXS,{"ZL","ggH_hww125","qqH_hww125","OutsideAcceptance"}}),
	    &cb,
	    1.00,
	    TheFile,CategoryArgs);
	}
      else
	{
	  AddShapesIfNotEmpty({"CMS_htt_boson_reso_met_0jet_2017","CMS_htt_boson_scale_met_0jet_2017"},
			      JoinStr({ggH_STXS,qqH_STXS,{"ZL","ggH_hww125","qqH_hww125"}}),
			      &cb,
			      1.00,
			      TheFile,
			      {"tt_0jet"});
      
	  AddShapesIfNotEmpty({"CMS_htt_boson_reso_met_1jet_2017","CMS_htt_boson_scale_met_1jet_2017"},
			      JoinStr({ggH_STXS,qqH_STXS,{"ZL","ggH_hww125","qqH_hww125"}}),
			      &cb,
			      1.00,
			      TheFile,
			      {"tt_boosted_onejet"});

	  AddShapesIfNotEmpty({"CMS_htt_boson_reso_met_2jet_2017","CMS_htt_boson_scale_met_2jet_2017"},
			      JoinStr({ggH_STXS,qqH_STXS,{"ZL","ggH_hww125","qqH_hww125"}}),
			      &cb,
			      1.00,
			      TheFile,
			      {"tt_boosted_multijet","tt_vbf_highHpT","tt_vbf_lowHpT"});
	}

      //ZPT Reweighting Shapes:      
      std::cout<<"ZPT Reweighting"<<std::endl;
      AddShapesIfNotEmpty({"CMS_htt_dyShape"},
                          {"ZL"},
                          &cb,
                          1.00,
                          TheFile,CategoryArgs);

      //Top Pt Reweighting      
      std::cout<<"ttbar shape"<<std::endl;
      AddShapesIfNotEmpty({"CMS_htt_ttbarShape"},
                          {"TTL"},
                          &cb,
                          1.00,
                          TheFile,CategoryArgs);

      //TES Uncertainty                  
      std::cout<<"TES"<<std::endl;
      AddShapesIfNotEmpty({"CMS_scale_t_1prong_2017","CMS_scale_t_3prong_2017","CMS_scale_t_1prong1pizero_2017","CMS_scale_t_3prong1pizero_2017"},
                          JoinStr({sig_procs,{"ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","OutsideAcceptance"}}),
                          &cb,
                          1.00,
                          TheFile,CategoryArgs);

      std::cout<<"JES"<<std::endl;
      AddShapesIfNotEmpty({"CMS_scale_j_Absolute","CMS_scale_j_Absolute_2017","CMS_scale_j_BBEC1","CMS_scale_j_BBEC1_2017","CMS_scale_j_EC2","CMS_scale_j_EC2_2017",
	    "CMS_scale_j_FlavorQCD","CMS_scale_j_HF","CMS_scale_j_HF_2017","CMS_scale_j_RelativeSample_2017","CMS_scale_j_RelativeBal"},
	JoinStr({sig_procs,{"ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","OutsideAcceptance"}}),
	&cb,
	1.000,
	TheFile,CategoryArgs);

      //JER      
      AddShapesIfNotEmpty({"CMS_res_j_2017"},
			  JoinStr({sig_procs,{"ggH_hww125","qqH_hww125","WH_hww125","ZH_hww125","OutsideAcceptance"}}),
			  &cb,
			  1.000,
			  TheFile,CategoryArgs);
      if (Input.OptionExists("-x0"))
	{
	  std::cout<<"Scaled ggH Theory"<<std::endl;
	  AddShapesIfNotEmpty({"THU_ggH_Mu_norm","THU_ggH_Res_norm","THU_ggH_Mig01_norm","THU_ggH_Mig12_norm","THU_ggH_VBF2j_norm",
		"THU_ggH_VBF3j_norm","THU_ggH_qmtop_norm","THU_ggH_PT60_norm","THU_ggH_PT120_norm"},
	    JoinStr({ggH_STXS,{"ggH_hww125"}}),
	    &cb,
	    1.00,
	    TheFile,CategoryArgs);            

	  //qqH theory uncertainties
	  //NOTE, We explicitly removed THU_qqH_yield from this.
	  std::cout<<"qqH Theory"<<std::endl;
	  AddShapesIfNotEmpty({"THU_qqH_PTH200","THU_qqH_Mjj60","THU_qqH_Mjj120","THU_qqH_Mjj350","THU_qqH_Mjj700",
		"THU_qqH_Mjj1000","THU_qqH_Mjj1500","THU_qqH_PTH25","THU_qqH_JET01"},
	    JoinStr({qqH_STXS,{"qqH_hww125"}}),
	    &cb,
	    1.00,
	    TheFile,CategoryArgs);
	}
      else if (Input.OptionExists("-dp") || Input.OptionExists("-dn") || Input.OptionExists("-dm")||Input.OptionExists("-dljpt"))
        {
	  std::cout<<"ggH Theory"<<std::endl;
	  AddShapesIfNotEmpty({"THU_ggH_Mu","THU_ggH_Res","THU_ggH_Mig01","THU_ggH_Mig12","THU_ggH_VBF2j",
		"THU_ggH_VBF3j","THU_ggH_qmtop","THU_ggH_PT60","THU_ggH_PT120"},
	    JoinStr({ggH_STXS,{"ggH_hww125","OutsideAcceptance"}}),
	    &cb,
	    1.00,
	    TheFile,CategoryArgs);            
        }
      //unscaled for either mu measurement
      else if(not(Input.OptionExists("-x0")||Input.OptionExists("-x1")))
	{
	  std::cout<<"ggH Theory"<<std::endl;
	  AddShapesIfNotEmpty({"THU_ggH_Mu","THU_ggH_Res","THU_ggH_Mig01","THU_ggH_Mig12","THU_ggH_VBF2j",
		"THU_ggH_VBF3j","THU_ggH_qmtop","THU_ggH_PT60","THU_ggH_PT120"},
	    JoinStr({ggH_STXS,{"ggH_hww125"}}),
	    &cb,
	    1.00,
	    TheFile,CategoryArgs);            

	  //qqH theory uncertainties
	  std::cout<<"qqH Theory"<<std::endl;
	  AddShapesIfNotEmpty({"THU_qqH_yield","THU_qqH_PTH200","THU_qqH_Mjj60","THU_qqH_Mjj120","THU_qqH_Mjj350","THU_qqH_Mjj700",
		"THU_qqH_Mjj1000","THU_qqH_Mjj1500","THU_qqH_PTH25","THU_qqH_JET01"},
	    JoinStr({qqH_STXS,{"qqH_hww125"}}),
	    &cb,
	    1.00,
	    TheFile,CategoryArgs);
	}


      if(not(Input.OptionExists("-dp") || Input.OptionExists("-dn") || Input.OptionExists("-dm")||Input.OptionExists("-dljpt")))
	{
	  //new theory shapes
	  AddShapesIfNotEmpty({"VH_scale"},
			      {"WH_had_htt125",
				  "ZH_had_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );
	  AddShapesIfNotEmpty({"WHlep_scale"},
			      {"WH_lep_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );
	  AddShapesIfNotEmpty({"ZHlep_scale"},
			      {"ZH_lep_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );

	  //individual STXS bin shapes
	  AddShapesIfNotEmpty({"ggH_scale_0jet"},
			      {"ggH_PTH_0_200_0J_PTH_10_200_htt125",
				  "ggH_PTH_0_200_0J_PTH_0_10_htt125",
				  "ggZH_PTH_0_200_0J_PTH_10_200_htt125",
				  "ggZH_PTH_0_200_0J_PTH_0_10_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );
	  AddShapesIfNotEmpty({"ggH_scale_1jet_lowpt"},
			      {"ggH_PTH_0_200_1J_PTH_0_60_htt125",
				  "ggH_PTH_0_200_1J_PTH_60_120_htt125",
				  "ggH_PTH_0_200_1J_PTH_120_200_htt125",
				  "ggZH_PTH_0_200_1J_PTH_0_60_htt125",
				  "ggZH_PTH_0_200_1J_PTH_60_120_htt125",
				  "ggZH_PTH_0_200_1J_PTH_120_200_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );
	  AddShapesIfNotEmpty({"ggH_scale_2jet_lowpt"},
			      {"ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125",		   
				  "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125",		   
				  "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125"
				  "ggZH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125",		   
				  "ggZH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125",		   
				  "ggZH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );
	  AddShapesIfNotEmpty({"ggH_scale_vbf"},
			      {"ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125",
				  "ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125",
				  "ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125",
				  "ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125",
				  "ggZH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125",
				  "ggZH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125",
				  "ggZH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125",
				  "ggZH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );
	  AddShapesIfNotEmpty({"ggH_scale_highpt"},
			      {"ggH_PTH_200_300_htt125",
				  "ggH_PTH_300_450_htt125",
				  "ggZH_PTH_200_300_htt125",
				  "ggZH_PTH_300_450_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );
	  AddShapesIfNotEmpty({"ggH_scale_very_highpt"},
			      {"ggH_PTH_450_650_htt125",
				  "ggH_PTH_GE650_htt125",
				  "ggZH_PTH_450_650_htt125",
				  "ggZH_PTH_GE650_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );

	  AddShapesIfNotEmpty({"vbf_scale_0jet"},
			      {"qqH_0J_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );
	  AddShapesIfNotEmpty({"vbf_scale_1jet"},
			      {"qqH_1J_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );
	  AddShapesIfNotEmpty({"vbf_scale_lowmjj"},
			      {"qqH_GE2J_MJJ_0_60_htt125",
				  "qqH_GE2J_MJJ_60_120_htt125",
				  "qqH_GE2J_MJJ_120_350_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );

	  AddShapesIfNotEmpty({"vbf_scale_highmjj_lowpt"},
			      {"qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125",
				  "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125",
				  "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125",
				  "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );

	  AddShapesIfNotEmpty({"vbf_scale_highmjj_highpt"},
			      {"qqH_GE2J_MJJ_GE350_PTH_GE200_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );

	  AddShapesIfNotEmpty({"VH_scale_0jet"},
			      {"WH_0J_htt125",
				  "ZH_0J_htt125,"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );
	  AddShapesIfNotEmpty({"VH_scale_1jet"},
			      {"WH_1J_htt125",
				  "ZH_1J_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );
	  AddShapesIfNotEmpty({"VH_scale_lowmjj"},
			      {"WH_GE2J_MJJ_0_60_htt125",
				  "WH_GE2J_MJJ_60_120_htt125",
				  "WH_GE2J_MJJ_120_350_htt125",
				  "ZH_GE2J_MJJ_0_60_htt125",
				  "ZH_GE2J_MJJ_60_120_htt125",
				  "ZH_GE2J_MJJ_120_350_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );

	  AddShapesIfNotEmpty({"VH_scale_highmjj_lowpt"},
			      {"WH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125",
				  "WH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125",
				  "WH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125",
				  "WH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125",
				  "ZH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125",
				  "ZH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125",
				  "ZH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125",
				  "ZH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125"},
			      &cb,
			      1.00,
			      TheFile,
			      CategoryArgs
			      );
	}

      AddShapesIfNotEmpty({"VH_scale_highmjj_highpt"},
			  {"WH_GE2J_MJJ_GE350_PTH_GE200_htt125",
			      "ZH_GE2J_MJJ_GE350_PTH_GE200_htt125"},
			  &cb,
			  1.00,
			  TheFile,
			  CategoryArgs
			  );
      
      if (Input.OptionExists("-dp") || Input.OptionExists("-dn") || Input.OptionExists("-dm")||Input.OptionExists("-dljpt"))
	{
	  if (not(Input.OptionExists("-r"))) {
	    AddShapesIfNotEmpty({"QCDscale_qqH","QCDscale_ggZH","QCDscale_VH","QCDscale_ttH"},
				JoinStr({qqH_STXS,{"OutsideAcceptance"}}),
				&cb,
				1.00,
				TheFile,
				CategoryArgs);
	  }
	}
    }

  //*****************************************************************
  //embedded uncertainties. 
  //*****************************************************************
  if(not Input.OptionExists("-e"))
    {      
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_htt_doublemutrg_2017", "lnN", SystMap<>::init(1.04));
      // Tau ID eff
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_t_embedded_dm0_2017", "shape", SystMap<>::init(1.000));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_t_embedded_dm1_2017", "shape", SystMap<>::init(1.000));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_t_embedded_dm10_2017", "shape", SystMap<>::init(1.000));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_t_embedded_dm11_2017", "shape", SystMap<>::init(1.000));


      // TTBar Contamination
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_htt_emb_ttbar_2017", "shape", SystMap<>::init(1.00));

      //TES uncertainty
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_1prong_2017", "shape", SystMap<>::init(0.866));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_1prong1pizero_2017", "shape", SystMap<>::init(0.866));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_3prong_2017", "shape", SystMap<>::init(0.866));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_3prong1pizero_2017", "shape", SystMap<>::init(0.866));

      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_t_1prong_2017", "shape", SystMap<>::init(0.500));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_t_1prong1pizero_2017", "shape", SystMap<>::init(0.500));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_t_3prong_2017", "shape", SystMap<>::init(0.500));     
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_t_3prong1pizero_2017", "shape", SystMap<>::init(0.500));

      //Trigger Uncertainty
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_doubletautrg_emb_dm0_2017","shape",SystMap<>::init(0.866));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_doubletautrg_dm0_2017","shape",SystMap<>::init(0.500));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_doubletautrg_emb_dm1_2017","shape",SystMap<>::init(0.866));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_doubletautrg_dm1_2017","shape",SystMap<>::init(0.500));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_doubletautrg_emb_dm10_2017","shape",SystMap<>::init(0.866));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_doubletautrg_dm10_2017","shape",SystMap<>::init(0.500));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_doubletautrg_emb_dm11_2017","shape",SystMap<>::init(0.866));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_doubletautrg_dm11_2017","shape",SystMap<>::init(0.500));

    }  

  //********************************************************************************************************************************                          
  if (Input.OptionExists("-c"))
    {
      cb.cp().backgrounds().ExtractShapes(
					  aux_shapes + "tt_controls_2017.root",
					  "$BIN/$PROCESS",
					  "$BIN/$PROCESS_$SYSTEMATIC");
      cb.cp().signals().ExtractShapes(
				      aux_shapes + "tt_controls_2017.root",
				      "$BIN/$PROCESS$MASS",
				      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
    }
  else if(Input.OptionExists("-gf"))
    {
      cb.cp().backgrounds().ExtractShapes(
                      aux_shapes + "smh2017tt_GOF.root",
                      "$BIN/$PROCESS",
                      "$BIN/$PROCESS_$SYSTEMATIC");
      cb.cp().signals().ExtractShapes(
                      aux_shapes + "smh2017tt_GOF.root",
                      "$BIN/$PROCESS$MASS",
                      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
    }
  else if(Input.OptionExists("-dp")||Input.OptionExists("-dn")||Input.OptionExists("-dm")||Input.OptionExists("-dljpt"))
    {
      cb.cp().backgrounds().ExtractShapes(
      aux_shapes + "smh2017tt_Differential.root",
      "$BIN/$PROCESS",
      "$BIN/$PROCESS_$SYSTEMATIC");
      cb.cp().signals().ExtractShapes(
      aux_shapes + "smh2017tt_Differential.root",
      "$BIN/$PROCESS$MASS",
      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
    }
  else
    {
      cb.cp().backgrounds().ExtractShapes(
					  aux_shapes + "smh2017tt.root",
					  "$BIN/$PROCESS",
					  "$BIN/$PROCESS_$SYSTEMATIC");
      cb.cp().signals().ExtractShapes(
				      aux_shapes + "smh2017tt.root",
				      "$BIN/$PROCESS$MASS",
				      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
    }
  //auto rebinning of low background bins
  auto rebin = ch::AutoRebin()
    .SetBinThreshold(1.00);
  rebin.Rebin(cb.cp().channel({"tt"}), cb);
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
  //TFile output("smh2017_tt.input.root", "RECREATE");
  TFile output((Input.ReturnToken(0)+"/"+"smh2017_tt.input.root").c_str(), "RECREATE");

  // Finally we iterate through each bin,mass combination and write a
  // datacard.
  for (auto b : bins) {
    for (auto m : masses) {
      cout << ">> Writing datacard for bin: " << b << " and mass: " << m
           << "\n";
      // We need to filter on both the mass and the mass hypothesis,
      // where we must remember to include the "*" mass entry to get
      // all the data and backgrounds.
      //cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(
      //    b + "_" + m + ".txt", output);
      cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(Input.ReturnToken(0)+"/"+b + "_" + m + ".txt", output);
    }
  }
  //! [part9]

}
