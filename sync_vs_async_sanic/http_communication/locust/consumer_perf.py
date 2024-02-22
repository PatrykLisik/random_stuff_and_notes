from locust import HttpUser, task


class ClientPerf(HttpUser):
    host = "http://http_consumer_server:8080"

    @task
    def make_request_httpx_async(self):
        self.client.post("/consume/0")
