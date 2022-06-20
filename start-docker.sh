# Just create interactive container. No start but named for future reference.
sudo docker create -it --name rpa-container redis-performance-analytics-py

# Now start it.
sudo docker start rpa-container

# Now attach bash session.
sudo docker exec -it rpa-container bash
