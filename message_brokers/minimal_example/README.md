# Minimal example 

This is very minimal example of web application in flask that communicates with some receiver via rabbitmq.


## How to start

`docker-compose up --scale receiver=3`
This command will spawn 5 containers. Web-app sender, rabitmq que and 3 receivers. 
Rabbitmq need some time to start.
If que is not available receiver will throw an error and restart.
Log like this indicates that everything is ready.
```log
minimal_example-receiver-1  | INFO:root:Creating channel
minimal_example-receiver-1  | INFO:pika.adapters.blocking_connection:Created channel=1
minimal_example-receiver-1  | INFO:root:Declare channel
minimal_example-receiver-1  | INFO:root:set consumer
minimal_example-receiver-1  | INFO:root:consuming start
```

Browser can be used to do request like this
`GET http://localhost:8000/add?sleep_count=50`
This request will spawn 50 jobs for receivers. 
Job task 2 to 10 second to finish. 
Logs below shows information about starting and finishing jobs.

```log
minimal_example-receiver-2  | INFO:root: [x] Received b'0'
minimal_example-receiver-3  | INFO:root: [x] Received b'1'
minimal_example-receiver-1  | INFO:root: [x] Received b'2'
```

```log
minimal_example-receiver-1  | INFO:root: [x] Processed b'2'
minimal_example-receiver-1  | INFO:root: [x] Received b'5'
minimal_example-receiver-3  | INFO:root: [x] Processed b'1'
minimal_example-receiver-3  | INFO:root: [x] Received b'4'
```




