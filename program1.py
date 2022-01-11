from datetime import datetime as dt

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
    for fragedServer in stoppingServerList:
        # サーバーのアドレスが停止リストにある、かつログが"-"ではなくサーバーが動いた場合、停止リストに追加された日時と動いた日時から計算し出力
        if(server["address"] == fragedServer["address"] and server["pingTime"] != '-'):
            stopDatatime = dt.strptime(fragedServer["date"], '%Y%m%d%H%M%S')
            startDatatime = dt.strptime(server["date"], '%Y%m%d%H%M%S')
            stopInterval = startDatatime - stopDatatime
            # 表示が終わった場合、停止リストから削除
            print("サーバー("+fragedServer["address"]+")は"+stopDatatime.strftime('%Y/%m/%d %H:%M:%S')+"から"+startDatatime.strftime('%Y/%m/%d %H:%M:%S')+"までの"+str(stopInterval)+"停止していました。")
            stoppingServerList.remove(fragedServer)

    #ログが"-"で停止しているかまだ停止しているとみなされていない場合、停止状態のサーバーリストであるstoppingServerListに追加
    if (server["pingTime"] == '-' and server["address"] not in [f["address"] for f in stoppingServerList]):
      stoppingServerList.append(server)

# 最後にまだ再開していないサーバーをprint
for fragedServer in stoppingServerList:
  stopDatatime = dt.strptime(fragedServer["date"], '%Y%m%d%H%M%S')
  print("サーバー("+fragedServer["address"]+")は"+stopDatatime.strftime('%Y/%m/%d %H:%M:%S')+"から現在まで停止しています。")
