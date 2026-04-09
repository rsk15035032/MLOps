import requests
from typing import Dict, Any, Optional


class LambdaInvoker:
    """
    A reusable client for invoking AWS Lambda (local container or remote endpoint).

    Supports:
    - Local Lambda Runtime Interface Emulator (RIE)
    - API Gateway endpoints (with slight modification)
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        function_path: str = "/2015-03-31/functions/function/invocations",
        timeout: int = 10,
    ) -> None:
        """
        Initialize the Lambda invoker.

        Args:
            base_url (str): Base URL of Lambda service (local or remote)
            function_path (str): Lambda invocation endpoint path
            timeout (int): Request timeout in seconds
        """
        self.url = f"{base_url.rstrip('/')}{function_path}"
        self.timeout = timeout

    def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke Lambda function with given payload.

        Args:
            payload (dict): JSON payload to send

        Returns:
            dict: Parsed JSON response from Lambda
        """
        try:
            response = requests.post(
                self.url,
                json=payload,
                timeout=self.timeout
            )

            # Raise exception for HTTP errors (4xx, 5xx)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout:
            return {"error": "Request timed out"}

        except requests.exceptions.ConnectionError:
            return {"error": "Failed to connect to Lambda service"}

        except requests.exceptions.HTTPError as e:
            return {
                "error": f"HTTP error occurred: {e}",
                "status_code": response.status_code
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Unexpected error: {e}"}


# -------------------------------------------------------------------
# Example Usage
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Initialize client (can be reused across multiple calls)
    client = LambdaInvoker()

    # Example payload (can be anything depending on your model/API)
    payload = {
        "url": "http://bit.ly/mlbookcamp-pants"
    }

    # Invoke Lambda
    result = client.invoke(payload)

    # Pretty print result
    print("✅ Lambda Response:")
    print(result)