#!/usr/bin/env python3
"""Wait until Elasticsearch accepts HTTP connections."""

import os
import sys
import time
import urllib.error
import urllib.request


url = os.environ.get("ELASTICSEARCH_URL", "http://elasticsearch:9200/")
timeout = float(os.environ.get("ELASTICSEARCH_WAIT_TIMEOUT", "60"))
deadline = time.monotonic() + timeout

while True:
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            if 200 <= response.status < 500:
                print("Elasticsearch is ready.")
                break
    except (OSError, urllib.error.URLError):
        pass

    if time.monotonic() >= deadline:
        print(
            f"Elasticsearch did not become available at {url} within {timeout:g} seconds.",
            file=sys.stderr,
        )
        sys.exit(1)

    time.sleep(1)
