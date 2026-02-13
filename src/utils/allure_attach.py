import json

import allure
import curlify


def _clean_value(value):
    if isinstance(value, str):
        return (value
                .replace("\\r\\n", "\n")
                .replace("\\n", "\n")
                .replace("\\r", "")
                .replace("\\t", "\t")
                .replace('\\"', '"'))
    elif isinstance(value, dict):
        return {k: _clean_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_clean_value(item) for item in value]
    return value


def format_response(response) -> str:
    lines = [f"HTTP {response.status_code}"]

    for header, value in response.headers.items():
        lines.append(f"{header}: {value}")

    lines.append("")

    try:
        body = response.json()
        cleaned = _clean_value(body)
        lines.append(json.dumps(cleaned, indent=2, ensure_ascii=False))
    except (ValueError, TypeError):
        lines.append(response.text[:3000])

    return "\n".join(lines)


def attach_request_response(method: str, endpoint: str, response):
    allure.attach(
        body=curlify.to_curl(response.request),
        name=f"Request: {method} {endpoint}",
        attachment_type=allure.attachment_type.TEXT,
    )

    allure.attach(
        body=format_response(response),
        name=f"Response: {response.status_code}",
        attachment_type=allure.attachment_type.TEXT,
    )
