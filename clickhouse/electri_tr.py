# coding=utf-8
import os

from clickhouse_driver import Client
import scipy.io as scio
import numpy as np

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("DBcenter\\") + len("DBcenter\\")]


def countSpace():
    """
    统计电磁暂态数据空间大小
    :return: float unit:(M)
    """
    client = Client(host='192.168.0.133', database='cloudpss')

    sql = "SELECT  sum(data_compressed_bytes) as data_compressed_bytes FROM system.columns WHERE database = 'cloudpss' and table like '%result%' "
    res = client.execute(sql)[0][0] / (1024 ** 2)
    return res


def deleteTable(tableName=''):
    client = Client(host='192.168.0.133', database='cloudpss')

    sql = "drop table if exists " + tableName
    client.execute(sql)


def getTables(searchParam):
    client = Client(host='192.168.0.133', database='cloudpss')
    searchParam = searchParam.replace('_', '\\\\_')
    sql = "SELECT table, sum(data_uncompressed_bytes) from system.columns WHERE database='cloudpss' and   data_uncompressed_bytes!=0 and table like '%result%' and  table like '%" + searchParam + "%' group by table"
    # sql = "SELECT name from system.tables WHERE database='cloudpss' and name like '%result%' and name like '%" + searchParam + "%'"
    res = list(client.execute(sql))
    templist = []
    for i in res:
        templist.append({'tableName': i[0], 'filesize': round(i[1] / 1024**2,4)})
    return templist


def getChannels(tableName=''):
    """
    :param tableName:
    :return: ('整流侧电压谐波:0', '整流侧电压谐波:1', '整流侧电压谐波:10', '整流侧电压谐波:11', '整流侧电压谐波:2', '整流侧电压谐波:3', '整流侧电压谐波:4', '整流侧电压谐波:5', '整流侧电压谐波:6', '整流侧电压谐波:7', '整流侧电压谐波:8', '整流侧电压谐波:9', '正极直流电压:0')
    """
    sql = 'select names from ' + tableName + ' limit 1'
    client = Client(host='192.168.0.133', database='cloudpss')

    res = client.execute(sql)
    if len(res) > 0:
        return res[0][0]
    else:
        return []


def selectchannelexec(tableName=None, channels=[]):
    """
    :param startid:
    :param endid:
    :param tableName:
    :param channel:
    :return:
    [(1, '整流侧电压谐波:1', (217.94054558081288, 342.4467365888453, 397.34617496712883, 467.67095294250163, 474.19872161836406, 453.1596432425776, 369.15004213913977, 311.5063749013177, 190.0755924861298, 147.96697268162194, 184.48290258389548, 289.8746897968707, 336.34626963891424, 395.8750200248873, 401.4003972324493, 383.59135571236175, 312.47888284323693, 263.68431265513215, 160.89552660495778, 125.25159654865182, 156.16119824999063, 245.37362145228926, 284.71114954163846, 335.10088077922217, 339.77809763239327, 324.7032314165036, 264.5075462837351, 223.20373561251782, 136.19546899698813, 106.02292149442302, 132.1872694550898, 207.7044899810023, 241.00289839135758, 283.65661652125584, 287.6160977069352, 274.85544771116673, 223.90061895755875, 188.9378892161196, 115.28717280364752, 89.74605595941891, 111.89410920574653, 175.8181831948057, 204.00444438521083, 240.11013480508623, 243.46186210164623, 232.66001777720058, 189.52778431430298, 159.9326828593077, 97.58826913065458, 75.96840699205993, 94.71663922029906, 148.8267593739482, 172.68586142672683, 203.2489865409226, 206.0859295113061, 196.94230256028106, 160.4319858627702, 135.38021511760832, 82.60636603049825, 64.3062702748718, 80.17609570011531, 125.97893619025427, 146.17542332572978, 172.04664717215712, 174.44783198800596, 166.70806186192956, 135.80285028085052, 114.59674595565583, 69.92479501163588, 54.43431398652508, 67.8674052186966, 106.63886505677361, 123.73498968726112, 145.6342589336536, 147.66690137840573, 141.1154743780585, 114.9545207796117, 97.00385401384099, 59.19038007993864, 46.077402677788825, 57.44821621191408, 90.26803833411854, 104.73950930660254, 123.27659710963633, 124.99746949845888, 119.45175648970975, 97.30673219716121, 82.11199865718929, 50.10375154337879, 39.00330582246064, 48.62887155213943, 76.4103598846067, 88.65998213202933, 104.35138232031994, 105.80815576262995, 101.11363911999635, 82.36837540606219, 69.50650212326302, 42.411707966016365, 33.01560189621051, 41.163739644344794, 64.67977379626055, 75.04879814262061, 88.33169139117456, 89.56482826629552, 85.59092485845773, 69.7233010465771, 58.835633317675494, 35.89991792597392, 27.946947819400194, 34.84403669619552, 54.750010922970866, 63.527643291297125, 74.7717674128281, 75.81526333416383, 72.45130517563457, 59.01917087106737, 49.802590897196474, 30.388112795320215, 23.656180032281963, 29.494176305221888, 46.34489253484003, 53.77540803760773, 63.29344623601875, 64.17646688075077, 61.32876643188777, 49.958284258203065, 42.15665907581629, 25.72309768082144, 20.024236882594256, 24.966029737642792, 39.23017741186731, 45.51995437445484, 53.576823958210554, 54.32441059912696, 51.9137579390579, 42.28858293028996, 35.6847143707361, 21.77401646711248, 16.949874487525324, 21.13320810183228, 33.20762600632198, 38.53180323648584, 45.35197762635918, 45.98475311637813, 43.9440440790234, 35.796413435403345, 30.20636817876712, 18.431065406225176, 14.347659863856219, 17.888838806428787, 28.10958127482249, 32.61648395563236, 38.38982184740096, 38.92533805853859, 37.197838068822136, 30.300931367390657, 25.56899211064741, 15.60135431355599, 12.14497430828813, 15.142467154686651, 23.794194984180695, 27.609321696337773, 32.49645286741304, 32.94967959106342, 31.48733513658079, 25.649075110565335, 21.643501015177605, 13.206129115759687, 10.280373824358621, 12.817660442811235, 20.141335907464008, 23.370860590176026, 27.50779941480083, 27.891418492125535, 26.653508215984214, 21.7113412890329, 18.320655252157106, 11.178629124682132, 8.701976197603877, 10.84976489765059, 17.049265329573817, 19.783063115079624, 23.2849999544552, 23.609699830640608, 22.561748718805095, 18.37812661455003, 15.507948464718178, 9.462359555142857, 7.365902925943831, 9.184006326750916, 14.431870380630386, 16.746046040595587, 19.710490491810713, 19.985294818364412, 19.098139145165437, 15.556633881558419, 13.12704745247231, 8.009550553113657, 6.234968024968582), (0.20100000000006024, 0.20200000000006124, 0.20300000000006224, 0.20400000000006324, 0.20500000000006424, 0.20600000000006524, 0.20700000000006624, 0.20800000000006724, 0.20900000000006824, 0.21000000000006924, 0.21100000000007024, 0.21200000000007124, 0.21300000000007224, 0.21400000000007324, 0.21500000000007424, 0.21600000000007524, 0.21700000000007624, 0.21800000000007724, 0.21900000000007824, 0.22000000000007924, 0.22100000000008024, 0.22200000000008124, 0.22300000000008224, 0.22400000000008324, 0.22500000000008424, 0.22600000000008524, 0.22700000000008624, 0.22800000000008724, 0.22900000000008824, 0.23000000000008924, 0.23100000000009024, 0.23200000000009124, 0.23300000000009224, 0.23400000000009324, 0.23500000000009424, 0.23600000000009524, 0.23700000000009624, 0.23800000000009724, 0.23900000000009824, 0.24000000000009925, 0.24100000000010025, 0.24200000000010125, 0.24300000000010225, 0.24400000000010325, 0.24500000000010425, 0.24600000000010525, 0.24700000000010625, 0.24800000000010725, 0.24900000000010825, 0.25000000000010925, 0.25100000000011025, 0.25200000000011125, 0.25300000000011225, 0.25400000000011325, 0.25500000000011425, 0.25600000000011525, 0.25700000000011625, 0.25800000000011725, 0.25900000000011825, 0.26000000000011925, 0.26100000000012025, 0.26200000000012125, 0.26300000000012225, 0.26400000000012325, 0.26500000000012425, 0.26600000000012525, 0.26700000000012625, 0.26800000000012725, 0.26900000000012825, 0.27000000000012925, 0.27100000000013025, 0.27200000000013125, 0.27300000000013225, 0.27400000000013325, 0.27500000000013425, 0.27600000000013525, 0.27700000000013625, 0.27800000000013725, 0.27900000000013825, 0.28000000000013925, 0.28100000000014025, 0.28200000000014125, 0.28300000000014225, 0.28400000000014325, 0.28500000000014425, 0.28600000000014525, 0.28700000000014625, 0.28800000000014725, 0.28900000000014825, 0.29000000000014925, 0.29100000000015025, 0.29200000000015125, 0.29300000000015225, 0.29400000000015325, 0.29500000000015425, 0.29600000000015525, 0.29700000000015625, 0.29800000000015725, 0.29900000000015825, 0.30000000000015925, 0.30100000000016025, 0.30200000000016125, 0.30300000000016225, 0.30400000000016325, 0.30500000000016425, 0.30600000000016525, 0.30700000000016625, 0.30800000000016725, 0.30900000000016825, 0.31000000000016925, 0.31100000000017025, 0.31200000000017125, 0.31300000000017225, 0.31400000000017325, 0.31500000000017425, 0.31600000000017525, 0.31700000000017625, 0.31800000000017725, 0.31900000000017825, 0.32000000000017925, 0.32100000000018025, 0.32200000000018125, 0.32300000000018225, 0.32400000000018325, 0.32500000000018425, 0.32600000000018525, 0.32700000000018625, 0.32800000000018725, 0.32900000000018825, 0.33000000000018925, 0.33100000000019025, 0.33200000000019125, 0.33300000000019225, 0.33400000000019325, 0.33500000000019425, 0.33600000000019525, 0.33700000000019625, 0.33800000000019725, 0.33900000000019825, 0.34000000000019925, 0.34100000000020025, 0.34200000000020125, 0.34300000000020225, 0.34400000000020325, 0.34500000000020425, 0.34600000000020525, 0.34700000000020625, 0.34800000000020725, 0.34900000000020825, 0.35000000000020925, 0.35100000000021025, 0.35200000000021126, 0.35300000000021226, 0.35400000000021326, 0.35500000000021426, 0.35600000000021526, 0.35700000000021626, 0.35800000000021726, 0.35900000000021826, 0.36000000000021926, 0.36100000000022026, 0.36200000000022126, 0.36300000000022226, 0.36400000000022326, 0.36500000000022426, 0.36600000000022526, 0.36700000000022626, 0.36800000000022726, 0.36900000000022826, 0.37000000000022926, 0.37100000000023026, 0.37200000000023126, 0.37300000000023226, 0.37400000000023326, 0.37500000000023426, 0.37600000000023526, 0.37700000000023626, 0.37800000000023726, 0.37900000000023826, 0.38000000000023926, 0.38100000000024026, 0.38200000000024126, 0.38300000000024226, 0.38400000000024326, 0.38500000000024426, 0.38600000000024526, 0.38700000000024626, 0.38800000000024726, 0.38900000000024826, 0.39000000000024926, 0.39100000000025026, 0.39200000000025126, 0.39300000000025226, 0.39400000000025326, 0.39500000000025426, 0.39600000000025526, 0.39700000000025626, 0.39800000000025726, 0.39900000000025826, 0.40000000000025926)),
     (2, '整流侧电压谐波:1', (7.773979151327734, 12.21628399665022, 14.175269688167417, 16.68473689589565, 16.917295555770433, 16.16625896632797, 13.168294808779084, 11.11164992060852, 6.779779651661932, 5.277658127350621, 6.580406373368723, 10.340833013471867, 11.99916135175927, 14.123487083306433, 14.320291394109622, 13.684481405481636, 11.146604897547011, 9.405647448493417, 5.738811726346701, 4.467302890931189, 5.570061179175822, 8.753303351299099, 10.157126831902042, 11.955432414902237, 12.121978403845526, 11.58370337432114, 9.435278112221875, 7.961549163392201, 4.857653384843399, 3.781345190895665, 4.7148241111871, 7.409489597230556, 8.597875688906061, 10.12021445676537, 10.261147601810517, 9.805431200825405, 7.986672042058196, 6.739149466783163, 4.111764866005936, 3.20069628980155, 3.9908857856872046, 6.271973801566657, 7.27799635995282, 8.566737898768821, 8.685987097369402, 8.30015487836778, 6.760455308087086, 5.704410994354352, 3.480381264214202, 2.7091914874572036, 3.378086200276805, 5.309086124153472, 6.160743103946404, 7.251748848099679, 7.3526415619548935, 7.025966296351231, 5.722485667090402, 4.828522564148335, 2.9459274006805463, 2.2931424637381363, 2.859361002561381, 4.49401967350953, 5.2150096415374705, 6.13863395841637, 6.223989113761217, 5.947389740299077, 4.843862671667797, 4.087098256424147, 2.4935235238022284, 1.9409631174499418, 2.420268507589623, 3.8040815977277833, 4.414463749304706, 5.196402042199104, 5.268605964391034, 5.034394584597535, 4.10012390369596, 3.4594963768535005, 2.1105721853659065, 1.6428487649743122, 2.0485849970598866, 3.220061783196127, 3.7368159072489777, 4.39882005212798, 4.459891726740601, 4.261560587055377, 3.4705627513823805, 2.9282433075214884, 1.786410279390404, 1.3905006860434943, 1.7339623170017346, 2.7256993957959845, 3.1631991504611907, 3.7236817498799786, 3.7753297250971722, 3.607370533315059, 2.9376510121452384, 2.4785473669319718, 1.5120127803986962, 1.1768932180292364, 1.4676400924138646, 2.307248635609713, 2.6776371958250675, 3.1521398694734524, 3.1958293668857456, 3.053599583048292, 2.4865430079248134, 2.0979013545127025, 1.279815556064027, 0.9961537329160909, 1.2422300487191429, 1.953052317518957, 2.266694049957506, 2.668384165806101, 2.704940872151053, 2.5844247262387396, 2.1046198477196683, 1.7758951044174818, 1.0835584573810655, 0.8435394866158399, 1.051897431963334, 1.6533662837105132, 1.9187351463438342, 2.258688532214645, 2.28947970788343, 2.1874423032338064, 1.781478186173466, 1.5033990338278533, 0.9175296802032322, 0.7144173348558599, 0.8908086619758269, 1.3998712674235507, 1.6242495158407255, 1.9114435024304897, 1.9378749648394167, 1.8518148606308122, 1.5082514307384909, 1.2726603367356337, 0.776516272190067, 0.6046936106200806, 0.753882206788484, 1.184861588685872, 1.374963975455349, 1.6179524900818647, 1.640005352589134, 1.567206484081389, 1.2769473275566396, 1.0777503939102377, 0.6573942919907494, 0.5117778907637232, 0.638142861164811, 1.0024357420615213, 1.1644041981993283, 1.371910799995747, 1.3903406686610789, 1.3273762127810098, 1.0781879214193864, 0.9091830366179569, 0.5524405768521313, 0.43016701857512457, 0.5429173472685859, 0.8497611918501207, 0.9864332436231678, 1.1614973870939762, 1.17749807693414, 1.123896792415468, 0.9114689803510237, 0.7658241290635543, 0.4674827274611515, 0.36611892344962194, 0.45999522283155486, 0.7217362439011787, 0.8353129286278939, 0.97947761289693, 0.9922397237451984, 0.9482411466395306, 0.7744140550232638, 0.651655011676389, 0.39802456056074875, 0.31593516125916865, 0.38583375688805166, 0.6091075246116187, 0.7049994517147435, 0.8283900449395658, 0.8386236223378519, 0.801732875828223, 0.6535996368959164, 0.5530862746748596, 0.3363269867344347, 0.2655832294070046, 0.3263033848479775, 0.5147118616135009, 0.5965797728170448, 0.7019418881461567, 0.7099869302614699, 0.6779937592576208, 0.5489491059558873, 0.4659851318768274, 0.2838811313014134, 0.21773433444041632), (0.40100000000026026, 0.40200000000026126, 0.40300000000026226, 0.40400000000026326, 0.40500000000026426, 0.40600000000026526, 0.40700000000026626, 0.40800000000026726, 0.40900000000026826, 0.41000000000026926, 0.41100000000027026, 0.41200000000027126, 0.41300000000027226, 0.41400000000027326, 0.41500000000027426, 0.41600000000027526, 0.41700000000027626, 0.41800000000027726, 0.41900000000027826, 0.42000000000027926, 0.42100000000028026, 0.42200000000028126, 0.42300000000028226, 0.42400000000028326, 0.42500000000028426, 0.42600000000028526, 0.42700000000028626, 0.42800000000028726, 0.42900000000028826, 0.43000000000028926, 0.43100000000029026, 0.43200000000029126, 0.43300000000029226, 0.43400000000029326, 0.43500000000029426, 0.43600000000029526, 0.43700000000029626, 0.43800000000029726, 0.43900000000029826, 0.44000000000029926, 0.44100000000030026, 0.44200000000030126, 0.44300000000030226, 0.44400000000030326, 0.44500000000030426, 0.44600000000030526, 0.44700000000030626, 0.44800000000030726, 0.44900000000030826, 0.45000000000030926, 0.45100000000031026, 0.45200000000031126, 0.45300000000031226, 0.45400000000031326, 0.45500000000031426, 0.45600000000031526, 0.45700000000031626, 0.45800000000031726, 0.45900000000031826, 0.46000000000031926, 0.46100000000032026, 0.46200000000032126, 0.46300000000032226, 0.46400000000032326, 0.46500000000032427, 0.46600000000032527, 0.46700000000032627, 0.46800000000032727, 0.46900000000032827, 0.47000000000032927, 0.47100000000033027, 0.47200000000033127, 0.47300000000033227, 0.47400000000033327, 0.47500000000033427, 0.47600000000033527, 0.47700000000033627, 0.47800000000033727, 0.47900000000033827, 0.48000000000033927, 0.48100000000034027, 0.48200000000034127, 0.48300000000034227, 0.48400000000034327, 0.48500000000034427, 0.48600000000034527, 0.48700000000034627, 0.48800000000034727, 0.48900000000034827, 0.49000000000034927, 0.49100000000035027, 0.49200000000035127, 0.49300000000035227, 0.49400000000035327, 0.49500000000035427, 0.49600000000035527, 0.49700000000035627, 0.49800000000035727, 0.49900000000035827, 0.5000000000003593, 0.5010000000003547, 0.5020000000003502, 0.5030000000003456, 0.5040000000003411, 0.5050000000003365, 0.506000000000332, 0.5070000000003274, 0.5080000000003229, 0.5090000000003183, 0.5100000000003138, 0.5110000000003092, 0.5120000000003047, 0.5130000000003001, 0.5140000000002956, 0.515000000000291, 0.5160000000002865, 0.5170000000002819, 0.5180000000002773, 0.5190000000002728, 0.5200000000002682, 0.5210000000002637, 0.5220000000002591, 0.5230000000002546, 0.52400000000025, 0.5250000000002455, 0.5260000000002409, 0.5270000000002364, 0.5280000000002318, 0.5290000000002273, 0.5300000000002227, 0.5310000000002182, 0.5320000000002136, 0.5330000000002091, 0.5340000000002045, 0.5350000000002, 0.5360000000001954, 0.5370000000001909, 0.5380000000001863, 0.5390000000001818, 0.5400000000001772, 0.5410000000001727, 0.5420000000001681, 0.5430000000001636, 0.544000000000159, 0.5450000000001545, 0.5460000000001499, 0.5470000000001454, 0.5480000000001408, 0.5490000000001363, 0.5500000000001317, 0.5510000000001272, 0.5520000000001226, 0.5530000000001181, 0.5540000000001135, 0.555000000000109, 0.5560000000001044, 0.5570000000000999, 0.5580000000000953, 0.5590000000000908, 0.5600000000000862, 0.5610000000000817, 0.5620000000000771, 0.5630000000000726, 0.564000000000068, 0.5650000000000635, 0.5660000000000589, 0.5670000000000543, 0.5680000000000498, 0.5690000000000452, 0.5700000000000407, 0.5710000000000361, 0.5720000000000316, 0.573000000000027, 0.5740000000000225, 0.5750000000000179, 0.5760000000000134, 0.5770000000000088, 0.5780000000000043, 0.5789999999999997, 0.5799999999999952, 0.5809999999999906, 0.5819999999999861, 0.5829999999999815, 0.583999999999977, 0.5849999999999724, 0.5859999999999679, 0.5869999999999633, 0.5879999999999588, 0.5889999999999542, 0.5899999999999497, 0.5909999999999451, 0.5919999999999406, 0.592999999999936, 0.5939999999999315, 0.5949999999999269, 0.5959999999999224, 0.5969999999999178, 0.5979999999999133, 0.5989999999999087, 0.5999999999999042))]

    """
    client = Client(host='192.168.0.133', database='cloudpss')

    sqlstr = "select id ,nl, da,tm from (select id, names,datas,times from `" + tableName + "` " + " order by id) array join names as nl,datas as da,times as tm"
    cond = " where nl = '" + channels[0] + "'"
    """多个通道同时查询"""
    channels.pop(0)
    for val in channels:
        cond = cond + " or nl = '" + val + "'"
    sqlstr = sqlstr + cond
    data = client.execute(sqlstr)
    return list(data)


def getChannelIdCount(tableName=None, channel=''):
    """
    :param tableName:
    :param channel:
    :return: number
    """
    client = Client(host='192.168.0.133', database='cloudpss')

    sqlstr = "select count(id) from (select id,names,datas,times from `" + tableName + "` order by `id`) array join names as nl,datas as da,times as tm"
    cond = " where nl = '" + channel + "'"
    sqlstr = sqlstr + cond
    data = client.execute(sqlstr)
    return data[0][0]


def selectIdChannelexec(id=None, tableName=None, channel=''):
    """
    :param id:
    :param tableName:
    :param channel:
    :return: tuple n-2

    """
    client = Client(host='192.168.0.133', database='cloudpss')

    sqlstr = "select da,tm from (select id,names,datas,times from `" + tableName + "`  where id = " + str(
        id) + ") array join names as nl,datas as da,times as tm"
    cond = " where nl = '" + channel + "'"
    sqlstr = sqlstr + cond
    data = client.execute(sqlstr)
    return data[0]


def saveToMat(tableName=None, channels=[]):
    channels_len = len(channels)
    channels_copy = channels.copy()
    channels_utf = []
    for i in channels:
        channels_utf.append(i.encode('utf-8'))
    channels_data = selectchannelexec(tableName, channels)
    mat_data = {}
    if len(channels_data) > 0:
        for i in range(channels_len):
            key = 'Ch_' + str(i + 1)
            for item in channels_data:
                if channels_copy[i] == item[1]:
                    if key not in mat_data:
                        mat_data[key] = {'data': item[2], 'time': item[3], 'name': channels_copy[i]}
                    else:
                        mat_data[key]['data'] += item[2]
                        mat_data[key]['time'] += item[3]
    else:
        mat_data['data'] = ()
        mat_data['time'] = ()
    filePath = os.path.abspath(rootPath + 'clickhouse\\example.mat')
    data = scio.loadmat(filePath)
    ch = data['Ch']
    output = {}
    for key, v in mat_data.items():
        ch_copy = ch.copy()
        data = np.array(v['data']).reshape(len(v['data']), 1)
        time = np.array(v['time']).reshape(len(v['time']), 1)
        print(v['name'])
        ch_copy[0][0][0] = v['name'].encode('utf-8')
        ch_copy[0][0][1] = np.concatenate((data, time), axis=1)
        output[key] = ch_copy
    output['ChannelName'] = np.array(channels_utf, dtype='object')
    scio.savemat('output.mat', output)  # 写入mat文件
