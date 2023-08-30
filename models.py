import re
from functools import reduce
from typing import Dict, List, Literal, Optional, Union

from pydantic import (
    AnyUrl,
    BaseModel,
    Field,
    StrictFloat,
    StrictInt,
    conlist,
    constr,
    field_validator,
    ConfigDict,
    field_serializer,
)
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import FieldValidationInfo
from typing_extensions import Annotated, TypedDict


def extract_mustached_keys(commands: List[Optional[str]]) -> List[str]:
    result = []
    for command in commands:
        if command:
            matches = re.finditer(r"#{(.*?)}", command, re.MULTILINE)
            keys = [list(i.groups()) for i in matches]
            keys = list(reduce(lambda x, y: x + y, keys, []))
            result.extend(keys)
    return list(set(result))


InputArgType = Literal["url", "string", "float", "integer", "path"]
Platform = Literal[
    "windows",
    "macos",
    "linux",
    "office-365",
    "azure-ad",
    "google-workspace",
    "saas",
    "iaas",
    "containers",
    "iaas:gcp",
    "iaas:azure",
    "iaas:aws",
]
ExecutorType = Literal["manual", "powershell", "sh", "bash", "command_prompt"]


class BaseArgument(TypedDict):
    description: str


class UrlArg(BaseArgument):
    default: AnyUrl
    type: Literal["url"]

    @field_serializer("default")
    def serialize_url(self, value):
        return str(value)


class StringArg(BaseArgument):
    default: str
    type: Literal["string", "path"]


class IntArg(BaseArgument):
    default: StrictInt
    type: Literal["integer"]


class FloatArg(BaseArgument):
    default: StrictFloat
    type: Literal["float"]


Argument = Annotated[Union[FloatArg, IntArg, UrlArg, StringArg], Field(discriminator="type")]


class Executor(BaseModel):
    name: ExecutorType
    elevation_required: bool = False


class ManualExecutor(Executor):
    name: Literal["manual"]
    steps: str


class CommandExecutor(Executor):
    name: Literal["powershell", "sh", "bash", "command_prompt"]
    command: constr(min_length=1)
    cleanup_command: Optional[str] = None

    @field_serializer("cleanup_command")
    def serialize_gpc(self, command):
        if command == "":
            return None
        return command


class Dependency(BaseModel):
    description: constr(min_length=1)
    prereq_command: constr(min_length=1)
    get_prereq_command: Optional[str]

    @field_serializer("get_prereq_command")
    def serialize_gpc(self, command):
        if command == "":
            return None
        return command


class Atomic(BaseModel):
    model_config = ConfigDict(validate_default=True)

    name: constr(min_length=1)
    description: constr(min_length=1)
    supported_platforms: conlist(Platform, min_length=1)
    executor: Union[ManualExecutor, CommandExecutor] = Field(..., discriminator="name")
    input_arguments: Optional[Dict[str, Argument]] = {}
    dependencies: Optional[List[Dependency]] = []
    dependency_executor: Optional[ExecutorType] = None

    @classmethod
    def extract_mustached_keys(cls, value: dict) -> List[str]:
        commands = []
        executor = value.get("executor")
        if isinstance(executor, CommandExecutor):
            commands = [executor.command, executor.cleanup_command]
        for d in value.get("dependencies", []):
            commands.extend([d.get_prereq_command, d.prereq_command])
        return extract_mustached_keys(commands)

    @field_validator("input_arguments", mode="before")  # noqa
    @classmethod
    def validate(cls, v, info: FieldValidationInfo):
        atomic = info.data
        keys = cls.extract_mustached_keys(atomic)
        for key, _value in v.items():
            if key not in keys:
                raise PydanticCustomError(
                    "unused_input_argument",
                    f"'{key}' is not used in any of the commands",
                    {"loc": ["input_arguments", key]},
                )
            else:
                keys.remove(key)

        if len(keys) > 0:
            for x in keys:
                raise PydanticCustomError(
                    "missing_input_argument",
                    f"{x} is not defined in input_arguments",
                    {"loc": ["input_arguments"]},
                )
        return v


class Technique(BaseModel):
    attack_technique: str
    display_name: str
    atomic_tests: List[Atomic]
