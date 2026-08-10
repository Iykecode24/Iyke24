class StorageClient:
    def __init__(self, provider: str, config: dict):
        self.provider = provider
        self.config = config

    def upload(self, file_data, path: str): pass
    def download(self, path: str): pass
    def delete(self, path: str): pass
    def list(self, prefix: str): pass
    def signed_url(self, path: str): return ""
    def check_connection(self) -> bool: return True
