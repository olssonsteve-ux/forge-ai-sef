"""Build only the stable runtime and copy authoritative bootstrap data into wheels."""

from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py

EXPERIMENTAL = {"adaptive_loop", "fal002", "fal002_io", "fal002_model", "fal002_inventory"}


class StableBuild(build_py):
    def find_package_modules(self, package, package_dir):
        return [
            item
            for item in super().find_package_modules(package, package_dir)
            if item[1] not in EXPERIMENTAL
        ]

    def run(self):
        super().run()
        destination = Path(self.build_lib) / "forge" / "data" / "bootstrap"
        destination.mkdir(parents=True, exist_ok=True)
        guide = Path(__file__).parent / "docs" / "Forge-1.0-guide.md"
        self.copy_file(str(guide), str(destination.parent / "Forge-1.0-guide.md"))
        for name, source in {
            "INTENT.md": Path(__file__).parent / "INTENT.md",
            "Forge-Concept-v1.0.md": Path(__file__).parent / "docs" / "Forge-Concept-v1.0.md",
        }.items():
            self.copy_file(str(source), str(destination.parent / name))
        for source in (Path(__file__).parent / "templates" / "bootstrap").iterdir():
            if source.is_file():
                self.copy_file(str(source), str(destination / source.name))


setup(cmdclass={"build_py": StableBuild})
