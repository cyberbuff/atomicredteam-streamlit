import pytest
from pydantic import ValidationError

from models import Atomic, extract_mustached_keys


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("#{test1} #{test2}", ["test1", "test2"]),
        ("cat #{test1} > ~/.bash_history", ["test1"]),
    ],
)
def test_keys(test_input, expected):
    assert sorted(extract_mustached_keys([test_input])) == expected


@pytest.mark.parametrize(
    "input_type,default",
    [
        ("url", "github.com/redcanaryco/atomic-red-team"),
        ("float", "1.0"),
        ("int", "1"),
        ("string", 1),
        ("path", 1.0),
    ],
)
def test_input_args(input_type, default):
    atomic = {
        "name": "Curl atomic repo",
        "description": "Curl atomic repo",
        "supported_platforms": ["windows"],
        "input_arguments": {
            "random_variable": {
                "description": "Some random variable",
                "type": input_type,
                "default": default,
            }
        },
        "executor": {"name": "bash", "command": "curl #{random_variable}"},
    }
    with pytest.raises(ValidationError):
        Atomic(**atomic)


def test_unused_arg():
    atomic = {
        "name": "Curl atomic repo",
        "description": "Curl atomic repo",
        "supported_platforms": ["windows"],
        "input_arguments": {
            "random_variable": {
                "description": "Some random variable",
                "type": "string",
                "default": "github.com/redcanaryco/atomic-red-team",
            }
        },
        "executor": {"name": "bash", "command": "curl"},
    }
    with pytest.raises(ValidationError) as exc:
        Atomic(**atomic)
    assert "'random_variable' is not used" in str(exc.value)


def test_missing_arg():
    atomic = {
        "name": "Curl atomic repo",
        "description": "Curl atomic repo",
        "supported_platforms": ["windows"],
        "executor": {"name": "bash", "command": "curl #{random_variable}"},
    }

    with pytest.raises(ValidationError) as exc:
        Atomic(**atomic)
    assert "random_variable is not defined" in str(exc.value)
