import streamlit as st

from utils import validate, yaml, hide_streamlit_header

st.set_page_config(page_title="New Atomic")
hide_streamlit_header(st)


def add_executor():
    return {
        "name": st.selectbox("Executor", ["bash", "sh", "command_prompt", "manual", "powershell"]),
        "command": st.text_area("Command", placeholder="cat /dev/null > ~/.bash_history"),
        "elevation_required": st.toggle("Elevation Required ?"),
        "cleanup_command": st.text_area("Cleanup Command"),
    }


def add_input_args():
    input_args = {}

    with st.container():
        with st.expander("Input Arguments"):
            input_args_slider = st.slider(
                "Number of input args", min_value=0, max_value=10, key="input_args"
            )

            for row in range(input_args_slider):
                with st.container():
                    var_name = st.text_input("Variable Name", key=f"input_arg_name{row}")
                    if var_name:
                        input_args[var_name] = {}
                        input_args[var_name]["description"] = st.text_input(
                            "Description", key=f"input_arg_desc{row}"
                        )

                        _type = st.selectbox(
                            "Type",
                            ["integer", "float", "path", "url", "string"],
                            key=f"input_arg_type{row}",
                        )
                        if _type in ["path", "url", "string"]:
                            input_args[var_name]["default"] = st.text_input(
                                "Default", key=f"input_arg_val{row}"
                            )
                        elif _type == "float":
                            input_args[var_name]["default"] = st.number_input(
                                "Default", key=f"input_arg_val{row}"
                            )
                        elif _type == "integer":
                            input_args[var_name]["default"] = st.number_input(
                                "Default", step=1, key=f"input_arg_val{row}"
                            )
                        input_args[var_name]["type"] = _type
                    st.divider()
    return input_args


def add_dependencies():
    dependencies = []
    with st.container():
        with st.expander("Dependencies"):
            st.selectbox(
                label="Dependency Executor",
                options=["bash", "sh", "command_prompt", "manual", "powershell"],
                key="dependency_executor_name",
            )

            deps = st.slider("Number of dependencies", min_value=0, max_value=10, key="deps")
            for r in range(deps):
                x = {}
                with st.container():
                    x["description"] = st.text_area("Description", key=f"deps_desc{r}")
                    x["prereq_command"] = st.text_area("PreReq", key=f"deps_prereq{r}")
                    x["get_prereq_command"] = st.text_area("Get PreReq", key=f"deps_getprereq{r}")
                    st.divider()
                dependencies.append(x)
    return dependencies


def render_technique():
    atomic = {}
    atomic["name"] = st.text_input("Name", placeholder="Clear bash history")
    atomic["description"] = st.text_area(
        "Description", placeholder="This atomic clears bash history via cat /dev/null"
    )
    atomic["supported_platforms"] = st.multiselect(
        "Supported Platforms",
        [
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
        ],
        [],
    )

    st.divider()
    atomic["executor"] = add_executor()
    atomic["input_arguments"] = add_input_args()
    atomic["dependencies"] = add_dependencies()

    serialized_atomic, errors = validate(atomic)
    if len(errors) == 0:
        st.sidebar.success("This atomic is valid", icon="✅")
        atomic = serialized_atomic
    else:
        for e in errors:
            st.sidebar.error(e, icon="🚨")
    return {
        "attack_technique": "T1000.000",
        "display_name": "New Technique",
        "atomic_tests": [atomic],
    }


st.header("New Atomic")

st.markdown(
    """
   <style>
   [data-testid="stSidebar"][aria-expanded="true"]{
       min-width: 450px;
       max-width: 450px;
   }
   """,
    unsafe_allow_html=True,
)

st.sidebar.code(
    yaml.dump(render_technique(), default_flow_style=False, sort_keys=False),
    language="yaml",
)
