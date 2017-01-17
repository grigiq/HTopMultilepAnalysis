#!/usr/bin/env python

""" MakePlots_HTopMultilep.py: plotting script for the HTopMultilep Run 2 analysis """

__author__     = "Marco Milesi, Francesco Nuti"
__email__      = "marco.milesi@cern.ch, francesco.nuti@cern.ch"
__maintainer__ = "Marco Milesi"

import os, sys, math, array

sys.path.append(os.path.abspath(os.path.curdir))

# -------------------------------
# Parser for command line options
# -------------------------------

import argparse

parser = argparse.ArgumentParser(description='Plotting script for the HTopMultilep Run 2 analysis')

channels     = ["TwoLepSR(,NO_CORR)","ThreeLepSR","FourLepSR","MMRates(,DATA,CLOSURE,NO_CORR,TP,LH,TRUTH_TP,SUSY_TP,TRUTH_ON_PROBE,DATAMC,TRIGMATCH_EFF,NOT_TRIGMATCH_EFF)",
                "TwoLepLowNJetCR(,NO_CORR)", "ThreeLepLowNJetCR",
                "WZonCR", "WZoffCR", "WZHFonCR", "WZHFoffCR",
                "ttWCR", "ttZCR","ZSSpeakCR", "DataMC", "MMClosureTest(,NO_CORR,HIGHNJ,LOWNJ,ALLNJ,LOWPT)",
                "CutFlowChallenge(,MM,2LepSS,2LepSS1Tau,3Lep)","MMSidebands(,NO_CORR,CLOSURE,HIGHNJ,LOWNJ,ALLNJ)"]

categories   = ["ALL","ee","mm","OF"]

fakemethods  = ["MC","MM","FF","THETA"]

flavours     = ["TEST","ICHEP_2016","OF","SF","INCLUSIVE"]

efficiencies = ["ALL_EFF","REAL_EFF","FAKE_EFF"]

luminosities = { "Moriond 2016 GRL":3.209,            # March 2016
                 "ICHEP 2015+2016 DS":13.20768,       # August 2016
                 "POST-ICHEP 2015+2016 DS":22.07036,  # October 2016
                 "FULL 2015+2016 DS":36.4702          # December 2016 (full 2015+2016 DS)
               }

triggers     = ["TEST","SLT","DLT","SLT_OR_DLT"]

parser.add_argument('inputpath', metavar='inputpath',type=str,
                   help='Path to the directory containing input files')
parser.add_argument('--samplesCSV', dest='samplesCSV',action='store',const='Files/samples_HTopMultilep_Priority1.csv',default='Files/samples_HTopMultilep_Priority1.csv',type=str,nargs='?',
                    help='Path to the .csv file containing the processes of interest with their cross sections and other metadata. If this option is unspecified, or it is not followed by any command-line argument, default will be \'Files/samples_HTopMultilep_Priority1.csv\'')
parser.add_argument('--lumi', dest='lumi', action='store', type=float, default=luminosities["FULL 2015+2016 DS"],choices=list(luminosities.items()),
                    help="The luminosity of the dataset. Choose a numerical value among the ones listed above. If this option is not specified, default will be (\'{0}\', {1})".format("FULL 2015+2016 DS",luminosities["FULL 2015+2016 DS"] ) )
parser.add_argument("--trigger", dest="trigger", action="store", default=triggers[0], type=str, nargs=1, choices=triggers, # nargs=1 ensures argument will be stored in a list
                    help="The trigger strategy to be used. If this option is not specified, default will be \'{0}\'".format(triggers[0]))
parser.add_argument('--channel', dest='channel', action='store', default=channels[0], type=str, nargs='+',
                    help='The channel chosen. Full list of available options:\n{0}. Can pass multiple space-separated arguments to this command-line option (picking amonge the above list). If this option is not specified, default will be \'{1}\''.format(channels,channels[0]))
parser.add_argument('--category', dest='category', action='store', default=categories[0], type=str, nargs='+', choices=categories,
                    help='The category chosen. Can pass multiple space-separated arguments to this command-line option (picking amonge the above list). Use w/ option --channel={{TwoLepSR,TwoLepLowNJetCR,MMClosureTest,MMSidebands}}. If this option is not specified, default will be \'{0}\''.format(categories[0]))
parser.add_argument('--efficiency', dest='efficiency', action='store', default=efficiencies[0], type=str, nargs='+', choices=efficiencies,
                    help='The efficiency type to be measured. Can pass multiple space-separated arguments to this command-line option (picking amonge the above list). Use w/ option --channel=MMRates. If this option is not specified, default will be \'{0}\''.format(efficiencies[0]))
parser.add_argument('--ratesMC', dest='ratesMC', action='store_true', default=False,
                    help='Distributions to get rates/efficiencies from pure simulation. Use w/ option --channel=MMRates')
parser.add_argument('--useMCQMisID', dest='useMCQMisID', action='store_true', default=False,
                    help='Use Monte-Carlo based estimate of QMisID')
parser.add_argument('--outdirname', dest='outdirname', action='store', default='', type=str,
                    help='Specify a name to append to the output directory')
parser.add_argument('--fakeMethod', dest='fakeMethod', action='store', default=None, type=str, choices=fakemethods,
                    help='The fake estimation method chosen. If this option is not specified, default will be None (i.e.,no fakes need to be estimated)')
parser.add_argument('--lepFlavComp', dest='lepFlavComp', action='store', default=flavours[0], type=str, choices=flavours,
                    help='Flavour composition in the CRs used for r/f efficiency measurement. Use w/ option --channel=MMRates. If this option is not specified, default will be \'{0}\''.format(flavours[0]))
parser.add_argument('--doShowRatio', action='store_true', dest='doShowRatio', default=False,
                    help='Show ratio plot with data/expected')
parser.add_argument('--mergeOverflow', dest='mergeOverflow', action='store_true', default=False,
                    help='Merge the overflow bin to the last visible bin. Default is False.')
parser.add_argument('--doLogScaleX', dest='doLogScaleX', action='store_true', default=False,
                    help='Use log scale on the X axis')
parser.add_argument('--doLogScaleY', dest='doLogScaleY', action='store_true', default=False,
                    help='Use log scale on the Y axis')
parser.add_argument('--doSyst', dest='doSyst', action='store_true', default=False,
                    help='Run systematics')
parser.add_argument('--noSignal', action='store_true', dest='noSignal',
                    help='Exclude signal')
parser.add_argument('--noWeights', action='store_true', dest='noWeights', default=False,
                    help='Do not apply any weight, correction. Also the Xsec weight and mcEvtWeight are reset to 1. This is used e.g. to get raw cutflow.')
parser.add_argument('--makeStandardPlots', action='store_true', dest='makeStandardPlots', default=False,
                    help='Produce a set of standard plots. Default is False.')
parser.add_argument('--doQMisIDRate', dest='doQMisIDRate', action='store_true',
                    help='Measure charge flip rate in MC (to be used with --channel=MMRates CLOSURE)')
parser.add_argument('--doUnblinding', dest='doUnblinding', action='store_true', default=False,
                    help='Unblind data in SRs')
parser.add_argument('--printEventYields', dest='printEventYields', action='store_true', default=False,
                    help='Prints out event yields in tabular form (NB: can be slow)')
parser.add_argument('--useMoriondTruth', dest='useMoriondTruth', action='store_true', default=False,
                    help='Use 2016 Moriond-style truth matching (aka, just rely on type/origin info)')
parser.add_argument('--debug', dest='debug', action='store_true', default=False,
                    help='Run in debug mode')

args = parser.parse_args()

# -----------------
# Some ROOT imports
# -----------------

from ROOT import gROOT, gStyle, gPad
from ROOT import TH1I, TH1D, TH2D, TH2F, TH2I, TMath, TFile, TAttFill, TColor, Double
from ROOT import kBlack, kWhite, kGray, kBlue, kRed, kYellow, kAzure, kTeal, kSpring, kOrange, kGreen, kCyan, kViolet, kMagenta, kPink
from ROOT import TCanvas, TPaveText, TGraph, TGraph2D, TGraphErrors

def appended( inlist, *elem ):
    """
    Append an aribitrary number of elements to an input list, and return the list.
    NB: the input list will be effectively extended.
    """

    inlist.extend( list(elem) )

    return inlist

def calculate_Z( s, b, err_s, err_b, method="SoverSqrtB" ):

    if method == "SoverSqrtB":
        Z = s / math.sqrt(b)
        dZ_ds = 1.0 / math.sqrt(b)
        dZ_db = -s / ( 2.0 * pow(b,3.0/2.0) )

    if method == "Cowan":
        Z = math.sqrt( 2.0 * ( ( s + b ) * math.log( 1.0 + s/b ) - s ) )
        dZ_ds = ( -1.0 + ( b + s )/( b * ( 1.0 + s/b ) ) + math.log( 1 + s/b ) ) / ( math.sqrt(2.0) * math.sqrt( -s + ( b + s ) * math.log( 1.0 + s/b ) ) )
        dZ_db = ( -( s * ( b + s ) )/( b*b * ( 1.0 + s/b ) ) + math.log( 1.0 + s/b ) ) / ( math.sqrt(2.0) * math.sqrt( -s + ( b + s ) * math.log( 1.0 + s/b ) ) )

    err_Z = math.sqrt( ( dZ_ds * dZ_ds ) * ( err_s * err_s ) + ( dZ_db * dZ_db ) *( err_b * err_b ) )

    return (Z, err_Z)


def plot_significance( Z_dict, dim ):

    gROOT.SetBatch(True)

    for key, value in Z_dict.iteritems():

        print("pT-SORTED:\nkey: {0}".format(key) + ",\n(lep_Pt_0,lep_Pt_1) cut: [" + ",".join( "({0},{1})".format(val[0],val[1]) for val in sorted(value) )  + "],\nZ: [" + ",".join( "{0:.3f} +- {1:.3f}".format(val[2],val[3]) for val in sorted(value) ) + "]\n")

        if dim == "1D":

            bins  = [ val[1] for val in sorted(value) ]
            Z     = [ val[2] for val in sorted(value) ]
            Z_err = [ val[3] for val in sorted(value) ]

            import ROOT

            graph_significance = TGraphErrors( len(value), array.array("f", bins ), array.array("f", Z ), ROOT.nullptr,  array.array("f", Z_err ) )
            graph_significance.SetName(key)
            graph_significance.GetXaxis().SetTitle("p_{T}^{2nd lead lep} [GeV]")
            graph_significance.GetYaxis().SetTitle("Z significance")
            graph_significance.SetLineWidth(2)
            graph_significance.SetMarkerStyle(20)
            graph_significance.SetMarkerSize(1.3)
            graph_significance.SetMarkerColor(2)

            c = TCanvas("c_Z_Significance_lep_Pt_1_"+ key,"Z")

            graph_significance.Draw("ACP")

            max_Z = max( value, key=(lambda val : val[2]) )
            print("Z max: {0:.3f} +- {1:.3f} ({2}{3})\n".format(max_Z[2], max_Z[3], max_Z[0], max_Z[1]))

            text = TPaveText(0.22,0.80,0.50,0.87,"blNDC")
            text.AddText("Z_{{max}}: {0:.2f} #pm {1:.2f} ({2},{3})".format(max_Z[2], max_Z[3], max_Z[0], max_Z[1]))
            text.Paint("NDC")
            text.Draw()

            c.SaveAs(os.path.abspath(os.path.curdir) + "/" + basedirname + "Z_Significance_lep_Pt_1_"+key+".png")

        elif dim == "2D":

            graph_significance = TGraph2D()

            for idx, val in enumerate(sorted(value)):
                graph_significance.SetPoint(idx, val[0], val[1], val[2])

            graph_significance.SetName(key)

            set_fancy_2D_style()

            c = TCanvas("c_Z_Significance_lep_Pt_0_lep_Pt_1_"+ key,"Z")

            gPad.SetRightMargin(0.2)

	    graph_significance.Draw("COLZ")

            max_Z = max( value, key=(lambda val : val[2]) )

            print("Z max: {0:.3f} +- {1:.3f} ({2},{3})".format(max_Z[2], max_Z[3], max_Z[0], max_Z[1]))

            text = TPaveText(0.22,0.80,0.50,0.87,"blNDC")
            text.AddText("Z_{{max}}: {0:.2f} #pm {1:.2f} ({2},{3})".format(max_Z[2], max_Z[3], max_Z[0], max_Z[1]))
            text.SetFillColor(0)
	    text.Paint("NDC")
            text.Draw()

	    gPad.Update()
            graph_significance.GetXaxis().SetTitle("p_{T}^{lead lep} [GeV]")
            graph_significance.GetYaxis().SetTitle("p_{T}^{2nd lead lep} [GeV]")

            c.SaveAs(os.path.abspath(os.path.curdir) + "/" + basedirname + "Z_Significance_lep_Pt_0_lep_Pt_1_"+key+".png")


# ---------------------------------------------------------------------
# Importing all the tools and the definitions used to produce the plots
# ---------------------------------------------------------------------

from Plotter.BackgroundTools import loadSamples, Category, Background, Process, VariableDB, Variable, Cut, Systematics, Category, set_fancy_2D_style

# ---------------------------------------------------------------------------
# Importing the classes for the different processes.
# They contains many info on the normalization and treatment of the processes
# ---------------------------------------------------------------------------

from Plotter.Backgrounds_HTopMultilep import MyCategory, TTHBackgrounds

if __name__ == "__main__":

    doTwoLepSR              = bool( "TwoLepSR" in args.channel )
    doThreeLepSR            = bool( "ThreeLepSR" in args.channel )
    doFourLepSR             = bool( "FourLepSR" in args.channel )
    doMMRates               = bool( "MMRates" in args.channel )
    doTwoLepLowNJetCR       = bool( "TwoLepLowNJetCR" in args.channel )
    doThreeLepLowNJetCR     = bool( "ThreeLepLowNJetCR" in args.channel )
    doWZonCR                = bool( "WZonCR" in args.channel )
    doWZoffCR               = bool( "WZoffCR" in args.channel )
    doWZHFonCR              = bool( "WZHFonCR" in args.channel )
    doWZHFoffCR             = bool( "WZHFoffCR" in args.channel )
    dottWCR                 = bool( "ttWCR" in args.channel )
    dottZCR                 = bool( "ttZCR" in args.channel )
    doZSSpeakCR             = bool( "ZSSpeakCR" in args.channel )
    doDataMCCR              = bool( "DataMC" in args.channel )
    doMMClosureTest         = bool( "MMClosureTest" in args.channel )
    doCFChallenge           = bool( "CutFlowChallenge" in args.channel )
    doMMSidebands           = bool( "MMSidebands" in args.channel )

    print( "input directory: {0}\n".format(args.inputpath) )
    print( "channel = {0}\n".format(args.channel) )

    # ------------------------------------------------------------------------------
    # Make sure correct trigger selection is used for measuring the r/f efficiencies
    # ------------------------------------------------------------------------------

    if doMMRates and args.trigger[0] not in ["SLT","DLT"]:
        sys.exit("ERROR: the chosen trigger selection: {0}\nis not allowed for r/f efficiency measurement. Please choose one of {1}".format(args.trigger[0],["SLT","DLT"]))

    # -----------------------------------------
    # A comprehensive flag for all possible SRs
    # -----------------------------------------

    doSR = (doTwoLepSR or doThreeLepSR or doFourLepSR)

    # -----------------------------------------
    # A comprehensive flag for the low-Njet CR
    # -----------------------------------------

    doLowNJetCR = (doTwoLepLowNJetCR or doThreeLepLowNJetCR)

    # ------------------------------------------
    # A comprehensive flag for all the other CRs
    # ------------------------------------------

    doOtherCR = (doWZonCR or doWZoffCR or doWZHFonCR or doWZHFoffCR or dottWCR or dottZCR or doZSSpeakCR or doMMRates or doDataMCCR or doMMClosureTest or doCFChallenge or doMMSidebands )

    # -------------------------------------------------------------
    # Make standard plots in SR and VR unless differently specified
    # -------------------------------------------------------------

    makeStandardPlots = False if ( not args.makeStandardPlots ) else ( doSR or doLowNJetCR or doOtherCR )

    # ----------------------------
    # Check fake estimation method
    # ----------------------------

    doMM    = bool( args.fakeMethod == "MM" )
    doFF    = bool( args.fakeMethod == "FF" )
    doTHETA = bool( args.fakeMethod == "THETA" )
    doMC    = bool( args.fakeMethod == "MC" )

    # ----------------------------------------------------
    # When in debug mode, print out all the input commands
    # ----------------------------------------------------

    if ( args.debug ):
        print ("Executing MakePlots_HTopMultilep.py w/ following command-line options:\n")
        print args
        print ("")

    # --------------------------
    # Retrieve the input samples
    # --------------------------

    inputs = loadSamples(
        # path of the data to be processed
        inputdir    = args.inputpath,
        samplescsv  = args.samplesCSV,
        nomtree     = "physics",
        # name of the trees that contains values for shifted systematics
        systrees =  [
            ##'METSys',
            #'ElEnResSys',
            #'ElES_LowPt',
            #'ElES_Zee',
            #'ElES_R12',
            #'ElES_PS',
            ##'EESSys',
            #'MuSys',
            ##'METResSys',
            ##'METScaleSys',
            #'JES_Total',
            #'JER',
            ],
        )

    # ------------------------------------------------------
    # Here you include all names of variables to be plotted,
    # with min, max, number of bins and ntuple name.
    # ------------------------------------------------------

    vardb = VariableDB()

    # -----------------------------------------------------
    # The list of event-level TCuts
    #
    # WARNING:
    # To avoid unexpected behaviour,
    # ALWAYS enclose the cut string in '()'!!!
    #
    # -----------------------------------------------------

    # ---------------------
    # General cuts
    # ---------------------

    vardb.registerCut( Cut('DummyCut',    '( 1 )') )

    #vardb.registerCut( Cut('BlindingCut', '( isBlinded == 0 )') ) # <--- use this cut to get blinded results!
    vardb.registerCut( Cut('BlindingCut', '( 1 )') )
    if args.doUnblinding:
        vardb.getCut('BlindingCut').cutstr = '( 1 )'

    vardb.registerCut( Cut('IsMC', '( mc_channel_number != 0 )') )

    # -------
    # Trigger
    # -------

    e_SLT = "( ( RunYear == 2015 && ( HLT_e24_lhmedium_L1EM20VH || HLT_e60_lhmedium || HLT_e120_lhloose ) ) || ( RunYear == 2016 && ( HLT_e26_lhtight_nod0_ivarloose || HLT_e60_lhmedium_nod0 || HLT_e140_lhloose_nod0 ) ) )"
    m_SLT = "( ( RunYear == 2015 && ( HLT_mu20_iloose_L1MU15 || HLT_mu50 ) ) || ( RunYear == 2016 && ( HLT_mu26_ivarmedium || HLT_mu50 ) ) )"

    ee_DLT = "( ( RunYear == 2015 && HLT_2e12_lhloose_L12EM10VH ) || ( RunYear == 2016 && HLT_2e17_lhvloose_nod0 ) )"
    mm_DLT = "( ( RunYear == 2015 && HLT_mu18_mu8noL1 ) || ( RunYear == 2016 && HLT_mu22_mu8noL1 ) )"
    of_DLT = "( ( RunYear == 2015 && HLT_e17_lhloose_mu14 ) || ( RunYear == 2016 && HLT_e17_lhloose_nod0_mu14 ) )"

    SLT_matching = '( lep_isTrigMatch_0 == 1 || lep_isTrigMatch_1 == 1 )'
    DLT_matching = '( lep_isTrigMatchDLT_0 == 1 && lep_isTrigMatchDLT_1 == 1 )'

    ee_DLT_OR_SLT = "( ( RunYear == 2015 && ( ( ( HLT_e24_lhmedium_L1EM20VH || HLT_e60_lhmedium || HLT_e120_lhloose ) && {0} ) || ( HLT_2e12_lhloose_L12EM10VH && {1} ) ) ) || ( RunYear == 2016 && ( ( ( HLT_e26_lhtight_nod0_ivarloose || HLT_e60_lhmedium_nod0 || HLT_e140_lhloose_nod0 ) && {0} ) || ( HLT_2e17_lhvloose_nod0 && {1} ) ) ) )".format( SLT_matching, DLT_matching )
    mm_DLT_OR_SLT = "( ( RunYear == 2015 && ( ( ( HLT_mu20_iloose_L1MU15 || HLT_mu50 ) && {0} ) || ( HLT_mu18_mu8noL1 && {1} ) ) ) || ( RunYear == 2016 && ( ( ( HLT_mu26_ivarmedium || HLT_mu50 ) && {0} ) || ( HLT_mu22_mu8noL1 && {1} ) ) ) )".format( SLT_matching, DLT_matching )
    #of_DLT_OR_SLT = "( ( RunYear == 2015 && ( ( ( HLT_e24_lhmedium_L1EM20VH || HLT_e60_lhmedium || HLT_e120_lhloose || HLT_mu20_iloose_L1MU15 || HLT_mu50 ) && {0} ) || ( HLT_e17_lhloose_mu14 && {1} ) ) ) || ( RunYear == 2016 && ( ( ( HLT_e26_lhtight_nod0_ivarloose || HLT_e60_lhmedium_nod0 || HLT_e140_lhloose_nod0 || HLT_mu26_ivarmedium || HLT_mu50 ) && {0} ) || ( HLT_e17_lhloose_nod0_mu14 && {1} ) ) ) )".format( SLT_matching, DLT_matching ) # Using ~symmetric OF DLT only
    of_DLT_OR_SLT = "( ( RunYear == 2015 && ( ( ( HLT_e24_lhmedium_L1EM20VH || HLT_e60_lhmedium || HLT_e120_lhloose || HLT_mu20_iloose_L1MU15 || HLT_mu50 ) && {0} ) || ( HLT_e24_medium_L1EM20VHI_mu8noL1 || HLT_e7_medium_mu24 && {1} ) ) ) || ( RunYear == 2016 && ( ( ( HLT_e26_lhtight_nod0_ivarloose || HLT_e60_lhmedium_nod0 || HLT_e140_lhloose_nod0 || HLT_mu26_ivarmedium || HLT_mu50 ) && {0} ) || ( HLT_e26_lhmedium_nod0_L1EM22VHI_mu8noL1 || HLT_e7_lhmedium_nod0_mu24 && {1} ) ) ) )".format( SLT_matching, DLT_matching ) # Using asymmetric OF DLT only

    if "SLT" in args.trigger: # use SLT for all categories

        vardb.registerCut( Cut("TrigDec", "( " + e_SLT + " || " + m_SLT + " )" ) )

    elif "DLT" in args.trigger: # use DLT for all categories

        vardb.registerCut( Cut("TrigDec", "( " + "( dilep_type == 1 && " + mm_DLT + " )" + " || " + "( dilep_type == 2 && " + of_DLT + " )" + " || " + "( dilep_type == 3 && " + ee_DLT + " )" + " )" ) )

    elif "SLT_OR_DLT" in args.trigger: # use ( DLT || SLT ) for all categories (includes trigger matching already!)

        vardb.registerCut( Cut("TrigDec", "( " + "( dilep_type == 1 && " + mm_DLT_OR_SLT + " )" + " || " + "( dilep_type == 2 && " + of_DLT_OR_SLT + " )" + " || " + "( dilep_type == 3 && " + ee_DLT_OR_SLT + " )" + " )" ) )

    elif "TEST" in args.trigger: # use a trigger selection for each category

        vardb.registerCut( Cut("TrigDec", "( " + "( dilep_type == 1 && " + mm_DLT + " )" + " || " + "( dilep_type == 2 && " + of_DLT_OR_SLT + " )" + " || " + "( dilep_type == 3 && " + ee_DLT + " )" + " )" ) ) # DLT for mm, SLT for ee, ( DLT || SLT ) for OF
        #vardb.registerCut( Cut("TrigDec", "( " + "( dilep_type == 1 && " + mm_DLT + " )" + " || " + "( dilep_type == 2 && ( " + e_SLT + " || " + m_SLT + " ) )" + " || " + "( dilep_type == 3 && " + ee_DLT + " )" + " )" ) ) # use DLT for ee, mm, SLT for OF

    vardb.registerCut( Cut('LargeNBJet',      '( nJets_OR_T_MV2c10_70 > 1 )') )
    vardb.registerCut( Cut('VetoLargeNBJet',  '( nJets_OR_T_MV2c10_70 < 4 )') )
    vardb.registerCut( Cut('BJetVeto',        '( nJets_OR_T_MV2c10_70 == 0 )') )
    vardb.registerCut( Cut('OneBJet',         '( nJets_OR_T_MV2c10_70 == 1 )') )
    vardb.registerCut( Cut('TauVeto',         '( nTaus_OR_Pt25 == 0 )') )
    vardb.registerCut( Cut('OneTau',          '( nTaus_OR_Pt25 == 1 )') )

    # ---------------------
    # 2Lep SS + 0 tau cuts
    # ---------------------

    # ----------------
    # Trigger matching
    # ----------------

    if "SLT" in args.trigger:

        vardb.registerCut( Cut('2Lep_TrigMatch', '( lep_isTrigMatch_0 == 1 || lep_isTrigMatch_1 == 1 )') )

    elif "DLT" in args.trigger:

        vardb.registerCut( Cut('2Lep_TrigMatch', '( lep_isTrigMatchDLT_0 == 1 && lep_isTrigMatchDLT_1 == 1 )') ) # For DLT, require BOTH leptons to be matched

    elif "SLT_OR_DLT" in args.trigger:

        vardb.registerCut( Cut('2Lep_TrigMatch', '( 1 )') ) # trigger matching already implemented in trigger selection cut

    elif "TEST" in args.trigger:

        vardb.registerCut( Cut('2Lep_TrigMatch', '( ( dilep_type == 1 && ( lep_isTrigMatchDLT_0 == 1 && lep_isTrigMatchDLT_1 == 1 ) ) || ( dilep_type == 2 ) || ( dilep_type == 3 && ( lep_isTrigMatch_0 == 1 || lep_isTrigMatch_1 == 1 ) ) )') ) # use DLT matching for mm, SLT matching for ee, a mix for OF (already implemented above)
        #vardb.getCut('2Lep_TrigMatch').cutstr = '( ( ( dilep_type == 1 || dilep_type == 3 ) && ( lep_isTrigMatchDLT_0 == 1 && lep_isTrigMatchDLT_1 == 1 ) ) || ( dilep_type == 2 && ( lep_isTrigMatch_0 == 1 || lep_isTrigMatch_1 == 1 ) ) )' # use DLT matching for ee, mm, SLT matching for OF

    # For LH fit, use this cuts in order to introduce the trigger bias from SLT
    # This is safe as we will use the likelihood to fit fake muon efficiency in mm events
    # The following will work also if doing LH fit for fake muons in a (mm + OF) CR

    vardb.registerCut( Cut('2Lep_BothTrigMatchSLT',       '( ( dilep_type == 1 && ( lep_isTrigMatch_0 == 1 && lep_isTrigMatch_1 == 1 ) ) || ( dilep_type == 2 && ( ( TMath::Abs( lep_ID_0 ) == 13 && lep_isTrigMatch_0 == 1 ) || ( TMath::Abs( lep_ID_1 ) == 13 && lep_isTrigMatch_1 == 1 ) ) ) )') )
    vardb.registerCut( Cut('2Lep_BothAntiTrigMatchSLT',   '( ( dilep_type == 1 && ( lep_isTrigMatch_0 == 0 && lep_isTrigMatch_1 == 0 ) ) || ( dilep_type == 2 && ( ( TMath::Abs( lep_ID_0 ) == 13 && lep_isTrigMatch_0 == 0 ) || ( TMath::Abs( lep_ID_1 ) == 13 && lep_isTrigMatch_1 == 0 ) ) ) )') )

    vardb.registerCut( Cut('2Lep_NBJet',                  '( nJets_OR_T_MV2c10_70 > 0 )') )
    vardb.registerCut( Cut('2Lep_NBJet_SR',		  '( nJets_OR_T_MV2c10_70 > 0 )') )
    vardb.registerCut( Cut('2Lep_MinNJet',		  '( nJets_OR_T > 1 )') )
    vardb.registerCut( Cut('2Lep_NJet_SR',		  '( nJets_OR_T > 4 )') )
    vardb.registerCut( Cut('2Lep_NJet_CR',		  '( nJets_OR_T > 1 && nJets_OR_T <= 4 )') )
    vardb.registerCut( Cut('2Lep_NJet_CR_SStt', 	  '( nJets_OR_T < 4 )') )
    vardb.registerCut( Cut('2Lep_SS',			  '( lep_ID_0 * lep_ID_1 > 0 )') )
    vardb.registerCut( Cut('2Lep_OS',			  '( !( lep_ID_0 * lep_ID_1 > 0 ) )') )
    vardb.registerCut( Cut('2Lep_NLep', 		  '( dilep_type > 0 )') )
    vardb.registerCut( Cut('2Lep_pT',			  '( lep_Pt_0 > 25e3 && lep_Pt_1 > 25e3 )') )
    vardb.registerCut( Cut('2Lep_pT_MMRates',		  '( lep_Pt_0 > 10e3 && lep_Pt_1 > 10e3 )') )
    vardb.registerCut( Cut('2Lep_pT_Relaxed',		  '( lep_Pt_0 > 25e3 && lep_Pt_1 > 10e3 )') )
    vardb.registerCut( Cut('2Lep_SF_Event',		  '( dilep_type == 1 || dilep_type == 3 )') )
    vardb.registerCut( Cut('2Lep_MuMu_Event',		  '( dilep_type == 1 )') )
    vardb.registerCut( Cut('2Lep_ElEl_Event',		  '( dilep_type == 3 )') )
    vardb.registerCut( Cut('2Lep_OF_Event',		  '( dilep_type == 2 )') )
    vardb.registerCut( Cut('2Lep_MuEl_Event',		  '( dilep_type == 2 && TMath::Abs( lep_ID_0 ) == 13  )') )
    vardb.registerCut( Cut('2Lep_ElMu_Event',		  '( dilep_type == 2 && TMath::Abs( lep_ID_0 ) == 11  )') )
    vardb.registerCut( Cut('2Lep_Zsidescut',              '( ( dilep_type != 3 ) || ( TMath::Abs( Mll01 - 91.2e3 ) > 7.5e3 ) )' ) )  # Use this to require the 2 SF electrons to be outside Z peak
    vardb.registerCut( Cut('2Lep_Zpeakcut',               '( ( dilep_type == 2 ) || ( TMath::Abs( Mll01 - 91.2e3 ) < 30e3  ) )' ) )  # Use this to require the 2 SF leptons to be around Z peak
    vardb.registerCut( Cut('2Lep_Zmincut',                '( ( dilep_type == 2 ) || ( Mll01  > 20e3 ) )' ) )   # Remove J/Psi, Upsilon peak in SF events

    gROOT.LoadMacro("$ROOTCOREBIN/user_scripts/HTopMultilepAnalysis/ROOT_TTreeFormulas/largeEtaEvent.cxx+")
    from ROOT import largeEtaEvent

    vardb.registerCut( Cut('2Lep_ElEtaCut',               '( largeEtaEvent( dilep_type,lep_ID_0,lep_ID_1,lep_EtaBE2_0,lep_EtaBE2_1 ) == 0 )') )

    # ------------------
    # Tag and probe cuts
    # ------------------

    if doMMRates:

        if "SLT" in args.trigger:

            vardb.registerCut( Cut('2Lep_LepTagTightTrigMatched',   '( lep_Tag_SLT_isTightSelected == 1 && lep_Tag_SLT_isTrigMatch == 1 )') )
            vardb.registerCut( Cut('2Lep_LepTagTrigMatched',        '( lep_Tag_SLT_isTrigMatch == 1 )') )
            vardb.registerCut( Cut('2Lep_LepProbeTrigMatched',      '( lep_Probe_SLT_isTrigMatch == 1 )') )
            vardb.registerCut( Cut('2Lep_LepProbeAntiTrigMatched',  '( lep_Probe_SLT_isTrigMatch == 0 )') )
            vardb.registerCut( Cut('2Lep_ElTag',                    '( TMath::Abs( lep_Tag_SLT_ID ) == 11 )') )
            vardb.registerCut( Cut('2Lep_MuTag',                    '( TMath::Abs( lep_Tag_SLT_ID ) == 13 )') )
            vardb.registerCut( Cut('2Lep_ElProbe',                  '( TMath::Abs( lep_Probe_SLT_ID ) == 11 )') )
            vardb.registerCut( Cut('2Lep_MuProbe',                  '( TMath::Abs( lep_Probe_SLT_ID ) == 13 )') )
            vardb.registerCut( Cut('2Lep_ProbeTight',               '( lep_Probe_SLT_isTightSelected == 1 )') )
            vardb.registerCut( Cut('2Lep_ProbeAntiTight',           '( lep_Probe_SLT_isTightSelected == 0 )') )
            vardb.registerCut( Cut('2Lep_TagAndProbe_GoodEvent',    '( event_isBadTP_SLT == 0 )') )
            vardb.registerCut( Cut('2Lep_ElTagEtaCut',              '( ( TMath::Abs( lep_Tag_SLT_ID ) == 13 ) || ( TMath::Abs( lep_Tag_SLT_ID ) == 11 && TMath::Abs( lep_Tag_SLT_EtaBE2 ) < 1.37 ) )') )
            vardb.registerCut( Cut('2Lep_TagVeryTightSelected',     '( lep_Tag_SLT_ptVarcone30/lep_Tag_SLT_Pt < 0.01 )' ) ) # Tighten the track iso of the tag to increase fake purity for the probe

        elif "DLT" in args.trigger:

            vardb.registerCut( Cut('2Lep_LepTagTightTrigMatched',   '( lep_Tag_DLT_isTightSelected == 1 && lep_Tag_DLT_isTrigMatch == 1 )') )
            vardb.registerCut( Cut('2Lep_LepTagTrigMatched',        '( lep_Tag_DLT_isTrigMatch == 1 )') )
            vardb.registerCut( Cut('2Lep_LepProbeTrigMatched',      '( lep_Probe_DLT_isTrigMatch == 1 )') )
            vardb.registerCut( Cut('2Lep_LepProbeAntiTrigMatched',  '( lep_Probe_DLT_isTrigMatch == 0 )') )
            vardb.registerCut( Cut('2Lep_ElTag',                    '( TMath::Abs( lep_Tag_DLT_ID ) == 11 )') )
            vardb.registerCut( Cut('2Lep_MuTag',                    '( TMath::Abs( lep_Tag_DLT_ID ) == 13 )') )
            vardb.registerCut( Cut('2Lep_ElProbe',                  '( TMath::Abs( lep_Probe_DLT_ID ) == 11 )') )
            vardb.registerCut( Cut('2Lep_MuProbe',                  '( TMath::Abs( lep_Probe_DLT_ID ) == 13 )') )
            vardb.registerCut( Cut('2Lep_ProbeTight',               '( lep_Probe_DLT_isTightSelected == 1 )') )
            vardb.registerCut( Cut('2Lep_ProbeAntiTight',           '( lep_Probe_DLT_isTightSelected == 0 )') )
            vardb.registerCut( Cut('2Lep_TagAndProbe_GoodEvent',    '( event_isBadTP_DLT == 0 )') )
            vardb.registerCut( Cut('2Lep_ElTagEtaCut',              '( ( TMath::Abs( lep_Tag_DLT_ID ) == 13 ) || ( TMath::Abs( lep_Tag_DLT_ID ) == 11 && TMath::Abs( lep_Tag_DLT_EtaBE2 ) < 1.37 ) )') )
            vardb.registerCut( Cut('2Lep_TagVeryTightSelected',     '( lep_Tag_DLT_ptVarcone30/lep_Tag_DLT_Pt < 0.01 )' ) ) # Tighten the track iso of the tag to increase fake purity for the probe

        if "SUSY_TP" in args.channel:

            # The presence of a T (& T.M.) lepton to tag the event is implemented in the MiniNTup code.
            # The reason is b/c vector branches are used, and for the Real CR both leptons can be the tag.

            if "SLT" in args.trigger:
                vardb.getCut('2Lep_LepTagTightTrigMatched').cutstr = '( event_isBadTP_SLT == 0 )'
            elif "DLT" in args.trigger:
                vardb.getCut('2Lep_LepTagTightTrigMatched').cutstr = '( event_isBadTP_DLT == 0 )'

            # SUSY T&P uses vector branches for probe el and mu: do not specify the flavour of the probe
            # (this is particularly crucial for the Real CR, where in the ambiguous "both T&TM leptons" case there is no distinction between T&P)

            vardb.getCut('2Lep_ElProbe').cutstr = '( 1 )'
            vardb.getCut('2Lep_MuProbe').cutstr = '( 1 )'

    # -----------------
    # Event "tightness"
    # -----------------

    vardb.registerCut( Cut('TT',      '( is_T_T == 1 )') )
    vardb.registerCut( Cut('TL',      '( is_T_AntiT == 1 )') )
    vardb.registerCut( Cut('LT',      '( is_AntiT_T == 1 )') )
    vardb.registerCut( Cut('TL_LT',   '( is_T_AntiT == 1 || is_AntiT_T == 1 )') )
    vardb.registerCut( Cut('LL',      '( is_AntiT_AntiT == 1 )') )
    vardb.registerCut( Cut('TelLmu',  '( is_Tel_AntiTmu == 1 )') )
    vardb.registerCut( Cut('LelTmu',  '( is_AntiTel_Tmu == 1 )') )
    vardb.registerCut( Cut('TmuLel',  '( is_Tmu_AntiTel == 1 )') )
    vardb.registerCut( Cut('LmuTel',  '( is_AntiTmu_Tel == 1 )') )

    # ---------------------------
    # Cuts for ttW Control Region
    # ---------------------------

    # >= 2 btag
    # <= 3 jets
    # HT(jets) > 220 GeV in ee and emu
    # Z peak [+- 15 GeV] veto in ee
    # MET > 50 GeV in ee

    vardb.registerCut( Cut('2Lep_HTJ_ttW',        '( dilep_type == 1 || HT_jets > 220e3 )') )
    vardb.registerCut( Cut('2Lep_MET_ttW',        '( dilep_type != 3 || ( MET_RefFinal_et > 50e3 ) )') )
    vardb.registerCut( Cut('2Lep_Zsidescut_ttW',  '( dilep_type != 3 || ( TMath::Abs( Mll01 - 91.2e3 ) > 15e3 ) )') )
    vardb.registerCut( Cut('2Lep_NJet_ttW',       '( nJets_OR_T <= 4 )') )
    vardb.registerCut( Cut('2Lep_NBJet_ttW',      '( nJets_OR_T_MV2c10_70 >= 2 )') )
    vardb.registerCut( Cut('2Lep_Zmincut_ttW',    '( Mll01 > 40e3 )'))

    # -------------------
    # TRUTH MATCHING CUTS
    # -------------------
    #
    # The following cuts must be used in the SRs only on MC :
    #
    #   -) Plot only prompt-matched MC to avoid double counting of non prompt
    #      (as they are estimated via MM or FF). In case there are electrons in the regions,
    #      also brem electrons (but not QMisID) must be taken into account as prompt leptons.
    #   -) Veto events w/ charge flip electrons, as they are estimated data-driven
    #
    # Values of MC truth matching flags ( i.e., 'truthType', 'truthOrigin' ) are defined in MCTruthClassifier:
    #
    # https://svnweb.cern.ch/trac/atlasoff/browser/PhysicsAnalysis/MCTruthClassifier/trunk/MCTruthClassifier/MCTruthClassifierDefs.h
    #
    # Flags for brems and QMisID are defined in ttHML Group FW
    #
    # -------------------------------------------------------------------------------

    # 1.
    #
    # Event passes this cut if ALL leptons are prompt (MCTruthClassifier --> Iso), and none is charge flip
    # We classify as 'prompt' also a 'brems' lepton whose charge has been reconstructed with the correct sign

    vardb.registerCut( Cut('2Lep_TRUTH_PurePromptEvent', '( ( mc_channel_number == 0 ) || ( ( ( lep_isPrompt_0 == 1 || ( lep_isBrems_0 == 1 && lep_isQMisID_0 == 0 ) ) && ( lep_isPrompt_1 == 1 || ( lep_isBrems_1 == 1 && lep_isQMisID_1 == 0 ) ) ) && ( isQMisIDEvent == 0 ) ) )') )

    # 2.
    #
    # Event passes this cut if AT LEAST ONE lepton is !prompt (MCTruthClassifier --> !Iso), and none is charge flip
    # (i.e., the !prompt lepton will be ( HF lepton || photon conv || lepton from Dalitz decay || mis-reco jet...)
    # We classify as 'prompt' also a 'brems' lepton whose charge has been reconstructed with the correct sign

    vardb.registerCut( Cut('2Lep_TRUTH_NonPromptEvent', '( ( mc_channel_number == 0 ) || ( ( ( lep_isPrompt_0 == 0 && !( lep_isBrems_0 == 1 && lep_isQMisID_0 == 0 ) ) || ( lep_isPrompt_1 == 0 && !( lep_isBrems_1 == 1 && lep_isQMisID_1 == 0 ) ) ) && ( isQMisIDEvent == 0 ) ) )') )

    # 3.
    #
    # Event passes this cut if AT LEAST ONE lepton is charge flip (does not distinguish trident VS charge-misreconstructed)

    vardb.registerCut( Cut('2Lep_TRUTH_QMisIDEvent',    '( ( mc_channel_number == 0 ) || ( ( isQMisIDEvent == 1 ) ) )') )

    # 3a.
    #
    # Event passes this cut if AT LEAST ONE lepton is (prompt and charge flip) (it will be a charge-misId charge flip)

    vardb.registerCut( Cut('2Lep_TRUTH_QMisIDPromptEvent',  '( ( mc_channel_number == 0 ) || ( ( ( lep_isQMisID_0 == 1 && lep_isPrompt_0 == 1 ) || ( lep_isQMisID_1 == 1 && lep_isPrompt_1 == 1 ) ) ) )') )

    # 3b.
    #
    # Event passes this cut if AT LEAST ONE object is charge flip from bremsstrahlung (this will be a trident charge flip)

    vardb.registerCut( Cut('2Lep_TRUTH_QMisIDBremEvent', '( ( mc_channel_number == 0 ) || ( ( ( lep_isBrems_0 == 1 && lep_isQMisID_0 == 1 ) || ( lep_isBrems_1 == 1 && lep_isQMisID_1 == 1 ) ) ) )') )

    # 3c.
    #
    # Event passes this cut if AT LEAST ONE lepton is (!prompt and charge flip)

    vardb.registerCut( Cut('2Lep_TRUTH_QMisIDNonPromptEvent', '( ( mc_channel_number == 0 ) || ( ( ( lep_isQMisID_0 == 1 && lep_isPrompt_0 == 0 ) || ( lep_isQMisID_1 == 1 && lep_isPrompt_1 == 0 ) ) ) )') )

    # 4.
    #
    # Event passes this cut if NONE of the leptons is charge flip

    vardb.registerCut( Cut('2Lep_TRUTH_QMisIDVeto', '( ( mc_channel_number == 0 ) || ( isQMisIDEvent == 0 ) )') )

    # 4.a
    #
    # Event passes this cut if NONE of the leptons is charge flip / from photon conversion

    vardb.registerCut( Cut('2Lep_TRUTH_QMisIDANDConvPhVeto',   '( ( mc_channel_number == 0 ) || ( isQMisIDEvent == 0 && isLepFromPhEvent == 0 ) )') )

    # 5.
    #
    # Event passes this cut if AT LEAST ONE lepton is from a primary photon conversion

    vardb.registerCut( Cut('2Lep_TRUTH_LepFromPhEvent', '( ( mc_channel_number == 0 ) || ( isLepFromPhEvent == 1 ) )') )

    # 6.
    #
    # Event passes this cut if AT LEAST ONE lepton is charge flip OR from a primary photon conversion

    vardb.registerCut( Cut('2Lep_TRUTH_QMisIDORLepFromPhEvent', '( ( mc_channel_number == 0 ) || ( ( isQMisIDEvent == 1 || isLepFromPhEvent == 1 ) ) )') )

    # 6a.
    # Event passes this cut if AT LEAST ONE lepton is coming from ISR/FSR photon

    vardb.registerCut( Cut('2Lep_TRUTH_ISRPhEvent',  '( ( mc_channel_number == 0 ) || ( ( lep_isISRFSRPh_0 == 1 || lep_isISRFSRPh_1 == 1 ) ) )') )

    # ------------------------------------------------------------------------------
    # The following cuts enforce truth requirements only on the probe lepton for T&P
    # ------------------------------------------------------------------------------

    if doMMRates:

        if "SLT" in args.trigger:

            vardb.registerCut( Cut('2Lep_TRUTH_ProbePromptEvent',             '( ( mc_channel_number == 0 ) || ( ( ( lep_Probe_SLT_isPrompt == 1 || ( lep_Probe_SLT_isBrems == 1 && lep_Probe_SLT_isQMisID == 0 ) ) && lep_Probe_SLT_isQMisID == 0 ) ) )') )
            vardb.registerCut( Cut('2Lep_TRUTH_ProbeNonPromptEvent',          '( ( mc_channel_number == 0 ) || ( ( ( lep_Probe_SLT_isPrompt == 0 && !( lep_Probe_SLT_isBrems == 1 && lep_Probe_SLT_isQMisID == 0 ) ) && lep_Probe_SLT_isQMisID == 0 ) ) )') )
            vardb.registerCut( Cut('2Lep_TRUTH_ProbeNonPromptOrQMisIDEvent',  '( ( mc_channel_number == 0 ) || ( ( ( lep_Probe_SLT_isPrompt == 0 && !( lep_Probe_SLT_isBrems == 1 && lep_Probe_SLT_isQMisID == 0 ) ) || lep_Probe_SLT_isQMisID == 1 ) ) )') )
            vardb.registerCut( Cut('2Lep_TRUTH_ProbeQMisIDEvent',             '( ( mc_channel_number == 0 ) || ( ( lep_Probe_SLT_isQMisID == 1 ) ) )') )
            vardb.registerCut( Cut('2Lep_TRUTH_ProbeLepFromPhEvent',          '( ( mc_channel_number == 0 ) || ( ( lep_Probe_SLT_isConvPh == 1 || lep_Probe_SLT_isISRFSRPh_0 == 1 ) ) )') )

        elif "DLT" in args.trigger:

            vardb.registerCut( Cut('2Lep_TRUTH_ProbePromptEvent',             '( ( mc_channel_number == 0 ) || ( ( ( lep_Probe_DLT_isPrompt == 1 || ( lep_Probe_DLT_isBrems == 1 && lep_Probe_DLT_isQMisID == 0 ) ) && lep_Probe_DLT_isQMisID == 0 ) ) )') )
            vardb.registerCut( Cut('2Lep_TRUTH_ProbeNonPromptEvent',          '( ( mc_channel_number == 0 ) || ( ( ( lep_Probe_DLT_isPrompt == 0 && !( lep_Probe_DLT_isBrems == 1 && lep_Probe_DLT_isQMisID == 0 ) ) && lep_Probe_DLT_isQMisID == 0 ) ) )') )
            vardb.registerCut( Cut('2Lep_TRUTH_ProbeNonPromptOrQMisIDEvent',  '( ( mc_channel_number == 0 ) || ( ( ( lep_Probe_DLT_isPrompt == 0 && !( lep_Probe_DLT_isBrems == 1 && lep_Probe_DLT_isQMisID == 0 ) ) || lep_Probe_DLT_isQMisID == 1 ) ) )') )
            vardb.registerCut( Cut('2Lep_TRUTH_ProbeQMisIDEvent',             '( ( mc_channel_number == 0 ) || ( ( lep_Probe_DLT_isQMisID == 1 ) ) )') )
            vardb.registerCut( Cut('2Lep_TRUTH_ProbeLepFromPhEvent',          '( ( mc_channel_number == 0 ) || ( ( lep_Probe_DLT_isConvPh == 1 || lep_Probe_DLT_isISRFSRPh_0 == 1 ) ) )') )

    if args.useMoriondTruth:

        vardb.getCut('2Lep_TRUTH_PurePromptEvent').cutstr             = '( ( mc_channel_number == 0 ) || ( ( ( lep_truthType_0 == 2 || lep_truthType_0 == 6 ) && ( lep_truthType_1 == 2 || lep_truthType_1 == 6 ) ) ) )'
        vardb.getCut('2Lep_TRUTH_NonPromptEvent').cutstr              = '( ( mc_channel_number == 0 ) || ( ( ( !( lep_truthType_0 == 2 || lep_truthType_0 == 6 ) || !( lep_truthType_1 == 2 || lep_truthType_1 == 6 ) ) && !( lep_truthType_0 == 4 && lep_truthOrigin_0 == 5 ) && !( lep_truthType_1 == 4 && lep_truthOrigin_1 == 5 ) ) ) )'
        vardb.getCut('2Lep_TRUTH_QMisIDVeto').cutstr                  = '( ( mc_channel_number == 0 ) || ( ( !( lep_truthType_0 == 4 && lep_truthOrigin_0 == 5 ) && !( lep_truthType_1 == 4 && lep_truthOrigin_1 == 5 ) ) ) )'
        vardb.getCut('2Lep_TRUTH_ProbePromptEvent').cutstr            = '( ( mc_channel_number == 0 ) || ( ( lep_Probe_truthType == 2 || lep_Probe_truthType == 6 ) ) )'
        vardb.getCut('2Lep_TRUTH_ProbeNonPromptOrQMisIDEvent').cutstr = '( ( mc_channel_number == 0 ) || ( !( lep_Probe_truthType == 2 || lep_Probe_truthType == 6 ) ) )'
        vardb.getCut('2Lep_TRUTH_ProbeNonPromptEvent').cutstr         = '( ( mc_channel_number == 0 ) || ( ( !( lep_Probe_truthType == 2 || lep_Probe_truthType == 6 ) && !( lep_Probe_truthType == 4 && lep_Probe_truthOrigin == 5 ) ) ) )'


    # ---------
    # 3lep cuts
    # ---------

    vardb.registerCut( Cut('3Lep_NLep',         '( trilep_type > 0 )') )
    vardb.registerCut( Cut('3Lep_pT',           '( lep_Pt_0 > 10e3 && lep_Pt_1 > 20e3 && lep_Pt_2 > 20e3 )') )
    vardb.registerCut( Cut('3Lep_Charge',       '( TMath::Abs(total_charge) == 1 )') )
    vardb.registerCut( Cut('3Lep_TightLeptons', '( ( TMath::Abs( lep_Z0SinTheta_0 ) < 0.5 && ( TMath::Abs( lep_ID_0 ) == 13 && TMath::Abs( lep_sigd0PV_0 ) < 3.0 || TMath::Abs( lep_ID_0 ) == 11 && TMath::Abs( lep_sigd0PV_0 ) < 5.0 ) ) && ( ( TMath::Abs( lep_ID_1 ) == 13 && lep_isolationFixedCutTightTrackOnly_1 > 0 && TMath::Abs( lep_sigd0PV_1 ) < 3.0 ) || ( TMath::Abs( lep_ID_1 ) == 11 && lep_isolationFixedCutTight_1 > 0 && lep_isTightLH_1 > 0 && TMath::Abs( lep_sigd0PV_1 ) < 5.0 ) ) && ( ( TMath::Abs( lep_ID_2 ) == 13 && lep_isolationFixedCutTightTrackOnly_2 > 0 && TMath::Abs( lep_sigd0PV_2 ) < 3.0 ) || ( TMath::Abs( lep_ID_2 ) == 11 && lep_isolationFixedCutTight_2 > 0 && lep_isTightLH_2 > 0 && TMath::Abs( lep_sigd0PV_2 ) < 5.0 ) ) ) ') )
    vardb.registerCut( Cut('3Lep_TrigMatch',    '( lep_isTrigMatch_0 || lep_isTrigMatch_1 || lep_isTrigMatch_2 )') )
    vardb.registerCut( Cut('3Lep_ZVeto',        '( ( lep_ID_0 != -lep_ID_1 || TMath::Abs( Mll01 - 91.2e3 ) > 10e3 ) && ( lep_ID_0! = -lep_ID_2 || TMath::Abs( Mll02 - 91.2e3 ) > 10e3 ) )') )
    vardb.registerCut( Cut('3Lep_MinZCut',      '( ( lep_ID_0 != -lep_ID_1 || Mll01 > 12e3 ) && ( lep_ID_0 != -lep_ID_2 || Mll02 > 12e3 ) )') )
    vardb.registerCut( Cut('3Lep_NJets',        '( ( nJets_OR >= 4 && nJets_OR_MV2c10_70 >= 1 ) || ( nJets_OR >=3 && nJets_OR_MV2c10_70 >= 2 ) )') )

    # ---------
    # 4lep cuts
    # ---------

    # FIXME!
    vardb.registerCut( Cut('4Lep_NJets',  '( nJets_OR_T >= 2 )') )
    vardb.registerCut( Cut('4Lep',        '( nleptons == 4 )') )

    # ---------------------
    # 2Lep SS + 1 tau cuts
    # ---------------------

    vardb.registerCut( Cut('2Lep1Tau_NLep',         '( dilep_type > 0 )') )
    vardb.registerCut( Cut('2Lep1Tau_TightLeptons', '( is_T_T == 1 )') )
    vardb.registerCut( Cut('2Lep1Tau_pT',           '( lep_Pt_0 > 25e3 && lep_Pt_1 > 15e3  )') )
    vardb.registerCut( Cut('2Lep1Tau_TrigMatch',    '( lep_isTrigMatch_0|| lep_isTrigMatch_1 )') )
    vardb.registerCut( Cut('2Lep1Tau_SS',           '( lep_ID_0 * lep_ID_1 > 0 )') )
    vardb.registerCut( Cut('2Lep1Tau_1Tau',         '( nTaus_OR_Pt25 == 1 && ( lep_ID_0 * tau_charge_0 ) < 0 )') )
    vardb.registerCut( Cut('2Lep1Tau_Zsidescut',    '( dilep_type != 3 || TMath::Abs( Mll01 - 91.2e3 ) > 10e3 )' )  )
    vardb.registerCut( Cut('2Lep1Tau_NJet_SR',      '( nJets_OR_T >= 4 )') )
    vardb.registerCut( Cut('2Lep1Tau_NJet_CR',      '( nJets_OR_T > 1 && nJets_OR_T < 4 )') )
    vardb.registerCut( Cut('2Lep1Tau_NBJet',        '( nJets_OR_T_MV2c10_70 > 0 )') )

    # ---------------------------
    # A list of variables to plot
    # ---------------------------

    if args.doSyst:
        print("De-activating standard plots for systematics...")
        makeStandardPlots = False

    # Reconstructed pT of the Z

    pT_Z = '( TMath::Sqrt( (lep_Pt_0*lep_Pt_0) + (lep_Pt_1*lep_Pt_1) + 2*lep_Pt_0*lep_Pt_1*(TMath::Cos( lep_Phi_0 - lep_Phi_1 )) ) )/1e3'

    # Calculate DeltaR(lep0,lep1) in 2LepSS + 0 tau category

    gROOT.LoadMacro("$ROOTCOREBIN/user_scripts/HTopMultilepAnalysis/ROOT_TTreeFormulas/deltaR.cxx+")
    from ROOT import deltaR
    delta_R_lep0lep1 = 'deltaR( lep_ID_0, lep_Eta_0, lep_EtaBE2_0, lep_Phi_0, lep_ID_1, lep_Eta_1, lep_EtaBE2_1, lep_Phi_1 )'
    delta_R_lep0lep2 = 'deltaR( lep_ID_0, lep_Eta_0, lep_EtaBE2_0, lep_Phi_0, lep_ID_2, lep_Eta_2, lep_EtaBE2_2, lep_Phi_2 )'
    delta_R_lep1lep2 = 'deltaR( lep_ID_1, lep_Eta_1, lep_EtaBE2_1, lep_Phi_1, lep_ID_2, lep_Eta_2, lep_EtaBE2_2, lep_Phi_2 )'

    if doSR or doLowNJetCR:
        print ''
        #vardb.registerVar( Variable(shortname = 'NJets', latexname = 'Jet multiplicity', ntuplename = 'nJets_OR_T', bins = 10, minval = -0.5, maxval = 9.5, weight = 'JVT_EventWeight') )
        if doSR:
	    vardb.registerVar( Variable(shortname = 'NJets5j', latexname = 'Jet multiplicity', ntuplename = 'nJets_OR_T', bins = 6, minval = 3.5, maxval = 9.5, weight = "JVT_EventWeight", sysvar = True) )
        elif doLowNJetCR:
            vardb.registerVar( Variable(shortname = 'NJets2j3j4j', latexname = 'Jet multiplicity', ntuplename = 'nJets_OR_T', bins = 4, minval = 1.5, maxval = 5.5, weight = "JVT_EventWeight", sysvar = True) )
        #vardb.registerVar( Variable(shortname = 'NBJets', latexname = 'BJet multiplicity', ntuplename = 'nJets_OR_T_MV2c10_70', bins = 4, minval = -0.5, maxval = 3.5, weight = 'JVT_EventWeight * MV2c10_70_EventWeight') )
        #vardb.registerVar( Variable(shortname = 'Mll01_inc', latexname = 'm(l_{0}l_{1}) [GeV]', ntuplename = 'Mll01/1e3', bins = 13, minval = 0.0, maxval = 260.0,) )
        #vardb.registerVar( Variable(shortname = 'Lep0Eta', latexname = '#eta^{lead lep}', ntuplename = 'lep_Eta_0', bins = 16, minval = -2.6, maxval = 2.6) )
        #vardb.registerVar( Variable(shortname = 'Lep1Eta', latexname = '#eta^{2nd lead lep}', ntuplename = 'lep_Eta_1', bins = 16, minval = -2.6, maxval = 2.6) )
        #vardb.registerVar( Variable(shortname = 'Lep0Pt', latexname = 'p_{T}^{lead lep} [GeV]', ntuplename = 'lep_Pt_0/1e3', bins = 18, minval = 25.0, maxval = 205.0,) )
        #vardb.registerVar( Variable(shortname = 'Lep1Pt', latexname = 'p_{T}^{2nd lead lep} [GeV]', ntuplename = 'lep_Pt_1/1e3', bins = 6, minval = 25.0, maxval = 145.0,) )
        #vardb.registerVar( Variable(shortname = 'MET_FinalTrk', latexname = 'E_{T}^{miss} (FinalTrk) [GeV]', ntuplename = 'MET_RefFinal_et/1e3', bins = 9, minval = 0.0, maxval = 180.0,) )
        #vardb.registerVar( Variable(shortname = 'deltaRLep0Lep1', latexname = '#DeltaR(lep_{0},lep_{1})', ntuplename = delta_R_lep0lep1, bins = 10, minval = 0.0, maxval = 5.0) )

    if doMMSidebands:
        #vardb.registerVar( Variable(shortname = 'MMWeight', latexname = 'MM weight', ntuplename = 'MMWeight', bins = 50, minval = -0.5, maxval = 0.5) )
        #vardb.registerVar( Variable(shortname = 'Lep0Pt', latexname = 'p_{T}^{lead lep} [GeV]', ntuplename = 'lep_Pt_0/1e3', bins = 9, minval = 25.0, maxval = 205.0,) )
        vardb.registerVar( Variable(shortname = 'Lep0TM_VS_Lep1TM', latexnameX = 'lead lep TM', latexnameY = '2nd lead lep TM', ntuplename = 'lep_isTrigMatch_1:lep_isTrigMatch_0', bins = 2, minval = -0.5, maxval = 1.5, typeval = TH2F) )
        if "HIGHNJ" in args.channel:
            vardb.registerVar( Variable(shortname = 'NJets5j', latexname = 'Jet multiplicity', ntuplename = 'nJets_OR_T', bins = 6, minval = 3.5, maxval = 9.5, weight = 'JVT_EventWeight') )
        elif "LOWNJ" in args.channel:
            vardb.registerVar( Variable(shortname = 'NJets2j3j4j', latexname = 'Jet multiplicity', ntuplename = 'nJets_OR_T', bins = 4, minval = 1.5, maxval = 5.5, weight = 'JVT_EventWeight') )
        elif "ALLNJ" in args.channel:
            vardb.registerVar( Variable(shortname = 'NJets', latexname = 'Jet multiplicity', ntuplename = 'nJets_OR_T', bins = 8, minval = 1.5, maxval = 9.5, weight = 'JVT_EventWeight') )

    if doMMClosureTest:
        print ''
        if "ALLNJ" in args.channel:
            #vardb.registerVar( Variable(shortname = 'NJets', latexname = 'Jet multiplicity', ntuplename = 'nJets_OR_T', bins = 8, minval = 1.5, maxval = 9.5, weight = 'JVT_EventWeight', sysvar = True) )
            #
            vardb.registerVar( Variable(shortname = 'Lep0Pt', latexname = 'p_{T}^{lead lep} [GeV]', ntuplename = 'lep_Pt_0/1e3', bins = 10, minval = 20.0, maxval = 220.0, sysvar = True) )
            #vardb.registerVar( Variable(shortname = 'Lep1Pt', latexname = 'p_{T}^{2nd lead lep} [GeV]', ntuplename = 'lep_Pt_1/1e3', bins = 10, minval = 20.0, maxval = 220.0) )
            #
            #vardb.registerVar( Variable(shortname = 'Lep0PtManualBins_Rebin', latexname = 'p_{T}^{lead lep} [GeV]', ntuplename = 'lep_Pt_0/1e3', bins = 10, minval = 20.0, maxval = 220.0, manualbins = [20.0,26.0,35.0,60.0,80.0,140.0,220.0], sysvar = True) )
            #vardb.registerVar( Variable(shortname = 'Lep1PtManualBins_Rebin', latexname = 'p_{T}^{2nd lead lep} [GeV]', ntuplename = 'lep_Pt_1/1e3', bins = 10, minval = 20.0, maxval = 220.0, manualbins = [20.0,26.0,35.0,60.0,80.0,140.0,220.0], sysvar = True) )
            #
            #vardb.registerVar( Variable(shortname = 'Lep0PtManualBins_LowPt', latexname = 'p_{T}^{lead lep} [GeV]', ntuplename = 'lep_Pt_0/1e3', bins = 10, minval = 20.0, maxval = 220.0, manualbins = [10.0,15.0,20.0,25.0], sysvar = True ) )
            #vardb.registerVar( Variable(shortname = 'Lep1PtManualBins_LowPt', latexname = 'p_{T}^{2nd lead lep} [GeV]', ntuplename = 'lep_Pt_1/1e3', bins = 10, minval = 20.0, maxval = 220.0, manualbins = [10.0,15.0,20.0,25.0], sysvar = True ) )
            #
        elif "HIGHNJ" in args.channel:
            vardb.registerVar( Variable(shortname = 'NJets5j', latexname = 'Jet multiplicity', ntuplename = 'nJets_OR_T', bins = 6, minval = 3.5, maxval = 9.5, weight = 'JVT_EventWeight') )
        elif "LOWNJ" in args.channel:
            vardb.registerVar( Variable(shortname = 'NJets2j3j4j', latexname = 'Jet multiplicity', ntuplename = 'nJets_OR_T', bins = 4, minval = 1.5, maxval = 5.5, weight = 'JVT_EventWeight') )
        #vardb.registerVar( Variable(shortname = 'NBJets', latexname = 'BJet multiplicity', ntuplename ='nJets_OR_T_MV2c10_70', bins = 4, minval = -0.5, maxval = 3.5, weight = 'JVT_EventWeight * MV2c10_70_EventWeight') )
        #vardb.registerVar( Variable(shortname = 'Mll01_inc', latexname = 'm(l_{0}l_{1}) [GeV]', ntuplename = 'Mll01/1e3', bins = 13, minval = 0.0, maxval = 260.0,) )
	#vardb.registerVar( Variable(shortname = 'Lep0Pt', latexname = 'p_{T}^{lead lep} [GeV]', ntuplename = 'lep_Pt_0/1e3', bins = 10, minval = 25.0, maxval = 205.0) )
        #vardb.registerVar( Variable(shortname = 'Lep1Pt', latexname = 'p_{T}^{2nd lead lep} [GeV]', ntuplename = 'lep_Pt_1/1e3', bins = 6, minval = 25.0, maxval = 145.0) )
	#vardb.registerVar( Variable(shortname = 'Lep0Pt_ElBinning', latexname = 'p_{T}^{lead lep} [GeV]', ntuplename = 'lep_Pt_0/1e3', bins = 18, minval = 25.0, maxval = 205.0, manualbins = [25,35,60,80,100,140,180,220]) )
        #vardb.registerVar( Variable(shortname = 'Lep1Pt_ElBinning', latexname = 'p_{T}^{2nd lead lep} [GeV]', ntuplename = 'lep_Pt_1/1e3', bins = 18, minval = 25.0, maxval = 205.0, manualbins = [25,35,60,80,100,140,180,220]) )
        #vardb.registerVar( Variable(shortname = 'Lep0Pt_MuBinning', latexname = 'p_{T}^{lead lep} [GeV]', ntuplename = 'lep_Pt_0/1e3', bins = 18, minval = 25.0, maxval = 205.0, manualbins = [25,35,50,200]) )
        #vardb.registerVar( Variable(shortname = 'Lep1Pt_MuBinning', latexname = 'p_{T}^{2nd lead lep} [GeV]', ntuplename = 'lep_Pt_1/1e3', bins = 18, minval = 25.0, maxval = 205.0, manualbins = [25,35,50,200]) )
        #vardb.registerVar( Variable(shortname = 'MET_FinalTrk', latexname = 'E_{T}^{miss} (FinalTrk) [GeV]', ntuplename = 'MET_RefFinal_et/1e3', bins = 9, minval = 0.0, maxval = 180.0,) )
        #vardb.registerVar( Variable(shortname = 'deltaRLep0Lep1', latexname = '#DeltaR(lep_{0},lep_{1})', ntuplename = delta_R_lep0lep1, bins = 10, minval = 0.0, maxval = 5.0) )

    if doZSSpeakCR:
        print ''
        vardb.registerVar( Variable(shortname = 'Mll01_NarrowPeak', latexname = 'm(l_{0}l_{1}) [GeV]', ntuplename = 'Mll01/1e3', bins = 26, minval = 60.0, maxval = 125.0) )

    if doCFChallenge:
        print ''
        vardb.registerVar( Variable(shortname = 'NJets', latexname = 'Jet multiplicity', ntuplename = 'nJets_OR_T', bins = 10, minval = -0.5, maxval = 9.5, weight = 'JVT_EventWeight') )

    if makeStandardPlots:
        print ''
        vardb.registerVar( Variable(shortname = 'NJets', latexname = 'Jet multiplicity', ntuplename = 'nJets_OR_T', bins = 8, minval = 1.5, maxval = 9.5, weight = 'JVT_EventWeight') )
        vardb.registerVar( Variable(shortname = 'NJets2j3j4j', latexname = 'Jet multiplicity', ntuplename = 'nJets_OR_T', bins = 4, minval = 1.5, maxval = 5.5, weight = 'JVT_EventWeight') )
        vardb.registerVar( Variable(shortname = 'NBJets', latexname = 'BJet multiplicity', ntuplename = 'nJets_OR_T_MV2c10_70', bins = 4, minval = -0.5, maxval = 3.5, weight = 'JVT_EventWeight * MV2c10_70_EventWeight') )
        vardb.registerVar( Variable(shortname = 'NJetsPlus10NBJets', latexname = 'N_{Jets}+10*N_{BJets}', ntuplename = 'nJets_OR_T+10.0*nJets_OR_T_MV2c10_70', bins = 40, minval = 0, maxval = 40, basecut = vardb.getCut('VetoLargeNBJet'), weight = 'JVT_EventWeight * MV2c10_70_EventWeight') )
        vardb.registerVar( Variable(shortname = 'NElectrons', latexname = 'Electron multiplicity', ntuplename = 'nelectrons', bins = 5, minval = -0.5, maxval = 4.5) )
        vardb.registerVar( Variable(shortname = 'NMuons', latexname = 'Muon multiplicity', ntuplename = 'nmuons', bins = 5, minval = -0.5, maxval = 4.5) )
        #
        # Inclusive m(ll) plot
        #
        vardb.registerVar( Variable(shortname = 'Mll01_inc', latexname = 'm(l_{0}l_{1}) [GeV]', ntuplename = 'Mll01/1e3', bins = 46, minval = 10.0, maxval = 240.0,) )
        #
        # Z peak plot
        #
        vardb.registerVar( Variable(shortname = 'Mll01_peak', latexname = 'm(l_{0}l_{1}) [GeV]', ntuplename = 'Mll01/1e3', bins = 40, minval = 40.0, maxval = 120.0,) )
        #
        vardb.registerVar( Variable(shortname = 'pT_Z', latexname = 'p_{T} Z (reco) [GeV]', ntuplename = pT_Z, bins = 100, minval = 0.0, maxval = 1000.0, logaxisX = True) )
        vardb.registerVar( Variable(shortname = 'Lep0Pt', latexname = 'p_{T}^{lead lep} [GeV]', ntuplename = 'lep_Pt_0/1e3', bins = 36, minval = 10.0, maxval = 190.0) )
        vardb.registerVar( Variable(shortname = 'Lep1Pt', latexname = 'p_{T}^{2nd lead lep} [GeV]', ntuplename = 'lep_Pt_1/1e3', bins = 20, minval = 10.0, maxval = 110.0) )
        vardb.registerVar( Variable(shortname = 'Lep0Eta', latexname = '#eta^{lead lep}', ntuplename = 'lep_Eta_0', bins = 16, minval = -2.6, maxval = 2.6) )
        vardb.registerVar( Variable(shortname = 'Lep1Eta', latexname = '#eta^{2nd lead lep}', ntuplename = 'lep_Eta_1', bins = 16, minval = -2.6, maxval = 2.6) )
        vardb.registerVar( Variable(shortname = 'deltaRLep0Lep1', latexname = '#DeltaR(lep_{0},lep_{1})', ntuplename = delta_R_lep0lep1, bins = 20, minval = 0.0, maxval = 5.0) )
        vardb.registerVar( Variable(shortname = 'deltaRLep0Lep2', latexname = '#DeltaR(lep_{0},lep_{2})', ntuplename = delta_R_lep0lep2, bins = 20, minval = 0.0, maxval = 5.0) )
        vardb.registerVar( Variable(shortname = 'deltaRLep1Lep2', latexname = '#DeltaR(lep_{1},lep_{2})', ntuplename = delta_R_lep1lep2, bins = 20, minval = 0.0, maxval = 5.0) )
        vardb.registerVar( Variable(shortname = 'Mll12', latexname = 'm(l_{1}l_{2}) [GeV]', ntuplename = 'Mll12/1e3', bins = 15, minval = 0.0, maxval = 300.0,) )
        vardb.registerVar( Variable(shortname = 'Jet0Pt', latexname = 'p_{T}^{lead jet} [GeV]', ntuplename = 'lead_jetPt/1e3', bins = 36, minval = 20.0, maxval = 200.0,) )
        vardb.registerVar( Variable(shortname = 'Jet0Eta', latexname = '#eta^{lead jet}', ntuplename = 'lead_jetEta', bins = 50, minval = -5.0, maxval = 5.0) )
        vardb.registerVar( Variable(shortname = 'avgint', latexname = 'Average Interactions Per Bunch Crossing', ntuplename = 'averageIntPerXing*1.16', bins = 50, minval = 0, maxval = 50, typeval = TH1I) )
        vardb.registerVar( Variable(shortname = 'MET_FinalTrk', latexname = 'E_{T}^{miss} (FinalTrk) [GeV]', ntuplename = 'MET_RefFinal_et/1e3', bins = 45, minval = 0.0, maxval = 180.0,) )
        vardb.registerVar( Variable(shortname = 'Tau0Pt', latexname = 'p_{T}^{lead tau} [GeV]', ntuplename = 'tau_pt_0', bins = 30, minval = 25.0, maxval = 100.0,) )

    # -------------------------------------------------
    # Alterantive ranges and binning for the histograms
    # -------------------------------------------------

    midstatsbin = {
        'MMC': (25, 0., 250.),
        'mvis': (25, 0., 250.),
        'mT': (30, 0., 120.),
        'MET': (25, 0., 100.),
        'leppt': (30, 17., 77.),
        'taupt': (25, 20., 70.),
        'jetpt': (25, 25., 125.),
    }
    lowstatsbin = {
        'MMC': (12, 0., 240.),
        'mvis': (12, 0., 240.),
        'mT': (12, 0., 120.),
        'MET': (12, 0., 120.),
        'leppt': (12, 17., 77.),
        'taupt': (12, 20., 80.),
        'jetpt': (12, 25., 121.),
    }

    # ---------------------
    # A list of systematics
    # ---------------------

    if args.doSyst:

        #vardb.registerSystematics( Systematics(name='PU',             eventweight='evtsel_sys_PU_rescaling_') )
        #vardb.registerSystematics( Systematics(name='el_reco',        eventweight='evtsel_sys_sf_el_reco_') )
        #vardb.registerSystematics( Systematics(name='el_id',          eventweight='evtsel_sys_sf_el_id_') )
        #vardb.registerSystematics( Systematics(name='el_iso',         eventweight='evtsel_sys_sf_el_iso_') )
        #vardb.registerSystematics( Systematics(name='mu_id',          eventweight='evtsel_sys_sf_mu_id_') )
        #vardb.registerSystematics( Systematics(name='mu_iso',         eventweight='evtsel_sys_sf_mu_iso_') )
        #vardb.registerSystematics( Systematics(name='lep_trig',       eventweight='evtsel_sys_sf_lep_trig_') )
        #vardb.registerSystematics( Systematics(name='bjet_b',         eventweight='evtsel_sys_sf_bjet_b_') )
        #vardb.registerSystematics( Systematics(name='bjet_c',         eventweight='evtsel_sys_sf_bjet_c_') )
        #vardb.registerSystematics( Systematics(name='bjet_m',         eventweight='evtsel_sys_sf_bjet_m_') )

        #vardb.registerSystematics( Systematics(name='METSys',         treename='METSys') )
        #vardb.registerSystematics( Systematics(name='ElEnResSys',     treename='ElEnResSys') )
        #vardb.registerSystematics( Systematics(name='ElES_LowPt',     treename='ElES_LowPt') )
        #vardb.registerSystematics( Systematics(name='ElES_Zee',       treename='ElES_Zee') )
        #vardb.registerSystematics( Systematics(name='ElES_R12',       treename='ElES_R12') )
        #vardb.registerSystematics( Systematics(name='ElES_PS',        treename='ElES_PS') )
        #vardb.registerSystematics( Systematics(name='EESSys',         treename='EESSys') )
        #vardb.registerSystematics( Systematics(name='MuSys',          treename='MuSys') )
        #vardb.registerSystematics( Systematics(name='JES_Total',      treename='JES_Total') )
        #vardb.registerSystematics( Systematics(name='JER',            treename='JER') )

        if doMMRates and "DATA" in args.channel:
            vardb.registerSystematics( Systematics(name='QMisIDsys', eventweight='QMisIDWeight_', process='QMisID') )

        # Get the number of systematics shifts for the MMWeight systematics (aka, the number of bins of the r/f efficiency)
        # from the reweighted tree.
        # Use the Data sample. For MM closure test, use 410000 (ttbar_nonallhad)
        # The number of indexes is by construction the same for any source of systematic uncertainty,
        # thus we can use "Stat" to get the number of bins.

        sampleID = ""
        if doMMClosureTest:
            sampleID = "410000"

        bins_real_el_pt = inputs.getSysIndexes( sampleID=sampleID, branchID="MMWeight_Real_El_Pt_Stat" )
        bins_real_mu_pt = inputs.getSysIndexes( sampleID=sampleID, branchID="MMWeight_Real_Mu_Pt_Stat" )
        bins_fake_el_pt = inputs.getSysIndexes( sampleID=sampleID, branchID="MMWeight_Fake_El_Pt_Stat" )
        bins_fake_mu_pt = inputs.getSysIndexes( sampleID=sampleID, branchID="MMWeight_Fake_Mu_Pt_Stat" )

        print "bins_real_el_pt", bins_real_el_pt
        print "bins_real_mu_pt", bins_real_mu_pt
        print "bins_fake_el_pt", bins_fake_el_pt
        print "bins_fake_mu_pt", bins_fake_mu_pt

        if doMMClosureTest:

	    if doMM:
		for ibin in bins_real_el_pt:
		   thiscat    = "MMsys_Real_El_Pt_Stat_" + str(ibin)
		   thisweight = "MMWeight_Real_El_Pt_Stat_" + str(ibin) + "_"
		   vardb.registerSystematics(Systematics(name=thiscat, eventweight=thisweight, process="FakesClosureMM"))
		for ibin in bins_real_mu_pt:
		   thiscat    = "MMsys_Real_Mu_Pt_Stat_" + str(ibin)
		   thisweight = "MMWeight_Real_Mu_Pt_Stat_" + str(ibin) + "_"
		   vardb.registerSystematics(Systematics(name=thiscat, eventweight=thisweight, process="FakesClosureMM"))
		for ibin in bins_fake_el_pt:
		   thiscat    = "MMsys_Fake_El_Pt_Stat_" + str(ibin)
		   thisweight = "MMWeight_Fake_El_Pt_Stat_" + str(ibin) + "_"
		   vardb.registerSystematics(Systematics(name=thiscat, eventweight=thisweight, process="FakesClosureMM"))
		for ibin in bins_fake_mu_pt:
		   thiscat    = "MMsys_Fake_Mu_Pt_Stat_" + str(ibin)
		   thisweight = "MMWeight_Fake_Mu_Pt_Stat_" + str(ibin) + "_"
		   vardb.registerSystematics(Systematics(name=thiscat, eventweight=thisweight, process="FakesClosureMM"))

	    if doFF:
                vardb.registerSystematics( Systematics(name="FFsys", eventweight="FFWeight_", process="FakesClosureMM") )

        if doTwoLepSR or doThreeLepSR or doTwoLepLowNJetCR or doThreeLepLowNJetCR:

	    #vardb.registerSystematics( Systematics(name="QMisIDsys", eventweight="QMisIDWeight_") )

	    if doMM:

		#sys_sources = ["Stat","numerator_QMisID","denominator_QMisID"]
		sys_sources = ["Stat"]

		for sys in sys_sources:
		   for ibin in bins_real_el_pt:
		       thiscat    = "MMsys_Real_El_Pt_" + sys + "_" + str(ibin)
		       thisweight = "MMWeight_Real_El_Pt_" + sys + "_" + str(ibin) + "_"
		       vardb.registerSystematics(Systematics(name=thiscat, eventweight=thisweight, process="FakesMM"))
		   for ibin in bins_real_mu_pt:
		       thiscat    = "MMsys_Real_Mu_Pt_" + sys + "_" + str(ibin)
		       thisweight = "MMWeight_Real_Mu_Pt_" + sys + "_" + str(ibin) + "_"
		       vardb.registerSystematics(Systematics(name=thiscat, eventweight=thisweight, process="FakesMM"))
		   for ibin in bins_fake_el_pt:
		       thiscat    = "MMsys_Fake_El_Pt_" + sys + "_" + str(ibin)
		       thisweight = "MMWeight_Fake_El_Pt_" + sys + "_" + str(ibin) + "_"
		       vardb.registerSystematics(Systematics(name=thiscat, eventweight=thisweight, process="FakesMM"))
		   for ibin in bins_fake_mu_pt:
		       thiscat    = "MMsys_Fake_Mu_Pt_" + sys + "_" + str(ibin)
		       thisweight = "MMWeight_Fake_Mu_Pt_" + sys + "_" + str(ibin) + "_"
		       vardb.registerSystematics(Systematics(name=thiscat, eventweight=thisweight, process="FakesMM"))

            if doFF:
                vardb.registerSystematics( Systematics(name="FFsys", eventweight="FFWeight_", process="FakesMM") )

    # -------------------------------------------------------------------
    # Definition of the categories for which one wants produce histograms
    # -------------------------------------------------------------------

    weight_SR_CR = "tauSFTight * weight_event_trig * weight_event_lep * JVT_EventWeight * MV2c10_70_EventWeight"

    cc_2Lep_list = ['TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_NBJet_SR','2Lep_NLep','2Lep_pT','2Lep_SS','TauVeto','2Lep_TRUTH_PurePromptEvent','2Lep_ElEtaCut']
    common_cuts_2Lep = vardb.getCuts(cc_2Lep_list)

    cc_2Lep1Tau_list = ['TrigDec','BlindingCut','2Lep1Tau_NLep','2Lep1Tau_pT','2Lep1Tau_TrigMatch','2Lep1Tau_SS','2Lep1Tau_1Tau','2Lep1Tau_Zsidescut','2Lep1Tau_NBJet']
    common_cuts_2Lep1Tau = vardb.getCuts(cc_2Lep1Tau_list)

    cc_3Lep_list = ['TrigDec','BlindingCut','3Lep_pT','3Lep_TrigMatch','3Lep_NLep','3Lep_Charge','3Lep_TightLeptons','3Lep_ZVeto','3Lep_MinZCut','3Lep_NJets']
    common_cuts_3Lep = vardb.getCuts(cc_3Lep_list)

    cc_4Lep_list = ['TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_NBJet_SR','4Lep','4Lep_NJets']
    common_cuts_4Lep = vardb.getCuts(cc_4Lep_list)

    cat_names_2Lep = {
                       'mm' : 'MuMuSS',
                       'ee' : 'ElElSS',
                       'OF' : 'OFSS',
                       'em' : 'ElMuSS',
                       'me' : 'MuElSS',
                     }

    append_2Lep = ""

    # --------------
    # Signal Regions
    # --------------

    if doSR:

        if doTwoLepSR :

            append_2Lep += "_SR"

            if ( doMM or doFF or doTHETA ):
                append_2Lep += "_DataDriven"

            if any( cat in args.category for cat in ["mm","ALL"] ): vardb.registerCategory( MyCategory(cat_names_2Lep["mm"] + append_2Lep,  cut = common_cuts_2Lep & vardb.getCuts(['2Lep_MuMu_Event','2Lep_NJet_SR']), weight = weight_SR_CR ) )
            if any( cat in args.category for cat in ["ee","ALL"] ): vardb.registerCategory( MyCategory(cat_names_2Lep["ee"] + append_2Lep,  cut = common_cuts_2Lep & vardb.getCuts(['2Lep_ElEl_Event','2Lep_NJet_SR']), weight = weight_SR_CR ) )
            if any( cat in args.category for cat in ["OF","ALL"] ): vardb.registerCategory( MyCategory(cat_names_2Lep["OF"] + append_2Lep,  cut = common_cuts_2Lep & vardb.getCuts(['2Lep_OF_Event','2Lep_NJet_SR']), weight = weight_SR_CR ) )
            #
            #vardb.registerCategory( MyCategory('TwoLepSSTau_SR', cut = common_cuts_2Lep1Tau & vardb.getCut('2Lep1Tau_NJet_SR') ), weight = weight_SR_CR )

        if doThreeLepSR:
            vardb.registerCategory( MyCategory('ThreeLep_SR',    cut = common_cuts_3Lep, weight = weight_SR_CR ) )

        if doFourLepSR:
            vardb.registerCategory( MyCategory('FourLep_SR',     cut = common_cuts_4Lep, weight = weight_SR_CR ) )

    # -------------
    # Low N-jet CRs
    # -------------

    if doTwoLepLowNJetCR :

        append_2Lep += "_LowNJetCR"

        if ( doMM or doFF or doTHETA ):
            append_2Lep += "_DataDriven"

        if any( cat in args.category for cat in ["OF","ALL"] ): vardb.registerCategory( MyCategory(cat_names_2Lep["OF"] + append_2Lep, cut = common_cuts_2Lep & vardb.getCuts(['2Lep_OF_Event','2Lep_NJet_CR']), weight = weight_SR_CR ) )
        if not ( doTHETA ):
            if any( cat in args.category for cat in ["mm","ALL"] ): vardb.registerCategory( MyCategory(cat_names_2Lep["mm"] + append_2Lep, cut = common_cuts_2Lep & vardb.getCuts(['2Lep_MuMu_Event','2Lep_NJet_CR']), weight = weight_SR_CR ) )
            if any( cat in args.category for cat in ["ee","ALL"] ): vardb.registerCategory( MyCategory(cat_names_2Lep["ee"] + append_2Lep, cut = common_cuts_2Lep & vardb.getCuts(['2Lep_ElEl_Event','2Lep_NJet_CR']), weight = weight_SR_CR ) )
        #vardb.registerCategory( MyCategory('TwoLepSSTau_LowNJetCR',  cut = common_cuts_2Lep1Tau & vardb.getCut('2Lep1Tau_NJet_CR'), weight = weight_SR_CR ) )

    if doThreeLepLowNJetCR:
        # take OS pairs
        #
        vardb.registerCategory( MyCategory('ThreeLep_LowNJetCR',   cut = vardb.getCuts(['TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_NBJet','3Lep_NLep','2Lep_NJet_CR','ZOSsidescut','2Lep_OS']), weight = weight_SR_CR ) )

    # -------------
    # Other CRs
    # -------------

    if doWZonCR:
        vardb.registerCategory( MyCategory('WZonCR',      cut = vardb.getCuts(['TrigDec','BlindingCut','2Lep_TrigMatch','BJetVeto','3Lep_NLep','2Lep_Zpeakcut','2Lep_OS']), weight = weight_SR_CR ) )

    if doWZoffCR:
        vardb.registerCategory( MyCategory('WZoffCR',     cut = vardb.getCuts(['TrigDec','BlindingCut','2Lep_TrigMatch','BJetVeto','3Lep_NLep','2Lep_Zsidescut','2Lep_OS']), weight = weight_SR_CR ) )

    if doWZHFonCR:
        vardb.registerCategory( MyCategory('WZHFonCR',    cut = vardb.getCuts(['TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_NBJet','3Lep_NLep','2Lep_Zpeakcut','2Lep_OS']), weight = weight_SR_CR ) )

    if doWZHFoffCR:
        vardb.registerCategory( MyCategory('WZHFoffCR',   cut = vardb.getCuts(['TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_NBJet','3Lep_NLep','2Lep_Zsidescut','2Lep_OS']), weight = weight_SR_CR ) )

    if dottZCR:
        vardb.registerCategory( MyCategory('ttZCR',       cut = vardb.getCuts(['TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_NBJet','3Lep_NLep','NJet3L','2Lep_Zpeakcut','2Lep_OS']), weight = weight_SR_CR ) )

    if dottWCR:
        vardb.registerCategory( MyCategory('ttWCR',       cut = vardb.getCuts(['TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_NJet_ttW','2Lep_NBJet_ttW','2Lep_NLep','2Lep_pT_Relaxed','TauVeto','TT','2Lep_Zmincut_ttW','2Lep_OS']), weight = weight_SR_CR ) )

    if doZSSpeakCR:
        vardb.registerCategory( MyCategory('ZSSpeakCR_ElEl',   cut = vardb.getCuts(['2Lep_NLep','2Lep_pT','TrigDec','BlindingCut','2Lep_TrigMatch','TauVeto','2Lep_ElEl_Event','2Lep_SS','2Lep_Zpeakcut','2Lep_TRUTH_PurePromptEvent']), weight = weight_SR_CR ) )
        vardb.registerCategory( MyCategory('ZSSpeakCR_MuMu',   cut = vardb.getCuts(['2Lep_NLep','2Lep_pT','TrigDec','BlindingCut','2Lep_TrigMatch','TauVeto','2Lep_MuMu_Event','2Lep_SS','2Lep_Zpeakcut','2Lep_TRUTH_PurePromptEvent']), weight = weight_SR_CR ) )


    # ------------------------------------
    # Special CR for Data/MC control plots
    # ------------------------------------

    if doDataMCCR:

        # Inclusive OS dilepton (ee,mumu, emu)

        vardb.registerCategory( MyCategory('DataMC_InclusiveOS_MuMu', cut = vardb.getCuts(['2Lep_NLep','2Lep_pT_Relaxed','TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_MuMu_Event','TT','2Lep_Zmincut','2Lep_OS']), weight = weight_SR_CR ) )
        vardb.registerCategory( MyCategory('DataMC_InclusiveOS_ElEl', cut = vardb.getCuts(['2Lep_NLep','2Lep_pT_Relaxed','TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_ElEl_Event','TT','2Lep_ElEtaCut','2Lep_Zmincut','2Lep_OS']), weight = weight_SR_CR ) )
        vardb.registerCategory( MyCategory('DataMC_InclusiveOS_OF',   cut = vardb.getCuts(['2Lep_NLep','2Lep_pT_Relaxed','TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_OF_Event','TT','2Lep_ElEtaCut','2Lep_Zmincut','2Lep_OS']), weight = weight_SR_CR ) )

        # OS ttbar ( top dilepton) (ee,mumu,emu)

        vardb.registerCategory( MyCategory('DataMC_OS_ttbar_MuMu',    cut = vardb.getCuts(['2Lep_NLep','2Lep_pT_Relaxed','TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_MuMu_Event','TT','4Lep_NJets','2Lep_NBJet','2Lep_Zsidescut','2Lep_Zmincut','2Lep_OS']), weight = weight_SR_CR ) )
        vardb.registerCategory( MyCategory('DataMC_OS_ttbar_ElEl',    cut = vardb.getCuts(['2Lep_NLep','2Lep_pT_Relaxed','TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_ElEl_Event','TT','2Lep_ElEtaCut','4Lep_NJets','2Lep_NBJet','2Lep_Zsidescut','2Lep_Zmincut','2Lep_OS']), weight = weight_SR_CR ) )
        vardb.registerCategory( MyCategory('DataMC_OS_ttbar_OF',      cut = vardb.getCuts(['2Lep_NLep','2Lep_pT_Relaxed','TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_OF_Event','TT','2Lep_ElEtaCut','4Lep_NJets','2Lep_NBJet','2Lep_Zsidescut','2Lep_Zmincut','2Lep_OS']), weight = weight_SR_CR ) )

        # SS ttbar (ee,mumu,emu)

        vardb.registerCategory( MyCategory('DataMC_SS_ttbar',        cut = vardb.getCuts(['2Lep_NLep','2Lep_pT_Relaxed','TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_NJet_CR_SStt','TT','2Lep_ElEtaCut','OneBJet','2Lep_SS','2Lep_Zmincut']), weight = weight_SR_CR ) )

    # --------------------------------------------
    # Full breakdown of cuts for cutflow challenge
    # --------------------------------------------

    if doCFChallenge:

        weight_CFC    = "lepSFObjTight * lepSFTrigTight * tauSFTight * JVT_EventWeight * MV2c10_70_EventWeight"
        weight_CFC_MM = "tauSFTight * JVT_EventWeight * MV2c10_70_EventWeight"

        if "MM" in args.channel:

            basecutlist_CFC_MM = []

            cat_name = "CFChallenge_2Lep_MMRates_"

            # NB: here order of cuts is important b/c they will be applied on top of each other

            basecutlistnames_CFC_MM = [
                                 ["TrigDec","1.0"],
                                 ["2Lep_NLep","1.0"],
                                 ["2Lep_pT_MMRates","1.0"]
                                 ["2Lep_TrigMatch","1.0"],
                                 ["TauVeto","1.0"],
                                 ["2Lep_NBJet","1.0"]
                                 ["2Lep_ElEtaCut","1.0"],
                                 ["2Lep_NJet_CR","1.0"],
                                 ["2Lep_LepTagTightTrigMatched", weight_CFC_MM + " * weight_tag"]
                                     ]

            # CF Challenge for MM efficiency measurement

            for cut in basecutlistnames_CFC_MM:
                vardb.registerCategory( MyCategory(cat_name + cut[0],    cut = vardb.getCuts( appended( basecutlist_CFC_MM, cut[0] ) ), weight = cut[1] ) )

            vardb.registerCategory( MyCategory(cat_name + 'OS',                     cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_OS']), weight = ( weight_CFC_MM + " * weight_tag" ) ) )
            vardb.registerCategory( MyCategory(cat_name + 'OS_OF',                  cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_OS','2Lep_OF_Event']), weight = ( weight_CFC_MM + " * weight_tag" ) ) )
            vardb.registerCategory( MyCategory(cat_name + 'OS_ProbeElT',            cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_OS','2Lep_OF_Event','2Lep_ElProbe','2Lep_ProbeTight']), weight = ( weight_CFC_MM + " * weight_tag * weight_probe" ) ) )
            vardb.registerCategory( MyCategory(cat_name + 'OS_ProbeMuT',            cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_OS','2Lep_OF_Event','2Lep_MuProbe','2Lep_ProbeTight']), weight = ( weight_CFC_MM + " * weight_tag * weight_probe" )  ) )
            vardb.registerCategory( MyCategory(cat_name + 'OS_ProbeElAntiT',        cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_OS','2Lep_OF_Event','2Lep_ElProbe','2Lep_ProbeAntiTight']), weight = ( weight_CFC_MM + " * weight_tag * weight_probe" )  ) )
            vardb.registerCategory( MyCategory(cat_name + 'OS_ProbeMuAntiT',        cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_OS','2Lep_OF_Event','2Lep_MuProbe','2Lep_ProbeAntiTight']), weight = ( weight_CFC_MM + " * weight_tag * weight_probe" ) ) )

            vardb.registerCategory( MyCategory(cat_name + 'SS',                     cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_SS']), weight = ( weight_CFC_MM + " * weight_tag" ) ) )
            vardb.registerCategory( MyCategory(cat_name + 'SS_Zmin',                cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_SS','2Lep_Zmincut']), weight = ( weight_CFC_MM + " * weight_tag" ) ) )
            vardb.registerCategory( MyCategory(cat_name + 'SS_Zveto',               cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_SS','2Lep_Zmincut','2Lep_Zsidescut']), weight = ( weight_CFC_MM + " * weight_tag" ) ) )
            vardb.registerCategory( MyCategory(cat_name + 'SS_ProbeElT',            cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_SS','2Lep_Zmincut','2Lep_Zsidescut','2Lep_ElProbe','2Lep_ProbeTight']), weight = ( weight_CFC_MM + " * weight_tag * weight_probe" ) ) )
            vardb.registerCategory( MyCategory(cat_name + 'SS_ProbeMuT',            cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_SS','2Lep_Zmincut','2Lep_Zsidescut','2Lep_MuMu_Event','2Lep_MuProbe','2Lep_ProbeTight']), weight = ( weight_CFC_MM + " * weight_tag * weight_probe" ) ) )
            vardb.registerCategory( MyCategory(cat_name + 'SS_ProbeElAntiT',        cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_SS','2Lep_Zmincut','2Lep_Zsidescut','2Lep_ElProbe','2Lep_ProbeAntiTight']), weight = ( weight_CFC_MM + " * weight_tag * weight_probe" ) ) )
            vardb.registerCategory( MyCategory(cat_name + 'SS_ProbeMuAntiT',        cut = basecutlist_CFC_MM & vardb.getCuts(['2Lep_SS','2Lep_Zmincut','2Lep_Zsidescut','2Lep_MuMu_Event','2Lep_MuProbe','2Lep_ProbeAntiTight']), weight = ( weight_CFC_MM + " * weight_tag * weight_probe" ) ) )

        if "2LepSS" in args.channel:

            cutlist_CFC_2Lep = []

            cat_name = "CFChallenge_2LepSS0Tau_SR_DataDriven_"

            # NB: here order of cuts is important b/c they will be applied on top of each other

            cutlistnames_CFC_2Lep = [
                                 ["TrigDec",weight_CFC],
                                 ["2Lep_NLep",weight_CFC],
                                 ["TT",weight_CFC],
                                 ["2Lep_TrigMatch",weight_CFC],
                                 ["2Lep_SS",weight_CFC],
                                 ["2Lep_pT",weight_CFC],
                                 ["2Lep_ElEtaCut",weight_CFC],
                                 ["TauVeto",weight_CFC],
                                 ["2Lep_NJet_SR",weight_CFC],
                                 ["2Lep_NBJet_SR",weight_CFC]
                                    ]

            for cut in cutlistnames_CFC_2Lep:
                vardb.registerCategory( MyCategory(cat_name + cut[0],    cut = vardb.getCuts( appended( cutlist_CFC_2Lep, cut[0] ) ), weight = cut[1] ) )
                print("registering category:\t{0}".format(cat_name+cut[0]) + " - defined by cuts: [" + ",".join( "\'{0}\'".format(c) for c in cutlist_CFC_2Lep ) + "] - weight : \'{0}\'".format(cut[1]))


        if "2LepSS1Tau" in args.channel:

            cutlist_CFC_2Lep1Tau = []

            cat_name = "CFChallenge_2LepSS1Tau_"

            # NB: here order of cuts is important b/c they will be applied on top of each other

            cutlistnames_CFC_2Lep1Tau = [
                                 ["2Lep1Tau_NLep",weight_CFC],
                                 ["2Lep1Tau_TightLeptons",weight_CFC],
                                 ["2Lep1Tau_pT",weight_CFC],
                                 ["2Lep1Tau_TrigMatch",weight_CFC],
                                 ["2Lep1Tau_SS",weight_CFC],
                                 ["2Lep1Tau_1Tau",weight_CFC],
                                 ["2Lep1Tau_Zsidescut",weight_CFC],
                                 ["2Lep1Tau_NJet_SR",weight_CFC],
                                 ["2Lep1Tau_NBJet",weight_CFC],
                                    ]

            for cut in cutlistnames_CFC_2Lep1Tau:
                vardb.registerCategory( MyCategory(cat_name + cut[0],    cut = vardb.getCuts( appended( cutlist_CFC_2Lep1Tau, cut[0] ) ), weight = cut[1] ) )
                print("registering category:\t{0}".format(cat_name+cut[0]) + " - defined by cuts: [" + ",".join( "\'{0}\'".format(c) for c in cutlist_CFC_2Lep1Tau ) + "] - weight : \'{0}\'".format(cut[1]))


        if "3Lep" in args.channel:

            cutlist_CFC_3Lep = []

            cat_name = "CFChallenge_2LepSS1Tau_"

            # NB: here order of cuts is important b/c they will be applied on top of each other

            cutlistnames_CFC_3Lep = [
                                 ["3Lep_NLep",weight_CFC],
                                 ["3Lep_Charge",weight_CFC],
                                 ["3Lep_TightLeptons",weight_CFC],
                                 ["3Lep_pT",weight_CFC],
                                 ["3Lep_TrigMatch",weight_CFC],
                                 ["3Lep_ZVeto",weight_CFC],
                                 ["3Lep_MinZCut",weight_CFC],
                                 ["3Lep_NJets",weight_CFC],
                                    ]

            for cut in cutlistnames_CFC_3Lep:
                vardb.registerCategory( MyCategory(cat_name + cut[0],    cut = vardb.getCuts( appended( cutlist_CFC_3Lep, cut[0] ) ), weight = cut[1] ) )
                print("registering category:\t{0}".format(cat_name+cut[0]) + " - defined by cuts: [" + ",".join( "\'{0}\'".format(c) for c in cutlist_CFC_3Lep ) + "] - weight : \'{0}\'".format(cut[1]))


    # ----------------------------------------------
    # CRs where r/f rates for MM method are measured
    # ----------------------------------------------

    if "MMRates" in args.channel:

        # ----------------------
	# Tag & Probe selection
        # ----------------------

        if "TP" in args.channel:

            el_tag   = mu_tag   = "lep_Tag_"
            el_probe = mu_probe = "lep_Probe_"

            if "SUSY_TP" in args.channel: # Use vector branches!
                el_tag   = "electron_TagVec_"
                el_probe = "electron_ProbeVec_"
                mu_tag   = "muon_TagVec_"
                mu_probe = "muon_ProbeVec_"
                # NB: uncomment this if you want to see the fake probe truth type/origin in SS CR
                #if "FAKE_EFF" in args.efficiency:
                #    el_tag   = mu_tag   = "lep_Tag_"
                #    el_probe = mu_probe = "lep_Probe_"

            if "SLT" in args.trigger:
                el_tag   += "SLT_"
                mu_tag   += "SLT_"
                el_probe += "SLT_"
                mu_probe += "SLT_"
            elif "DLT" in args.trigger:
                el_tag   += "DLT_"
                mu_tag   += "DLT_"
                el_probe += "DLT_"
                mu_probe += "DLT_"

            # ---------------------------------------
            # Special plots for MM real/fake eff CRs
            # ---------------------------------------

            vardb.registerVar( Variable(shortname = "ElProbePt", latexname = "p_{T}^{probe e} [GeV]", ntuplename = el_probe + "Pt/1e3", bins = 40, minval = 10.0, maxval = 210.0,) )
            #vardb.registerVar( Variable(shortname = "ElProbeEta",latexname = "#eta^{probe e}", ntuplename = "TMath::Abs( " + el_probe + "EtaBE2 )", bins = 26, minval = 0.0,  maxval = 2.6) )
            #vardb.registerVar( Variable(shortname = "ElProbeDistanceClosestBJet", latexname = '#DeltaR(probe e, closest b-jet)', ntuplename = el_probe + "deltaRClosestBJet", bins = 20, minval = 0.0, maxval = 5.0) )
            #vardb.registerVar( Variable(shortname = "ElProbed0sig", latexname = "|d_{0}^{sig}| probe e", ntuplename = "TMath::Abs(" + el_probe + "sigd0PV)", bins = 40, minval = 0.0, maxval = 10.0,) )
            #vardb.registerVar( Variable(shortname = "ElProbez0sintheta", latexname = "|z_{0}*sin(#theta)| probe e [mm]", ntuplename = "TMath::Abs(" + el_probe + "Z0SinTheta)", bins = 15, minval = 0.0, maxval = 1.5,) )
            #vardb.registerVar( Variable(shortname = "ElProbePtFakeRebinned", latexname = "p_{T}^{probe e} [GeV]", ntuplename = el_probe + "Pt/1e3", bins = 40, minval = 10.0, maxval = 210.0, manualbins = [10,15,20,25,40,200,210]) )
            #vardb.registerVar( Variable(shortname = "ElProbePtRealRebinned", latexname = "p_{T}^{probe e} [GeV]", ntuplename = el_probe + "Pt/1e3", bins = 40, minval = 10.0, maxval = 210.0, manualbins = [10,15,20,25,30,40,60,200,210]) )
            #vardb.registerVar( Variable(shortname = "ElProbeNJets", latexname = "Jet multiplicity", ntuplename = "nJets_OR_T", bins = 8, minval = 2, maxval = 10, weight = "JVT_EventWeight") )
            #if any( e in args.efficiency for e in ["FAKE_EFF","ALL_EFF"] ):
            #    vardb.registerVar( Variable(shortname = "ElProbeType", latexname = "truthType^{probe e}", ntuplename = el_probe + "truthType", bins = 41, minvalX = -0.5, maxvalX = 40.5, manualbins = range(0,41) ) )
            #    vardb.registerVar( Variable(shortname = 'ElProbeType_VS_ElProbeOrigin', latexnameX = 'truthType^{probe e}', latexnameY = 'truthOrigin^{probe e}', ntuplename = el_probe + "truthOrigin" + ":" + el_probe + "truthType", binsX = 21, minvalX = -0.5, maxvalX = 20.5, binsY = 41, minvalY = -0.5, maxvalY = 40.5, typeval = TH2D) )
            #    vardb.registerVar( Variable(shortname = 'ElProbeType_VS_ElProbeOrigin', latexnameX = 'truthType^{probe e}', latexnameY = 'truthOrigin^{probe e}', ntuplename = el_probe + "truthOrigin" + ":" + el_probe + "truthType", binsX = 41, minvalX = -0.5, maxvalX = 40.5, binsY = 46, minvalY = -0.5, maxvalY = 45.5, typeval = TH2D) )
            #    #vardb.registerVar( Variable(shortname = 'ElProbeType_VS_ElProbePt', latexnameX = 'truthType^{probe e}', latexnameY = 'p_{T}^{probe e} [GeV]', ntuplename = el_probe + "truthType" + ":" + el_probe + "Pt/1e3", binsX = 41, minvalX = -0.5, maxvalX = 40.5, binsY = 40, minvalY = 10.0, maxvalY = 210.0, typeval = TH2D) )
            #
            #vardb.registerVar( Variable(shortname = "ElTagPt", latexname = "p_{T}^{tag e} [GeV]", ntuplename = el_tag + "Pt/1e3", bins = 40, minval = 10.0, maxval = 210.0,) )
            #vardb.registerVar( Variable(shortname = "ElTagEta", latexname = "#eta^{tag e}", ntuplename = "TMath::Abs( " + el_tag + "EtaBE2 )",bins = 8, minval = 0.0,  maxval = 2.6) )
            #vardb.registerVar( Variable(shortname = "ElTagDistanceClosestBJet", latexname = '#DeltaR(tag e, closest b-jet)', ntuplename = el_tag + "deltaRClosestBJet", bins = 20, minval = 0.0, maxval = 5.0) )
            #vardb.registerVar( Variable(shortname = 'ElTagType_VS_ElTagOrigin', latexnameX = 'truthType^{tag e}', latexnameY = 'truthOrigin^{tag e}', ntuplename = el_tag + "truthOrigin" + ":" + el_tag + "truthType", binsX = 41, minvalX = -0.5, maxvalX = 40.5, binsY = 46, minvalY = -0.5, maxvalY = 45.5, typeval = TH2D) )
            #
            #vardb.registerVar( Variable(shortname = 'ElTagPt_VS_ElProbePt', latexnameX = 'p_{T}^{tag e} [GeV]', latexnameY = 'p_{T}^{probe e} [GeV]', ntuplename = el_probe + "Pt/1e3" + ":" + el_tag + "Pt/1e3", binsX = 40, minvalX = 10.0, maxvalX = 210.0, binsY = 40, minvalY = 10.0, maxvalY = 210.0, typeval = TH2D) )
            #vardb.registerVar( Variable(shortname = "ElTagDistanceClosestBJet_VS_ElProbeDistanceClosestBJet", latexnameX = '#DeltaR(tag e, closest b-jet)', latexnameY = '#DeltaR(probe e, closest b-jet)', ntuplename = el_probe + "deltaRClosestBJet" + ":" + el_tag + "deltaRClosestBJet", binsX = 20, minvalX = 0.0, maxvalX = 5.0, binsY = 20, minvalY = 0.0, maxvalY = 5.0, typeval = TH2D) )
            #vardb.registerVar( Variable(shortname = "ElTagMassClosestBJet_VS_ElProbeMassClosestBJet", latexnameX = 'm(tag e, closest b-jet) [GeV]', latexnameY = 'm(probe e, closest b-jet) [GeV]', ntuplename = el_probe + "massClosestBJet/1e3" + ":" + el_tag + "massClosestBJet/1e3", binsX = 20, minvalX = 0.0, maxvalX = 200.0, binsY = 20, minvalY = 0.0, maxvalY = 200.0, typeval = TH2D) )

            vardb.registerVar( Variable(shortname = "MuProbePt", latexname = "p_{T}^{probe #mu} [GeV]", ntuplename = mu_probe + "Pt/1e3", bins = 40, minval = 10.0, maxval = 210.0) )
            #vardb.registerVar( Variable(shortname = "MuProbeEta", latexname = "#eta^{probe #mu}", ntuplename = "TMath::Abs( " + mu_probe + "Eta )", bins = 25, minval = 0.0, maxval = 2.5) )
            #vardb.registerVar( Variable(shortname = "MuProbeDistanceClosestBJet", latexname = '#DeltaR(probe #mu, closest b-jet)', ntuplename = mu_probe + "deltaRClosestBJet", bins = 20, minval = 0.0, maxval = 5.0) )
            #vardb.registerVar( Variable(shortname = "MuProbed0sig", latexname = "|d_{0}^{sig}| mu_probe #mu", ntuplename = "TMath::Abs(" + mu_probe + "sigd0PV)", bins = 40, minval = 0.0, maxval = 10.0,) )
            #vardb.registerVar( Variable(shortname = "MuProbez0sintheta", latexname = "|z_{0}*sin(#theta)| mu_probe #mu [mm]", ntuplename = "TMath::Abs(" + mu_probe + "Z0SinTheta)", bins = 15, minval = 0.0, maxval = 1.5,) )
            #vardb.registerVar( Variable(shortname = "MuProbePtFakeRebinned", latexname = "p_{T}^{probe #mu} [GeV]", ntuplename = mu_probe + "Pt/1e3", bins = 40, minval = 10.0, maxval = 210.0, manualbins = [10,15,20,25,200,210]) )
            #vardb.registerVar( Variable(shortname = "MuProbePtRealRebinned", latexname = "p_{T}^{probe #mu} [GeV]", ntuplename = mu_probe + "Pt/1e3", bins = 40, minval = 10.0, maxval = 210.0, manualbins = [10,15,20,25,200,210]) )
            #vardb.registerVar( Variable(shortname = "MuProbeNJets", latexname = "Jet multiplicity", ntuplename = "nJets_OR_T", bins = 8, minval = 2, maxval = 10, weight = "JVT_EventWeight") )
            #if any( e in args.efficiency for e in ["FAKE_EFF","ALL_EFF"] ):
            #    vardb.registerVar( Variable(shortname = "MuProbeType", latexname = "truthType^{probe #mu}", ntuplename = mu_probe + "truthType", bins = 41, minvalX = -0.5, maxvalX = 40.5, manualbins = range(0,41) ) )
            #    vardb.registerVar( Variable(shortname = 'MuProbeType_VS_MuProbeOrigin', latexnameX = 'truthType^{probe #mu}', latexnameY = 'truthOrigin^{probe #mu}', ntuplename = mu_probe + "truthOrigin" + ":" + mu_probe + "truthType", binsX = 21, minvalX = -0.5, maxvalX = 20.5, binsY = 41, minvalY = -0.5, maxvalY = 40.5, typeval = TH2D) )
            #    vardb.registerVar( Variable(shortname = 'MuProbeType_VS_MuProbeOrigin', latexnameX = 'truthType^{probe #mu}', latexnameY = 'truthOrigin^{probe #mu}', ntuplename = mu_probe + "truthOrigin" + ":" + mu_probe + "truthType", binsX = 41, minvalX = -0.5, maxvalX = 40.5, binsY = 46, minvalY = -0.5, maxvalY = 45.5, typeval = TH2D) )
            #    #vardb.registerVar( Variable(shortname = 'MuProbeType_VS_MuProbePt', latexnameX = 'truthType^{probe #mu}', latexnameY = 'p_{T}^{probe #mu} [GeV]', ntuplename = mu_probe + "truthType" + ":" + mu_probe + "Pt/1e3", binsX = 41, minvalX = -0.5, maxvalX = 40.5, binsY = 40, minvalY = 10.0, maxvalY = 210.0, typeval = TH2D) )
            #
            #vardb.registerVar( Variable(shortname = "MuTagPt", latexname = "p_{T}^{tag #mu} [GeV]", ntuplename = mu_tag + "Pt/1e3", bins = 40, minval = 10.0, maxval = 210.0,) )
            #vardb.registerVar( Variable(shortname = "MuTagEta", latexname = "#eta^{tag #mu}", ntuplename = "TMath::Abs( " + mu_tag + "Eta )", bins = 8,  minval = 0.0, maxval = 2.5) )
            #vardb.registerVar( Variable(shortname = "MuTagDistanceClosestBJet", latexname = '#DeltaR(tag #mu, closest b-jet)', ntuplename = mu_tag + "deltaRClosestBJet", bins = 20, minval = 0.0, maxval = 5.0) )
            #vardb.registerVar( Variable(shortname = 'MuTagType_VS_MuTagOrigin', latexnameX = 'truthType^{tag #mu}', latexnameY = 'truthOrigin^{tag #mu}', ntuplename = mu_tag + "truthOrigin" + ":" + mu_tag + "truthType", binsX = 41, minvalX = -0.5, maxvalX = 40.5, binsY = 46, minvalY = -0.5, maxvalY = 45.5, typeval = TH2D) )
            #
            #vardb.registerVar( Variable(shortname = 'MuTagPt_VS_MuProbePt', latexnameX = 'p_{T}^{tag #mu} [GeV]', latexnameY = 'p_{T}^{probe #mu} [GeV]', ntuplename = mu_probe + "Pt/1e3" + ":" + mu_tag + "Pt/1e3", binsX = 40, minvalX = 10.0, maxvalX = 210.0, binsY = 40, minvalY = 10.0, maxvalY = 210.0, typeval = TH2D) )
            #vardb.registerVar( Variable(shortname = "MuTagDistanceClosestBJet_VS_MuProbeDistanceClosestBJet", latexnameX = '#DeltaR(tag #mu, closest b-jet)', latexnameY = '#DeltaR(probe #mu, closest b-jet)', ntuplename = mu_probe + "deltaRClosestBJet" + ":" + mu_tag + "deltaRClosestBJet", binsX = 20, minvalX = 0.0, maxvalX = 5.0, binsY = 20, minvalY = 0.0, maxvalY = 5.0, typeval = TH2D) )
            #vardb.registerVar( Variable(shortname = "MuTagMassClosestBJet_VS_MuProbeMassClosestBJet", latexnameX = 'm(tag #mu, closest b-jet) [GeV]', latexnameY = 'm(probe #mu, closest b-jet) [GeV]', ntuplename = mu_probe + "massClosestBJet/1e3" + ":" + mu_tag + "massClosestBJet/1e3", binsX = 20, minvalX = 0.0, maxvalX = 200.0, binsY = 20, minvalY = 0.0, maxvalY = 200.0, typeval = TH2D) )

            # -----------------------------------------------------------------------------------------------------------------
            # MC subtraction: what gets plotted will be subtracted to data:
            #
            # -) Real OS CR:
            #
            # ---> events where PROBE is !prompt (aka, a fake or QMisID (negligible) or photon conv)
            # This removes events where the probe is a fake lepton.
            # This procedure can be questioned, as we'd be trusting MC for the fakes...
            # However, for a ttbar-dominated OS CR, the fake contamination is pretty low, and mostly @ low pT ( < 25 GeV ), so we could forget about the bias...
            #
            # -) Fake SS CR:
            #
            # ---> events where PROBE is prompt
            # This removes ttV,VV, rare top, and events where the probe was mis-assigned (i.e, we picked the real lepton in the pair rather than the fake)
            # The MC subtraction here is justified, as we can trust MC at modeling prompts.
            #
            # ---> all events w/ at least one QMisID
            # By default we use the data-driven charge flip estimate. To use MC charge flips, use appropriate command-line option.
            # When using DD QMisID, we need to veto in MC all events w/ at least one (truth) QMisID, to avoid double subtraction (since ttV, VV might have QMisID leptons)

            truth_sub_OS = vardb.getCut('2Lep_TRUTH_ProbeNonPromptOrQMisIDEvent')
            truth_sub_SS = vardb.getCut('2Lep_TRUTH_ProbePromptEvent') & vardb.getCut('2Lep_TRUTH_QMisIDVeto')

            if "SUSY_TP" in args.channel:
                truth_sub_OS = vardb.getCut('2Lep_TRUTH_NonPromptEvent') | vardb.getCut('2Lep_TRUTH_QMisIDEvent')

            if "DATAMC" in args.channel:

            	# Plot all MC, except for QMisID (as we estimate them separately using DD/MC)

            	truth_sub_OS = truth_sub_SS = vardb.getCut('2Lep_TRUTH_QMisIDVeto')

                # NB: uncomment this if you want to see the fake probe truth type/origin in SS CR
                # In SS CR, plot events where probe lepton is fake, and not QMisID

                #truth_sub_SS = truth_sub_SS & vardb.getCut('2Lep_TRUTH_ProbeNonPromptEvent')

            # ------------------------------------------------------------
            # Closure test: truth selection in MC for Real/Fake OS/SS CRs:
            # ------------------------------------------------------------
            #
            # 1.
            # REAL CR: select events w/ only prompt leptons, and veto on charge flips.
            #
            # 2.
            # FAKE CR: select events w/ at least one non-prompt lepton, and veto on charge flips.

            if ( "CLOSURE" in args.channel or args.ratesMC ) :

            	truth_sub_OS = vardb.getCut('2Lep_TRUTH_PurePromptEvent') # Both leptons be real ( and none is QMisID )
                truth_sub_SS = vardb.getCut('2Lep_TRUTH_NonPromptEvent')  # At least one lepton is fake ( and none is QMisID ). NB: w/ this cut, the fake could be either the tag or the probe.
                # This is what we did for ICHEP:
                if ( "TRUTH_ON_PROBE" in args.channel ):
                    truth_sub_SS = vardb.getCut('2Lep_TRUTH_ProbeNonPromptEvent') # Probe lepton is fake, and not QMisID

                # Use this truth cut if T&P was defined at truth level in skimming code.
		# Simply ensure event is not "bad" and nothing else ( !bad = RR (OS), RF||FR (SS, QMisID vetoed) ).

		if "TRUTH_TP" in args.channel:
		    truth_sub_OS = truth_sub_SS = vardb.getCut("2Lep_TagAndProbe_GoodEvent")

            	if ( args.doQMisIDRate ):
            	    print ("\n\Measuring efficiency/rate for QMisID leptons in MC!\n")
            	    truth_sub_SS = vardb.getCut('2Lep_TRUTH_ProbeQMisIDEvent')

                # --------------------------------------------
                # Fake probe assignment efficiency
                # (Make sure all events w/ QMisID are removed)
                # --------------------------------------------

                fake_match_cut = vardb.getCut('2Lep_TRUTH_ProbeNonPromptEvent')  # Require probe to be fake
                real_match_cut = -vardb.getCut('2Lep_TRUTH_ProbeNonPromptEvent') # Require probe to be !fake

                probe_sel_cut = vardb.getCuts(['2Lep_ProbeTight','2Lep_LepProbeTrigMatched']) # This selects only ambiguous events w/ both leptons T & TM
                #probe_sel_cut = vardb.getCut('DummyCut')                                     # This selects any event (remembering that the tag lepton is always required to be T & TM)


            # ------------------------------------------
            # Define common event weight and common cuts
            # ------------------------------------------

            weight_TP_MM = "tauSFTight * JVT_EventWeight * MV2c10_70_EventWeight * weight_tag"

            cc_list = ['TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_LepTagTightTrigMatched','2Lep_NBJet','2Lep_NLep','2Lep_pT_MMRates','TauVeto','2Lep_NJet_CR','2Lep_ElEtaCut','2Lep_Zsidescut','2Lep_Zmincut']

            if "TRIGMATCH_EFF" in args.channel:
            	cc_list.append('2Lep_LepProbeTrigMatched')
            elif "NOT_TRIGMATCH_EFF" in args.channel:
            	cc_list.append('2Lep_LepProbeAntiTrigMatched')

            common_cuts = vardb.getCuts(cc_list)

            # --------------------------
            # Define the control regions
            # --------------------------

            if ( args.lepFlavComp == "TEST" ):

                # Test something similar to SUSY SS analysis:

            	# Real CR: OF only

                if any( e in args.efficiency for e in ["REAL_EFF","ALL_EFF"] ):
                    vardb.registerCategory( MyCategory('RealCRMuL',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_OF_Event']) & truth_sub_OS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('RealCRMuAntiT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_OF_Event','2Lep_ProbeAntiTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRMuT',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_OF_Event','2Lep_ProbeTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRElL',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_OF_Event']) & truth_sub_OS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('RealCRElAntiT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_OF_Event','2Lep_ProbeAntiTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRElT',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_OF_Event','2Lep_ProbeTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )

            	# Fake CR: OF for electrons (w/ tag *always* muon), SF for muons

                if any( e in args.efficiency for e in ["FAKE_EFF","ALL_EFF"] ):
                    vardb.registerCategory( MyCategory('FakeCRMuL',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_MuMu_Event']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRMuAntiT', cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_MuMu_Event','2Lep_ProbeAntiTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRMuT',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_MuMu_Event','2Lep_ProbeTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRElL',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuTag','2Lep_TagVeryTightSelected','2Lep_ElProbe','2Lep_OF_Event']) & truth_sub_SS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('FakeCRElAntiT', cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuTag','2Lep_TagVeryTightSelected','2Lep_ElProbe','2Lep_OF_Event','2Lep_ProbeAntiTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRElT',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuTag','2Lep_TagVeryTightSelected','2Lep_ElProbe','2Lep_OF_Event','2Lep_ProbeTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )

                if "CLOSURE" in args.channel:

                    # Probe fake assignment efficiency

                    #"""
                    midstr = "ProbeTMatchedTo"
                    vardb.registerCategory( MyCategory('FakeCRMu' + midstr + 'Fake', cut = probe_sel_cut & fake_match_cut & common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_MuMu_Event']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRMu' + midstr + 'Real', cut = probe_sel_cut & real_match_cut & common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_MuMu_Event']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRMu' + midstr + 'Any',  cut = probe_sel_cut & common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_MuMu_Event']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCREl' + midstr + 'Fake', cut = probe_sel_cut & fake_match_cut & common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuTag','2Lep_TagVeryTightSelected','2Lep_ElProbe','2Lep_OF_Event']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCREl' + midstr + 'Real', cut = probe_sel_cut & real_match_cut & common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuTag','2Lep_TagVeryTightSelected','2Lep_ElProbe','2Lep_OF_Event']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCREl' + midstr + 'Any',  cut = probe_sel_cut & common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuTag','2Lep_TagVeryTightSelected','2Lep_ElProbe','2Lep_OF_Event']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    #"""

            if ( args.lepFlavComp == "ICHEP_2016" ): # Real CR: OF, Fake CR: INCLUSIVE(el), SF(mu)

                if any( e in args.efficiency for e in ["REAL_EFF","ALL_EFF"] ):
                    vardb.registerCategory( MyCategory('RealCRMuL',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_OF_Event']) & truth_sub_OS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('RealCRMuAntiT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_OF_Event','2Lep_ProbeAntiTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRMuT',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_OF_Event','2Lep_ProbeTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRElL',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_OF_Event']) & truth_sub_OS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('RealCRElAntiT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_OF_Event','2Lep_ProbeAntiTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRElT',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_OF_Event','2Lep_ProbeTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                if any( e in args.efficiency for e in ["FAKE_EFF","ALL_EFF"] ):
                    vardb.registerCategory( MyCategory('FakeCRMuL',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_MuMu_Event']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRMuAntiT', cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_MuMu_Event','2Lep_ProbeAntiTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRMuT',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_MuMu_Event','2Lep_ProbeTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRElL',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElProbe']) & truth_sub_SS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('FakeCRElAntiT', cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElProbe','2Lep_ProbeAntiTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRElT',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElProbe','2Lep_ProbeTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )

            if ( args.lepFlavComp == "INCLUSIVE" ): # combine OF + SF

                if any( e in args.efficiency for e in ["REAL_EFF","ALL_EFF"] ):
                    vardb.registerCategory( MyCategory('RealCRMuL',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe']) & truth_sub_OS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('RealCRMuAntiT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_ProbeAntiTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRMuT',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_ProbeTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRElL',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe']) & truth_sub_OS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('RealCRElAntiT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_ProbeAntiTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRElT',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_ProbeTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                if any( e in args.efficiency for e in ["FAKE_EFF","ALL_EFF"] ):
                    vardb.registerCategory( MyCategory('FakeCRMuL',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRMuAntiT', cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_ProbeAntiTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRMuT',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_ProbeTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRElL',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElProbe']) & truth_sub_SS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('FakeCRElAntiT', cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElProbe','2Lep_ProbeAntiTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRElT',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElProbe','2Lep_ProbeTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )

            if ( args.lepFlavComp == "SF" ): # SF only

                if any( e in args.efficiency for e in ["REAL_EFF","ALL_EFF"] ):
                    vardb.registerCategory( MyCategory('RealCRMuL',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_MuMu_Event']) & truth_sub_OS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('RealCRMuAntiT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_MuMu_Event','2Lep_ProbeAntiTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRMuT',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_MuMu_Event','2Lep_ProbeTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRElL',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_ElEl_Event']) & truth_sub_OS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('RealCRElAntiT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_ElEl_Event','2Lep_ProbeAntiTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRElT',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_ElEl_Event','2Lep_ProbeTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                if any( e in args.efficiency for e in ["FAKE_EFF","ALL_EFF"] ):
                    vardb.registerCategory( MyCategory('FakeCRMuL',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_MuMu_Event']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRMuAntiT', cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_MuMu_Event','2Lep_ProbeAntiTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRMuT',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_MuMu_Event','2Lep_ProbeTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRElL',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElProbe','2Lep_ElEl_Event']) & truth_sub_SS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('FakeCRElAntiT', cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElProbe','2Lep_ElEl_Event','2Lep_ProbeAntiTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRElT',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElProbe','2Lep_ElEl_Event','2Lep_ProbeTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )

            if ( args.lepFlavComp == "OF" ): # OF only

                if any( e in args.efficiency for e in ["REAL_EFF","ALL_EFF"] ):
                    vardb.registerCategory( MyCategory('RealCRMuL',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_OF_Event']) & truth_sub_OS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('RealCRMuAntiT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_OF_Event','2Lep_ProbeAntiTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRMuT',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuProbe','2Lep_OF_Event','2Lep_ProbeTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRElL',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_OF_Event']) & truth_sub_OS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('RealCRElAntiT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_OF_Event','2Lep_ProbeAntiTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('RealCRElT',     cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElProbe','2Lep_OF_Event','2Lep_ProbeTight']) & truth_sub_OS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                if any( e in args.efficiency for e in ["FAKE_EFF","ALL_EFF"] ):
                    vardb.registerCategory( MyCategory('FakeCRMuL',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_OF_Event']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRMuAntiT', cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_OF_Event','2Lep_ProbeAntiTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRMuT',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuProbe','2Lep_OF_Event','2Lep_ProbeTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRElL',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElProbe','2Lep_OF_Event']) & truth_sub_SS, weight = weight_TP_MM ) )
                    vardb.registerCategory( MyCategory('FakeCRElAntiT', cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElProbe','2Lep_OF_Event','2Lep_ProbeAntiTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )
                    vardb.registerCategory( MyCategory('FakeCRElT',     cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElProbe','2Lep_OF_Event','2Lep_ProbeTight']) & truth_sub_SS, weight = ( weight_TP_MM + " * weight_probe" ) ) )

        # ------------------------
	# Likelihood fit selection
        # ------------------------

	elif "LH" in args.channel:

            vardb.registerVar( Variable(shortname = 'Lep0Pt_VS_Lep1Pt', latexnameX = 'p_{T}^{lead lep} [GeV]', latexnameY = 'p_{T}^{2nd lead lep} [GeV]', ntuplename = 'lep_Pt_1/1e3:lep_Pt_0/1e3', bins = 40, minval = 10.0, maxval = 210.0, typeval = TH2D) )

            # For measurement in data: select MC events to be subtracted afterwards

            truth_sub_OS = vardb.getCut('2Lep_TRUTH_NonPromptEvent')  # Will subtract events w/ at least one non-prompt, and no QMisID
            truth_sub_SS = vardb.getCut('2Lep_TRUTH_PurePromptEvent') # Will subtract events w/ both prompt leptons, and no QMisID. This assumes QMisID will be estimated independently from data

            # For closure rates
            #
            # Emulate the subtraction w/ a truth selection

            if "CLOSURE" in args.channel:

		truth_sub_OS = vardb.getCut('2Lep_TRUTH_PurePromptEvent') # Both leptons be real ( and no QMisID )
            	truth_sub_SS = vardb.getCut('2Lep_TRUTH_NonPromptEvent')  # At least one lepton is fake, and no QMisID

            cc_list = ['TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_NBJet','2Lep_NLep','2Lep_pT_MMRates','TauVeto','2Lep_NJet_CR','2Lep_ElEtaCut','2Lep_Zsidescut','2Lep_Zmincut']

            if "TRIGMATCH_EFF" in args.channel:
            	cc_list.append('2Lep_BothTrigMatchSLT')
            elif "NOT_TRIGMATCH_EFF" in args.channel:
            	cc_list.append('2Lep_BothAntiTrigMatchSLT')

            common_cuts = vardb.getCuts(cc_list)

            # Real CR - SF

            if ( args.lepFlavComp == "SF" or args.lepFlavComp == "INCLUSIVE" ):

            	vardb.registerCategory( MyCategory('OS_ElEl_TT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElEl_Event','TT']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_ElEl_TL', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElEl_Event','TL']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_ElEl_LT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElEl_Event','LT']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_ElEl_LL', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElEl_Event','LL']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_MuMu_TT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuMu_Event','TT']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_MuMu_TL', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuMu_Event','TL']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_MuMu_LT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuMu_Event','LT']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_MuMu_LL', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuMu_Event','LL']) & truth_sub_OS, weight = weight_SR_CR ) )

            # Real CR - OF

            if ( args.lepFlavComp == "OF" or args.lepFlavComp == "INCLUSIVE" ):

            	vardb.registerCategory( MyCategory('OS_MuEl_TT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuEl_Event','TT']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_ElMu_TT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElMu_Event','TT']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_MuEl_TL', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuEl_Event','TL']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_ElMu_TL', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElMu_Event','TL']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_MuEl_LT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuEl_Event','LT']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_ElMu_LT', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElMu_Event','LT']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_MuEl_LL', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_MuEl_Event','LL']) & truth_sub_OS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('OS_ElMu_LL', cut = common_cuts & vardb.getCuts(['2Lep_OS','2Lep_ElMu_Event','LL']) & truth_sub_OS, weight = weight_SR_CR ) )

            # Fake CR - SF

            if ( args.lepFlavComp == "SF" or args.lepFlavComp == "INCLUSIVE" ):

            	vardb.registerCategory( MyCategory('SS_ElEl_TT',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElEl_Event','TT']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_ElEl_TL',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElEl_Event','TL']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_ElEl_LT',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElEl_Event','LT']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_ElEl_LL',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElEl_Event','LL']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_MuMu_TT',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuMu_Event','TT']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_MuMu_TL',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuMu_Event','TL']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_MuMu_LT',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuMu_Event','LT']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_MuMu_LL',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuMu_Event','LL']) & truth_sub_SS, weight = weight_SR_CR ) )

            # Fake CR - OF

            if ( args.lepFlavComp == "OF" or args.lepFlavComp == "INCLUSIVE" ):

            	vardb.registerCategory( MyCategory('SS_MuEl_TT',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuEl_Event','TT']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_ElMu_TT',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElMu_Event','TL']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_MuEl_TL',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuEl_Event','LT']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_ElMu_TL',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElMu_Event','LL']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_MuEl_LT',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuEl_Event','TT']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_ElMu_LT',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElMu_Event','TL']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_MuEl_LL',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_MuEl_Event','LT']) & truth_sub_SS, weight = weight_SR_CR ) )
            	vardb.registerCategory( MyCategory('SS_ElMu_LL',    cut = common_cuts & vardb.getCuts(['2Lep_SS','2Lep_ElMu_Event','LL']) & truth_sub_SS, weight = weight_SR_CR ) )


    if doMMClosureTest:

        append_2Lep += "_SR"

        # NB: Plot only events where at least one lepton is !prompt, and none is charge flip

        cc_MMClosure_list = ['TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_NBJet_SR','2Lep_NLep','2Lep_pT','2Lep_SS','TauVeto','2Lep_TRUTH_NonPromptEvent','2Lep_ElEtaCut']

        if "LOWPT" in args.channel:
            cc_MMClosure_list = [ cut.replace('2Lep_pT','2Lep_pT_MMRates') for cut in cc_MMClosure_list ]

        if "ALLNJ" in args.channel:
            append_2Lep += "_AllJet"
            cc_MMClosure_list.append('2Lep_MinNJet')
        elif "HIGHNJ" in args.channel:
            append_2Lep += "_HighJet"
            cc_MMClosure_list.append('2Lep_NJet_SR')
        elif "LOWNJ" in args.channel:
            append_2Lep += "_LowJet"
            cc_MMClosure_list.append('2Lep_NJet_CR')

        append_2Lep += "_DataDriven_Closure"

        common_cuts_MMClosure = vardb.getCuts(cc_MMClosure_list)

        if ( doMM or doFF ):

            if any( cat in args.category for cat in ["mm","ALL"] ): vardb.registerCategory( MyCategory(cat_names_2Lep["mm"] + append_2Lep,  cut = common_cuts_MMClosure & vardb.getCuts(['2Lep_MuMu_Event']), weight = weight_SR_CR ) )
            if any( cat in args.category for cat in ["ee","ALL"] ): vardb.registerCategory( MyCategory(cat_names_2Lep["ee"] + append_2Lep,  cut = common_cuts_MMClosure & vardb.getCuts(['2Lep_ElEl_Event']), weight = weight_SR_CR ) )
            if any( cat in args.category for cat in ["OF","ALL"] ): vardb.registerCategory( MyCategory(cat_names_2Lep["OF"] + append_2Lep,  cut = common_cuts_MMClosure & vardb.getCuts(['2Lep_OF_Event']), weight = weight_SR_CR ) )

        elif ( doTHETA ):

            # NB: for the theta method, the closure test is meaningful only in the OF LowNJ CR, b/c the [SF, LowNJ] CRs are already used to derive the theta factors.

            if "LOWNJ" in args.channel:
                vardb.registerCategory( MyCategory(cat_names_2Lep["OF"] + append_2Lep,  cut = common_cuts_MMClosure & vardb.getCuts(['2Lep_OF_Event']), weight = weight_SR_CR ) )
            else:
                sys.exit("ERROR: closure test for THETA method makes sense only for LOWNJ option (You are currently using {0})".format(args.channel))


    # ---------------------------------------------
    # Sidebands (and SR) used for MM fakes estimate
    # ---------------------------------------------

    if doMMSidebands:

        append_2Lep += "_MMSidebands"

        cc_MMSidebands_list = ['TrigDec','BlindingCut','2Lep_TrigMatch','2Lep_NBJet_SR','2Lep_NLep','2Lep_pT','2Lep_SS','TauVeto','2Lep_ElEtaCut']

        if "CLOSURE" in args.channel:
            # If doing TTBar closure, use a trth cut to require at least 1 fake, and QMisID veto
            cc_MMSidebands_list.append('2Lep_TRUTH_NonPromptEvent')
        else:
            cc_MMSidebands_list.append('2Lep_TRUTH_PurePromptEvent')

        if "ALLNJ" in args.channel:
            append_2Lep += "_AllJet"
        elif "HIGHNJ" in args.channel:
            append_2Lep += "_HighJet"
            cc_MMSidebands_list.append('2Lep_NJet_SR')
        elif "LOWNJ" in args.channel:
            append_2Lep += "_LowJet"
            cc_MMSidebands_list.append('2Lep_NJet_CR')

        common_cuts_MMSidebands = vardb.getCuts(cc_MMSidebands_list)

        if any( cat in args.category for cat in ["mm","ALL"] ):
            vardb.registerCategory( MyCategory(cat_names_2Lep["mm"] + append_2Lep + '_LL',  cut = common_cuts_MMSidebands & vardb.getCuts(['2Lep_MuMu_Event','LL']), weight = weight_SR_CR ) )
            vardb.registerCategory( MyCategory(cat_names_2Lep["mm"] + append_2Lep + '_TL',  cut = common_cuts_MMSidebands & vardb.getCuts(['2Lep_MuMu_Event','TL']), weight = weight_SR_CR ) )
            vardb.registerCategory( MyCategory(cat_names_2Lep["mm"] + append_2Lep + '_LT',  cut = common_cuts_MMSidebands & vardb.getCuts(['2Lep_MuMu_Event','LT']), weight = weight_SR_CR ) )
            vardb.registerCategory( MyCategory(cat_names_2Lep["mm"] + append_2Lep + '_TT',  cut = common_cuts_MMSidebands & vardb.getCuts(['2Lep_MuMu_Event','TT']), weight = weight_SR_CR ) )

        if any( cat in args.category for cat in ["ee","ALL"] ):
            vardb.registerCategory( MyCategory(cat_names_2Lep["ee"] + append_2Lep + '_LL',  cut = common_cuts_MMSidebands & vardb.getCuts(['2Lep_ElEl_Event','LL']), weight = weight_SR_CR ) )
            vardb.registerCategory( MyCategory(cat_names_2Lep["ee"] + append_2Lep + '_TL',  cut = common_cuts_MMSidebands & vardb.getCuts(['2Lep_ElEl_Event','TL']), weight = weight_SR_CR ) )
            vardb.registerCategory( MyCategory(cat_names_2Lep["ee"] + append_2Lep + '_LT',  cut = common_cuts_MMSidebands & vardb.getCuts(['2Lep_ElEl_Event','LT']), weight = weight_SR_CR ) )
            vardb.registerCategory( MyCategory(cat_names_2Lep["ee"] + append_2Lep + '_TT',  cut = common_cuts_MMSidebands & vardb.getCuts(['2Lep_ElEl_Event','TT']), weight = weight_SR_CR ) )

        if any( cat in args.category for cat in ["OF","ALL"] ):
            vardb.registerCategory( MyCategory(cat_names_2Lep["OF"] + append_2Lep + '_LL',  cut = common_cuts_MMSidebands & vardb.getCuts(['2Lep_OF_Event','LL']), weight = weight_SR_CR ) )
            vardb.registerCategory( MyCategory(cat_names_2Lep["OF"] + append_2Lep + '_TL',  cut = common_cuts_MMSidebands & vardb.getCuts(['2Lep_OF_Event','TL']), weight = weight_SR_CR ) )
            vardb.registerCategory( MyCategory(cat_names_2Lep["OF"] + append_2Lep + '_LT',  cut = common_cuts_MMSidebands & vardb.getCuts(['2Lep_OF_Event','LT']), weight = weight_SR_CR ) )
            vardb.registerCategory( MyCategory(cat_names_2Lep["OF"] + append_2Lep + '_TT',  cut = common_cuts_MMSidebands & vardb.getCuts(['2Lep_OF_Event','TT']), weight = weight_SR_CR ) )

    # --------------------------------------------------------
    # TTHBackgrounds is the class used to manage each process:
    #
    #   Pass the input informations and the definitions and it
    #   will perform the background estimation
    # --------------------------------------------------------

    ttH = TTHBackgrounds(inputs, vardb)

    # ------------------------------------
    # Set the integrated luminosity (fb-1)
    # ------------------------------------

    ttH.luminosity = args.lumi

    ttH.lumi_units = 'fb-1'

    print ("\nNormalising to lumi ==> {0} [{1}]\n".format( args.lumi, ttH.lumi_units ) )

    # ----------------------------------
    # Set the global event weight for MC
    # ----------------------------------

    ttH.eventweight = "mcWeightOrg * pileupEventWeight_090"

    if args.noWeights:
        ttH.eventweight = "1.0"
        ttH.luminosity  = 1.0
        ttH.rescaleXsecAndLumi = True

    if doMMClosureTest or "CLOSURE" in args.channel:

        # Closure w/o any correction (but keep MC evt weight!)

        if "NO_CORR" in args.channel:
            ttH.eventweight = "mcWeightOrg"

    # ------------------------------------

    ttH.noWeights = args.noWeights

    # ------------------------------------

    ttH.useZCorrections = False

    # ------------------------------------

    ttH.useSherpaNNPDF30NNLO = False

    # ------------------------------------

    if doTwoLepSR or doTwoLepLowNJetCR or dottWCR or doMMClosureTest:
        ttH.channel = 'TwoLepSS'
    elif doThreeLepSR or doThreeLepLowNJetCR or dottZCR or doWZonCR or doWZoffCR or doWZHFonCR or doWZHFoffCR:
        ttH.channel = 'ThreeLep'
    elif doFourLepSR:
        ttH.channel = 'FourLep'
    elif doDataMCCR or doZSSpeakCR or doMMRates or doCFChallenge or doMMSidebands:
        ttH.channel = 'TwoLepCR'

    events = {}
    hists  = {}

    # --------------------------------------
    # Dictionary with systematics histograms
    # --------------------------------------

    systs = {}

    # ----------------------------------
    # List of the backgrounds considered
    # ----------------------------------

    samplenames = {
        'Observed':('observed','Observed'),
        'TTBarH':('signal','Signal'),
        'TTBarHDilep':('signal','Signal'),
        'tHbj':('tHbbkg','tHbj'),
        'WtH':('WtHbkg','tWH'),
        'TTBarW':('ttbarwbkg','$t\\bar{t}W$'),
        'TTBarZ':('ttbarzbkg','$t\\bar{t}Z$'),
        'SingleTop':('singletopbkg','Single $t$, $tW$'),
        'RareTop':('raretopbkg','Others'),
        'Triboson':('tribosonbkg','VVV'),
        'Rare':('raretopbkg','Others'),
        'TTBar':('ttbarbkg','$t\\bar{t}$'),
        'TopCF':('topcfbkg','$t\\bar{t}$ (Charge mis-ID)'),
        'Diboson':('dibosonbkg','$WW$,$WZ$,$ZZ$'),
        'DibosonCF':('dibosoncfbkg','$WW$,$WZ$,$ZZ$ (Charge mis-ID)'),
        'Zjets':('zjetsbkg','$Z/\gamma^{*}$~+~jets'),
        'Zeejets':('zeejetsbkg','$Z/\gamma^{*}\rightarrowee$~+~jets'),
        'Zmumujets':('zmumujetsbkg','$Z/\gamma^{*}\rightarrow\mu\mu$~+~jets'),
        'Ztautaujets':('ztautaujetsbkg','$Z/\gamma^{*}\rightarrow\tau\tau$~+~jets'),
        'ZjetsHF':('zjetsbkg','$Z/\gamma^{*}$~+~ HF~jets'),
        'ZjetsLF':('zjetsbkg','$Z/\gamma^{*}$~+~LF~jets'),
        'ZjetsCF':('zjetscfbkg','$Z/\gamma^{*}$~+~jets (Charge mis-ID)'),
        'Wjets':('wjetsbkg','$W$~+~jets'),
        'Wenujets':('wenujets','$W\rightarrowe\nu$~+~jets'),
        'Wmunujets':('wmunujets','$W\rightarrow\mu\nu$~+~jets'),
        'Wtaunujets':('wtaunujets','$W\rightarrow\tau\nu$~+~jets'),
        'Prompt':('promptbkg','Prompt $\ell$ backgrounds'),
        'QMisID':('qmisidbkg','Charge mis-ID'),
        'QMisIDMC':('qmisidbkg','Charge mis-ID (simulation)'),
        'FakesMC':('fakesbkg','Fake $\ell$ backgrounds (simulation)'),
        'FakesFF':('fakesbkg','Fake $\ell$ backgrounds (Fake Factor)'),
        'FakesMM':('fakesbkg','Fake $\ell$ backgrounds (Matrix Method)'),
        'FakesTHETA':('fakesbkg','Fake $\ell$ backgrounds ($\theta$ method)'),
        'FakesClosureMM':('fakesbkg','Fake $\ell$ backgrounds (Matrix Method closure)'),
        'FakesClosureTHETA':('fakesbkg','Fake $\ell$ backgrounds ($\theta$ method closure)'),
        'FakesClosureDataTHETA':('fakesbkg','Fake $\ell$ backgrounds ($\theta$ method closure)'),
    }

    # Override colours!
    #
    colours = {
        'Observed':kBlack,
        'TTBarH':kRed,
        'TTBarHDilep':kRed,
        'tHbj':kPink+7,
        'WtH':kPink-4,
        'TTBarW':kYellow-9,
        'TTBarZ':kAzure+1,
        'SingleTop':kOrange+6,
        'RareTop':kOrange+7,
        'Triboson':kTeal+10,
        'Rare':kGray,
        'TTBar': kRed - 4,
        'TopCF':kAzure-4,
        'Diboson':kGreen-9,
        'DibosonCF':kOrange-3,
        'Zjets': kCyan -9,
        'Zeejets':kAzure+10,
        'Zmumujets':kAzure-3,
        'Ztautaujets':kCyan-7,
        'ZjetsHF':kGreen+2,
        'ZjetsLF':kGreen,
        'ZjetsCF':kGreen+4,
        'Wjets':kWhite,
        'Wenujets':kGray,
        'Wmunujets':kGray+1,
        'Wtaunujets':kGray+2,
        'Prompt':kOrange-3,
        'QMisID':kMagenta+1,
        'QMisIDMC':kMagenta+1,
        'FakesMC':kMagenta-9,
        'FakesMM':kMagenta-9,
        'FakesFF':kMagenta-9,
        'FakesMM':kMagenta-9,
        'FakesTHETA':kMagenta-9,
        'FakesClosureMM':kTeal+1,
        'FakesClosureTHETA':kCyan-9,
        'FakesClosureDataTHETA': kMagenta-9,
    }

    if ( doSR or doLowNJetCR ):

        ttH.signals     = ['TTBarH']
        ttH.observed    = ['Observed']
        ttH.backgrounds = []
        ttH.sub_backgrounds = []

        if doMM:

            # ---> all the MC backgrounds use a truth selection of only prompt leptons in the event (and QMisID veto)
            #      to avoid double counting with
            #      data-driven/MC-based charge flip and fakes estimate

            ttH.backgrounds.extend(['TTBarW','TTBarZ','Diboson','Rare','FakesMM'])
            #ttH.backgrounds.extend(['Prompt','FakesMM'])

            if args.useMCQMisID:
                ttH.backgrounds.append('QMisIDMC')
                ttH.sub_backgrounds.append('QMisIDMC')
            else:
                ttH.backgrounds.append('QMisID')
                ttH.sub_backgrounds.append('QMisID')

        elif doFF:

            ttH.backgrounds.extend(['TTBarW','TTBarZ','Diboson','Rare','FakesFF'])
            ttH.sub_backgrounds.extend(['TTBarW','TTBarZ','Diboson','Rare'])

            if args.useMCQMisID:
                ttH.backgrounds.append('QMisIDMC')
                ttH.sub_backgrounds.append('QMisIDMC')
            else:
                ttH.backgrounds.append('QMisID')
                ttH.sub_backgrounds.append('QMisID')

        elif doTHETA:

            ttH.backgrounds.extend(['TTBarW','TTBarZ','Diboson','Rare','FakesTHETA'])
            ttH.sub_backgrounds.extend(['TTBarW','TTBarZ','Diboson','Rare'])

            if args.useMCQMisID:
                ttH.backgrounds.append('QMisIDMC')
                ttH.sub_backgrounds.append('QMisIDMC')
            else:
                ttH.backgrounds.append('QMisID')
                ttH.sub_backgrounds.append('QMisID')

        else: # MC based estimate of fakes

            ttH.backgrounds.extend(['Prompt','FakesMC']) # This includes all the following processes: ['TTBar','SingleTop','RareTop','Zjets','Wjets','TTBarW','TTBarZ','Diboson','Triboson','THbj','WtH']

            if args.useMCQMisID:
                ttH.backgrounds.append('QMisIDMC')
                ttH.sub_backgrounds.append('QMisIDMC')
            else:
                ttH.backgrounds.append('QMisID')
                ttH.sub_backgrounds.append('QMisID')

        if doFourLepSR:
            # no fakes in 4lep
            ttH.backgrounds.extend(['TTBarW','TTBarZ','Diboson','TTBar','Rare','Zjets'])

    if doMMRates:

        ttH.signals     = []
        ttH.observed    = ['Observed']
        if args.ratesMC:
            ttH.observed = []
        ttH.backgrounds = []

        #ttH.backgrounds.extend(['Prompt','FakesMC']) # This includes all the following processes: ['TTBar','SingleTop','Rare','Zjets','Wjets','TTBarW','TTBarZ','Diboson']
        ttH.backgrounds.extend(['TTBar','SingleTop','Rare','Zjets','Wjets','TTBarW','TTBarZ','Diboson']) # NB: if using this list, make sure a QMisID veto is applied (in SS CR), since QMisID is added separately below
        #
        # TEMP!
        # Use the following for 25ns_v24_ElNoIso (missing Triboson, tHbj, WtH in "Rare"):
        #
        ttH.observed = []
        #ttH.backgrounds.extend(['TTBar','SingleTop','Zjets','Wjets','TTBarW','TTBarZ','Diboson'])
        ttH.backgrounds.remove("Rare")

        if args.useMCQMisID:
            ttH.backgrounds.append('QMisIDMC')
        else:
            ttH.backgrounds.append('QMisID')

        if "CLOSURE" in args.channel:
            ttH.signals     = []
            ttH.observed    = []
            ttH.backgrounds = ['TTBar']
            #ttH.backgrounds = ['Zjets']

    if doMMSidebands:

        ttH.signals     = ['TTBarH']
        ttH.observed    = ['Observed']
        #ttH.backgrounds = ['TTBarW','TTBarZ','Diboson','Rare']
        ttH.backgrounds = ['Prompt']

        if args.useMCQMisID:
            ttH.backgrounds.append('QMisIDMC')
        else:
            ttH.backgrounds.append('QMisID')

        if "CLOSURE" in args.channel:
            ttH.signals     = []
            ttH.observed    = ['Observed']
            ttH.backgrounds = ['TTBar']

    if doDataMCCR:

        ttH.signals     = []
        ttH.observed    = ['Observed']
        ttH.backgrounds = ['TTBar','SingleTop','Rare','Zeejets','Zmumujets','Ztautaujets','Wjets','TTBarW','TTBarZ','Diboson']
        if not args.useMCQMisID:
            ttH.backgrounds.append('QMisID')

    if doZSSpeakCR:

        ttH.signals     = ['TTBarH']
        ttH.observed    = ['Observed']
        ttH.backgrounds = ['QMisIDMC','FakesMC','Prompt']

    if doCFChallenge:

        ttH.signals     = ['TTBarHDilep']
        ttH.observed    = ['Observed']
        ttH.backgrounds = ['TTBar']

    if doMMClosureTest:

        if doMM:
            ttH.signals     = [] # ['FakesClosureTHETA']
            ttH.observed    = ['TTBar']
            ttH.backgrounds = ['FakesClosureMM']
        elif doFF:
            ttH.signals     = []
            ttH.observed    = ['TTBar']
            ttH.backgrounds = ['FakesClosureFF']
        elif doTHETA:
            ttH.signals     = []
            ttH.observed    = ['TTBar']
            ttH.backgrounds = ['FakesClosureTHETA']
        else:
            ttH.signals     = []
            ttH.observed    = []
            ttH.backgrounds = ['TTBar']

    if args.noSignal:
        ttH.signals = []

    showRatio = args.doShowRatio
    if doMMClosureTest:
        showRatio = True

    # Make blinded plots in SR unless configured from input

    if ( doSR or ( doMMSidebands and ( "HIGHNJ" in args.channel or "ALLJ" in args.channel ) ) ) and not args.doUnblinding:
        ttH.observed = []
        showRatio  = False

    # -------------------------------------------------------
    # Filling histname with the name of the variables we want
    #
    # Override colours as well
    # -------------------------------------------------------

    histname   = {'Expected':('expectedbkg','Tot. bkg.'),'AllSimulation':('allsimbkg','Tot. simulation')}
    histcolour = {'Expected': kGray+1,'AllSimulation':kOrange+2}

    for sample in ttH.backgrounds:
        histname[sample]   = samplenames[sample]
        histcolour[sample] = colours[sample]
        #
        # Will override default colour based on the dictionary provided above
        #
        ttH.str_to_class(sample).colour = colours[sample]
    for sample in ttH.observed:
        histname[sample]   = samplenames[sample]
        histcolour[sample] = colours[sample]
        ttH.str_to_class(sample).colour = colours[sample]
    for sample in ttH.signals:
        histname[sample]   = samplenames[sample]
        histcolour[sample] = colours[sample]
        ttH.str_to_class(sample).colour = colours[sample]

    print "Processes:\n", histname
    print "Processes' colours:\n", histcolour

    # ---------------------------------
    # Processing categories in sequence
    # ---------------------------------

    fakeestimate = ""
    if doMM:
        fakeestimate="_MM"
    if doFF:
        fakeestimate="_FF"
    if doTHETA:
        fakeestimate="_THETA"
    if doMC:
        fakeestimate="_MC"

    basedirname = "OutputPlots" + fakeestimate + "_" + args.outdirname + "/"

    significance_dict = {}

    for category in sorted(vardb.categorylist, key=(lambda category: category.name) ):

        print ("\n*********************************************\n\n")
        print ("Making plots in category:\t{0}\n".format( category.name ))

        # ----------------------------------------------------
        # Reset the weight for *this* category to 1 if neeeded
        # ----------------------------------------------------

        if args.noWeights or "NO_CORR" in args.channel:
	    print("Resetting category weight to 1...\n")
            category.weight = "1.0"

        # TEMP!
        # For DLT, trigger SF not available in yet...
        # Set trigger weight to 1

        if "DLT" in args.trigger and "weight_event_trig" in category.weight:
	    print("Using DLT. Trigger SFs not available yet. Do not apply trigger SF...\n")
            category.weight = category.weight.replace("weight_event_trig","1.0")

        # ------------------------------
        # Processing different variables
        # ------------------------------

        for idx,var in enumerate(vardb.varlist, start=0):

            # ----------------------------------------------------
            # Reset the weight for *this* variable to 1 if neeeded
            # ----------------------------------------------------

            if args.noWeights or "NO_CORR" in args.channel and var.weight:
                var.weight = "1.0"

            # --------------------------
            # Avoid making useless plots
            # --------------------------

            if not ("OF") in category.name and ("Mu0Pt_VS_El0Pt") in var.shortname:
                print ("\tSkipping variable:\t{0}\n".format( var.shortname ))
                continue

            if ( ("MuMu") in category.name and ("El") in var.shortname ) or ( ("ElEl") in category.name and ("Mu") in var.shortname ):
                print ("\tSkipping variable:\t{0}\n".format( var.shortname ))
                continue

            if ( ( ("MuEl") in category.name ) and ( ("Mu1") in var.shortname ) ) :
                print ("\tSkipping variable:\t{0}\n".format( var.shortname ))
                continue

            if ( ( ("ElMu") in category.name ) and ( ("El1") in var.shortname ) ) :
                print ("\tSkipping variable:\t{0}\n".format( var.shortname ))
                continue

            if doMMRates:
                # if probe is a muon, do not plot ElProbe* stuff!
                if ( ( ("MuProbe") in category.cut.cutname ) and ( ("ElProbe") in var.shortname ) ):
                    print ("\tSkipping variable:\t{0}\n".format( var.shortname ))
                    continue
                # if probe is an electron, do not plot MuProbe* stuff!
                if ( ( ("ElProbe") in category.cut.cutname ) and ( ("MuProbe") in var.shortname ) ):
                    print ("\tSkipping variable:\t{0}\n".format( var.shortname ))
                    continue

            print ("\tPlotting variable:\t{0}\n\tNTup name:\t{1}\n".format(var.shortname, var.ntuplename))

            total_weight = ttH.eventweight
            if category.weight:
                total_weight += ( " * " + category.weight )
            if var.weight and not var.weight in category.weight:
                total_weight += ( " * " + var.weight )

            print ("\t-----------------------------------------------------------------------------------------------------------------------------\n")
            print ("\tMC event weight for this (category, variable):\n\n\t\t{0}\n".format( total_weight ) )
            print ("\t-----------------------------------------------------------------------------------------------------------------------------\n")

            # Get table w/ event yields for *this* category. Do it only for the first variable in the list
            #
            if ( args.printEventYields and idx is 0 ):
                events[category.name] = ttH.events(eventweight=category.weight, category=category, hmass=['125'])

            #"""

            # ---------------------------------------------------------
            # Creating a directory for the category if it doesn't exist
            # ---------------------------------------------------------

            dirname = basedirname + category.name

            if args.doLogScaleX:
                dirname += "_LOGX"
            if args.doLogScaleY:
                dirname += "_LOGY"

            if not os.path.exists(dirname):
                os.makedirs(dirname)

            # -----------------------------------------------
            # Making a plot with ( category + variable ) name
            # -----------------------------------------------

            plotname = dirname + "/" + category.name + "_" + var.shortname

            if ( args.debug ):
                print ("\tPlotname: {0}\n".format( plotname ))


            # If this option is set True, the last visible bin of the histogram will contain ALSO the overflow

            merge_overflow = args.mergeOverflow

            list_formats = [ plotname + ".png", plotname + ".eps" ]

            # Here is where the plotting is actually performed!

            hists[category.name + ' ' + var.shortname] = ttH.plot( var,
                                                                   eventweight=category.weight,
                                                                   category=category,
                                                                   signal='',#'125',
                                                                   signalfactor=1.0,
                                                                   overridebackground=ttH.backgrounds,
                                                                   overflowbins=merge_overflow,
                                                                   showratio=showRatio,
                                                                   wait=False,
                                                                   save=list_formats,
                                                                   log=args.doLogScaleY,
                                                                   logx=args.doLogScaleX
                                                                 )

            # Creating a file with the observed and expected distributions and systematics.

            foutput = TFile(plotname + ".root","RECREATE")
            if any( v in var.shortname for v in ["Mll01","NJets","ProbePt"] ) and not ( var.typeval in [TH2I,TH2D,TH2F] ):
                outfile = open(plotname + "_yields.txt", "w")

            if args.doSyst and not var.sysvar:

                print("\nVariable {0} not scheduled for systematics plots. Try with another one...\n".format(var.shortname))

            elif args.doSyst and var.sysvar:

                # Systematics go into a different folder

                dirname += "_Syst"

                # Loop on the defined systematics

                total_syst      = 0.0
                total_syst_up   = 0.0
                total_syst_down = 0.0
                histograms_syst = {}

                for syst in vardb.systlist:

                    if not os.path.exists(dirname):
                        os.makedirs(dirname)

                    plotname = dirname + "/" + category.name + "_" + var.shortname + "_" + syst.name

                    print("")
		    print ("\t\t-----------------------------------------------------------------------------------------------------------------------------\n")
                    print ("\t\tSystematic:\t{0}\n".format( syst.name ))
                    if args.debug:
		        print ("\t\tDirectory for systematic plot:\t{0}/".format( dirname ))
                    print ("\t\t-----------------------------------------------------------------------------------------------------------------------------\n")

                    list_formats_sys = [ plotname + ".png"] # [ plotname + ".eps" ]

                    # plotSystematics is the function which takes care of the systematics

                    systs[category.name + " " + var.shortname] = ttH.plotSystematics( syst,
                                                                                      var=var,
                                                                                      eventweight=category.weight,
                                                                                      category=category,
                                                                                      overflowbins=merge_overflow,
                                                                                      showratio=True,
                                                                                      wait=False,
                                                                                      save=list_formats_sys,
                                                                                      log=args.doLogScaleY,
                                                                                      logx=args.doLogScaleX
                                                                                      )

                    # Obtaining histograms for processes and total expected histogram with a particular systematics shifted,
                    # and saving them in the ROOT file

                    systobs, systnom, systup, systdown, systlistup, systlistdown = systs[category.name + " " + var.shortname]

                    histograms_syst["Expected_"+syst.name+"_up"]=systup
                    histograms_syst["Expected_"+syst.name+"_up"].SetNameTitle(histname["Expected"][0]+"_"+syst.name+"_up","")
                    histograms_syst["Expected_"+syst.name+"_up"].SetLineColor(histcolour["Expected"])
                    histograms_syst["Expected_"+syst.name+"_up"].Write()
                    histograms_syst["Expected_"+syst.name+"_dn"]=systdown
                    histograms_syst["Expected_"+syst.name+"_dn"].SetNameTitle(histname["Expected"][0]+"_"+syst.name+"_dn","")
                    histograms_syst["Expected_"+syst.name+"_dn"].SetLineColor(histcolour["Expected"])
                    histograms_syst["Expected_"+syst.name+"_dn"].Write()

                    # The code does not consider systematics on the signal.
                    # Put the signal in the backgrounds list if you want systematics on it.

                    for sample in ttH.backgrounds:
                        if syst.process and not ( syst.process == sample ) :
                            continue
                        histograms_syst[sample+"_"+syst.name+"_up"] = systlistup[sample]
                        histograms_syst[sample+"_"+syst.name+"_up"].SetNameTitle(histname[sample][0]+"_"+syst.name+"_up","")
                        histograms_syst[sample+"_"+syst.name+"_up"].SetLineColor(histcolour[sample])
                        histograms_syst[sample+"_"+syst.name+"_up"].Write()
                        histograms_syst[sample+"_"+syst.name+"_dn"] = systlistdown[sample]
                        histograms_syst[sample+"_"+syst.name+"_dn"].SetNameTitle(histname[sample][0]+"_"+syst.name+"_dn","")
                        histograms_syst[sample+"_"+syst.name+"_dn"].SetLineColor(histcolour[sample])
                        histograms_syst[sample+"_"+syst.name+"_dn"].Write()

                    if any( v in var.shortname for v in ["Mll01","NJets","ProbePt"] ) and not ( var.typeval in [TH2I,TH2D,TH2F] ):
                        outfile.write("Integral syst: \n")
                        outfile.write("syst %s up:   delta_yields = %.2f \n" %(syst.name,(systup.Integral()-systnom.Integral())))
                        outfile.write("syst %s down: delta_yields = %.2f \n" %(syst.name,(systdown.Integral()-systnom.Integral())))
                        if ( args.debug ):
                            outfile.write("GetEntries syst: \n")
                            outfile.write("syst %s up:   delta_entries %.2f \n" %(syst.name,(systup.GetEntries()-systnom.GetEntries())))
                            outfile.write("syst %s down: delta_entries %.2f \n" %(syst.name,(systdown.GetEntries()-systnom.GetEntries())))

                    total_syst      += (systup.Integral()-systdown.Integral())/2.0*(systup.Integral()-systdown.Integral())/2.0
                    total_syst_up   += (systup.Integral()-systnom.Integral())*(systup.Integral()-systnom.Integral())
                    total_syst_down += (systdown.Integral()-systnom.Integral())*(systdown.Integral()-systnom.Integral())

                total_syst      = math.sqrt(total_syst)
                total_syst_up   = math.sqrt(total_syst_up)
                total_syst_down = math.sqrt(total_syst_down)

                if any( v in var.shortname for v in ["Mll01","NJets","ProbePt"] ) and not ( var.typeval in [TH2I,TH2D,TH2F] ):
                    outfile.write("yields total syst UP: %.2f \n" %(total_syst_up))
                    outfile.write("yields total syst DN: %.2f \n" %(total_syst_down))
                    outfile.write("yields total syst: %.2f \n" %(total_syst))

            # ------------------------------------------------------------------

            # Obtain the histograms correctly normalized

            bkghists, expected, observed, signal, _ = hists[category.name + " " + var.shortname]
            histograms = {}

            for sample in ttH.observed:

                histograms[sample] = observed

            if ttH.backgrounds:

                histograms["Expected"] = expected

                # Store an additional histogram as the sum of all the MC-based backgrounds (useful e.g. to get all "prompt" backgrounds in one go)
                # Take the first *non-data-driven* sample in the background histograms list and clone it, then add all the others

                allsim = TH1D()
                (firstsim_idx, firstsim_name) = ttH.getFirstSimulatedProc(category)
                if firstsim_name:
                    allsim = bkghists[firstsim_name].Clone(histname["AllSimulation"][0])

                for idx, sample in enumerate(ttH.backgrounds):
                    histograms[sample] = bkghists[sample]
                    if idx != firstsim_idx  and ( not "QMisID" in sample ) and ( not "Fakes" in sample):
                        allsim.Add(bkghists[sample].Clone(histname[sample][0]))

                histograms["AllSimulation"] = allsim

                if ttH.signals:
                    for sample in ttH.signals:
                        histograms[sample] = signal

                # ------------------------------------------------------------------

                # Set basic properties for histograms

                for sample in histograms.keys():
                    histograms[sample].SetNameTitle(histname[sample][0],"")
                    histograms[sample].SetLineColor(histcolour[sample])
                    histograms[sample].SetMarkerColor(histcolour[sample])

                # ------------------------------------------------------------------

                # Print yields

                outfile_exists = False

                if any( v in var.shortname for v in ["Mll01","NJets","ProbePt"] ) and not ( var.typeval in [TH2I,TH2D,TH2F] ):

                    outfile_exists = True

                    s = 0
                    err_s = Double(0)
                    err_b = Double(0)
                    if ttH.signals:
                        if merge_overflow:
                            last_bin_idx_s = histograms["TTBarH"].GetNbinsX()
                        else:
                            last_bin_idx_s = histograms["TTBarH"].GetNbinsX()+1
                        s = histograms["TTBarH"].IntegralAndError(0,last_bin_idx_s,err_s)

                    if merge_overflow:
                        last_bin_idx_b = histograms["Expected"].GetNbinsX()
                    else:
                        last_bin_idx_b = histograms["Expected"].GetNbinsX()+1
                    b = histograms["Expected"].IntegralAndError(0,last_bin_idx_b,err_b)

                    Z = (-1,-1)
                    if b:
                        Z = calculate_Z( s, b, err_s, err_b, method="SoverSqrtB" )

                    print (" ")
                    print ("\t\tCategory: {0} - Variable: {1}\n".format( category.name, var.shortname ))
                    print ("\t\tIntegral:\n")

                    outfile.write("Category: %s \n" %(category.name))
                    outfile.write("Variable: %s \n" %(var.shortname))
                    outfile.write("\n")
                    outfile.write("\\begin{table}\n\\begin{center}\n\\begin{tabular}{ccc}\n\\toprule\n & Yields & N/(Tot. bkg.) \\\\ \n\\midrule\n")

                    err=Double(0)  # integral error
                    value=0        # integral value

		    for sample in histograms.keys():

			# Include underflow, but if option merge_overflow = True, do not take overflow bin!
                        # In fact, in that case, the last visible bin will contain the OFlow bin.

                        if merge_overflow:
                            last_bin_idx = histograms[sample].GetNbinsX()
                        else:
                            last_bin_idx = histograms[sample].GetNbinsX()+1

                        value = histograms[sample].IntegralAndError(0,last_bin_idx,err)

                        percentage_str = percentage_outfilestr = ""
                        if b and not sample in ["Observed","TTBarH","Expected"]:
			    percentage_str        = " ({0:.1f} % tot. bkg.)".format((value/b)*1e2)
			    percentage_outfilestr = "{0:.1f} $\%$".format((value/b)*1e2)

			yields_outstream     = "\t\t{0}: {1:.2f} +- {2:.2f}".format(histname[sample][0], value, err) + percentage_str
			yields_outfilestream = "{0} & {1:.2f} $\pm$ {2:.2f} & ".format(histname[sample][1], value, err) + percentage_outfilestr + " \\\\ \n"

			print (yields_outstream)
                        outfile.write(yields_outfilestream)

                        # Print each bin content

			if "NJets" in var.shortname:

                            # Neglect underflow, but not overflow!

                            for bin in range(1,histograms[sample].GetNbinsX()+2):
                                err_bin   = Double(0)
                                value_bin = 0
                                this_bin  = histograms[sample].GetBinCenter(bin)
                                value_bin = histograms[sample].GetBinContent(bin)
                                err_bin   = histograms[sample].GetBinError(bin)

                                if (histograms[sample].IsBinOverflow(bin)):
                                    print ("\t\t  OVERFLOW BIN:")
                                    outfile.write("  OVERFLOW BIN:\n")

                                # If it"s the last visible bin, and merge_overflow = True, subtract overflow from this bin

                                if ( merge_overflow and histograms[sample].IsBinOverflow(bin+1) ):
                                    value_bin -= histograms[sample].GetBinContent(bin+1)
                                    err_bin   = 0
                                print ("\t\t  {0}-jets bin: {1:.2f} +- {2:.2f}".format(this_bin, value_bin, err_bin))
                                outfile.write("  %i-jets bin: %.2f +- %.2f \n" %(this_bin, value_bin, err_bin))

                            # Get integral and error from njets>=5 bins (including OFlow) in one go!

                            if ( var.shortname == "NJets" ):
                                err_HJ   = Double(0)
                                value_HJ = histograms[sample].IntegralAndError (6,last_bin_idx,err_HJ)
                                print ("\n\t\t  >=5-jets bin: {0:.2f} +- {1:.2f}".format(value_HJ, err_HJ))
                                outfile.write("\n  >=5-jets bin: %.2f +- %.2f \n" %(value_HJ, err_HJ))

                    if Z[0] >= 0:
                        Z_outstream     = "\t\t{0}: {1:.2f} +- {2:.2f}".format("S/sqrt(B)", Z[0], Z[1])
                        Z_outfilestream = "{0} & {1:.2f} $\pm$ {2:.2f} & ".format("S/$\\sqrt\\textrm{B}$", Z[0], Z[1]) + " \\\\ \n"
			print Z_outstream
                        outfile.write(Z_outfilestream)

                    outfile.write("\\bottomrule\n\\end{tabular}\n\\end{center}\n\\end{table}\n")

                    print ("\n\t\tGetEntries:\n")
                    print ("\t\tNB 1): this is actually N = GetEntries()-2 \n\t\t       Still not understood why there's such an offset...\n")
                    print ("\t\tNB 2): this number does not take into account overflow bin. Better to look at the integral obtained with --noWeights option...\n")
                    outfile.write("\nGetEntries: \n")
                    for sample in histograms.keys():
                        print ("\t\t{0}: {1}".format(histname[sample][0], histograms[sample].GetEntries()-2))
                        outfile.write("entries %s: %f \n" %(histname[sample][0], histograms[sample].GetEntries()-2))

                for sample in histograms.keys():
                    histograms[sample].Write()
                foutput.Close()

                if outfile_exists:
                    outfile.close()

            #"""
