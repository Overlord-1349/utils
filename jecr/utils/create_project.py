from pathlib import Path
from typing import List

from jecr.utils._Resource import Resource
from jecr.utils._Project import Project


def create_python_project(target_dir: str | Path, name: str, version: str):
    resources: List[Resource] = [
        Resource(
            "readme",
            "update",
            "README.md",
            parameters={"name": name, "version": version},
        ),
        Resource("gitignore", "copy", ".gitignore"),
        Resource("pyproject", "copy", "pyproject.toml"),
        Resource("license", "copy", "LICENSE"),
        Resource("src_folder", "mkdir", "src"),
        Resource("pkg_folder", "mkdir", "src/pkg"),
        Resource("init_pkg", "new", "src/pkg/__init__.py"),
        Resource("test_folder", "mkdir", "tests"),
        Resource("init_test", "new", "__init__.py"),
    ]
    project = Project(Path(target_dir) / name, resources)
    project.create()
    return project
