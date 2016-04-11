#!/usr/bin/env python

""" run_modifytree_QMisID.py: simple script to execute a ROOT macro by calling the CINT interpreter with TROOT::ProcessLine() """

__author__     = "Marco Milesi, Francesco Nuti"
__email__      = "marco.milesi@cern.ch, francesco.nuti@cern.ch"
__maintainer__ = "Marco Milesi"

import os, subprocess, sys, time, shlex, copy

sys.path.append(os.path.abspath(os.path.curdir))

from ROOT import gROOT

gROOT.SetBatch(True)

#oldpath  = '/data/mmilesi/ttH/MergedDatasets/Merged_v027/Merged_Melb15_ttH_027_DxAOD_DATA_MM/'
#newpath  = '/data/mmilesi/ttH/MergedDatasets/Merged_v027/Merged_Melb15_ttH_027_DxAOD_DATA_QMisID_WEIGHTED/'
#oldpath  = '/data/mmilesi/ttH/MergedDatasets/Merged_v028/Merged_Melb15_ttH_028_DxAOD_DATA_MM/'
#newpath  = '/data/mmilesi/ttH/MergedDatasets/Merged_v028/Merged_Melb15_ttH_028_DxAOD_DATA_QMisID_WEIGHTED/'

oldpath  = '/data/mmilesi/ttH/MergedDatasets/Merged_v029/ICHEP_BASELINE/Merged_Melb15_ttH_029_Baseline_DxAOD_DATA/'
newpath  = '/data/mmilesi/ttH/MergedDatasets/Merged_v029/ICHEP_BASELINE/Merged_Melb15_ttH_029_Baseline_DxAOD_DATA_QMisID_WEIGHTED/'

# Are we using group ntuples?
#
useGroupNTup = "YES"

# Set only if QMisID weight branch does not exist yet
#
addQMisID = True

treename = 'physics'
nentries = 'ALL' #ALL

if not os.path.exists(newpath):
    os.makedirs(newpath)

if addQMisID:
  gROOT.LoadMacro("modifyttree_AddQMisID.cxx+g")
else: 
  gROOT.LoadMacro("modifyttree_QMisID.cxx+g")

group_list = os.listdir(oldpath)
group_list = group_list[:]
for group in group_list:
    if not os.path.isdir(oldpath+group):
        continue
    if not os.path.exists(newpath+group):
        os.makedirs(newpath+group)
    sample_list = os.listdir(oldpath+group+'/')
    for sample in sample_list:
        print group+'/'+sample
        infile=oldpath+group+'/'+sample
        outfile=newpath+group+'/'+sample

        if addQMisID:
	   command_line = 'modifyttree_AddQMisID(\"'+infile+'\",\"'+nentries+'\",\"'+treename+'\",\"'+outfile+'\",\"'+useGroupNtup+'\")'
        else:  
	   command_line = 'modifyttree_QMisID(\"'+infile+'\",\"'+nentries+'\",\"'+treename+'\",\"'+outfile+'\")'

        print command_line
        gROOT.ProcessLine(command_line);

        #command_line = 'root -l -q \"modifyttree_AddQMisID.cxx+g(\"'+infile+'\",\"'+treename+'\",\"'+outfile+'\")\"'
        #print command_line
        #args = shlex.split(command_line)
        #print args
        #subprocess.cxxall(args)
        #subprocess.cxxall(['root', '-l', '-q', '"modifyttree_AddQMisID.cxx+g(\"'+infile+'\",\"'+treename+'\",\"'+outfile+'\")"'])
        #f = TFile.Open(path+group+'/'+sample)
        #h_tot = f.Get('TotalEvents')
        #t = f.Get('physics')
