
# Endpoints

[OpenAPI redisPerformanceAnalyticsPy](https://app.swaggerhub.com/apis/LaFleet/redisPerformanceAnalyticsPy/0.1)

* GET /
* GET /health
* POST devices/stats
* POST devices/data
* DELETE devices

  
# Install the app

[How do I create a Python 3 virtual environment with the Boto 3 library on Amazon Linux 2?](https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-python3-boto3/)
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3 -y
python3 --version
which python3
sudo apt install python3-pip
pip3 install --user virtualenv
sudo apt install python3.9-venv
python3 -m venv venv

source $PWD/venv/bin/activate
echo "source $PWD/venv/bin/activate" >> ~/.bashrc
which python
pip install pip --upgrade
pip3 install -r requirements.txt
which python
```

```
deactivate
```

# Start the app

```
python3 main.py
DEBUG=True python3 main.py
waitress-serve --port=5973 --call main:create_app
```

```
curl -X DELETE http://10.0.2.15:5972/devices
//curl -X POST -H "Content-Type: application/json" -d '{"key1":"value1", "key2":"value2"}' http://10.0.2.15:5972/devices/stats
//curl -X POST -d "param1=value1&param2=value2" http://10.0.2.15:5972/devices/stats
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/devices/stats
curl -s -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/devices/stats | jq '.summary'
curl -s -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/devices/stats | jq '.stats'
curl -s -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/devices/stats | jq '.data'
curl --silent --raw --show-error --verbose -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/devices/stats
curl -X POST -H "Content-Type: text/html" http://127.0.0.1:5000/devices/stats
```

[Use this tool to convert JSON into CSV](http://convertcsv.com/json-to-csv.htm)


# Play with docker locally

```
docker build --tag redis-performance-analytics-py:v0.01 .
sudo docker run -it -p 5972:5972 redis-performance-analytics-py:v0.01
curl -X GET -H "Content-Type: text/html" http://127.0.0.1:5972/
sudo docker logs da29d22cb82d

sudo docker run -it -p 5973:5973 redis-performance-analytics-py:v0.01
```

## Playing around

```
npm start --idle true
docker run --env IDLE=true -t mock-iot-gps-device-awsskdv2:v0.01
docker run --detach --rm --env IDLE=true
```

# Play with redis locally

```
sudo docker run --name redis-service -d redis
sudo docker run --name redis-service -d -p 6379:6379 redis
//redis-cli -h 172.17.0.3 -p 6379
//sudo docker run -it -p 6379:6379 redis bash
sudo docker exec -it redis-service bash
root@72c388dc2cb8:/data# redis-cli
```

# Statistics in plain text (example)
  
- td_dev_srv: Time Device to IoT Core  
- td_srv_wrk: IoT Core to Worker  
- td_wrk_db: Worker to Redisearch  
- td_dev_db: Device to Redisearch (total)  

```
Start time 2022-04-12 21:29:55.039000 and end 2022-04-12 21:32:25.340000
First record 2022-04-12 21:29:55.039000 and last 2022-04-12 21:32:25.343000, timedelta 150.304 seconds
5 devices with stats out of 5
75000 records with stats out of 75000, 498.9887162018309 records/sec
metric:td_dev_srv, measure:mean => min:14.3, max:16.5, mean:15.3
metric:td_dev_srv, measure:median => min:11.0, max:12.0, mean:11.4
metric:td_dev_srv, measure:max => min:212, max:309, mean:268.8
metric:td_dev_srv, measure:min => min:5, max:6, mean:5.4
metric:td_dev_srv, measure:p90 => min:21.0, max:25.0, mean:23.0
metric:td_dev_srv, measure:p95 => min:26.0, max:31.0, mean:29.2
metric:td_dev_srv, measure:p99 => min:66.6, max:92.0, mean:82.1
metric:td_srv_wrk, measure:mean => min:75.4, max:75.9, mean:75.6
metric:td_srv_wrk, measure:median => min:67.0, max:68, mean:67.2
metric:td_srv_wrk, measure:max => min:203, max:419, mean:254.2
metric:td_srv_wrk, measure:min => min:36, max:36, mean:36
metric:td_srv_wrk, measure:p90 => min:104.0, max:107.0, mean:105.4
metric:td_srv_wrk, measure:p95 => min:119.0, max:121.0, mean:120.0
metric:td_srv_wrk, measure:p99 => min:144.0, max:158.0, mean:152.8
metric:td_wrk_db, measure:mean => min:1.5, max:1.7, mean:1.6
metric:td_wrk_db, measure:median => min:1.0, max:1.0, mean:1.0
metric:td_wrk_db, measure:max => min:53, max:121, mean:82.2
metric:td_wrk_db, measure:min => min:0, max:0, mean:0
metric:td_wrk_db, measure:p90 => min:3.0, max:3.0, mean:3.0
metric:td_wrk_db, measure:p95 => min:5.0, max:6.0, mean:5.2
metric:td_wrk_db, measure:p99 => min:10.0, max:14.0, mean:11.4
metric:td_srv_db, measure:mean => min:76.9, max:77.5, mean:77.2
metric:td_srv_db, measure:median => min:69.0, max:70, mean:69.2
metric:td_srv_db, measure:max => min:204, max:420, mean:259.4
metric:td_srv_db, measure:min => min:36, max:38, mean:37
metric:td_srv_db, measure:p90 => min:106.0, max:109.0, mean:107.2
metric:td_srv_db, measure:p95 => min:121.0, max:123.0, mean:122.2
metric:td_srv_db, measure:p99 => min:146.0, max:161.0, mean:155.0
metric:td_dev_db, measure:mean => min:91.4, max:93.5, mean:92.5
metric:td_dev_db, measure:median => min:83.0, max:86.0, mean:84.6
metric:td_dev_db, measure:max => min:286, max:432, mean:379.4
metric:td_dev_db, measure:min => min:43, max:47, mean:45.4
metric:td_dev_db, measure:p90 => min:124.0, max:127.0, mean:125.8
metric:td_dev_db, measure:p95 => min:142.0, max:145.0, mean:143.0
metric:td_dev_db, measure:p99 => min:186.1, max:203.2, mean:190.8
```
