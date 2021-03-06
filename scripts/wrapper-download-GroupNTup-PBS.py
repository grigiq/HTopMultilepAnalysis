#!/usr/bin/env python

import glob, os, sys, subprocess, shutil, string, argparse, time

parser = argparse.ArgumentParser(description="Wrapper script for download-GroupNTup-PBS.py. This gets called on the PBS worker node via the PBS script generated by download-GroupNTup-PBS.py. The sample to be processed gets retrieved via the PBS_ARRAYID index.")

parser.add_argument("--ntup_tag", dest="ntup_tag", action="store", type=str)
parser.add_argument("--downloadpath", dest="downloadpath", action="store", type=str)
parser.add_argument("--samplelist", dest="samplelist", action="store", type=str, nargs="+")

args = parser.parse_args()

if __name__ == '__main__':

    # Read samplelist from argparse.
    # It will automagically re-create a python list from the multiple arguments of the input --samplelist option.

    samplelist = args.samplelist

    # Get the sample from the PBS_ARRAYID

    pbs_array_idx = int(os.getenv('PBS_ARRAYID'))

    sample = samplelist[pbs_array_idx]

    print("Current job index PBS_ARRAYID={0}, sample={1}".format(pbs_array_idx,sample))

    if sample[0:2] == "00":
        sample_type = "Data"
    elif sample == "304014":
        sample_type = "FastSim_PLICFT"
    elif sample in ["410276","410277","410278","410397","410398","410399"]:
        sample_type = "ttll/PLICFT"
    else:
        sample_type = "Nominal_PLICFT"

    downloadpath = args.downloadpath + "/" + sample_type + "/" + str(sample) + "/"

    if not os.path.exists(downloadpath):
        os.makedirs(downloadpath)

    # Dump job if the file for this sample already exists!
    if os.listdir(downloadpath):
        os.sys.exit("Exiting, file:\n{0}\nalready exists!".format(downloadpath+str(sample)+".root"))

    input_ntup = "root://eospublic.cern.ch//eos/escience/UniTexas/HSG8/multileptons_ntuple_run2/" + args.ntup_tag + "/" + sample_type + "/" + str(sample) + ".root"

    cmd = "xrdcp {0} {1}".format(input_ntup,downloadpath)

    print("Checking Kerberos credentials:")
    klist_proc = subprocess.Popen("klist",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    klist_out, klist_err = klist_proc.communicate()
    print klist_out, klist_err

    print("Executing:\n{0}".format(cmd))
    time.sleep(10)
    proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = proc.communicate()
    print out, err
