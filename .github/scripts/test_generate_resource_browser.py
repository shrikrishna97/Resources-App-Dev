import tempfile
import unittest
from pathlib import Path

from generate_resource_browser import generate


class ResourceBrowserTest(unittest.TestCase):
    def test_lists_generated_files_in_folders_with_safe_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "Course & notes" / "Week 1"
            folder.mkdir(parents=True)
            (folder / "New #1.html").write_text("guide", encoding="utf-8")
            (folder / "diagram.svg").write_text("image", encoding="utf-8")
            (root / "index.html").write_text("home", encoding="utf-8")

            generate(root)

            page = (root / "resource-browser.html").read_text(encoding="utf-8")
            self.assertIn("<summary>Course &amp; notes/</summary>", page)
            self.assertIn("<summary>Week 1/</summary>", page)
            self.assertIn('href="Course%20%26%20notes/Week%201/New%20%231.html"', page)
            self.assertIn('href="Course%20%26%20notes/Week%201/diagram.svg"', page)
            self.assertIn('href="index.html"', page)
            self.assertNotIn('href="resource-browser.html"', page)

    def test_refuses_to_replace_existing_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing = root / "resource-browser.html"
            existing.write_text("existing", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                generate(root)
            self.assertEqual(existing.read_text(encoding="utf-8"), "existing")


if __name__ == "__main__":
    unittest.main()
