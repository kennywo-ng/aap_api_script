from requests import Session, Response, RequestException, adapters
from requests.auth import HTTPBasicAuth
from typing import Any, Iterator
from urllib3.util.retry import Retry

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class APIClient_tmp:
    def __init__(self, base_url: str, username: str, psw: str, timeout: float = 10.0, retries: int = 2, backoff: float = 0.3, verify: bool = False):
        self.verify = verify
        self.base_url = base_url
        self.timeout = timeout
        self.session = Session()
        self.session.auth = HTTPBasicAuth(username,psw)
        self.session.headers.update({
            "Accept": "application/json",
        })

        retry = Retry(total=retries, backoff_factor=backoff, status_forcelist=[429,500,502,503,504], allowed_methods=frozenset(["GET","POST"]))
        adapter = adapters.HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def get_pagination(self,
                path: str,
                params: dict | None = None,
                page_param: str = "page",
                results_key: str = "results") -> Iterator[dict]:
        params = dict(params or {})
        page = 1
        while True:
            params[page_param] = page
            resp = self.get(path, params=params)
            payload = resp.json().get(results_key)

            if resp.status_code >= 400:
                break
            if not payload:
                break
            
            resp.raise_for_status()

            yield from payload
            page += 1

    def get(self, path: str, params: dict | None = None, **kwargs) -> Response:
        try:
            return self.session.get(self._url(path), params=params, verify=self.verify,**kwargs)
        except RequestException as e:
            print("Error occured:", e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.session.close()