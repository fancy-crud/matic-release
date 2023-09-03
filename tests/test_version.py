import pytest
from matic_release.axioma.exceptions import UnprocessableVersionFormat
from matic_release.axioma.version import Version


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ("", "1.0.0-alpha.0"),
        ("invalid version", "1.0.0-alpha.0"),
        ("2.2.0-alpha.3", "2.2.0-alpha.3"),
        ("10.2.0-beta.10", "10.2.0-beta.10"),
        ("5.6.0-rc.3", "5.6.0-rc.3"),
        ("v2.0.1", "2.0.1"),
        ("1.2.3", "1.2.3"),
        ("2.0", "2.0.0"),
        ("2", "2.0.0"),
    ],
)
def test_create_version(input_value: str, expected_value: str) -> None:
    version = Version(input_value)
    assert version.current_tag.value == expected_value
    assert version.future_tag == version.current_tag


@pytest.mark.parametrize(
    "input_value, _",
    [
        ("2.2.0.3-alpha", "2.2.0-alpha.3"),
        ("2.0.0.11-beta", "2.0.0-beta.11"),
        ("2.2.0.3-rc", "2.2.0-rc.3"),
    ],
)
def test_unprocessable_version_format(input_value: str, _: str):
    with pytest.raises(UnprocessableVersionFormat):
        Version(input_value)