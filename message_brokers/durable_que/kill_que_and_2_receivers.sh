docker container kill $(docker ps | awk '/queue/ {print $1}')
docker container kill $(docker ps | awk '/receiver/ {print $1}' | shuf -n 3)
docker ps


