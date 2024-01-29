from pathlib import Path

import pytest
from jecr.utils.create_project import Project, create_python_project


@pytest.fixture(scope="class")
def python_project_instance(
    tmp_path_factory: pytest.TempPathFactory,
) -> Project:
    tmp_path = tmp_path_factory.mktemp(__name__)
    return create_python_project(tmp_path, "test", "0.1")


class TestProject:
    def test_create(self, python_project_instance: Project):
        assert python_project_instance.target_dir.exists()

    def test_update_file_content(self, python_project_instance: Project):
        readme_file: Path = python_project_instance.target_dir / "README.md"
        with readme_file.open("r") as fh:
            content = fh.read()

        assert content.find("# test 0.1") >= 0

    def test_copy_file(self, python_project_instance: Project):
        assert (python_project_instance.target_dir / ".gitignore").is_file()

    def test_new_file(self, python_project_instance: Project):
        assert (
            python_project_instance.target_dir / "src/pkg/__init__.py"
        ).exists()

    def test_mkdir(self, python_project_instance: Project):
        assert (
            python_project_instance.target_dir / "docs"
        ).exists()
        
