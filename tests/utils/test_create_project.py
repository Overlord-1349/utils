from pathlib import Path

import pytest

from jecr.utils.create_project import PythonProject


@pytest.fixture(scope="class")
def python_project_instance(
    tmp_path_factory: pytest.TempPathFactory,
) -> PythonProject:
    tmp_path = tmp_path_factory.mktemp(__name__)
    print("TMP PATH", tmp_path)
    python_project = PythonProject("test", tmp_path)
    python_project.create()
    return python_project


class TestPythonProject:
    def test_create(self, python_project_instance: PythonProject):
        assert python_project_instance.target_dir.exists()

    def test_check_update_file_content(
        self, python_project_instance: PythonProject
    ):
        readme_file: Path = python_project_instance.target_dir / "README.md"
        with readme_file.open("r") as fh:
            content = fh.read()

        assert content.find("# test 0.1") >= 0

    def test_copy_file(self, python_project_instance: PythonProject):
        assert (python_project_instance.target_dir / ".gitignore").is_file()
