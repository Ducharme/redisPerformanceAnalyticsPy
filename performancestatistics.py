import json
import sys, os
import logging
import time
from datetime import datetime, timedelta, timezone
from dateutil import tz
import statistics
import numpy as np
from storagehelper import StorageHelper


class PerformanceStatistics:

    metrics = ["td_dev_srv", "td_srv_wrk", "td_wrk_db", "td_srv_db", "td_dev_db"]
    measures = ["mean", "median", "max", "min", "p90", "p95", "p99"]

    @staticmethod
    def ts_to_str(ts):
        return ts.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    @staticmethod   
    def td_in_ms(ts1, ts2):
        td = timedelta(hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0)
        if ts2 >= ts1:
            td = ts2 - ts1
        else:
            td = ts1 - ts2

        secs = td.seconds * 1000.0
        ms = td.microseconds / 1000.0
        rounded = round(secs + ms, 0)
        if ts2 < ts1:
            rounded = -1 * rounded
        return int(rounded)

    @staticmethod
    def bts_to_str(b):
        str = b.decode("utf-8")
        i = int(str)
        f = i / 1000.0
        dt = datetime.utcfromtimestamp(f)
        return dt

    @staticmethod
    def getItems(records, dtStart, dtEnd):
        logger = logging.getLogger("Statistics")
        try:

            td_dic = {}
            allDeviceIds = []
            statsDeviceIds = []
            allRecords = 0
            statsRecords = 0
            firstRecord = datetime.max
            lastRecord = datetime.min
            

            lastDeviceId = ""
            for row in records:
                deviceId = row[0]
                seq = int(row[1])
                dev_timestamp = row[2]
                srv_timestamp = row[3]
                wrk_timestamp = row[4]
                db_timestamp = row[5]
                allRecords = allRecords + 1
                if dev_timestamp < firstRecord:
                    firstRecord = dev_timestamp
                if db_timestamp > lastRecord:
                    lastRecord = db_timestamp
                
                if deviceId != lastDeviceId:
                    allDeviceIds.append(deviceId)
                    lastDeviceId = deviceId
                    
                if td_dic.get(deviceId) is None:
                    td_dic[deviceId] = {
                        "data": {
                        },
                        "stats": {
                        }
                    }
                    
                    for metric in PerformanceStatistics.metrics:
                        td_dic[deviceId]["data"][metric] = []
                        
                td_dev_srv = PerformanceStatistics.td_in_ms(dev_timestamp, srv_timestamp)
                td_srv_wrk = PerformanceStatistics.td_in_ms(srv_timestamp, wrk_timestamp)
                td_wrk_db = PerformanceStatistics.td_in_ms(wrk_timestamp, db_timestamp)
                td_srv_db = PerformanceStatistics.td_in_ms(srv_timestamp, db_timestamp)
                td_dev_db = PerformanceStatistics.td_in_ms(dev_timestamp, db_timestamp)
                    
                td_dic[deviceId]["data"]["td_dev_srv"].append(td_dev_srv)
                td_dic[deviceId]["data"]["td_srv_wrk"].append(td_srv_wrk)
                td_dic[deviceId]["data"]["td_wrk_db"].append(td_wrk_db)
                td_dic[deviceId]["data"]["td_srv_db"].append(td_srv_db)
                td_dic[deviceId]["data"]["td_dev_db"].append(td_dev_db)
            
            
            lastDeviceId = ""
            for deviceId in td_dic.keys():
                if td_dic[deviceId].get("data") is not None:
                    for tdKey in td_dic[deviceId]["data"].keys():
                        data = td_dic[deviceId]["data"][tdKey]
                        if len(data) >= 5:
                            if deviceId != lastDeviceId:
                                statsDeviceIds.append(deviceId)
                                statsRecords = statsRecords + len(data)
                                lastDeviceId = deviceId
                        
                            mean = round(statistics.mean(data), 1)
                            median = round(statistics.median(data), 1)
                            max_val = round(max(data), 1)
                            min_val = round(min(data), 1)
                            std_dev = round(statistics.stdev(data), 1)
                            p90 = round(np.percentile(data, 90), 1)
                            p95 = round(np.percentile(data, 95), 1)
                            p99 = round(np.percentile(data, 99), 1)
                            
                            td_dic[deviceId]["stats"][tdKey] = {"mean": mean, "median": median, "max": max_val, "min": min_val, "p90": p90, "p95": p95, "p99": p99}

            summary = {}
            tdWholeInSecs = PerformanceStatistics.td_in_ms(firstRecord, lastRecord) / 1000.0
            ratePerSec = allRecords / tdWholeInSecs
            summary["start_end"] = "Start time {} and end {}".format(dtStart, dtEnd)
            summary["first_last"] = "First record {} and last {}, timedelta {} seconds".format(firstRecord, lastRecord, tdWholeInSecs)
            summary["devices"] = "{} devices with stats out of {}".format(len(statsDeviceIds), len(allDeviceIds))
            summary["records"] = "{} records with stats out of {}, {} records/sec".format(statsRecords, allRecords, ratePerSec)
            

            logger.info("Successfully generated stats data")
            return summary, td_dic
        except UnboundLocalError as ule:
            logger.error("Failed to save data to database", ule)
        except AttributeError as ae:
            logger.error("Failed to save data to database", ae)
        except ValueError as ve:
            logger.error("Failed to save data to database", ve) 
        except NameError as ne:
            logger.error("Failed to save data to database", ne)
        except IndexError as ie:
            logger.error("Failed to save data to database", ie)
        except TypeError as te:
            logger.error("Failed to save data to database", te)
        except KeyError as ke:
            logger.error("Failed to save data to database", ke)
        except RuntimeError as re:
            logger.error("Failed to save data to database", re)
        except OSError as roee:
            logger.error("Failed to save data to database", roee)
        except:
            logger.error("Failed to save data to database")
            logger.error(sys.exc_info()[0])


    @staticmethod
    def getStats():
        logger = logging.getLogger("Statistics")

        table = []
        deviceId = ''
        dtStart = ''
        dtEnd = ''
        dtLastStart = datetime.min
        dtFirstEnd = datetime.max
        keys = StorageHelper.getStreamsKey()
        for key in keys:
            stream = StorageHelper.getStreamFromKey(key)

            tokens = key.split(':')
            deviceId = tokens[1]
            topic = tokens[2]

            length = len(stream)
            logger.info("length = " + str(length))
            streamArr = []
            for entry in stream:
                k = entry[1]

                seq = int(k[b'seq'])
                dts = PerformanceStatistics.bts_to_str(k[b'dts'])
                sts = PerformanceStatistics.bts_to_str(k[b'sts'])
                wts = PerformanceStatistics.bts_to_str(k[b'wts'])
                rts = PerformanceStatistics.bts_to_str(k[b'rts'])
                
                row = [deviceId, seq, dts, sts, wts, rts]
                streamArr.append(row)


            # Sort the stream then add row to the table
            npArr = np.array(streamArr)
            sortedArr = npArr[npArr[:, 1].argsort()]
            index = 0
            for row in sortedArr:

                if index == 0:
                    dts = row[2]
                    if dtStart == '':
                        dtStart = dts
                    elif dts < dtStart:
                        dtStart = dts

                    if dts > dtLastStart:
                        dtLastStart = dts

                if index == len(sortedArr) - 1:
                    rts = row[5]
                    if dtEnd == '':
                        dtEnd = rts
                    elif rts > dtEnd:
                        dtEnd = rts

                    if rts < dtFirstEnd:
                        dtFirstEnd = rts

                row = sortedArr[index]
                table.append(row)
                index = index + 1


        #print(f"index={index}, dts={dts}, dtLastStart={dtLastStart}, dtFirstEnd={dtFirstEnd}")
        summary_all, td_dic_all = PerformanceStatistics.getItems(table, dtStart, dtEnd)

        index = 0
        filteredTable = []
        td_diff = timedelta(seconds=5)
        dtLastStartPlusDelta = dtLastStart + td_diff
        dtFirstEndPlusDelta = dtFirstEnd - td_diff
        for row in table:
            row = table[index] # [deviceId, seq, dts, sts, wts, rts]
            deviceId = row[0]
            seq = row[1]
            dts = row[2]
            sts = row[3]
            wts = row[4]
            rts = row[5]

            if dts < dtLastStartPlusDelta:
                #print (f"dts={dts} is smaller than dtLastStart + td_diff={dtLastStart + td_diff}, skipping")
                continue
            if rts > dtFirstEndPlusDelta:
                #print (f"dts={rts} is bigger than dtFirstEnd - td_diff={dtFirstEnd - td_diff}, skipping")
                continue

            #print (f"dts={dts} is added to the list")
            filteredTable.append(row)

        summary_rng, td_dic_rng = PerformanceStatistics.getItems(filteredTable, dtLastStartPlusDelta, dtFirstEndPlusDelta)

        return summary_all, td_dic_all, summary_rng, td_dic_rng

    @staticmethod
    def getDataAsJson():
        summary, data = PerformanceStatistics.getStats()
        return data

    @staticmethod
    def getStatsAsJson():
        summary_all, data_all, summary_rng, data_rng = PerformanceStatistics.getStats()
        globalStats = {}
        rangeStats = {}
        for metric in PerformanceStatistics.metrics:
            globalStats[metric] = { }
            rangeStats[metric] = { }
            for measure in PerformanceStatistics.measures:
                gvalues = []
                rvalues = []
                globalStats[metric][measure] = { }
                rangeStats[metric][measure] = { }
                for deviceId in data_all.keys():
                    stats = data_all[deviceId].get("stats")
                    if stats is not None and len(stats) > 0:
                        gvalues.append(stats[metric][measure])
                        
                min_val = round(min(gvalues), 1)
                max_val = round(max(gvalues), 1)
                mean_val = round(statistics.mean(gvalues), 1)
                globalStats[metric][measure] = { "min": min_val, "max": max_val, "mean": mean_val }
                #print ("metric:{}, measure:{} => min:{}, max:{}, mean:{}".format(metric, measure, min_val, max_val, mean_val))

                for deviceId in data_rng.keys():
                    stats = data_rng[deviceId].get("stats")
                    if stats is not None and len(stats) > 0:
                        rvalues.append(stats[metric][measure])
                
                if len(rvalues) > 0:
                    min_val = round(min(rvalues), 1)
                    max_val = round(max(rvalues), 1)
                    mean_val = round(statistics.mean(rvalues), 1)
                    rangeStats[metric][measure] = { "min": min_val, "max": max_val, "mean": mean_val }
                    #print ("metric:{}, measure:{} => min:{}, max:{}, mean:{}".format(metric, measure, min_val, max_val, mean_val))

        """
        {
            devideId:
                stats:
                    "td_dev_srv":
                        "mean":
                        "median":
                        "max":
                        "min":
                        "p90":
                        "p95":
                        "p99":
                    "td_srv_wrk",
                    "td_wrk_db",
                    "td_srv_db",
                    "td_dev_db"
        }
        
        "td_dev_srv": {
            "max": {
                "max": 97, 
                "mean": 97, 
                "min": 97
            }, 
            "mean": {
                "max": 87.7, 
                "mean": 87.7, 
                "min": 87.7
            }, 
            "median": {
                "max": 86.0, 
                "mean": 86.0, 
                "min": 86.0
            }, 
            "min": {
                "max": 84, 
                "mean": 84, 
                "min": 84
            }, 
            "p90": {
                "max": 97.0, 
                "mean": 97.0, 
                "min": 97.0
            }, 
            "p95": {
                "max": 97.0, 
                "mean": 97.0, 
                "min": 97.0
            }, 
            "p99": {
                "max": 97.0, 
                "mean": 97.0, 
                "min": 97.0
            }
        },
        "td_srv_wrk",
        "td_wrk_db",
        "td_srv_db",
        "td_dev_db"

        """
        return summary_all, globalStats, summary_rng, rangeStats

    @staticmethod
    def getStatsAsText():
        lines = []
        summary_all, globalStats, summary_rng, rangeStats = PerformanceStatistics.getStatsAsJson()

        lines.append(summary_all["start_end"])
        lines.append(summary_all["first_last"])
        lines.append(summary_all["devices"])
        lines.append(summary_all["records"])

        #metrics = ["td_dev_srv", "td_srv_wrk", "td_wrk_db", "td_srv_db", "td_dev_db"]
        #measures = ["mean", "median", "max", "min", "p90", "p95", "p99"]
        for metric in PerformanceStatistics.metrics:
            for measure in PerformanceStatistics.measures:
                entry = globalStats[metric][measure]
                min = entry['min']
                max = entry['max']
                mean = entry['mean']
                line = f'metric:{metric}, measure:{measure} => min:{min}, max:{max}, mean:{mean}'
                lines.append(line)

        lines.append(summary_rng["start_end"])
        lines.append(summary_rng["first_last"])
        lines.append(summary_rng["devices"])
        lines.append(summary_rng["records"])

        #metrics = ["td_dev_srv", "td_srv_wrk", "td_wrk_db", "td_srv_db", "td_dev_db"]
        #measures = ["mean", "median", "max", "min", "p90", "p95", "p99"]
        for metric in PerformanceStatistics.metrics:
            for measure in PerformanceStatistics.measures:
                entry = rangeStats[metric][measure]
                if "min" in entry:
                    min = entry['min']
                    max = entry['max']
                    mean = entry['mean']
                    line = f'metric:{metric}, measure:{measure} => min:{min}, max:{max}, mean:{mean}'
                    lines.append(line)

        """
        Start time 2021-12-11 05:40:23.731000 and end 2021-12-11 05:45:42.578000
        First record 2021-12-11 05:40:23.191000 and last 2021-12-11 05:45:42.578000, timedelta 319.387 seconds
        1 devices with stats out of 1
        300 records with stats out of 300, 0.9392993453083563 records/sec
        metric:td_dev_srv, measure:mean => min:20.9, max:20.9, mean:20.9
        metric:td_dev_srv, measure:median => min:10.0, max:10.0, mean:10.0
        metric:td_dev_srv, measure:max => min:168, max:168, mean:168
        metric:td_dev_srv, measure:min => min:6, max:6, mean:6
        metric:td_dev_srv, measure:p90 => min:22.0, max:22.0, mean:22.0
        metric:td_dev_srv, measure:p95 => min:135.0, max:135.0, mean:135.0
        metric:td_dev_srv, measure:p99 => min:168.0, max:168.0, mean:168.0
        metric:td_srv_wrk, measure:mean => min:317526.7, max:317526.7, mean:317526.7
        metric:td_srv_wrk, measure:median => min:317543.5, max:317543.5, mean:317543.5
        metric:td_srv_wrk, measure:max => min:318593, max:318593, mean:318593
        metric:td_srv_wrk, measure:min => min:316370, max:316370, mean:316370
        metric:td_srv_wrk, measure:p90 => min:318497.1, max:318497.1, mean:318497.1
        metric:td_srv_wrk, measure:p95 => min:318556.0, max:318556.0, mean:318556.0
        metric:td_srv_wrk, measure:p99 => min:318593.0, max:318593.0, mean:318593.0
        metric:td_wrk_db, measure:mean => min:3.0, max:3.0, mean:3.0
        metric:td_wrk_db, measure:median => min:3.0, max:3.0, mean:3.0
        metric:td_wrk_db, measure:max => min:7, max:7, mean:7
        metric:td_wrk_db, measure:min => min:1, max:1, mean:1
        metric:td_wrk_db, measure:p90 => min:5.0, max:5.0, mean:5.0
        metric:td_wrk_db, measure:p95 => min:6.0, max:6.0, mean:6.0
        metric:td_wrk_db, measure:p99 => min:7.0, max:7.0, mean:7.0
        metric:td_srv_db, measure:mean => min:317529.7, max:317529.7, mean:317529.7
        metric:td_srv_db, measure:median => min:317546.0, max:317546.0, mean:317546.0
        metric:td_srv_db, measure:max => min:318597, max:318597, mean:318597
        metric:td_srv_db, measure:min => min:316372, max:316372, mean:316372
        metric:td_srv_db, measure:p90 => min:318500.2, max:318500.2, mean:318500.2
        metric:td_srv_db, measure:p95 => min:318560.0, max:318560.0, mean:318560.0
        metric:td_srv_db, measure:p99 => min:318597.0, max:318597.0, mean:318597.0
        metric:td_dev_db, measure:mean => min:317550.6, max:317550.6, mean:317550.6
        metric:td_dev_db, measure:median => min:317616.5, max:317616.5, mean:317616.5
        metric:td_dev_db, measure:max => min:318612, max:318612, mean:318612
        metric:td_dev_db, measure:min => min:316379, max:316379, mean:316379
        metric:td_dev_db, measure:p90 => min:318508.3, max:318508.3, mean:318508.3
        metric:td_dev_db, measure:p95 => min:318574.0, max:318574.0, mean:318574.0
        metric:td_dev_db, measure:p99 => min:318612.0, max:318612.0, mean:318612.0
        """

        return '\n'.join(lines) + '\n'
