import streamlit as st
from utils import hide_streamlit_header

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
hide_streamlit_header(st)
st.title("Atomic Red Team")
st.markdown(
    """
#### Welcome

This is a helper web app for the
[Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) project

#### Features

 👈 Checkout the sidebar on the left.

 - New Atomic: Create new atomics via web forms
 - Validate Atomic: Upload your YAML file and validate them

More features coming soon...
"""
)
