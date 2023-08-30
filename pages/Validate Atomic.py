import streamlit as st
import yaml

from utils import validate, hide_streamlit_header

st.set_page_config(page_title="Validate Atomic")

st.title("Validate Atomic")
hide_streamlit_header(st)
uploaded_file = st.file_uploader("Upload YAML here")

if uploaded_file is not None:
    st.toast("File uploaded successfully!")
    contents = uploaded_file.getvalue().decode()
    st.code(contents, language="yaml")

    json_value = yaml.safe_load(contents)
    if isinstance(json_value, dict) and json_value.get("atomic_tests", []):
        st.sidebar.header(f"{json_value['attack_technique']}")

        for index, i in enumerate(json_value["atomic_tests"]):
            st.sidebar.subheader(i["name"] or f"Atomic {index + 1}")
            atomic, errors = validate(atomic=i)
            if len(errors) == 0:
                st.sidebar.success("This atomic is valid", icon="✅")
            else:
                for e in errors:
                    st.sidebar.error(e, icon="🚨")
