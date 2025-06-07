from locust import HttpUser, task


class ClientPerf(HttpUser):
    host = "http://http_consumer_server:8080"

    @task
    def make_request_httpx_async_fast(self):
        self.client.post("/consume/0")
        # print(response)

    @task
    def make_request_httpx_async_mid(self):
        self.client.post("/consume/0.3")
        # print(response)

    @task
    def make_request_httpx_slow(self):
        self.client.post("/consume/2")
        # print(response)
