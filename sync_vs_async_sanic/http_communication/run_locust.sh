# locust -f ./locust/consumer_perf.py             -t 120s --headless -r 10 -u 200 --csv ./data/consumer_perf.csv
locust -f ./locust/httpx_async_perf.py          -t 120s --headless -r 10 -u 200 --csv ./data/httpx_async_perf.csv
locust -f ./locust/httpx_async_resource_perf.py -t 121s --headless -r 10 -u 200 --csv ./data/httpx_async_resource_perf.csv
locust -f ./locust/httpx_sync.py                -t 120s --headless -r 10 -u 200 --csv ./data/httpx_sync.csv
locust -f ./locust/requests.py                  -t 120s --headless -r 10 -u 200 --csv ./data/requests.csv
