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
ndata     =  [14., 14.]	# Number of events observed in data
nbkg      =  [6,6  ]	# Number of predicted bkg events
nbkg2     =  [8.,0 ]
nsig      =  [0,10. ]	# Number of predicted signal events
nbkgErr   =  [1.,1. ]	# (Absolute) Statistical error on bkg estimate
nbkg2Err  =  [0.5,0.5] 	# (Absolute) Statistical error on bkg estimate
nsigErr   =  [0,2. ]	# (Absolute) Statistical error on signal estimate
nbkg_cr1  =  [200.]
nbkg2_cr1 =  [20.]
nbkg_cr2  =  [20.]
nbkg2_cr2 =  [300.]
ndata_cr1 = [210.]
ndata_cr2 = [300.]


lumiError = 0.039 	# Relative luminosity uncertainty

# Set uncorrelated systematics for bkg and signal (1 +- relative uncertainties)
ucb = Systematic("ucb", configMgr.weights, 1.2,0.8, "user","userOverallSys")
ucb2 = Systematic("ucb2", configMgr.weights, 1.1,0.9, "user","userOverallSys")
ucs = Systematic("ucs", configMgr.weights, 1.1,0.9, "user","userOverallSys")

# correlated systematic between background and signal (1 +- relative uncertainties)
corb = Systematic("cor",configMgr.weights, [1.1], [0.9], "user","userHistoSys")
cors = Systematic("cor",configMgr.weights, [1.15], [0.85], "user","userHistoSys")

##########################

# Setting the parameters of the hypothesis test
configMgr.doExclusion=True # True=exclusion, False=discovery
configMgr.nTOYs=3000
configMgr.calculatorType=0 # 2=asymptotic calculator, 0=frequentist calculator
configMgr.testStatType=3   # 3=one-sided profile likelihood test statistic (LHC default)
configMgr.nPoints=20       # number of values scanned of signal-strength for upper-limit determination of signal strength.

configMgr.writeXML = True
configMgr.autoScan = True

##########################

# Keep SRs also in background fit confuguration
configMgr.keepSignalRegionType = True

# Give the analysis a name
configMgr.analysisName = "MyUserAnalysisExtra"
configMgr.outputFileName = f"results/{configMgr.analysisName}s_Output.root"

# Define cuts
configMgr.cutsDict["UserRegion"] = "1."
configMgr.cutsDict["CR1"] = "1."
configMgr.cutsDict["CR2"] = "1."


# Define weights
configMgr.weights = "1."

# Define samples
bkgSample = Sample("Bkg",kGreen-9)
bkgSample.setStatConfig(True)
bkgSample.buildHisto(nbkg,"UserRegion","chan",0.5)
#bkgSample.buildStatErrors(nbkgErr,"UserRegion","cuts")
bkgSample.buildHisto(nbkg_cr1,"CR1","cuts",0.5)
bkgSample.buildHisto(nbkg_cr2,"CR2","cuts",0.5)
bkgSample.setNormFactor("mu_bkg", 1.,0,10)
#bkgSample.setNormFactor("test_func",1.,0,10)
bkgSample.addSystematic(corb)
bkgSample.addSystematic(ucb)

bkgSample2 = Sample("Bkg2",kBlue-9)
bkgSample2.setStatConfig(True)
#bkgSample2.setNormFactor("mu_bkg2", 1.,0,10)
bkgSample2.buildHisto(nbkg2,"UserRegion","chan",0.5)
#bkgSample2.buildHisto([1.],"UserRegion","cuts",0.5)
#bkgSample2.buildStatErrors(nbkg2Err,"UserRegion","cuts")
bkgSample2.buildHisto(nbkg2_cr1,"CR1","cuts",0.5)
bkgSample2.buildHisto(nbkg2_cr2,"CR2","cuts",0.5)
bkgSample2.addSystematic(corb)
bkgSample2.addSystematic(ucb2)


sigSample = Sample("Sig",kPink)
sigSample.setNormFactor("mu_Sig",1.,0.,100.)
sigSample.setStatConfig(True)
sigSample.setNormByTheory()
sigSample.buildHisto(nsig,"UserRegion","chan",0.5)
sigSample.buildHisto([0],"CR1","cuts",0.5)
sigSample.buildHisto([0],"CR2","cuts",0.5)
#sigSample.buildStatErrors(nsigErr,"UserRegion","cuts")
sigSample.addSystematic(cors)
sigSample.addSystematic(ucs)

dataSample = Sample("Data",kBlack)
dataSample.setData()
dataSample.buildHisto(ndata,"UserRegion","chan",0.5)
dataSample.buildHisto(ndata_cr1,"CR1","cuts",0.5)
dataSample.buildHisto(ndata_cr2,"CR2","cuts",0.5)

# Define top-level
ana = configMgr.addFitConfig("SPlusB")
ana.addSamples([bkgSample,bkgSample2,sigSample,dataSample])
ana.setSignalSample(sigSample)
#ana.addFunction("test_func","1 * mu_bkg2","mu_bkg2[1.,0,100]")


# Define measurement
meas = ana.addMeasurement(name="NormalMeasurement",lumi=1.0,lumiErr=lumiError)
meas.addPOI("mu_Sig")
#meas.addParamSetting("Lumi",True,1)

# Add the channel
chan = ana.addChannel("chan",["UserRegion"],2,0.5,2.5)
chan = ana.addChannel("cuts",["CR1"],1,0.5,1.5)
#chan = ana.addChannel("cuts",["CR2"],1,0.5,1.5)
ana.addSignalChannels([chan])

# These lines are needed for the user analysis to run
# Make sure file is re-made when executing HistFactory
if configMgr.executeHistFactory:
    if os.path.isfile(f"data/{configMgr.analysisName}.root"):
        os.remove(f"data/{configMgr.analysisName}.root")
