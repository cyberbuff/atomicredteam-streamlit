from typing import List, Optional

import yaml
from pydantic import ValidationError

from models import Atomic


class literal(str):
    pass


def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:
        return multiline_presenter(dumper, data)
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def multiline_presenter(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(str, str_presenter)
yaml.add_representer(literal, multiline_presenter)


def format_values(atomic):
    # TODO: Write a custom YAML Dumper and move all of these to Pydantic Models
    atomic["description"] = literal(atomic["description"])
    atomic["executor"]["command"] = literal(atomic["executor"]["command"])

    if atomic["executor"].get("cleanup_command"):
        atomic["executor"]["cleanup_command"] = literal(atomic["executor"]["cleanup_command"])
    else:
        atomic["executor"].pop("cleanup_command", None)

    if not atomic.get("dependencies", []):
        atomic.pop("dependencies", None)
    else:
        for i in atomic["dependencies"]:
            if i.get("get_prereq_command"):
                i["get_prereq_command"] = literal(i["get_prereq_command"])
            else:
                i.pop("get_prereq_command", None)
            i["prereq_command"] = literal(i["prereq_command"])

    return atomic


def validate(atomic) -> (Optional[Atomic], List[str]):
    def join_loc(x):
        return ".".join([str(i) for i in x])

    try:
        at = Atomic(**atomic).model_dump(
            exclude_defaults=True, exclude_none=True, exclude_unset=True
        )
        return format_values(at), []
    except ValidationError as e:
        errors = []
        for i in e.errors():
            if i["loc"]:
                loc = join_loc(i["loc"])
            else:
                loc = join_loc(i["ctx"]["loc"])
            errors.append(f"Error in '{loc}': {i['msg']}")
        return None, errors


def hide_streamlit_header(st):
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    </style>

    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
