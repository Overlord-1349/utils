from pathlib import Path
from shutil import copy
from typing import List
from jecr.utils._Resource import Resource
from jecr.utils._NonEmptyFolderError import NonEmptyFolderError


class Project:
    target_dir: Path
    resources: List[Resource]

    def __init__(
        self, target_dir: str | Path, resources: List[Resource]
    ) -> None:
        self.target_dir = Path(target_dir)
        self.resources = resources
        if self.target_dir.exists():
            raise NonEmptyFolderError(
                f"{self.target_dir} already exists"
            )

        self.target_dir.mkdir(parents=True, exist_ok=True)

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

    def _copy(self, resource: Resource) -> None:
        copy(
            self._resources_dir / resource.filename,
            self.target_dir / resource.filename,
        )

    def _new(self, resource: Resource) -> None:
        target_filename = self.target_dir / resource.filename
        target_filename.parent.mkdir(parents=True, exist_ok=True)
        with target_filename.open("w", encoding="utf-8") as _:
            pass

    def _mkdir(self, resource: Resource) -> None:
        (self.target_dir / resource.filename).mkdir(
            parents=True, exist_ok=True
        )

    def _update(self, resource: Resource) -> None:
        file_content = self._get_resource_content(resource)
        if resource.parameters:
            for key, value in resource.parameters.items():
                file_content = self._replace(
                    file_content,
                    f"{{{{{key}}}}}",
                    value,
                )
        target_file: Path = self.target_dir / resource.filename
        with target_file.open("w", encoding="utf-8") as fh:
            fh.write(file_content)

    def create(self):
        mapping = {
            "update": self._update,
            "copy": self._copy,
            "new": self._new,
            "mkdir": self._mkdir,
        }
        for resource in self.resources:
            mapping[resource.action](resource)
