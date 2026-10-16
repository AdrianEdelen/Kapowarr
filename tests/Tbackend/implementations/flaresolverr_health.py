import unittest
from unittest.mock import MagicMock, patch

from backend.implementations.flaresolverr import FlareSolverr


class flaresolverr_test(unittest.TestCase):
    def _health(self, session_cls: MagicMock, status_code: int, body: dict):
        session = session_cls.return_value.__enter__.return_value
        session.get.return_value.status_code = status_code
        session.get.return_value.json.return_value = body

    @patch("backend.implementations.flaresolverr.Session")
    def test_flaresolverr_status_ok(self, session_cls: MagicMock):
        self._health(session_cls, 200, {"status": "ok"})
        self.assertTrue(FlareSolverr.test_flaresolverr("http://fs:8191"))

    @patch("backend.implementations.flaresolverr.Session")
    def test_compatible_solver_without_status(self, session_cls: MagicMock):
        """Byparr answers 200 with a message but no status key."""
        self._health(session_cls, 200, {"msg": "Byparr is working!"})
        self.assertTrue(FlareSolverr.test_flaresolverr("http://byparr:8191"))

    @patch("backend.implementations.flaresolverr.Session")
    def test_explicit_non_ok_status(self, session_cls: MagicMock):
        self._health(session_cls, 200, {"status": "error"})
        self.assertFalse(FlareSolverr.test_flaresolverr("http://fs:8191"))

    @patch("backend.implementations.flaresolverr.Session")
    def test_non_200(self, session_cls: MagicMock):
        self._health(session_cls, 500, {"status": "ok"})
        self.assertFalse(FlareSolverr.test_flaresolverr("http://fs:8191"))
