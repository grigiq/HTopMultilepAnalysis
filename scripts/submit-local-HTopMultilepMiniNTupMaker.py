#!/usr/bin/env python

import glob, os, sys, subprocess, shutil

samplescsv = os.path.abspath(os.path.curdir) + "/HTopMultilepAnalysis/PlotUtils/Files/samples2015_HTopMultilep_25ns.csv"

sys.path.append(os.path.abspath(os.path.curdir)+"/HTopMultilepAnalysis/PlotUtils/")
from Core import NTupleTools, DatasetManager, listifyInputFiles

datasets = DatasetManager.DatasetManager()
sampledict = datasets.getListSamples(samplescsv,genericPath=True)

import normaliseTrees

infilelist = [
#"HTopMultilepAnalysis/doc/list-local-HTopGroupNTup.txt", # for data
#
# ttbar
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410000/410000.root",
# ttH Pythia8
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/343365/343365.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/343366/343366.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/343367/343367.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/343436/343436.root",
# ttV NLO
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410155/410155.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410156/410156.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410157/410157.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410159/410159.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410187/410187.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410188/410188.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410189/410189.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410215/410215.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410218/410218.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410219/410219.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410220/410220.root",
# Diboson
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361063/361063.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361064/361064.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361065/361065.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361066/361066.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361067/361067.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361068/361068.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361069/361069.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361070/361070.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361071/361071.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361072/361072.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361073/361073.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361074/361074.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361075/361075.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361076/361076.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361077/361077.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361078/361078.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361079/361079.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361080/361080.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361081/361081.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361082/361082.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361083/361083.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361084/361084.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361085/361085.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361086/361086.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361087/361087.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361088/361088.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361089/361089.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361090/361090.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361091/361091.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361092/361092.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361093/361093.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361094/361094.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361095/361095.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361096/361096.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361097/361097.root",
# ttH Herwig
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/341177/341177.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/341270/341270.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/341271/341271.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/342170/342170.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/342171/342171.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/342172/342172.root",
# ttV
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410066/410066.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410067/410067.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410068/410068.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410073/410073.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410074/410074.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410075/410075.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410080/410080.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410081/410081.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410111/410111.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410112/410112.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410113/410113.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410114/410114.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410115/410115.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410116/410116.root",
# All the rest
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301535/301535.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301536/301536.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301887/301887.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301888/301888.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301889/301889.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301890/301890.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301891/301891.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301892/301892.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301893/301893.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301894/301894.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301895/301895.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301896/301896.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301897/301897.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301898/301898.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301899/301899.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301900/301900.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301901/301901.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301902/301902.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301903/301903.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301904/301904.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301905/301905.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301906/301906.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301907/301907.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301908/301908.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301909/301909.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/301910/301910.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/304776/304776.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/341988/341988.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/341989/341989.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/341990/341990.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/341997/341997.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/341998/341998.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/341999/341999.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/342284/342284.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/342285/342285.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/343243/343243.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/343266/343266.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/343267/343267.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/343268/343268.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/344096/344096.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/344098/344098.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/344133/344133.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/344134/344134.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361101/361101.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361102/361102.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361103/361103.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361104/361104.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361105/361105.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361106/361106.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361107/361107.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361108/361108.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361300/361300.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361301/361301.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361302/361302.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361303/361303.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361304/361304.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361305/361305.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361306/361306.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361307/361307.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361308/361308.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361309/361309.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361310/361310.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361311/361311.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361312/361312.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361313/361313.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361314/361314.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361315/361315.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361316/361316.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361317/361317.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361318/361318.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361319/361319.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361320/361320.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361321/361321.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361322/361322.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361323/361323.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361324/361324.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361325/361325.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361326/361326.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361328/361328.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361329/361329.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361330/361330.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361331/361331.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361332/361332.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361333/361333.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361334/361334.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361335/361335.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361336/361336.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361337/361337.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361338/361338.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361339/361339.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361340/361340.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361341/361341.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361342/361342.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361343/361343.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361344/361344.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361345/361345.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361346/361346.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361347/361347.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361348/361348.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361349/361349.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361350/361350.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361351/361351.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361352/361352.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361353/361353.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361355/361355.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361357/361357.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361358/361358.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361359/361359.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361360/361360.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361361/361361.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361362/361362.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361363/361363.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361364/361364.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361365/361365.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361366/361366.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361367/361367.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361368/361368.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361369/361369.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361370/361370.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361371/361371.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361372/361372.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361373/361373.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361374/361374.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361375/361375.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361376/361376.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361377/361377.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361378/361378.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361379/361379.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361380/361380.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361381/361381.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361382/361382.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361383/361383.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361384/361384.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361385/361385.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361386/361386.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361387/361387.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361388/361388.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361389/361389.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361390/361390.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361391/361391.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361392/361392.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361393/361393.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361394/361394.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361395/361395.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361396/361396.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361397/361397.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361398/361398.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361399/361399.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361400/361400.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361401/361401.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361402/361402.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361403/361403.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361404/361404.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361405/361405.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361406/361406.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361407/361407.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361408/361408.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361409/361409.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361410/361410.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361411/361411.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361412/361412.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361413/361413.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361414/361414.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361415/361415.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361416/361416.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361417/361417.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361418/361418.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361419/361419.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361420/361420.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361421/361421.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361422/361422.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361423/361423.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361424/361424.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361425/361425.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361426/361426.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361427/361427.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361428/361428.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361429/361429.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361430/361430.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361431/361431.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361432/361432.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361433/361433.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361434/361434.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361435/361435.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361436/361436.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361437/361437.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361438/361438.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361439/361439.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361440/361440.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361441/361441.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361442/361442.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361443/361443.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361468/361468.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361469/361469.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361470/361470.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361471/361471.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361472/361472.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361473/361473.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361474/361474.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361475/361475.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361476/361476.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361477/361477.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361478/361478.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361479/361479.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361480/361480.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361481/361481.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361482/361482.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361483/361483.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361484/361484.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361485/361485.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361486/361486.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361487/361487.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361488/361488.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361489/361489.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361490/361490.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361491/361491.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361500/361500.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361502/361502.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361503/361503.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361504/361504.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361505/361505.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361506/361506.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361507/361507.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361508/361508.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361509/361509.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361510/361510.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361511/361511.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361512/361512.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361513/361513.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361514/361514.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361520/361520.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361521/361521.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361523/361523.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361525/361525.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361526/361526.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361527/361527.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361528/361528.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361529/361529.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361531/361531.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361533/361533.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361534/361534.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361625/361625.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361626/361626.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361627/361627.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361628/361628.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361629/361629.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361630/361630.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361631/361631.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361632/361632.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361633/361633.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361634/361634.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361635/361635.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361636/361636.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361637/361637.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361638/361638.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361639/361639.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361640/361640.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361641/361641.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/361642/361642.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363102/363102.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363103/363103.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363104/363104.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363105/363105.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363106/363106.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363107/363107.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363108/363108.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363109/363109.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363110/363110.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363111/363111.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363112/363112.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363113/363113.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363114/363114.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363115/363115.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363116/363116.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363117/363117.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363118/363118.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363119/363119.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363120/363120.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363121/363121.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363122/363122.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363331/363331.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363332/363332.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363333/363333.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363334/363334.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363335/363335.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363336/363336.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363337/363337.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363338/363338.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363339/363339.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363340/363340.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363341/363341.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363342/363342.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363343/363343.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363344/363344.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363345/363345.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363346/363346.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363347/363347.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363348/363348.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363349/363349.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363350/363350.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363351/363351.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363352/363352.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363353/363353.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363354/363354.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363361/363361.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363362/363362.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363363/363363.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363364/363364.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363365/363365.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363366/363366.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363367/363367.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363368/363368.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363369/363369.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363370/363370.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363371/363371.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363372/363372.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363373/363373.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363374/363374.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363375/363375.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363376/363376.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363377/363377.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363378/363378.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363379/363379.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363380/363380.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363381/363381.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363382/363382.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363383/363383.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363384/363384.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363385/363385.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363386/363386.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363387/363387.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363388/363388.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363389/363389.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363390/363390.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363391/363391.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363392/363392.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363393/363393.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363394/363394.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363395/363395.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363396/363396.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363397/363397.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363398/363398.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363399/363399.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363400/363400.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363401/363401.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363402/363402.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363403/363403.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363404/363404.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363405/363405.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363406/363406.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363407/363407.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363408/363408.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363409/363409.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363410/363410.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363411/363411.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363436/363436.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363437/363437.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363438/363438.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363439/363439.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363440/363440.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363441/363441.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363442/363442.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363443/363443.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363444/363444.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363445/363445.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363446/363446.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363447/363447.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363448/363448.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363449/363449.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363450/363450.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363451/363451.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363452/363452.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363453/363453.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363454/363454.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363455/363455.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363456/363456.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363457/363457.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363458/363458.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363459/363459.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363460/363460.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363461/363461.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363462/363462.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363463/363463.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363464/363464.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363465/363465.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363466/363466.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363467/363467.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363468/363468.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363469/363469.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363470/363470.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363471/363471.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363472/363472.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363473/363473.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363474/363474.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363475/363475.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363476/363476.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363477/363477.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363478/363478.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363479/363479.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363480/363480.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363481/363481.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363482/363482.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/363483/363483.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410001/410001.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410007/410007.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410009/410009.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410011/410011.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410012/410012.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410013/410013.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410014/410014.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410015/410015.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410016/410016.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410025/410025.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410026/410026.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410049/410049.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410050/410050.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410121/410121.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410142/410142.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410143/410143.root",
"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v17/Nominal/410144/410144.root",
#
#"/afs/cern.ch/user/m/mmilesi/work/private/HTopMultileptonsTestSamples/25ns_v13/Nominal/341270/341270.root",
#"/afs/cern.ch/user/m/mmilesi/work/private/HTopMultileptonsTestSamples/25ns_v14/Nominal/341270/341270.root",
#"/afs/cern.ch/user/m/mmilesi/work/private/HTopMultileptonsTestSamples/25ns_v17/Nominal/341270/341270.root",
#"/afs/cern.ch/user/m/mmilesi/work/private/HTopMultileptonsTestSamples/25ns_v13/Data/00280614.root",
#
#"/coepp/cephfs/mel/mmilesi/ttH/GroupNTup/25ns_v14/Nominal/410000/410000.root"
]

# -------------------------------------------------------------------------------------------------------

configpath = "$ROOTCOREBIN/user_scripts/HTopMultilepAnalysis/jobOptions_HTopMultilepMiniNTupMaker.py"
treename   = "nominal"
nevents    = 0

#motherdir = "/afs/cern.ch/user/m/mmilesi/work/private/ttH/MiniNTup/25ns_v14_testDilepTrig"
#motherdir = "/afs/cern.ch/user/m/mmilesi/work/private/ttH/MiniNTup/25ns_v17_test"
#motherdir = "/coepp/cephfs/mel/mmilesi/ttH/MiniNTup/25ns_v14/25ns_v14_Direct"
#motherdir = "/coepp/cephfs/mel/mmilesi/ttH/MiniNTup/25ns_v14/25ns_v14_Direct_DLT"
motherdir = "/coepp/cephfs/mel/mmilesi/ttH/MiniNTup/25ns_v17/25ns_v17_Direct"

if not os.path.exists(motherdir):
    os.makedirs(motherdir)
for s in sampledict:
    groupdir = motherdir + "/" + s["group"]
    if not os.path.exists(groupdir):
        os.makedirs(groupdir)

for infile in infilelist:

  xAH_run = None

  # In case of DATA, read the list of infiles from a txt file and execute one single job
  #
  if infile[-4:] == ".txt":
     outdir = "Data"
     xAH_run = "xAH_run.py -vv --files {0} --config {1} --inputList --treeName {2} --submitDir {3} --nevents {4} --force direct".format(infile,configpath,treename,outdir,nevents)
  else :
     outdir = ( infile.split("/") )[-1]
     outdir = outdir.replace(".root","")
     xAH_run = "xAH_run.py -vv --files {0} --config {1} --treeName {2} --submitDir {3} --nevents {4} --force direct".format(infile,configpath,treename,outdir,nevents)

  print("Executing command:\n{0}".format(xAH_run))
  subprocess.call(xAH_run,shell=True)

  # Move output file(s) from job directory to the proper one,
  # but first, change the file name to be readable in KG's FW!
  #
  knownDSID = False
  for s in sampledict:

     if outdir == s["ID"] or ( outdir == "Data" and not s["ID"] ):

        knownDSID = True
	outputfilepath = outdir +"/data-output"

        separator = "."
        if not s["ID"]:
          separator = ""

	INTREE  = outputfilepath + "/" + outdir + ".root"
	INHIST  = outdir + "/hist-" + outdir + ".root"
	if ( outdir == "Data" ):
	   INTREE  = outputfilepath + "/list-local-HTopGroupNTup.root"
	   INHIST  = outdir + "/hist-list-local-HTopGroupNTup.root"

	OUTTREE = motherdir + "/" + s["group"] + "/" + s["ID"] + separator + s["name"] + ".root"
	OUTHIST = motherdir + "/" + s["group"] + "/hist-" + s["ID"] + separator + s["name"] + ".root"

	print("Moving :\n{0}\nto:\n{1}".format(INTREE,OUTTREE))
	print("Moving :\n{0}\nto:\n{1}".format(INHIST,OUTHIST))

	shutil.move(INTREE,OUTTREE)
	shutil.move(INHIST,OUTHIST)

	normaliseTrees.applyWeight(OUTTREE,s,isdata=bool(outdir == "Data" and not s["ID"]))

        break

  if not knownDSID:
    print("Simply removing {0} b/c corresponding DSID is unknown...".format(outdir))
  shutil.rmtree(os.path.abspath(os.path.curdir) + "/" + outdir)













































































































































































































































































































































































































































































































