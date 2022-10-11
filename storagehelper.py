import os
import redis

host = os.environ.get('REDIS_HOST')
port_str = os.environ.get('REDIS_PORT')
if port_str is None or port_str == "":
    port = 6379
else:
    port = int(port_str)
#host = "172.17.0.1" # "redis-service" # "redisearch-service"
r = redis.Redis(host=host, port=port, db=0, ssl=False)


class StorageHelper():

    @staticmethod
    def flushAll():
        arr = []
        # Could use r.flushall()
        for bkey in r.scan_iter():
            key = bkey.decode("utf-8")
            r.delete(key)
            arr.append(key)

        return arr

    @staticmethod
    def getAllKeys(match):
        if match == None or match == '':
            match = '*'

        arr = []
        for bkey in r.scan_iter():
            # "STREAMDEV:test-299212:lafleet/devices/location/+/streaming:1" where 1 is streamId
            # "DEVLOC:test-299212:lafleet/devices/location/+/streaming"
            key = bkey.decode("utf-8")
            arr.append(key)

        return arr

    @staticmethod
    def getStreamsKey():
        keys = StorageHelper.getAllKeys('STREAMDEV:')

        # Getting the last stream only
        dic = {}
        for key in keys:
            if key.startswith('STREAMDEV:') and key.count(':') == 3:
                tokens = key.split(':')
                root = tokens[0] + ':' + tokens[1] + ':' + tokens[2]
                item = dic.get(root)
                index = int(tokens[3])
                if item == None:
                    dic[root] = index
                elif index > item:
                    dic[root] = index

        arr = []
        for item in dic.items():
            arr.append(item[0] + ':' + str(item[1]))

        return arr

    @staticmethod
    def getLocationsKey():
        keys = StorageHelper.getAllKeys('DEVLOC:')
        arr = []
        for key in keys:
            if key.startswith('DEVLOC:') and key.count(':') == 2:
                arr.append(key)
                
        return arr

    @staticmethod
    def getStreamFromKey(key):
        stream = r.xrange(key, '-', '+')
        return stream
