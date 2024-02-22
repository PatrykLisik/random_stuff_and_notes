from locust import HttpUser, task


class ClientPerf(HttpUser):
    host = "http://http_producer_server:8081"

    @task
    def make_request_httpx_sync(self):
        self.client.post("/make_request_httpx_sync")
