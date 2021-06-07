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

using namespace std;
using ch::JoinStr;

int main(int argc, char **argv)
{
  //! [part1]
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  cout<<"test"<<endl;
  InputParserUtility Input(argc,argv);
  string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/shapes/";

  // Create an all8pty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  // Here we will just define two categories for an 8TeV analysis. Each entry in
  // the vector below specifies a bin name and corresponding bin_id.
  ch::Categories cats = {
      {1, "eeet"},
      {2, "eemt"},
      {3, "eett"},
      {4, "mmet"},
      {5, "mmmt"},
      {6, "mmtt"}
    };
  vector<string> masses = {"125"};//ch::MassesFromRange("120");//120-135:5");
  cb.AddObservations({"*"}, {"zh"}, {"2017"}, {"all8"}, cats);

  vector<string> HWW;
  if(Input.OptionExists("--STXS_HWW"))HWW={"ggZH_lep_PTV_0_75_hww125","ggZH_lep_PTV_75_150_hww125","ggZH_lep_PTV_150_250_0J_hww125","ggZH_lep_PTV_150_250_GE1J_hww125","ggZH_lep_PTV_GT250_hww125","ZH_lep_PTV_0_75_hww125","ZH_lep_PTV_75_150_hww125","ZH_lep_PTV_150_250_0J_hww125","ZH_lep_PTV_150_250_GE1J_hww125","ZH_lep_PTV_GT250_hww125"}; 
  else HWW={"ZH_hww125"};
  vector<string> nonHiggs;
  nonHiggs={"Triboson","Reducible","ZZ"};
  vector<string> bkg_procs = ch::JoinStr({nonHiggs,HWW});
  cb.AddProcesses({"*"}, {"zh"}, {"2017"}, {"all8"}, bkg_procs, cats, false);
  vector<string> sig_procs;
  if(Input.OptionExists("--IncVH")) sig_procs = {"ZH_lep_htt","ggZH_lep_htt"};
  else sig_procs = {"ggZH_lep_PTV_0_75_htt","ggZH_lep_PTV_75_150_htt","ggZH_lep_PTV_150_250_0J_htt","ggZH_lep_PTV_150_250_GE1J_htt","ggZH_lep_PTV_GT250_htt","ZH_lep_PTV_0_75_htt","ZH_lep_PTV_75_150_htt","ZH_lep_PTV_150_250_0J_htt","ZH_lep_PTV_150_250_GE1J_htt","ZH_lep_PTV_GT250_htt"};

  cb.AddProcesses(masses, {"zh"}, {"2017"}, {"all8"}, sig_procs, cats, true);


  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;

  // Bkg normalization

  cb.cp().process({"Reducible"}).bin({"eeet"}).AddSyst(cb, "reducible_norm_eeet_statAI_2017", "lnN", SystMap<>::init(1.20));
  cb.cp().process({"Reducible"}).bin({"eeet"}).AddSyst(cb, "reducible_norm_eeet_statFR_2017", "lnN", SystMap<>::init(1.03));
  cb.cp().process({"Reducible"}).bin({"eeet"}).AddSyst(cb,"CMS_fakeEle_promptSubtraction_2017", "lnN", SystMap<>::init(1.005));

  cb.cp().process({"Reducible"}).bin({"mmet"}).AddSyst(cb, "reducible_norm_mmet_statAI_2017", "lnN", SystMap<>::init(1.15));
  cb.cp().process({"Reducible"}).bin({"mmet"}).AddSyst(cb, "reducible_norm_mmet_statFR_2017", "lnN", SystMap<>::init(1.03));
  cb.cp().process({"Reducible"}).bin({"mmet"}).AddSyst(cb,"CMS_fakeEle_promptSubtraction_2017", "lnN", SystMap<>::init(1.005));

  cb.cp().process({"Reducible"}).bin({"eemt"}).AddSyst(cb, "reducible_norm_eemt_statAI_2017", "lnN", SystMap<>::init(1.19));
  cb.cp().process({"Reducible"}).bin({"eemt"}).AddSyst(cb, "reducible_norm_eemt_statFR_2017", "lnN", SystMap<>::init(1.03));
  cb.cp().process({"Reducible"}).bin({"eemt"}).AddSyst(cb,"CMS_fakeMu_promptSubtraction_2017", "lnN", SystMap<>::init(1.01));

  cb.cp().process({"Reducible"}).bin({"mmmt"}).AddSyst(cb, "reducible_norm_mmmt_statAI_2017", "lnN", SystMap<>::init(1.13));
  cb.cp().process({"Reducible"}).bin({"mmmt"}).AddSyst(cb, "reducible_norm_mmmt_statFR_2017", "lnN", SystMap<>::init(1.03));
  cb.cp().process({"Reducible"}).bin({"mmmt"}).AddSyst(cb,"CMS_fakeMu_promptSubtraction_2017", "lnN", SystMap<>::init(1.01));

  cb.cp().process({"Reducible"}).bin({"eett"}).AddSyst(cb, "reducible_norm_eett_statAI_2017", "lnN", SystMap<>::init(1.25));
  cb.cp().process({"Reducible"}).bin({"eett"}).AddSyst(cb, "reducible_norm_eett_statFR_2017", "lnN", SystMap<>::init(1.02));

  cb.cp().process({"Reducible"}).bin({"mmtt"}).AddSyst(cb, "reducible_norm_mmtt_statAI_2017", "lnN", SystMap<>::init(1.17));
  cb.cp().process({"Reducible"}).bin({"mmtt"}).AddSyst(cb, "reducible_norm_mmtt_statFR_2017", "lnN", SystMap<>::init(1.02));


  // MC bkg normalization
  cb.cp().process({"ZZ"}).AddSyst(cb, "CMS_htt_zzXsec_13TeV", "lnN", SystMap<>::init(1.032));
  cb.cp().process({"Triboson"}).AddSyst(cb, "CMS_htt_triboson_13TeV", "lnN", SystMap<>::init(1.25));

  // Theory uncertainties
  cb.cp().process({sig_procs}).AddSyst(cb, "BR_htt_THU", "lnN", SystMap<>::init(1.017));
  cb.cp().process({sig_procs}).AddSyst(cb, "BR_htt_PU_mq", "lnN", SystMap<>::init(1.0099));
  cb.cp().process({sig_procs}).AddSyst(cb, "BR_htt_PU_alphas", "lnN", SystMap<>::init(1.0062));
  cb.cp().process({HWW}).AddSyst(cb, "BR_hww_PU_alphas", "lnN", ch::syst::SystMapAsymm<>::init(1.0066,1.0063));
  cb.cp().process({HWW}).AddSyst(cb, "BR_hww_PU_mq", "lnN", ch::syst::SystMapAsymm<>::init(1.0099,1.0098));
  cb.cp().process({HWW}).AddSyst(cb, "BR_hww_THU", "lnN", SystMap<>::init(1.0099));

  cb.cp().process(JoinStr({sig_procs,HWW})).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.016));

  cb.cp().process({"ZH_lep_htt","ZH_lep_PTV_0_75_htt","ZH_lep_PTV_75_150_htt","ZH_lep_PTV_150_250_0J_htt","ZH_lep_PTV_150_250_GE1J_htt","ZH_lep_PTV_GT250_htt","ZH_lep_hww125","ZH_lep_PTV_0_75_hww125","ZH_lep_PTV_75_150_hww125","ZH_lep_PTV_150_250_0J_hww125","ZH_lep_PTV_150_250_GE1J_hww125","ZH_lep_PTV_GT250_hww125"}).AddSyst(cb,"qqVH_NLOEWK", "shape", SystMap<>::init(1.00));
  cb.cp().process({"ZH_lep_htt","ggZH_lep_htt","ZH_lep_hww125","ggZH_lep_hww125"}).AddSyst(cb,"ZHlep_scale", "shape", SystMap<>::init(1.00));
  cb.cp().process({"ZH_lep_PTV_0_75_htt","ZH_lep_PTV_75_150_htt","ZH_lep_PTV_150_250_0J_htt","ZH_lep_PTV_150_250_GE1J_htt","ZH_lep_PTV_0_75_hww125","ZH_lep_PTV_75_150_hww125","ZH_lep_PTV_150_250_0J_hww125","ZH_lep_PTV_150_250_GE1J_hww125","ggZH_lep_PTV_0_75_htt","ggZH_lep_PTV_75_150_htt","ggZH_lep_PTV_150_250_0J_htt","ggZH_lep_PTV_150_250_GE1J_htt"}).AddSyst(cb,"ZH_scale_lowpt", "shape", SystMap<>::init(1.00));
  cb.cp().process({"ZH_lep_PTV_GT250_htt","ggZH_lep_PTV_GT250_htt","ZH_lep_PTV_GT250_hww125"}).AddSyst(cb,"ZH_scale_highpt", "shape", SystMap<>::init(1.00));

  // THU
  cb.cp().process({"ZH_lep_htt","ZH_lep_hww125","ZH_lep_PTV_0_75_htt","ZH_lep_PTV_75_150_htt","ZH_lep_PTV_150_250_0J_htt","ZH_lep_PTV_150_250_GE1J_htt","ZH_lep_PTV_GT250_htt","ZH_lep_PTV_0_75_hww125","ZH_lep_PTV_75_150_hww125","ZH_lep_PTV_150_250_0J_hww125","ZH_lep_PTV_150_250_GE1J_hww125","ZH_lep_PTV_GT250_hww125"}).AddSyst(cb, "THU_ZH_inc", "lnN", ch::syst::SystMapAsymm<>::init(0.994,1.005));
  cb.cp().process({"ZH_lep_PTV_0_75_htt","ZH_lep_PTV_0_75_hww125"}).AddSyst(cb, "THU_ZH_mig75", "lnN", SystMap<>::init(0.963));
  cb.cp().process({"ZH_lep_PTV_75_150_htt","ZH_lep_PTV_150_250_0J_htt","ZH_lep_PTV_150_250_GE1J_htt","ZH_lep_PTV_GT250_htt","ZH_lep_PTV_75_150_hww125","ZH_lep_PTV_150_250_0J_hww125","ZH_lep_PTV_150_250_GE1J_hww125","ZH_lep_PTV_GT250_hww125"}).AddSyst(cb, "THU_ZH_mig75", "lnN", SystMap<>::init(1.04));
  cb.cp().process({"ZH_lep_PTV_75_150_htt","ZH_lep_PTV_75_150_hww125"}).AddSyst(cb, "THU_ZH_mig150", "lnN", SystMap<>::init(0.995));
  cb.cp().process({"ZH_lep_PTV_150_250_0J_htt","ZH_lep_PTV_150_250_GE1J_htt","ZH_lep_PTV_GT250_htt","ZH_lep_PTV_150_250_0J_hww125","ZH_lep_PTV_150_250_GE1J_hww125","ZH_lep_PTV_GT250_hww125"}).AddSyst(cb, "THU_ZH_mig150", "lnN", SystMap<>::init(1.013));
  cb.cp().process({"ZH_lep_PTV_150_250_0J_htt","ZH_lep_PTV_150_250_GE1J_htt","ZH_lep_PTV_150_250_0J_hww125","ZH_lep_PTV_150_250_GE1J_hww125"}).AddSyst(cb, "THU_ZH_mig250", "lnN", SystMap<>::init(0.9958));
  cb.cp().process({"ZH_lep_PTV_GT250_htt","ZH_lep_PTV_GT250_hww125"}).AddSyst(cb, "THU_ZH_mig250", "lnN", SystMap<>::init(1.014));
  cb.cp().process({"ZH_lep_PTV_150_250_0J_htt","ZH_lep_PTV_150_250_0J_hww125"}).AddSyst(cb, "THU_ZH_mig01", "lnN", SystMap<>::init(0.956));
  cb.cp().process({"ZH_lep_PTV_150_250_GE1J_htt","ZH_lep_PTV_150_250_GE1J_hww125"}).AddSyst(cb, "THU_ZH_mig01", "lnN", SystMap<>::init(1.053));

  cb.cp().process({"ggZH_lep_htt","ggZH_lep_hww125","ggZH_lep_PTV_0_75_htt","ggZH_lep_PTV_75_150_htt","ggZH_lep_PTV_150_250_0J_htt","ggZH_lep_PTV_150_250_GE1J_htt","ggZH_lep_PTV_GT250_htt","ggZH_lep_PTV_0_75_hww125","ggZH_lep_PTV_75_150_hww125","ggZH_lep_PTV_150_250_0J_hww125","ggZH_lep_PTV_150_250_GE1J_hww125","ggZH_lep_PTV_GT250_hww125"}).AddSyst(cb, "THU_ggZH_inc", "lnN", ch::syst::SystMapAsymm<>::init(0.811,1.251));
  cb.cp().process({"ggZH_lep_PTV_0_75_htt","ggZH_lep_PTV_0_75_hww125"}).AddSyst(cb, "THU_ggZH_mig75", "lnN", ch::syst::SystMapAsymm<>::init(1.9,0.1));
  cb.cp().process({"ggZH_lep_PTV_75_150_htt","ggZH_lep_PTV_150_250_0J_htt","ggZH_lep_PTV_150_250_GE1J_htt","ggZH_lep_PTV_GT250_htt","ggZH_lep_PTV_75_150_hww125","ggZH_lep_PTV_150_250_0J_hww125","ggZH_lep_PTV_150_250_GE1J_hww125","ggZH_lep_PTV_GT250_hww125"}).AddSyst(cb, "THU_ggZH_mig75", "lnN", SystMap<>::init(1.27));
  cb.cp().process({"ggZH_lep_PTV_75_150_htt","ggZH_lep_PTV_75_150_hww125"}).AddSyst(cb, "THU_ggZH_mig150", "lnN", SystMap<>::init(0.882));
  cb.cp().process({"ggZH_lep_PTV_150_250_0J_htt","ggZH_lep_PTV_150_250_GE1J_htt","ggZH_lep_PTV_GT250_htt","ggZH_lep_PTV_150_250_0J_hww125","ggZH_lep_PTV_150_250_GE1J_hww125","ggZH_lep_PTV_GT250_hww125"}).AddSyst(cb, "THU_ggZH_mig150", "lnN", SystMap<>::init(1.142));
  cb.cp().process({"ggZH_lep_PTV_150_250_0J_htt","ggZH_lep_PTV_150_250_GE1J_htt","ggZH_lep_PTV_150_250_0J_hww125","ggZH_lep_PTV_150_250_GE1J_hww125"}).AddSyst(cb, "THU_ggZH_mig250", "lnN", SystMap<>::init(0.963));
  cb.cp().process({"ggZH_lep_PTV_GT250_htt","ggZH_lep_PTV_GT250_hww125"}).AddSyst(cb, "THU_ggZH_mig250", "lnN", SystMap<>::init(1.154));
  cb.cp().process({"ggZH_lep_PTV_150_250_0J_htt","ggZH_lep_PTV_150_250_0J_hww125"}).AddSyst(cb, "THU_ggZH_mig01", "lnN", ch::syst::SystMapAsymm<>::init(1.6,0.393));
  cb.cp().process({"ggZH_lep_PTV_150_250_GE1J_htt","ggZH_lep_PTV_150_250_GE1J_hww125"}).AddSyst(cb, "THU_ggZH_mig01", "lnN", SystMap<>::init(1.277));

  // Lumi uncertainties
  cb.cp().process(JoinStr({{"TriBoson","ZZ"},sig_procs,HWW})).AddSyst(cb, "lumi_13TeV_2017","lnN", SystMap<>::init(1.020));
  cb.cp().process(JoinStr({{"TriBoson","ZZ"},sig_procs,HWW})).AddSyst(cb, "lumi_13TeV_correlated","lnN", SystMap<>::init(1.009));
  cb.cp().process(JoinStr({{"TriBoson","ZZ"},sig_procs,HWW})).AddSyst(cb, "lumi_13TeV_1718","lnN", SystMap<>::init(1.006));

  // Trg and ID uncertainties
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).bin({"eeet","eemt","eett"}).AddSyst(cb, "CMS_singleeletrg_2017", "lnN", SystMap<>::init(1.01));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).bin({"mmet","mmmt","mmtt"}).AddSyst(cb, "CMS_singlemutrg_2017", "lnN", SystMap<>::init(1.01));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).bin({"eeet"}).AddSyst(cb, "CMS_eff_e_2017", "lnN", SystMap<>::init(1.06));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).bin({"eemt","eett"}).AddSyst(cb, "CMS_eff_e_2017", "lnN", SystMap<>::init(1.04));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).bin({"mmet"}).AddSyst(cb, "CMS_eff_e_2017", "lnN", SystMap<>::init(1.02));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).bin({"mmmt"}).AddSyst(cb, "CMS_eff_m_2017", "lnN", SystMap<>::init(1.06));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).bin({"mmet","mmtt"}).AddSyst(cb, "CMS_eff_m_2017", "lnN", SystMap<>::init(1.04));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).bin({"eemt"}).AddSyst(cb, "CMS_eff_m_2017", "lnN", SystMap<>::init(1.02));

  //Scale met
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs})).AddSyst(cb,"CMS_scale_met_unclustered_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_scale_j_Absolute", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_scale_j_Absolute_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_scale_j_BBEC1", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_scale_j_BBEC1_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_scale_j_EC2", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_scale_j_EC2_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_scale_j_FlavorQCD", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_scale_j_HF", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_scale_j_HF_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_scale_j_RelativeSample_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_scale_j_RelativeBal", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_res_j_2017", "shape", SystMap<>::init(1.00));

  //Scale mu, ele
  cb.cp().process(JoinStr({{"Reducible","Triboson","ZZ"},sig_procs})).bin({"eeet","eemt","eett","mmet"}).AddSyst(cb,"CMS_scale_e_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Reducible","Triboson","ZZ"},sig_procs})).bin({"eemt","mmet","mmmt","mmtt"}).AddSyst(cb,"CMS_scale_m_etalt1p2_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Reducible","Triboson","ZZ"},sig_procs})).bin({"eemt","mmet","mmmt","mmtt"}).AddSyst(cb,"CMS_scale_m_eta1p2to2p1_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Reducible","Triboson","ZZ"},sig_procs})).bin({"eemt","mmet","mmmt","mmtt"}).AddSyst(cb,"CMS_scale_m_etagt2p1_2017", "shape", SystMap<>::init(1.00));

  // TES
  cb.cp().process({"ZZ","ZH_lep_htt","ZH_lep_PTV_0_75_htt","ZH_lep_PTV_75_150_htt","ZH_lep_PTV_150_250_0J_htt","ZH_lep_PTV_150_250_GE1J_htt","ZH_lep_PTV_GT250_htt"}).bin({"eeet","eemt","eett","mmet","mmmt","mmtt"}).AddSyst(cb,"CMS_scale_t_1prong_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process({"ZZ","ZH_lep_htt","ZH_lep_PTV_0_75_htt","ZH_lep_PTV_75_150_htt","ZH_lep_PTV_150_250_0J_htt","ZH_lep_PTV_150_250_GE1J_htt","ZH_lep_PTV_GT250_htt"}).bin({"eeet","eemt","eett","mmet","mmmt","mmtt"}).AddSyst(cb,"CMS_scale_t_1prong1pizero_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process({"ZZ","ZH_lep_htt","ZH_lep_PTV_0_75_htt","ZH_lep_PTV_75_150_htt","ZH_lep_PTV_150_250_0J_htt","ZH_lep_PTV_150_250_GE1J_htt","ZH_lep_PTV_GT250_htt"}).bin({"eeet","eemt","eett","mmet","mmmt","mmtt"}).AddSyst(cb,"CMS_scale_t_3prong_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process({"ZZ","ZH_lep_htt","ZH_lep_PTV_0_75_htt","ZH_lep_PTV_75_150_htt","ZH_lep_PTV_150_250_0J_htt","ZH_lep_PTV_150_250_GE1J_htt","ZH_lep_PTV_GT250_htt"}).bin({"eeet","eemt","eett","mmet","mmmt","mmtt"}).AddSyst(cb,"CMS_scale_t_3prong1pizero_2017", "shape", SystMap<>::init(1.00));

  // Tau ID
  cb.cp().process(JoinStr({{"Reducible","Triboson","ZZ"},sig_procs,HWW})).bin({"eeet","eemt","eett","mmet","mmmt","mmtt"}).AddSyst(cb,"CMS_tauideff_pt20to25_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Reducible","Triboson","ZZ"},sig_procs,HWW})).bin({"eeet","eemt","eett","mmet","mmmt","mmtt"}).AddSyst(cb,"CMS_tauideff_pt25to30_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Reducible","Triboson","ZZ"},sig_procs,HWW})).bin({"eeet","eemt","eett","mmet","mmmt","mmtt"}).AddSyst(cb,"CMS_tauideff_pt30to35_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Reducible","Triboson","ZZ"},sig_procs,HWW})).bin({"eeet","eemt","eett","mmet","mmmt","mmtt"}).AddSyst(cb,"CMS_tauideff_pt35to40_2017", "shape", SystMap<>::init(1.00));
  cb.cp().process(JoinStr({{"Reducible","Triboson","ZZ"},sig_procs,HWW})).bin({"eeet","eemt","eett","mmet","mmmt","mmtt"}).AddSyst(cb,"CMS_tauideff_ptgt40_2017", "shape", SystMap<>::init(1.00));


  //Prefiring
  cb.cp().process(JoinStr({{"Triboson","ZZ"},sig_procs,HWW})).AddSyst(cb,"CMS_prefiring", "shape", SystMap<>::init(1.00));


  cb.cp().backgrounds().ExtractShapes(
      aux_shapes + "zh2017.root",
      "$BIN/$PROCESS",
      "$BIN/$PROCESS_$SYSTEMATIC");
  cb.cp().signals().ExtractShapes(
      aux_shapes + "zh2017.root",
      "$BIN/$PROCESS$MASS",
      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]

  //! [part9]
  // First we generate a set of bin names:
  set<string> bins = cb.bin_set();
  // This method will produce a set of unique bin names by considering all
  // Observation, Process and Systall8atic entries in the CombineHarvester
  // instance.

  // We create the output root file that will contain all the shapes.
  TFile output((Input.ReturnToken(0)+"/"+"zh2017.input.root").c_str(), "RECREATE");

  // Finally we iterate through each bin,mass combination and write a
  // datacard.
  for (auto b : bins) {
    for (auto m : masses) {
      cout << ">> Writing datacard for bin: " << b << " and mass: " << m
           << "\n";
      // We need to filter on both the mass and the mass hypothesis,
      // where we must rall8all8ber to include the "*" mass entry to get
      // all the data and backgrounds.
      cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(Input.ReturnToken(0)+"/"+b + "_" + m + ".txt", output);
    }
  }
  //! [part9]

}
