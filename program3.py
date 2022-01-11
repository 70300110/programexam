import sys
from datetime import datetime as dt

if(len(sys.argv) != 4):
    print("パラメータ(連続タイムアウト数, カウント回数, 平均応答時間)を入力してください")
else:
    N = int(sys.argv[1])
    m = int(sys.argv[2])
    t = int(sys.argv[3])

file = open('sample.log', 'r')
serverStrList = file.read().splitlines()
file.close()

serverList = []
stoppingServerList = []
keys = ['date', 'address', 'pingTime']

for serverStr in serverStrList:
    server = serverStr.split(',')
    d = dict(zip(keys, server))
    serverList.append(d)

for server in serverList:
    # for文で回しているサーバーが停止リストの中にコマンドライン引数以上ある、かつログが"-"ではなくサーバーが動いた場合、停止リストに追加された日時と動いた日時から計算し出力
    counter = len([1 for a in [f["address"] for f in stoppingServerList] if a==server["address"]])
    #TODO sys.argvのエラー処理を記述
    if (counter >= N) and server["pingTime"] != '-'):
        stopDatatime = dt.strptime([l for l in stoppingServerList if l["address"]==server["address"]][0]["date"], '%Y%m%d%H%M%S')
        startDatatime = dt.strptime(server["date"], '%Y%m%d%H%M%S')
        stopInterval = startDatatime - stopDatatime
        # 表示が終わった場合、停止リストから削除
        # TODO　forの部分をTで回数を変更できるように編集
        print("サーバー("+[l for l in stoppingServerList if l["address"]==server["address"]][0]["address"]+")は"+stopDatatime.strftime('%Y/%m/%d %H:%M:%S')+"から"+startDatatime.strftime('%Y/%m/%d %H:%M:%S')+"までの"+str(stopInterval)+"停止していました。")
        stoppingServerList = [l for l in stoppingServerList if l["address"] != server["address"] ]
        # for fragedServer in stoppingServerList:
        #     if fragedServer["address"] != server["address"]:
        #         tmpList = []
        #         tmpList.append(fragedServer)
        #         stoppingServerList = tmpList
    # for文で回しているサーバーが停止リストの中にコマンドライン引数以上無いが、サーバーが動いた場合
    elif(server["pingTime"] != '-'):
        stoppingServerList = [l for l in stoppingServerList if l["address"] != server["address"] ]
        # for fragedServer in stoppingServerList:
        #     if fragedServer["address"] != server["address"]:
        #         tmpList = []
        #         tmpList.append(fragedServer)
        #         stoppingServerList = tmpList
    # ログが"-"で停止している場合、停止リストに追加
    elif(server["pingTime"] == '-'):
        stoppingServerList.append(server)



# 最後にまだ再開していないサーバーをprint
for fragedServer in stoppingServerList:
    # 停止リストの中に同じアドレスのサーバーがコマンドライン引数以上あった場合
    counter = len([1 for a in [f["address"] for f in stoppingServerList] if a==fragedServer["address"]])
    if (counter >= N)):
        stopDatatime = dt.strptime(fragedServer["date"], '%Y%m%d%H%M%S')
        print("サーバー("+fragedServer["address"]+")は"+stopDatatime.strftime('%Y/%m/%d %H:%M:%S')+"から現在まで停止しています。")
        stoppingServerList = [l for l in stoppingServerList if l["address"] != fragedServer["address"] ]
