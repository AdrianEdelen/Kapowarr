import unittest
from unittest.mock import MagicMock

from backend.implementations.download_clients.base import \
    _pixeldrain_refusal_reason


class pixeldrain_refusal_reason(unittest.TestCase):
    def test_hotlink_reason(self):
        response = MagicMock()
        response.json.return_value = {
            "success": False,
            "value": "file_rate_limited_captcha_required",
            "message": "We have detected the use of hotlinking for this file."
        }
        self.assertEqual(
            _pixeldrain_refusal_reason(response),
            "file_rate_limited_captcha_required "
            "(We have detected the use of hotlinking for this file.)"
        )

    def test_non_json_falls_back_to_status_code(self):
        response = MagicMock()
        response.status_code = 403
        response.json.side_effect = ValueError
        self.assertEqual(_pixeldrain_refusal_reason(response), "HTTP 403")
