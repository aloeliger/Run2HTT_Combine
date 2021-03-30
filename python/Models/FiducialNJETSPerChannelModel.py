from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import re

class FiducialNJETSPerChannel(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        self.modelBuilder.doVar("mu_fid[1.0,-15.0,15.0]");
        self.modelBuilder.doVar("rho_0_em[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_1_em[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_2_em[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_3_em[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_4_em[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_0_et[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_1_et[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_2_et[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_3_et[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_4_et[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_1_mt[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_2_mt[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_3_mt[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_4_mt[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_1_tt[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_2_tt[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_3_tt[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_4_tt[1.0,-25.0,25.0]");
        pois = 'mu_fid,rho_0_em,rho_1_em,rho_2_em,rho_3_em,rho_4_em,rho_0_et,rho_1_et,rho_2_et,rho_3_et,rho_4_et,rho_1_mt,rho_2_mt,rho_3_mt,rho_4_mt,rho_1_tt,rho_2_tt,rho_3_tt,rho_4_tt'
        self.modelBuilder.doSet("POI",pois)
        if self.options.mass != 0:
            if self.modelBuilder.out.var("MH"):
              self.modelBuilder.out.var("MH").removeRange()
              self.modelBuilder.out.var("MH").setVal(self.options.mass)
            else:
              self.modelBuilder.doVar("MH[%g]" % self.options.mass);
	self.modelBuilder.factory_('expr::scale_0_em("@0*@1",mu_fid,rho_0_em)')
        self.modelBuilder.factory_('expr::scale_1_em("@0*@1",mu_fid,rho_1_em)')
        self.modelBuilder.factory_('expr::scale_2_em("@0*@1",mu_fid,rho_2_em)')
        self.modelBuilder.factory_('expr::scale_3_em("@0*@1",mu_fid,rho_3_em)')
        self.modelBuilder.factory_('expr::scale_4_em("@0*@1",mu_fid,rho_4_em)')
        self.modelBuilder.factory_('expr::scale_0_et("@0*@1",mu_fid,rho_0_et)')
        self.modelBuilder.factory_('expr::scale_1_et("@0*@1",mu_fid,rho_1_et)')
        self.modelBuilder.factory_('expr::scale_2_et("@0*@1",mu_fid,rho_2_et)')
        self.modelBuilder.factory_('expr::scale_3_et("@0*@1",mu_fid,rho_3_et)')
        self.modelBuilder.factory_('expr::scale_4_et("@0*@1",mu_fid,rho_4_et)')
        self.modelBuilder.factory_('expr::scale_0_mt("@0*(408.5-@1*12.337-@2*7.0248-@3*3.573-@4*1.0897-@5*0.5141-@6*63.893-@7*38.551-@8*19.326-@9*5.600-@10*2.5541-@11*52.6314-@12*25.489-13*7.2549-@14*3.4000-@15*39.663-@16*22.694-@17*7.1852-@18*3.70121)/91.802",mu_fid,rho_0_em,rho_1_em,rho_2_em,rho_3_em,rho_4_em,rho_0_et,rho_1_et,rho_2_et,rho_3_et,rho_4_et,rho_1_mt,rho_2_mt,rho_3_mt,rho_4_mt,rho_1_tt,rho_2_tt,rho_3_tt,rho_4_tt)')
        self.modelBuilder.factory_('expr::scale_0_mt("@0*@1",mu_fid,rho_0_mt)')
        self.modelBuilder.factory_('expr::scale_1_mt("@0*@1",mu_fid,rho_1_mt)')
        self.modelBuilder.factory_('expr::scale_2_mt("@0*@1",mu_fid,rho_2_mt)')
        self.modelBuilder.factory_('expr::scale_3_mt("@0*@1",mu_fid,rho_3_mt)')
        self.modelBuilder.factory_('expr::scale_4_mt("@0*@1",mu_fid,rho_4_mt)')
        self.modelBuilder.factory_('expr::scale_1_tt("@0*@1",mu_fid,rho_1_tt)')
        self.modelBuilder.factory_('expr::scale_2_tt("@0*@1",mu_fid,rho_2_tt)')
        self.modelBuilder.factory_('expr::scale_3_tt("@0*@1",mu_fid,rho_3_tt)')
        self.modelBuilder.factory_('expr::scale_4_tt("@0*@1",mu_fid,rho_4_tt)')
    def getYieldScale(self,bin,process):
      "Return the name of a RooAbsReal to scale this yield by or the two special values 1 and 0 (don't scale, and set to zero)"
      if re.search("em_",bin):
	if re.search("NJ_0",process):
	   return "scale_0_em"
        if re.search("NJ_1",process):
           return "scale_1_em"
        if re.search("NJ_2",process):
           return "scale_2_em"
        if re.search("NJ_3",process):
           return "scale_3_em"
        if re.search("NJ_GE4",process):
           return "scale_4_em"
      if re.search("et_",bin):
        if re.search("NJ_0",process):
           return "scale_0_et"
        if re.search("NJ_1",process):
           return "scale_1_et"
        if re.search("NJ_2",process):
           return "scale_2_et"
        if re.search("NJ_3",process):
           return "scale_3_et"
        if re.search("NJ_GE4",process):
           return "scale_4_et"
      if re.search("mt_",bin):
        if re.search("NJ_0",process):
           return "scale_0_mt"
        if re.search("NJ_1",process):
           return "scale_1_mt"
        if re.search("NJ_2",process):
           return "scale_2_mt"
        if re.search("NJ_3",process):
           return "scale_3_mt"
        if re.search("NJ_GE4",process):
           return "scale_4_mt"
      if re.search("tt_",bin):
        if re.search("NJ_1",process):
           return "scale_1_tt"
        if re.search("NJ_2",process):
           return "scale_2_tt"
        if re.search("NJ_3",process):
           return "scale_3_tt"
        if re.search("NJ_GE4",process):
           return "scale_4_tt"
      return 1

fiducialNJETSPerChannel = FiducialNJETSPerChannel()
