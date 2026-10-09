import json
import os
import sys
import unittest
from unittest import mock

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

import Spaller  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402


class CatalogTest(unittest.TestCase):
    def test_bundled_catalog_is_valid(self):
        with open(os.path.join(Spaller.APP_DIR, "packages.json"), encoding="utf-8") as f:
            Spaller.validate_catalog(json.load(f))

    def test_rejects_bad_entries(self):
        for app in ({"package": "--source=http://evil"}, {"package": "a & calc"}, {"package": 7},
                    {"package": "git", "size": "big"}, "git"):
            with self.assertRaises(ValueError, msg=app):
                Spaller.validate_catalog({"Cat": {"App": app}})

    def test_choco_install_rejects_option_injection(self):
        with self.assertRaises(ValueError):
            Spaller.choco_install("choco", "-y --source=http://evil")


class WindowTest(unittest.TestCase):
    def test_select_search_and_install_button(self):
        app = QApplication.instance() or QApplication([])
        with mock.patch.object(Spaller, "find_choco", return_value="choco"):
            window = Spaller.SpallerMainWindow()
            window.loader.wait()
            app.processEvents()  # deliver the catalog and run the Chocolatey check

        self.assertTrue(window.apps)
        self.assertEqual(window.choco, "choco")
        self.assertFalse(window.install_btn.isEnabled())

        first = next(iter(window.app_checkboxes))
        window.app_checkboxes[first].setChecked(True)
        self.assertEqual(window.selected, {first})
        self.assertTrue(window.install_btn.isEnabled())

        window.search_bar.setText("git")
        self.assertIn("Development:Git", window.app_checkboxes)
        self.assertTrue(window.app_checkboxes["Development:Git"].isEnabled())
        window.toggle_select_visible()
        self.assertTrue(window.selected.issuperset(window.app_checkboxes))

        window.switch_category("Browsers")
        self.assertEqual(window.search_bar.text(), "")
        window.toggle_select_all()
        self.assertEqual(len(window.selected), len(window.apps))
        window.toggle_select_all()
        self.assertFalse(window.selected)

        with mock.patch.object(Spaller, "choco_install", return_value=0), \
                mock.patch.object(Spaller.QMessageBox, "information") as summary:
            window.set_selected(["Development:Git"], True)
            window.start_installation()
            window.installer.wait()
            app.processEvents()  # deliver `finished`
        summary.assert_called_once()
        self.assertFalse(window.installing)
        self.assertFalse(window.selected)  # installed apps get deselected


class InstallationThreadTest(unittest.TestCase):
    def test_exit_codes(self):
        codes = {"ok": 0, "reboot": 3010, "bad": 1603}
        apps = [("a", "A", "ok"), ("b", "B", "reboot"), ("c", "C", "bad")]
        with mock.patch.object(Spaller, "choco_install", side_effect=lambda choco, package: codes[package]):
            thread = Spaller.InstallationThread("choco", apps)
            thread.run()
        self.assertEqual(thread.installed, ["a", "b"])
        self.assertTrue(thread.reboot_required)
        self.assertEqual(thread.failed, ["C (exit code 1603)"])


if __name__ == "__main__":
    unittest.main()
