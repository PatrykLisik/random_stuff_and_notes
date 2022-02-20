# Durable queue
In this example I wanted to emulate partial OS failure.
Code is heavily based on official rabbitmq guide which can be found here https://www.rabbitmq.com/tutorials/tutorial-two-python.html. 

For better logs separation, I recommend running every container in different console.
```shell
 docker-compose up queue 
```

```shell
 docker-compose up sender
```

```shell
docker-compose up receiver --scale receiver=4
```


RabbitQM queue is not ready immediately after container starts. 
`Receiver` has waiting mechanism.
If connection to queue has failed, receiver will wait for 10 seconds and reattempt to connect.

`Reciver` logs to console and to file `log.log`.
Script `processing_stats.sh` can monitor this file and provide information how may tasks were received by `recivers` and how many have finished. 
No matter how many times process are killed final number of acknowledgments should be equal to starting number of tasks(100) 


## Simulating failure
To test how system will behave, in case of exception or hardware failure, task has 10% chance to trow exception and script `kill_queue_and_2_receivers.sh` was prepared. 
Script "does what advertise" it kills queueue container and two random receivers.
```log
durable_queue-receiver-2 exited with code 137
durable_queue-receiver-4 exited with code 137
durable_queue-receiver-3 exited with code 137
durable_queue-receiver-1 exited with code 137
```


