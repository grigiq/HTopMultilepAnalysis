#!/usr/bin/env python

import ROOT

from xAH_config import xAH_config

# Hack to force just-in-time libraries to load,
# needed for Muon quality enum. Ask gstark@cern.ch for questions.
#
alg = ROOT.xAH.Algorithm()
del alg

trig_el = ['HLT_e24_lhmedium_L1EM20VH',
           'HLT_e24_lhmedium_L1EM18VH',
           'HLT_e60_lhmedium',
           'HLT_e120_lhloose'
          ]
trig_mu = ['HLT_mu20_iloose_L1MU15',
           'HLT_mu50'
          ]

all_triggers = trig_el + trig_mu
triglist = ",".join(all_triggers)

path_ext = "$ROOTCOREBIN/data/HTopMultilepAnalysis/External/"

PRW_files = ["tthML.PURWTconfig.410009.mc15b.root","tthML.PURWTconfig.341177.root","tthML.PURWTconfig.341270.root","tthML.PURWTconfig.341271.root","tthML.PURWTconfig.342170.root","tthML.PURWTconfig.342171.root","tthML.PURWTconfig.342172.root","tthML.PURWTconfig.410066.root","tthML.PURWTconfig.410067.root","tthML.PURWTconfig.410068.root","tthML.PURWTconfig.410080.root","tthML.PURWTconfig.410081.root","tthML.PURWTconfig.341997.root","tthML.PURWTconfig.341998.root","tthML.PURWTconfig.341999.root","tthML.PURWTconfig.342000.root","tthML.PURWTconfig.342001.root","tthML.PURWTconfig.342002.root","tthML.PURWTconfig.342003.root","tthML.PURWTconfig.342004.root","tthML.PURWTconfig.342005.root","tthML.PURWTconfig.361071.root","tthML.PURWTconfig.361072.root","tthML.PURWTconfig.361073.root","tthML.PURWTconfig.361077.root","tthML.PURWTconfig.361079.root","tthML.PURWTconfig.361081.root","tthML.PURWTconfig.361082.root","tthML.PURWTconfig.361083.root","tthML.PURWTconfig.361085.root","tthML.PURWTconfig.361087.root","tthML.PURWTconfig.361500.root","tthML.PURWTconfig.361501.root","tthML.PURWTconfig.361502.root","tthML.PURWTconfig.361503.root","tthML.PURWTconfig.361504.root","tthML.PURWTconfig.361505.root","tthML.PURWTconfig.361506.root","tthML.PURWTconfig.361507.root","tthML.PURWTconfig.361508.root","tthML.PURWTconfig.361509.root","tthML.PURWTconfig.361510.root","tthML.PURWTconfig.361511.root","tthML.PURWTconfig.361512.root","tthML.PURWTconfig.361513.root","tthML.PURWTconfig.361514.root","tthML.PURWTconfig.361520.root","tthML.PURWTconfig.361521.root","tthML.PURWTconfig.361522.root","tthML.PURWTconfig.361523.root","tthML.PURWTconfig.361524.root","tthML.PURWTconfig.361525.root","tthML.PURWTconfig.361526.root","tthML.PURWTconfig.361527.root","tthML.PURWTconfig.361528.root","tthML.PURWTconfig.361530.root","tthML.PURWTconfig.361531.root","tthML.PURWTconfig.361532.root","tthML.PURWTconfig.361533.root","tthML.PURWTconfig.361534.root"]

for idx,file in enumerate(PRW_files):
     PRW_files[idx] = ''.join((path_ext,file))

PRW_config = ','.join(PRW_files)

BasicEventSelectionDict = { "m_name"		      : "baseEventSel",
		            "m_debug"		      : False,
                            "m_applyGRLCut"	      : True,
			    "m_GRLxml"  	      : ''.join((path_ext,"data15_13TeV.periodAllYear_DetStatus-v73-pro19-08_DQDefects-00-01-02_PHYS_StandardGRL_All_Good_25ns.xml")),
                            "m_doPUreweighting"       : True,
			    "m_lumiCalcFileNames"     : ''.join((path_ext,"ilumicalc_histograms_HLT_mu20_iloose_L1MU15_276262-284484.root")),
			    "m_PRWFileNames"	      : PRW_config,
			    "m_PU_default_channel"    : 410009,
			    "m_applyPrimaryVertexCut" : False,
                            "m_vertexContainerName"   : "PrimaryVertices",
                            "m_PVNTrack"	      : 3,
                            "m_applyEventCleaningCut" : True,
			    "m_applyCoreFlagsCut"     : False,
                            "m_truthLevelOnly"        : False,
                            "m_derivationName"        : "HIGG8D1",
                            "m_useMetaData"	      : True,
 			    "m_checkDuplicatesData"   : True,
  			    "m_checkDuplicatesMC"     : False,
                            "m_triggerSelection"      : triglist,
                            "m_applyTriggerCut"       : True,
                            "m_storeTrigDecisions"    : True,
			    "m_storePassHLT"	      : True,
                          }

JetCalibratorDict = { "m_name"                   : "jetCalib_AntiKt4EMTopo",
		      "m_debug"                  : False,
                      "m_inContainerName"        : "AntiKt4EMTopoJets",
                      "m_jetAlgo"                : "AntiKt4EMTopo",
                      "m_outContainerName"       : "AntiKt4EMTopoJets_Calib",
                      "m_outputAlgo"             : "JetCalibrator_Syst",
                      "m_sort"                   : True,
                      "m_calibSequence"          : "JetArea_Residual_Origin_EtaJES_GSC",
                      "m_calibConfigAFII"        : "JES_MC15Prerecommendation_AFII_June2015.config",
                      "m_calibConfigFullSim"     : "JES_2015dataset_recommendation_Feb2016.config",
                      "m_calibConfigData"        : "JES_2015dataset_recommendation_Feb2016.config",
                      "m_JESUncertConfig"        : "$ROOTCOREBIN/data/JetUncertainties/JES_2015/Moriond2016/JES2015_AllNuisanceParameters.config",
                      "m_JESUncertMCType"        : "MC15",
                      "m_JERUncertConfig"        : "JetResolution/Prerec2015_xCalib_2012JER_ReducedTo9NP_Plots_v2.root",
                      "m_JERApplyNominal"        : False,
                      "m_JERFullSys"             : False,
                      "m_jetCleanCutLevel"       : "LooseBad",
		      "m_jetCleanUgly"           : False,
                      "m_cleanParent"            : False,
		      "m_saveAllCleanDecisions"  : True,
                      "m_redoJVT"                : True
                    }

MuonCalibratorDict = { "m_name"                : "muonCalib",
		       "m_debug"               : False,
                       "m_inContainerName"     : "Muons",
                       "m_outContainerName"    : "Muons_Calib",
		       "m_inputAlgoSystNames"  : "",
                       "m_outputAlgoSystNames" : "MuonCalibrator_Syst",
		       "m_release"             : "Recs2016_01_19",
	               "m_systName"            : "",
	               "m_systVal"             : 0.0,
                     }

ElectronCalibratorDict = { "m_name"                : "electronCalib",
		    	   "m_debug"		   : False,
                    	   "m_inContainerName"     : "Electrons",
                    	   "m_outContainerName"    : "Electrons_Calib",
		    	   "m_inputAlgoSystNames"  : "",
                    	   "m_outputAlgoSystNames" : "ElectronCalibrator_Syst",
   			   "m_esModel" 		   : "es2015PRE",
   			   "m_decorrelationModel"  : "FULL_ETACORRELATED_v1",
	            	   "m_systName" 	   : "",
	            	   "m_systVal"  	   : 0.0,
                         }

JetSelectorDict = { "m_name"                    :  "jetSelect_selection",
		    "m_debug"		        :  False,
                    "m_inContainerName"         :  "AntiKt4EMTopoJets_Calib",
                    "m_outContainerName"        :  "AntiKt4EMTopoJets_Selected",
                    "m_inputAlgo"               :  "",
                    "m_outputAlgo"              :  "JetSelector_Syst",
                    "m_createSelectedContainer" :  True,
		    "m_decorateSelectedObjects" :  True,
                    "m_useCutFlow"              :  True,
                    "m_pT_min"                  :  25e3,
                    "m_eta_max"                 :  2.5,
                    "m_doJVT"                   :  True,
                    "m_pt_max_JVT"              :  60e3,
                    "m_eta_max_JVT"             :  2.4,
                    "m_JVTCut"                  :  0.59,
                    "m_doBTagCut"               :  False,
                    "m_operatingPt"             :  "FixedCutBEff_77",
                  }

MuonSelectorDict = { "m_name"                      : "muonSelect_selection",
		     "m_debug"		           :  False,
                     "m_inContainerName"	   : "Muons_Calib",
                     "m_outContainerName"	   : "Muons_Selected",
                     "m_inputAlgoSystNames"	   : "MuonCalibrator_Syst",
                     "m_outputAlgoSystNames"	   : "MuonSelector_Syst",
                     "m_createSelectedContainer"   : True,
		     "m_decorateSelectedObjects"   : True,
		     "m_pass_min"		   : 0,
                     "m_pT_min"                    : 10e3,
                     "m_eta_max"                   : 2.5,
		     #"m_muonType"                : "Combined",
	             #"m_muonQuality"             : ROOT.xAOD.Muon.Loose,
	             "m_muonQualityStr"            : "Loose",
                     "m_d0sig_max"	     	   : 3.0,
                     "m_z0sintheta_max"      	   : 0.5,
                     "m_MinIsoWPCut"         	   : "Loose",
		     "m_IsoWPList"           	   : "Loose,GradientLoose,Gradient,FixedCutLoose,FixedCutTightTrackOnly,UserDefinedCut",
                     "m_CaloIsoEff"		   : "0.1*x",
                     "m_TrackIsoEff"		   : "0.1*x",
                     "m_CaloBasedIsoType"	   : "topoetcone20",
                     "m_TrackBasedIsoType"	   : "ptvarcone30",
                     "m_singleMuTrigChains"	   : "HLT_mu20_iloose_L1MU15,HLT_mu50",
                     "m_diMuTrigChains"		   : "",
		   }

ElectronSelectorDict = { "m_name"                      : "electronSelect_selection",
		         "m_debug"		       :  False,
                         "m_inContainerName"	       : "Electrons_Calib",
                         "m_outContainerName"	       : "Electrons_Selected",
                         "m_inputAlgoSystNames"        : "ElectronCalibrator_Syst",
                         "m_outputAlgoSystNames"       : "ElectronSelector_Syst",
                    	 "m_createSelectedContainer"   : True,
		    	 "m_decorateSelectedObjects"   : True,
			 "m_pass_min"		       : 0,
                         "m_pT_min"		       : 10e3,
                         "m_eta_max"		       : 2.47,
                         "m_vetoCrack"                 : True,
                         "m_d0sig_max"		       : 5.0,
                         "m_z0sintheta_max"            : 0.5,
                         "m_doAuthorCut"               : False,
                         "m_doOQCut"                   : False,
                         "m_doBLTrackQualityCut"       : True, # set this to True if reading ID flags from DAOD
                         "m_readIDFlagsFromDerivation" : True,
                         "m_confDirPID"	               : "mc15_20160113",
                         "m_doLHPIDcut"                : True,
                         "m_LHOperatingPoint"	       : "Loose", # for loose ID, use "LooseAndBLayer" if NOT reading ID flags from DAOD
                         "m_doCutBasedPIDcut"          : False,
                         "m_CutBasedOperatingPoint"    : "IsEMLoose",
                         "m_CutBasedConfigYear"	       : "",
                         "m_MinIsoWPCut"	       : "Loose",
                         "m_IsoWPList"  	       : "Loose,GradientLoose,Gradient,FixedCutLoose,FixedCutTight,FixedCutTightTrackOnly,UserDefinedCut",
                         "m_CaloIsoEff"  	       : "0.05*x",
                         "m_TrackIsoEff"  	       : "0.05*x",
                         "m_CaloBasedIsoType"  	       : "topoetcone20",
                         "m_TrackBasedIsoType"         : "ptvarcone20",
                         "m_ElTrigChains"  	       : "HLT_e24_lhmedium_L1EM20VH,HLT_e24_lhmedium_L1EM18VH,HLT_e60_lhmedium,HLT_e120_lhloose",
		       }

TauSelectorDict = { "m_name"                      : "tauSelect_selection",
		    "m_debug"			  :  False,
                    "m_inContainerName" 	  : "TauJets",
                    "m_outContainerName"	  : "Taus_Selected",
                    "m_inputAlgoSystNames"	  : "",
                    "m_outputAlgoSystNames"	  : "TauSelector_Syst",
                    "m_createSelectedContainer"   : True,
		    "m_decorateSelectedObjects"   : True,
                    "m_minPtDAOD"		  : 15e3,
                    "m_ConfigPath"		  : "$ROOTCOREBIN/data/HTopMultilepAnalysis/Taus/recommended_selection_mc15.conf",
		    #"m_EleOLRFilePath" 	   : "$ROOTCOREBIN/data/HTopMultilepAnalysis/Taus/eveto_cutvals.root"
		  }

METConstructorDict = { "m_name"                  : "met",
		       "m_debug"		 : False,
                       "m_referenceMETContainer" : "MET_Reference_AntiKt4EMTopo",
                       "m_mapName"               : "METAssoc_AntiKt4EMTopo",
                       "m_coreName"              : "MET_Core_AntiKt4EMTopo",
                       "m_outputContainer"       : "RefFinal_HTopMultilep",
                       "m_doPhotonCuts"          : True,
                       "m_useCaloJetTerm"        : True,
                       "m_useTrackJetTerm"       : False,
                       "m_inputElectrons"	 : "Electrons_Selected",
                       "m_inputPhotons" 	 : "Photons",
                       "m_inputTaus"		 : "Taus_Selected",
                       "m_inputMuons"		 : "Muons_Selected",
                       "m_inputJets"		 : "AntiKt4EMTopoJets_Calib",
                       "m_doJVTCut"	         : True,
                    }

OverlapRemoverDict = { "m_name"                       : "overlap_removal_ASG",
		       "m_debug"		      : False,
		       "m_useCutFlow"                 : True,
                       "m_createSelectedContainers"   : True,
		       "m_decorateSelectedObjects"    : True,
         	       "m_useSelected"  	      : True,
         	       "m_inContainerName_Muons"      : "Muons_Selected",
         	       "m_outContainerName_Muons"     : "Muons_OR",
         	       "m_inputAlgoMuons"	      : "",
         	       "m_inContainerName_Electrons"  : "Electrons_Selected",
         	       "m_outContainerName_Electrons" : "Electrons_OR",
         	       "m_inputAlgoElectrons"	      : "",
         	       "m_inContainerName_Jets"       : "AntiKt4EMTopoJets_Selected",
         	       "m_outContainerName_Jets"      : "AntiKt4EMTopoJets_OR",
         	       "m_inputAlgoJets"	      : "",
         	       "m_inContainerName_Taus"       : "Taus_Selected",
         	       "m_outContainerName_Taus"      : "Taus_OR",
         	       "m_inputAlgoTaus"	      : "",
                     }

BJetEfficiencyCorrectorDict = { "m_name"                : "bjetEffCor_BTag_MV2c20_Fix77",
		                "m_debug"		: False,
                        	"m_inContainerName"	: "AntiKt4EMTopoJets_OR",
         	        	"m_corrFileName"        : "$ROOTCOREBIN/data/xAODAnaHelpers/2016-Winter-13TeV-MC15-CDI-February14_v2.root",
         	        	"m_jetAuthor"           : "AntiKt4EMTopoJets",
         	        	"m_taggerName"          : "MV2c20",
         	        	"m_operatingPt"         : "FixedCutBEff_77",
		        	"m_useDevelopmentFile"  : False,
         	        	"m_coneFlavourLabel"    : True,
         	        	"m_systName"            : "",
                              }

MuonEfficiencyCorrectorDict = { "m_name"                  : "muonEfficiencyCorrector",
                                "m_debug"	          : False,
                                "m_inContainerName"       : "Muons_OR",
                                "m_inputAlgoSystNames"    : "MuonSelector_Syst",
                                "m_systNameReco"          : "",
                                "m_systNameIso"           : "",
                                "m_systNameTrig"          : "",
                                "m_systNameTTVA"          : "",
                                "m_runNumber"             : 276329,
                                "m_useRandomRunNumber"    : True,
                                "m_outputSystNamesReco"   : "MuonEfficiencyCorrector_RecoSyst",
                                "m_outputSystNamesIso"    : "MuonEfficiencyCorrector_IsoSyst",
                                "m_outputSystNamesTrig"   : "MuonEfficiencyCorrector_TrigSyst",
                                "m_outputSystNamesTTVA"   : "MuonEfficiencyCorrector_TTVASyst",
                                "m_calibRelease"          : "Data15_allPeriods_260116",
                                "m_WorkingPointReco"      : "Loose",
                                "m_WorkingPointIso"       : "Loose",
                                "m_WorkingPointRecoTrig"  : "Loose",
                                "m_WorkingPointIsoTrig"   : "Loose",
                                "m_WorkingPointTTVA"      : "TTVA",
                                "m_SingleMuTrig"	  : "HLT_mu20_iloose_L1MU15_OR_HLT_mu50",
                                "m_DiMuTrig"	          : "",
                              }

MuonEfficiencyCorrectorTightDict = { "m_name"                  : "muonEfficiencyCorrectorTight",
                                     "m_debug"	               : False,
                                     "m_inContainerName"       : "Muons_OR",
                                     "m_inputAlgoSystNames"    : "MuonSelector_Syst",
                                     "m_systNameReco"          : "",
                                     "m_systNameIso"           : "",
                                     "m_systNameTrig"          : "",
                                     "m_systNameTTVA"          : "",
                                     "m_runNumber"             : 276329,
                                     "m_useRandomRunNumber"    : True,
                                     "m_outputSystNamesReco"   : "MuonEfficiencyCorrector_RecoSyst",
                                     "m_outputSystNamesIso"    : "MuonEfficiencyCorrector_IsoSyst",
                                     "m_outputSystNamesTrig"   : "MuonEfficiencyCorrector_TrigSyst",
                                     "m_outputSystNamesTTVA"   : "MuonEfficiencyCorrector_TTVASyst",
                                     "m_calibRelease"          : "Data15_allPeriods_260116",
                                     "m_WorkingPointReco"      : "Loose",
                                     "m_WorkingPointIso"       : "FixedCutTightTrackOnly",
                                     "m_WorkingPointRecoTrig"  : "Loose",
                                     "m_WorkingPointIsoTrig"   : "FixedCutTightTrackOnly",
                                     "m_WorkingPointTTVA"      : "TTVA",
                                     "m_SingleMuTrig"	       : "HLT_mu20_iloose_L1MU15_OR_HLT_mu50",
                                     "m_DiMuTrig"	       : "",
                                   }

ElectronEfficiencyCorrectorDict = { "m_name"                  : "electronEfficiencyCorrectorTight",
                                    "m_debug"		      : False,
                                    "m_inContainerName"	      : "Electrons_OR",
                                    "m_inputAlgoSystNames"    : "ElectronSelector_Syst",
                                    "m_systNameReco"          : "",
                                    "m_systNamePID"           : "",
                                    "m_systNameTrig"	      : "",
                                    "m_systNameTrigMCEff"     : "",
                                    "m_outputSystNamesReco"   : "ElectronEfficiencyCorrector_RecoSyst",
                                    "m_outputSystNamesPID"    : "ElectronEfficiencyCorrector_PIDSyst",
                                    "m_outputSystNamesIso"    : "ElectronEfficiencyCorrector_IsoSyst",
                                    "m_outputSystNamesTrig"   : "ElectronEfficiencyCorrector_TrigSyst",
                                    "m_outputSystNamesTrigMCEff"   : "ElectronEfficiencyCorrector_TrigMCEffSyst",
                                    "m_corrFileNameReco"      : "$ROOTCOREBIN/data/ElectronEfficiencyCorrection/efficiencySF.offline.RecoTrk.2015.13TeV.rel20p0.25ns.v04.root",
                                    "m_corrFileNamePID"       : "$ROOTCOREBIN/data/ElectronEfficiencyCorrection/efficiencySF.offline.LooseAndBLayerLLH_d0z0.2015.13TeV.rel20p0.25ns.v04.root",
                                    #"m_corrFileNamePID"       : "$ROOTCOREBIN/data/ElectronEfficiencyCorrection/efficiencySF.offline.LooseAndBLayerLLH.2015.13TeV.rel20p0.25ns.v04.root",
                                    "m_corrFileNameIso"       : "$ROOTCOREBIN/data/ElectronEfficiencyCorrection/efficiencySF.Isolation.LooseAndBLayerLLH_d0z0_v8_isolLoose.2015.13TeV.rel20p0.25ns.v04.root",
                                    "m_WorkingPointIDTrig"    : "LHLooseAndBLayer",
				    "m_corrFileNameTrig"      : "$ROOTCOREBIN/data/ElectronEfficiencyCorrection/efficiencySF.e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose.LooseAndBLayerLLH_d0z0_v8.2015.13TeV.rel20p0.25ns.v04.root",
                                    "m_corrFileNameTrigMCEff" : "$ROOTCOREBIN/data/ElectronEfficiencyCorrection/efficiency.e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose.LooseAndBLayerLLH_d0z0_v8.2015.13TeV.rel20p0.25ns.v04.root",
                                   }

ElectronEfficiencyCorrectorTightDict = { "m_name"                  : "electronEfficiencyCorrectorTight",
		                         "m_debug"		   : False,
                                         "m_inContainerName"	   : "Electrons_OR",
                                         "m_inputAlgoSystNames"    : "ElectronSelector_Syst",
                                         "m_systNameReco"          : "",
                                         "m_systNamePID"           : "",
                                         "m_systNameTrig"	   : "",
                                         "m_systNameTrigMCEff"     : "",
                                         "m_outputSystNamesReco"   : "ElectronEfficiencyCorrector_RecoSyst",
                                         "m_outputSystNamesPID"    : "ElectronEfficiencyCorrector_PIDSyst",
                                         "m_outputSystNamesIso"    : "ElectronEfficiencyCorrector_IsoSyst",
                                         "m_outputSystNamesTrig"   : "ElectronEfficiencyCorrector_TrigSyst",
                                         "m_outputSystNamesTrigMCEff"   : "ElectronEfficiencyCorrector_TrigMCEffSyst",
                                         "m_corrFileNameReco"      : "$ROOTCOREBIN/data/ElectronEfficiencyCorrection/efficiencySF.offline.RecoTrk.2015.13TeV.rel20p0.25ns.v04.root",
                                         "m_corrFileNamePID"       : "$ROOTCOREBIN/data/ElectronEfficiencyCorrection/efficiencySF.offline.TightLLH_d0z0.2015.13TeV.rel20p0.25ns.v04.root",
                                         "m_corrFileNameIso"       : "$ROOTCOREBIN/data/ElectronEfficiencyCorrection/efficiencySF.Isolation.TightLLH_d0z0_v8_isolFixedCutTight.2015.13TeV.rel20p0.25ns.v04.root",
                                         "m_WorkingPointIDTrig"    : "LHTight",
                                         "m_corrFileNameTrig"      : "$ROOTCOREBIN/data/ElectronEfficiencyCorrection/efficiencySF.e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose.TightLLH_d0z0_v8.2015.13TeV.rel20p0.25ns.v04.root",
                                         "m_corrFileNameTrigMCEff" : "$ROOTCOREBIN/data/ElectronEfficiencyCorrection/efficiency.e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose.TightLLH_d0z0_v8.2015.13TeV.rel20p0.25ns.v04.root",
                                       }

HTopMultilepEventSelectorDict = { "m_name"                   : "eventSelect_skim",
		                  "m_debug"	             : False,
		                  "m_useCutFlow"             : True,
                		  "m_inContainerName_el"     : "Electrons_OR",
                		  "m_inContainerName_mu"     : "Muons_OR",
                		  "m_inContainerName_jets"   : "AntiKt4EMTopoJets_OR",
                		  "m_outContainerName_lep"   : "Leptons_OR",
		                  "m_doMinObjCut"            : True,
		                  "m_doMaxObjCut"            : False,
   				  "m_n_leptons_min"          : 0,
				  "m_BTag_WP"                : "FixedCutBEff_77",
                                  "m_n_jets_min"             : 0,
   				  "m_n_bjets_min"            : 0,
                                }

TruthMatchAlgoDict = { "m_name"                           : "truthMatching",
		       "m_debug"		          : False,
                       "m_inContainerName_Electrons"	  : "Electrons_OR",
                       "m_inContainerName_Muons"	  : "Muons_OR",
                       "m_inContainerName_Leptons"        : "Leptons_OR",
		       "m_doMuonTrackMatching"  	  : True,
		       "m_doMuonTruthPartMatching"  	  : False,
                     }

HTopMultilepAnalysisDict = { "m_name"                      : "multilep_analysis",
		             "m_debug"  		   : False,
		             "m_useCutFlow"		   : True,
                	     "m_inContainerName_Electrons" : "Electrons_OR",
                	     "m_inContainerName_Muons"	   : "Muons_OR",
                	     "m_inContainerName_Leptons"   : "Leptons_OR",
                	     "m_inContainerName_Jets"	   : "AntiKt4EMTopoJets_OR",
                	     "m_inContainerName_Taus"	   : "Taus_OR",
			     "m_TightElectronPID_WP"	   : "LHTight",
			     "m_TightElectronIso_WP"	   : "isIsolated_FixedCutTight",
   			     "m_TightMuonD0sig_cut"	   : 3.0,
			     "m_TightMuonIso_WP"	   : "isIsolated_FixedCutTightTrackOnly",
                             "m_ConfigPathTightTaus"       : "$ROOTCOREBIN/data/HTopMultilepAnalysis/Taus/recommended_selection_mc15_final_sel.conf",
		             "m_useMCForTagAndProbe"       : False,
                           }

HTopMultilepTreeAlgoDict = { "m_name"                  : "physics",
		             "m_debug"  	       : False,
                   	     "m_muContainerName"       : "Muons_OR",
                   	     "m_elContainerName"       : "Electrons_OR",
                   	     "m_jetContainerName"      : "AntiKt4EMTopoJets_OR",
                   	     "m_tauContainerName"      : "Taus_OR",
                   	     "m_lepContainerName"      : "Leptons_OR" ,
                   	     "m_METContainerName"      : "RefFinal_HTopMultilep",
		             "m_outHistDir"	       : True,
                   	     "m_evtDetailStr"	       : "pileup",
                   	     "m_trigDetailStr"         : "basic passTriggers",
                   	     "m_muDetailStr"	       : "kinematic trigger isolation quality trackparams effSF",
                   	     "m_elDetailStr"	       : "kinematic trigger isolation PID trackparams effSF",
                   	     "m_tauDetailStr"	       : "kinematic",
                   	     "m_jetDetailStr"	       : "kinematic energy flavorTag sfFTagFix77 truth trackPV",
                   	     "m_METDetailStr"	       : "all",
                           }
