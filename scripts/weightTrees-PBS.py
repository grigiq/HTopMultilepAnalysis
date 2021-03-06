#!/usr/bin/env python

import glob, os, sys, subprocess, shutil, argparse, datetime

samplescsv = os.path.abspath(os.path.curdir) + "/HTopMultilepAnalysis/PlotUtils/Files/samples_HTopMultilep_Priority1.csv"

sys.path.append(os.path.abspath(os.path.curdir)+"/HTopMultilepAnalysis/PlotUtils/")
from Core import NTupleTools, DatasetManager, listifyInputFiles

datasets = DatasetManager.DatasetManager()
sampledict = datasets.getListSamples(samplescsv,genericPath=True)

import normaliseTrees

parser = argparse.ArgumentParser(description='Weight ROOT trees created by PBS job w/ Xsec weight')

parser.add_argument('dest', metavar='dest',type=str,
                   help='Base directory where to store output for the process in question')
parser.add_argument('DSID', metavar='DSID',type=str,
                   help='Dataset ID of the process in question')

args = parser.parse_args()

if __name__ == '__main__':

    dest = args.dest

    if not os.path.exists(dest):
        os.makedirs(dest)

    for s in sampledict:
        groupdir = dest + "/" + s["group"]
        if not os.path.exists(groupdir):
            os.makedirs(groupdir)

    knownDSID = False

    # Clear cache (Sean's suggestion)

    subprocess.call(['ls','-l','/coepp/cephfs/mel/mmilesi/'])

    for s in sampledict:

        if args.DSID == s["ID"] or ( str(args.DSID[0:2]) == "00" and not s["ID"] ):

            knownDSID = True

            separator = "."
            if not s["ID"]:
                separator = ""

            INTREE  = args.DSID + "/data-output" + "/" + args.DSID + ".root"
            INHIST  = args.DSID + "/hist-" + args.DSID + ".root"

	    if ( str(args.DSID[0:2]) == "00" ):
                OUTTREE = dest + "/Data/" + args.DSID + ".physics_Main.root"
                OUTHIST = dest + "/Data/hist-" + args.DSID + ".physics_Main.root"
            else:
                OUTTREE = dest + "/" + s["group"] + "/" + s["ID"] + separator + s["name"] + ".root"
                OUTHIST = dest + "/" + s["group"] + "/hist-" + s["ID"] + separator + s["name"] + ".root"

            print("Moving :\n{0}\nto:\n{1}".format(INTREE,OUTTREE))
            print("Moving :\n{0}\nto:\n{1}".format(INHIST,OUTHIST))

            shutil.move(INTREE,OUTTREE)
            shutil.move(INHIST,OUTHIST)

            normaliseTrees.applyWeight( OUTTREE, s, isdata = bool( str( args.DSID[0:2] ) == "00" and not s["ID"] ) )

            break

    if not knownDSID:
        print("Simply removing {0} b/c corresponding DSID is unknown...".format(args.DSID))
    shutil.rmtree(os.path.abspath(os.path.curdir) + "/" + args.DSID)
