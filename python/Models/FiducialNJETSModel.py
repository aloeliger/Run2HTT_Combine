from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import re

class FiducialNJETS(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        self.modelBuilder.doVar("mu_fid[1.0,-15.0,15.0]");
        self.modelBuilder.doVar("rho_0[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_1[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_2[1.0,-25.0,25.0]");
        self.modelBuilder.doVar("rho_3[1.0,-25.0,25.0]");
        pois = 'mu_fid,rho_0,rho_1,rho_2,rho_3'
        self.modelBuilder.doSet("POI",pois)
        if self.options.mass != 0:
            if self.modelBuilder.out.var("MH"):
              self.modelBuilder.out.var("MH").removeRange()
              self.modelBuilder.out.var("MH").setVal(self.options.mass)
            else:
              self.modelBuilder.doVar("MH[%g]" % self.options.mass);
	self.modelBuilder.factory_('expr::scale_0("@0*@1",mu_fid,rho_0)')
        self.modelBuilder.factory_('expr::scale_1("@0*@1",mu_fid,rho_1)')
        self.modelBuilder.factory_('expr::scale_2("@0*@1",mu_fid,rho_2)')
        self.modelBuilder.factory_('expr::scale_3("@0*@1",mu_fid,rho_3)')
        self.modelBuilder.factory_('expr::scale_GE4("@0*(408.46-@1*168.14-@2*137.93-@3*71.10-@4*21.12)/10.16",mu_fid,rho_0,rho_1,rho_2,rho_3)')
    def getYieldScale(self,bin,process):
        "Return the name of a RooAbsReal to scale this yield by or the two special values 1 and 0 (don't scale, and set to zero)"
	if re.search("NJ_0",process):
	   return "scale_0"
        if re.search("NJ_1",process):
           return "scale_1"
        if re.search("NJ_2",process):
           return "scale_2"
        if re.search("NJ_3",process):
           return "scale_3"
        if re.search("NJ_GE4",process):
           return "scale_GE4"
        return 1

fiducialNJETS = FiducialNJETS()
