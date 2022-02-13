while true
do
    echo "$(date) Received: $(grep -c "Received" ./log.log )"
    echo "$(date) Acknowledged $(grep -c "Acknowledged" ./log.log )"
    echo "$(date) Task with runtime error $(grep -c "unlucky" ./log.log )"
    echo ""
    sleep 5
done

