"""
 **********************************************************************************
 * Project: HistFitter - A ROOT-based package for statistical data analysis       *
 * Package: HistFitter                                                            *
 *                                                                                *
 * Description:                                                                   *
 *      Minimal example configuration with two different uncertainties            *
 *                                                                                *
 * Authors:                                                                       *
 *      HistFitter group, CERN, Geneva                                            *
 *                                                                                *
 * Redistribution and use in source and binary forms, with or without             *
 * modification, are permitted according to the terms listed in the file          *
 * LICENSE.                                                                       *
 **********************************************************************************
"""

################################################################
## In principle all you have to setup is defined in this file ##
################################################################
from configManager import configMgr
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange
from configWriter import fitConfig,Measurement,Channel,Sample
from systematic import Systematic
from math import sqrt

import os

# Setup for ATLAS plotting
from ROOT import gROOT
#gROOT.LoadMacro("./macros/AtlasStyle.C")
import ROOT
#ROOT.SetAtlasStyle()

##########################

# Set observed and expected number of events in counting experiment
ndata_sr  =  12. 	# Number of events observed in data
nbkg1_sr  =  3.	 	# Number of predicted bkg events
nbkg2_sr  =  2.	 	# Number of predicted bkg events
nsig      =  5.  	# Number of predicted signal events
nbkg1Err  =  1.  	# (Absolute) Statistical error on bkg estimate
nbkg2Err  =  0.2  	# (Absolute) Statistical error on bkg estimate
nsigErr   =  2.  	# (Absolute) Statistical error on signal estimate

ndata_sr2  =  6. 	# Number of events observed in data
nbkg1_sr2  =  3.	 	# Number of predicted bkg events
nbkg2_sr2  =  2.	 	# Number of predicted bkg events
nsig2      =  3.  	# Number of predicted signal events
nbkg1Err2  =  1.  	# (Absolute) Statistical error on bkg estimate
nbkg2Err2  =  0.2  	# (Absolute) Statistical error on bkg estimate
nsigErr2  =  1.  	# (Absolute) Statistical error on signal estimate

ndata_cr = 100.
nbkg1_cr = 70.
nbkg2_cr = 10.

lumiError = 0.039 	# Relative luminosity uncertainty

# Set uncorrelated systematics for bkg and signal (1 +- relative uncertainties)
ucb = Systematic("ucb", configMgr.weights, 1.2,0.8, "user","userOverallSys")
ucs = Systematic("ucs", configMgr.weights, 1.1,0.9, "user","userOverallSys")

ucb2 = Systematic("ucb2", configMgr.weights, 1.1,0.9, "user","userOverallSys")

# correlated systematic between background and signal (1 +- relative uncertainties)
corb = Systematic("cor",configMgr.weights, [1.1],[0.9], "user","userHistoSys")
cors = Systematic("cor",configMgr.weights, [1.15],[0.85], "user","userHistoSys")

##########################

# Setting the parameters of the hypothesis test
configMgr.doExclusion=True # True=exclusion, False=discovery
#configMgr.nTOYs=5000
configMgr.calculatorType=2 # 2=asymptotic calculator, 0=frequentist calculator
configMgr.testStatType=3   # 3=one-sided profile likelihood test statistic (LHC default)
configMgr.nPoints=20       # number of values scanned of signal-strength for upper-limit determination of signal strength.

configMgr.writeXML = False

##########################

# Keep SRs also in background fit confuguration
configMgr.keepSignalRegionType = True
bkgonly = True
configMgr.blindSR=False

# Give the analysis a name
configMgr.analysisName = "hf_test"
configMgr.outputFileName = f"results/{configMgr.analysisName}s_Output.root"

# Define cuts
configMgr.cutsDict["SignalRegion"] = "1."
configMgr.cutsDict["SignalRegion2"] = "1."
configMgr.cutsDict["ControlRegion"] = "1."

# Define weights
configMgr.weights = "1."

# Define samples
bkgSample = Sample("Bkg1",kGreen-9)
bkgSample.setStatConfig(True)
bkgSample.buildHisto([nbkg1_sr],"SignalRegion","cuts",0.5)
bkgSample.buildStatErrors([nbkg1Err],"SignalRegion","cuts")
bkgSample.buildHisto([nbkg1_sr2],"SignalRegion2","cuts",0.5)
bkgSample.buildStatErrors([nbkg1Err2],"SignalRegion2","cuts")
bkgSample.buildHisto([nbkg1_cr],"ControlRegion","cuts",0.5)
bkgSample.buildStatErrors([sqrt(nbkg1_cr)/5.],"ControlRegion","cuts")
bkgSample.addSystematic(corb)
bkgSample.addSystematic(ucb)
bkgSample.setNormByTheory(False)
bkgSample.setNormFactor("mu_bkg",1.,0,10.)

bkg2Sample = Sample("Bkg2",kGreen-4)
bkg2Sample.setStatConfig(True)
bkg2Sample.buildHisto([nbkg2_sr],"SignalRegion","cuts",0.5)
bkg2Sample.buildStatErrors([nbkg2Err],"SignalRegion","cuts")
bkg2Sample.buildHisto([nbkg2_sr2],"SignalRegion2","cuts",0.5)
bkg2Sample.buildStatErrors([nbkg2Err2],"SignalRegion2","cuts")
bkg2Sample.buildHisto([nbkg2_cr],"ControlRegion","cuts",0.5)
bkg2Sample.buildStatErrors([sqrt(nbkg2_cr)/5.],"ControlRegion","cuts")
#bkg2Sample.addSystematic()
bkg2Sample.addSystematic(ucb2)


sigSample = Sample("Sig",kPink)
sigSample.setNormFactor("mu_Sig",1.,0.,100.)
sigSample.setStatConfig(True)
sigSample.setNormByTheory()
sigSample.buildHisto([nsig],"SignalRegion","cuts",0.5)
sigSample.buildStatErrors([nsigErr],"SignalRegion","cuts")
sigSample.buildHisto([nsig2],"SignalRegion2","cuts",0.5)
sigSample.buildStatErrors([nsigErr2],"SignalRegion2","cuts")
sigSample.addSystematic(cors)
sigSample.addSystematic(ucs)

dataSample = Sample("Data",kBlack)
dataSample.setData()
dataSample.buildHisto([ndata_sr],"SignalRegion","cuts",0.5)
dataSample.buildHisto([ndata_sr2],"SignalRegion2","cuts",0.5)
dataSample.buildHisto([ndata_cr],"ControlRegion","cuts",0.5)

# Define top-level
ana = configMgr.addFitConfig("SPlusB")
if configMgr.blindSR or bkgonly:
    ana.addSamples([bkgSample,bkg2Sample,dataSample])
else:
    ana.addSamples([bkgSample,bkg2Sample,sigSample,dataSample])
    ana.setSignalSample(sigSample)

# Define measurement
meas = ana.addMeasurement(name="NormalMeasurement",lumi=1.0,lumiErr=lumiError)
meas.addPOI("mu_Sig")
#meas.addParamSetting("Lumi",True,1)

# Add the channel
sr = ana.addChannel("cuts",["SignalRegion"],1,0.5,1.5)
sr2 = ana.addChannel("cuts",["SignalRegion2"],1,0.5,1.5)
ana.addSignalChannels([sr,sr2])

cr = ana.addChannel("cuts",["ControlRegion"],1,0.5,1.5)
ana.addBkgConstrainChannels([cr])

bkgSample.setNormRegions(["ControlRegion","cuts"])

# These lines are needed for the user analysis to run
# Make sure file is re-made when executing HistFactory
if configMgr.executeHistFactory:
    if os.path.isfile(f"data/{configMgr.analysisName}.root"):
        os.remove(f"data/{configMgr.analysisName}.root")
