import streamlit as st
def intro():
    import streamlit as st

    st.write("# Welcome to my portfolio!")
    st.sidebar.success("Select a demo above.")
    # load src/index.md to text
    with open("src/index.md") as f:
        st.markdown(f.read())

page_names_to_funcs = {
    "index": intro,
    # "linkedin post generator app": linkedin_post_app,
    # "linkedin post generator app": linkedin_post_app,
    # "DataFrame Demo": intro
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()