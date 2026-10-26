"""Regression checks for public asset boundaries; uses only Python's standard library."""
from pathlib import Path
import json
from copy import deepcopy
import shutil
from tempfile import TemporaryDirectory
import unittest

from validate_pages import DOCS, ORIGINAL_DEMO, VIEWER_DATA, validate_implementation_references, validate_public_assets


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

    def check_display_data(self, transform):
        data = deepcopy(json.loads((DOCS / VIEWER_DATA).read_text()))
        transform(data)
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for layer in data["layers"]:
                for candidate in layer["candidates"]:
                    for item in (candidate, *candidate["samples"]):
                        path = root / "assets/demo/public" / item["image"]
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(b"presentation-image-fixture")
            path = root / VIEWER_DATA
            path.write_text(json.dumps(data))
            errors = []
            validate_public_assets(root, errors)
            return errors

    def test_reviewed_display_only_results_are_allowed(self):
        self.assertFalse(self.check_display_data(lambda _: None))

    def test_extra_engine_metadata_is_rejected_at_each_level(self):
        for locate in (lambda d: d, lambda d: d["conditions"], lambda d: d["layers"][0],
                       lambda d: d["layers"][0]["candidates"][0],
                       lambda d: d["layers"][0]["candidates"][0]["samples"][0]):
            with self.subTest(locate=locate):
                self.assertTrue(self.check_display_data(lambda d: locate(d).update(internal_parameters={})))

    def test_missing_measurements_cannot_be_replaced_with_zero(self):
        def change(data):
            sample = data["layers"][0]["candidates"][0]["samples"][0]
            sample.update(cd_nm=0, status="measured")
        self.assertTrue(self.check_display_data(change))

    def original_fixture(self, change):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(DOCS / ORIGINAL_DEMO, root / ORIGINAL_DEMO)
            for filename in ("demo_legacy.html", "demo_legacy_ko.html"):
                shutil.copyfile(DOCS / filename, root / filename)
            change(root / ORIGINAL_DEMO)
            errors = []
            validate_public_assets(root, errors)
            return errors

    def test_original_demo_is_a_fixed_historical_exception(self):
        self.assertFalse(self.original_fixture(lambda _: None))

    def test_new_raw_files_cannot_hide_in_the_original_snapshot(self):
        self.assertTrue(self.original_fixture(lambda p: (p / "new-records.csv").write_text("new data")))

    def test_modified_original_iframe_is_rejected(self):
        self.assertTrue(self.original_fixture(lambda p: (p / "assets/demo/ui-guide/reference-draft.html").write_text("changed")))


if __name__ == "__main__":
    unittest.main()
