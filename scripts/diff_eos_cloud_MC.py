cloudlist = []

eoslist = [
301535,
301536,
301887,
301888,
301889,
301890,
301891,
301892,
301893,
301894,
301895,
301896,
301897,
301898,
301899,
301900,
301901,
301902,
301903,
301905,
301906,
301907,
301908,
301909,
301910,
304776,
341177,
341270,
341271,
341988,
341989,
341990,
341997,
341998,
341999,
342170,
342171,
342172,
342284,
342285,
343243,
343266,
343267,
343268,
343365,
343366,
343367,
361063,
361064,
361065,
361066,
361067,
361068,
361069,
361070,
361071,
361072,
361073,
361074,
361075,
361076,
361077,
361078,
361079,
361080,
361081,
361082,
361083,
361084,
361085,
361086,
361087,
361088,
361089,
361090,
361091,
361092,
361093,
361094,
361095,
361096,
361097,
361100,
361101,
361102,
361103,
361104,
361105,
361106,
361107,
361108,
361300,
361301,
361302,
361303,
361304,
361305,
361306,
361307,
361308,
361309,
361310,
361311,
361312,
361313,
361314,
361315,
361316,
361317,
361318,
361319,
361320,
361321,
361322,
361323,
361324,
361325,
361326,
361327,
361328,
361329,
361330,
361331,
361332,
361333,
361334,
361335,
361336,
361337,
361338,
361339,
361340,
361341,
361342,
361343,
361344,
361345,
361346,
361347,
361348,
361349,
361350,
361351,
361352,
361353,
361354,
361355,
361356,
361357,
361358,
361359,
361360,
361361,
361362,
361363,
361364,
361365,
361366,
361367,
361368,
361369,
361370,
361371,
361372,
361373,
361374,
361375,
361376,
361377,
361378,
361379,
361380,
361381,
361382,
361383,
361384,
361385,
361386,
361387,
361389,
361390,
361391,
361392,
361393,
361394,
361395,
361396,
361397,
361398,
361399,
361400,
361401,
361402,
361403,
361404,
361405,
361406,
361407,
361408,
361410,
361411,
361412,
361413,
361414,
361415,
361416,
361417,
361418,
361419,
361420,
361421,
361422,
361423,
361424,
361425,
361426,
361427,
361428,
361429,
361430,
361431,
361432,
361433,
361434,
361436,
361437,
361438,
361439,
361440,
361441,
361442,
361443,
361468,
361469,
361470,
361471,
361472,
361473,
361474,
361475,
361476,
361477,
361478,
361479,
361480,
361481,
361483,
361484,
361485,
361486,
361487,
361488,
361489,
361490,
361491,
361500,
361501,
361502,
361503,
361504,
361505,
361506,
361507,
361508,
361509,
361510,
361511,
361512,
361513,
361514,
361520,
361521,
361523,
361525,
361526,
361527,
361528,
361529,
361531,
361533,
361534,
361625,
361626,
361627,
361628,
361629,
361630,
361631,
361632,
361633,
361634,
361635,
361636,
361637,
361638,
361639,
361640,
361641,
361642,
363102,
363103,
363104,
363105,
363106,
363107,
363108,
363109,
363110,
363111,
363112,
363113,
363114,
363115,
363116,
363117,
363118,
363119,
363120,
363121,
363122,
363331,
363332,
363333,
363334,
363335,
363336,
363337,
363338,
363339,
363340,
363341,
363342,
363343,
363344,
363345,
363346,
363347,
363348,
363349,
363350,
363351,
363352,
363353,
363354,
363361,
363362,
363363,
363364,
363365,
363366,
363367,
363368,
363369,
363370,
363371,
363372,
363373,
363374,
363375,
363376,
363377,
363378,
363379,
363380,
363381,
363382,
363383,
363384,
363385,
363386,
363387,
363388,
363389,
363390,
363391,
363392,
363393,
363394,
363395,
363396,
363397,
363398,
363399,
363400,
363401,
363402,
363403,
363404,
363405,
363406,
363407,
363408,
363409,
363410,
363411,
363436,
363437,
363438,
363439,
363440,
363441,
363442,
363443,
363444,
363445,
363446,
363447,
363448,
363449,
363450,
363451,
363452,
363453,
363454,
363455,
363456,
363457,
363458,
363459,
363460,
363461,
363462,
363463,
363464,
363465,
363466,
363467,
363468,
363469,
363470,
363471,
363472,
363473,
363474,
363475,
363476,
363477,
363478,
363479,
363480,
363481,
363482,
363483,
410000,
410001,
410002,
410007,
410009,
410011,
410012,
410013,
410014,
410015,
410016,
410025,
410026,
410049,
410050,
410066,
410067,
410068,
410073,
410074,
410075,
410080,
410081,
410111,
410112,
410113,
410114,
410115,
410116,
410120,
410121,
410142,
410143,
410144,
410155,
410156,
410157,
410159,
410187,
410188,
410189,
410215,
410218,
410219,
410220,
410500,
]

for item in eoslist:
    if item not in cloudlist:
        print("WARNING! Sample {0} not copied yet from EOS to Melbourne cloud".format(item))
