from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from shutil import copy
from typing import List, Literal


@dataclass
class Resource:
    name: str
    action: Literal["update", "copy", "mkdir", "new"]
    filename: str


class Project(ABC):
    target_dir: Path
    resources: List[Resource]

    @property
    def _resources_dir(self) -> Path:
        resource_dir = Path(__file__).parent / "resources"
        if not resource_dir.is_dir():
            raise NotADirectoryError(f"{resource_dir} does not exist")
        return resource_dir

    def _get_resource_content(self, resource: Resource) -> str:
        file = self._resources_dir / resource.filename
        if not file.is_file():
            raise FileNotFoundError(
                f"File {file} does not exist or is not a valid file"
            )  # noqa E501
        with file.open("r", encoding="utf-8") as fh:
            content = fh.read()
        return content

    def _replace(self, content: str, match: str, replace: str):
        return content.replace(match, replace)

    def _copy_resource(self, resource: Resource):
        copy(
            self._resources_dir / resource.filename,
            self.target_dir / resource.filename,
        )

    def _create_empty_file(self, resource: Resource):
        target_filename = self.target_dir / resource.filename
        target_filename.parent.mkdir(parents=True, exist_ok=True)
        with target_filename.open("w", encoding="utf-8") as _:
            pass

    def _mkdir(self, resource: Resource):
        (self.target_dir / resource.filename).mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def _update_file_content(self, resource: Resource) -> None:
        pass

    @abstractmethod
    def create(self):
        pass


class PythonProject(Project):
    resources: List[Resource] = [
        Resource("readme", "update", "README.md"),
        Resource("gitignore", "copy", ".gitignore"),
        Resource("pyproject", "copy", "pyproject.toml"),
        Resource("license", "copy", "license"),
        Resource("src_folder", "mkdir", "src"),
        Resource("pkg_folder", "mkdir", "src/pkg"),
        Resource("init_pkg", "new", "src/pkg/__init__.py"),
        Resource("test_folder", "mkdir", "tests"),
        Resource("init_test", "new", "__init__.py"),
    ]

    def __init__(self, name: str, target_dir: str | Path) -> None:
        self.name = name
        self.target_dir = Path(target_dir)

    def _update_file_content(self, resource: Resource):
        file_content = self._get_resource_content(resource)
        if resource.name == "readme":
            file_content = self._replace(file_content, "{{name}}", self.name)
            file_content = self._replace(file_content, "{{version}}", "0.1")
        target_file: Path = self.target_dir / resource.filename
        with target_file.open("w", encoding="utf-8") as fh:
            fh.write(file_content)

    def create(self):
        for resource in self.resources:
            match resource.action:
                case "update":
                    self._update_file_content(resource)
                case "copy":
                    self._copy_resource(resource)
                case "new":
                    self._create_empty_file(resource)
                case "mkdir":
                    self._mkdir(resource)
