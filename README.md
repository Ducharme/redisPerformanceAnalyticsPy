
# Endpoints

* DELETE devices
* GET devices/stats
* GET devices/ids
* GET devices/<id>/location (last location)
* GET devices/<id>/stream

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
docker build --tag redis-performance-analitycs-py:v0.01 .
sudo docker run -it -p 5972:5972 redis-performance-analitycs-py:v0.01
curl -X GET -H "Content-Type: text/html" http://127.0.0.1:5972/
sudo docker logs da29d22cb82d

sudo docker run -it -p 5973:5973 redis-performance-analitycs-py:v0.01
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
