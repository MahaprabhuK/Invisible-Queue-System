import streamlit as st

st.set_page_config(
    page_title="Invisible Queue System",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

params = st.query_params
is_viewer = params.get("viewer") == "true"
target_page = params.get("page")

if is_viewer:
    viewer_page = st.Page("views/viewer.py", title="Queue Status")
    pg = st.navigation([viewer_page])
    pg.run()
else:
    pages = {
        "": [
            st.Page("views/home.py", title="Home", default=True, url_path="home"),
        ],
        "Tools": [
            st.Page("views/simulator.py",    title="Simulator \u2014 V1", url_path="simulator"),
            st.Page("views/video_upload.py", title="CV Detection \u2014 V2", url_path="cv_detection"),
        ],
    }
    pg = st.navigation(pages)

    if target_page == "simulator":
        del st.query_params["page"]
        st.switch_page("views/simulator.py")
    elif target_page == "cv_detection":
        del st.query_params["page"]
        st.switch_page("views/video_upload.py")

    pg.run()
