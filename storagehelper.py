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
            # "STREAMDEV:test-299212:lafleet/devices/location/+/streaming"
            # "DEVLOC:test-299212:lafleet/devices/location/+/streaming"
            key = bkey.decode("utf-8")
            arr.append(key)

        return arr

    @staticmethod
    def getStreamsKey():
        keys = StorageHelper.getAllKeys('STREAMDEV:')
        arr = []
        for key in keys:
            if key.startswith('STREAMDEV:') and key.count(':') == 2:
                arr.append(key)

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
