from locust import HttpUser, task


class TestMakeRequest(HttpUser):
    host = "http://http_producer_server:8081"

    @task
    def make_request_httpx_async(self):
        self.client.post("/make_request_httpx_async")

