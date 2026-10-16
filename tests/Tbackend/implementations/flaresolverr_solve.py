import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from backend.base.definitions import Constants
from backend.implementations.flaresolverr import FlareSolverr

CF_HEADERS = {
    Constants.CF_CHALLENGE_HEADER[0]: Constants.CF_CHALLENGE_HEADER[1]
}
TIMEOUT_RESPONSE = {"detail": "Timed out while loading the page"}


def _flaresolverr() -> FlareSolverr:
    fs = FlareSolverr.__new__(FlareSolverr)
    fs.base_url = "http://fs:8191"
    fs.proxy_data = None
    fs.session_semaphore = None
    return fs


class flaresolverr_failed_solve(unittest.TestCase):
    @patch("backend.implementations.flaresolverr.Session")
    def test_failed_solve_returns_none(self, session_cls: MagicMock):
        """A response without a solution (e.g. a timeout) must not raise."""
        with patch.object(
            FlareSolverr, "_FlareSolverr__api_request",
            return_value=TIMEOUT_RESPONSE
        ):
            self.assertIsNone(_flaresolverr().handle_cf_block(
                "https://example.com", CF_HEADERS
            ))

    def test_failed_solve_returns_none_async(self):
        with patch.object(
            FlareSolverr, "_FlareSolverr__async_api_request",
            new=AsyncMock(return_value=TIMEOUT_RESPONSE)
        ):
            result = asyncio.run(_flaresolverr().handle_cf_block_async(
                MagicMock(), "https://example.com", CF_HEADERS
            ))
        self.assertIsNone(result)

    def test_solution_is_extracted(self):
        solution = {
            "response": "<html></html>", "cookies": [], "userAgent": "UA"
        }
        self.assertEqual(
            FlareSolverr._extract_solution(
                "https://example.com", {"status": "ok", "solution": solution}
            ),
            solution
        )
