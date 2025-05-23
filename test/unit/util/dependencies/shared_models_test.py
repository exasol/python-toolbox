import pytest

from exasol.toolbox.util.dependencies.shared_models import Package


class TestPackage:
    @staticmethod
    @pytest.mark.parametrize(
        "name,expected",
        [
            ("numpy", "numpy"),
            ("sphinxcontrib-applehelp", "sphinxcontrib-applehelp"),
            ("Imaginary_package", "imaginary-package"),
            ("Imaginary_package_2", "imaginary-package-2"),
        ],
    )
    def test_normalized_name(name, expected):
        dep = Package(name=name, version="0.1.0")
        assert dep.normalized_name == expected
