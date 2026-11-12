"""
Test Suite 16: Menu-Driven Portal Navigation
Verifies that the portal at http(s)://localhost:11991/ is fully menu-driven:
- Project Overview is the landing page
- Every menu has an Overview page and every sub-menu has an Overview page
- Every page rendered by index.html is registered in the NAV menu registry (no orphan pages)
- Supporting endpoints (prototypes, source explorer, test certificate) work and are sandboxed
"""
import os
import re
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi.testclient import TestClient
from frontend.server import app

STATIC_DIR = os.path.join(PROJECT_ROOT, "frontend", "static")


def _read(name):
    with open(os.path.join(STATIC_DIR, name), "r") as f:
        return f.read()


class TestMenuDrivenNavigation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.index_html = _read("index.html")
        cls.nav_js = _read("navigation.js")
        # Keys registered in the NAV registry
        cls.menu_ids = re.findall(r"id: '(menu-[a-z0-9-]+)', title:", cls.nav_js)
        cls.child_keys = set(re.findall(r"key: '([a-z0-9-]+)', kind:", cls.nav_js))

    def test_root_serves_portal_with_navigation_router(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn('/static/navigation.js', resp.text)
        self.assertIn('id="sidebar-nav"', resp.text)
        self.assertEqual(self.client.get("/static/navigation.js").status_code, 200)

    def test_landing_page_is_project_overview(self):
        self.assertIn("loadView('project-overview')", self.index_html)
        self.assertIn("if (viewKey === 'project-overview')", self.index_html)
        self.assertIn("INDEX = { 'project-overview'", self.nav_js)

    def test_every_menu_has_overview_and_sub_menus(self):
        self.assertGreaterEqual(len(self.menu_ids), 7)
        self.assertEqual(len(self.menu_ids), len(set(self.menu_ids)))
        # Menu overview pages are generated for every menu, each sub-menu gets an overview panel
        self.assertIn("function renderMenuOverview", self.nav_js)
        self.assertIn("function subMenuOverviewPanel", self.nav_js)
        self.assertIn("INDEX[menu.id + '-page']", self.nav_js)

    def test_every_rendered_page_is_reachable_from_a_menu(self):
        """No orphan pages: each viewKey branch in index.html must be a NAV sub-menu."""
        rendered = set(re.findall(r"viewKey === '([a-z0-9-]+)'", self.index_html))
        legacy_menu_pages = {m + "-page" for m in self.menu_ids}
        orphans = rendered - self.child_keys - legacy_menu_pages - {"project-overview"}
        self.assertEqual(orphans, set(), f"Pages not reachable from any menu: {orphans}")

    def test_all_labs_modules_registered_as_sub_menus(self):
        import json
        with open(os.path.join(STATIC_DIR, "labs_200_curriculum.json")) as f:
            modules = json.load(f)
        for mod in modules:
            self.assertIn(f"['{mod['module_id']}',", self.nav_js, f"Missing sub-menu for {mod['module_id']}")

    def test_every_download_document_has_a_sub_menu_overview(self):
        from frontend.server import DOC_MAP
        for doc_key in DOC_MAP:
            self.assertIn(f"['{doc_key}',", self.nav_js, f"Missing overview sub-menu for doc '{doc_key}'")

    def test_custom_views_are_implemented(self):
        for key in self.child_keys:
            if f"key: '{key}', kind: 'custom'" in self.nav_js:
                self.assertIn(f"'{key}': ", self.nav_js, f"Custom view '{key}' has no renderer")

    def test_portal_javascript_has_no_syntax_errors(self):
        """A single stray backtick inside a template literal blanks every page; guard against it."""
        import shutil
        import subprocess
        import tempfile
        node = shutil.which("node")
        if not node:
            self.skipTest("node not installed")
        scripts = re.findall(r"<script>(.*?)</script>", self.index_html, re.S)
        sources = {"index.html inline script": max(scripts, key=len), "navigation.js": self.nav_js}
        for name, src in sources.items():
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tmp:
                tmp.write(src)
            res = subprocess.run([node, "--check", tmp.name], capture_output=True, text=True)
            os.unlink(tmp.name)
            self.assertEqual(res.returncode, 0, f"{name} has a JS syntax error:\n{res.stderr[:800]}")

    def test_prototypes_endpoint(self):
        resp = self.client.get("/api/v1/prototypes")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total"], 20)
        self.assertTrue(all(p["files"] for p in data["prototypes"]))

    def test_source_tree_and_file_endpoints(self):
        resp = self.client.get("/api/v1/source/tree", params={"root": "migration_sessions"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["total"], 8)
        first = resp.json()["files"][0]["path"]
        resp = self.client.get("/api/v1/source/file", params={"path": first})
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.json()["content"]), 0)

    def test_source_viewer_is_sandboxed(self):
        for bad in ["../../etc/passwd", ".env", "frontend/server.py", "customer_prototypes_20/../.env"]:
            resp = self.client.get("/api/v1/source/file", params={"path": bad})
            self.assertEqual(resp.status_code, 403, f"Path should be blocked: {bad}")
        resp = self.client.get("/api/v1/source/tree", params={"root": ".."})
        self.assertEqual(resp.status_code, 403)

    def test_test_certificate_endpoint(self):
        resp = self.client.get("/api/v1/test-certificate")
        self.assertIn(resp.status_code, (200, 404))
        if resp.status_code == 200:
            self.assertIn("tests_run", resp.json())


if __name__ == "__main__":
    unittest.main()
