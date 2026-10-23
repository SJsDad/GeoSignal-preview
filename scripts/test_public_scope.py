"""Regression checks for public asset boundaries; uses only Python's standard library."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from validate_pages import validate_implementation_references, validate_public_assets


class PublicScopeTests(unittest.TestCase):
    def check_asset(self, relative):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_text("test fixture")
            errors = []
            validate_public_assets(root, errors)
            return errors

    def test_unlinked_raw_records_and_layouts_are_rejected(self):
        for suffix in (".csv", ".csv.gz", ".gds", ".oas", ".npz", ".zip"):
            with self.subTest(suffix=suffix):
                self.assertTrue(self.check_asset("assets/hidden/results" + suffix))

    def test_layout_configuration_outside_the_public_policy_is_rejected(self):
        self.assertTrue(self.check_asset("assets/demo/conditions.json"))

    def test_embedded_demo_data_is_not_kept_as_an_html_workaround(self):
        self.assertTrue(self.check_asset("assets/demo/draft.html"))

    def test_annotated_engineering_figures_are_not_kept_as_an_image_workaround(self):
        self.assertTrue(self.check_asset("assets/release-notes/engineering-chart.png"))

    def test_approved_representative_images_and_educational_assets_are_allowed(self):
        for relative in ("assets/demo/public/overview.png", "assets/demo/public/narrow-line.png",
                         "assets/demo/public/narrow-gap.png", "assets/notes/research/paper.svg",
                         "assets/simulator/manifest.json", "assets/notes/diffraction-defocus/conditions.json"):
            with self.subTest(relative=relative):
                self.assertFalse(self.check_asset(relative))

    def test_private_source_references_and_reproduction_commands_are_rejected(self):
        for text in ("`src/internal_module.py`", "python -m src.internal_study",
                     "python experiments/internal_study.py"):
            with self.subTest(text=text):
                errors = []
                validate_implementation_references({Path("method.md"): text}, errors)
                self.assertTrue(errors)

    def test_standard_theory_external_paper_links_and_website_checks_are_allowed(self):
        errors = []
        validate_implementation_references({Path("note.md"):
            "I = |E|². [Official source](https://example.org/src/paper.py). "
            "python scripts/validate_pages.py"}, errors)
        self.assertFalse(errors)


if __name__ == "__main__":
    unittest.main()
