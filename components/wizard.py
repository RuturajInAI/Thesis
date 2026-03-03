import streamlit as st
from components.layout import apply_styles, top_progress, nav_buttons, step_nav
from services.file_utils import (
    detect_mode_from_filename,
    get_uploaded_bytes_and_name,
    load_image_from_bytes,
    load_mock_3d_image
)
from services.mock_analysis import mock_analyze_joints
from components.visualize import draw_2d_welds_overlay, render_3d_welds_plot, pil_to_plotly_figure


VIEW_HEIGHT = 420
TABLE_HEIGHT = 360
PLOTLY_CFG = {"displayModeBar": True, "scrollZoom": True}


def _init_state():
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "uploaded_bytes" not in st.session_state:
        st.session_state.uploaded_bytes = None
    if "uploaded_name" not in st.session_state:
        st.session_state.uploaded_name = None
    if "mode" not in st.session_state:
        st.session_state.mode = "2D"
    if "df" not in st.session_state:
        st.session_state.df = None
    if "analysis_done" not in st.session_state:
        st.session_state.analysis_done = False
    if "corrections_saved" not in st.session_state:
        st.session_state.corrections_saved = False


def _go_next():
    st.session_state.step = min(6, st.session_state.step + 1)


def _go_back():
    st.session_state.step = max(1, st.session_state.step - 1)


def _page_header(title: str, hint: str):
    st.markdown(
        f"""
        <div class="weld-card">
            <div class="weld-title">{title}</div>
            <div class="weld-subtle">{hint}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")


def _render_3d_weld_blocks(df):
    if df is None or df.empty:
        st.info("No 3D weld connections available.")
        return

    required = {"Part_A", "Part_B"}
    if not required.issubset(set(df.columns)):
        st.info("3D data does not contain Part A and Part B.")
        return

    groups = {}
    for _, r in df[["Part_A", "Part_B"]].dropna().iterrows():
        a = str(r["Part_A"]).strip()
        b = str(r["Part_B"]).strip()
        if a == "" or b == "":
            continue
        groups.setdefault(a, set()).add(b)

    if len(groups) == 0:
        st.info("No 3D weld connections available.")
        return

    for part in sorted(groups.keys()):
        weld_list = sorted(list(groups.get(part, [])))

        html = '<div class="weld3d-group">'
        html += f'<div class="weld3d-header">{part}</div>'

        for idx, other in enumerate(weld_list):
            is_bad = (idx == 1)
            chip_class = "weld3d-chip bad" if is_bad else "weld3d-chip"
            html += '<div class="weld3d-row">'
            html += f'<div class="{chip_class}">Weld with {other}</div>'
            html += '<div class="weld3d-check">✓</div>'
            html += "</div>"

        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)


def _screen_upload():
    _page_header(
        "Upload drawing",
        "Drag and drop the mock drawing file here. Next step shows 2D and 3D preview."
    )

    up = st.file_uploader("", type=["png", "jpg", "jpeg", "pdf"])

    if up is not None:
        data, name = get_uploaded_bytes_and_name(up)
        st.session_state.uploaded_bytes = data
        st.session_state.uploaded_name = name
        st.session_state.mode = detect_mode_from_filename(name)

        st.session_state.df = None
        st.session_state.analysis_done = False
        st.session_state.corrections_saved = False

        st.markdown('<div class="weld-accent">File received successfully</div>', unsafe_allow_html=True)
        st.write(f"File name: {name}")

    nav_buttons(
        can_next=(st.session_state.uploaded_bytes is not None),
        on_back=_go_back,
        on_next=_go_next
    )


def _screen_workflow_preview():
    _page_header(
        "Workflow preview",
        "Use zoom in and zoom out from the toolbar or mouse wheel. Left is 2D. Right is mock 3D."
    )

    if st.session_state.uploaded_bytes is None or st.session_state.uploaded_name is None:
        st.warning("No file uploaded yet. Go back and upload the drawing.")
        nav_buttons(False, _go_back, _go_next)
        return

    img_2d = load_image_from_bytes(st.session_state.uploaded_bytes, st.session_state.uploaded_name)
    img_3d = load_mock_3d_image()

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="weld-accent">2D preview</div>', unsafe_allow_html=True)
        fig2d = pil_to_plotly_figure(img_2d, height=VIEW_HEIGHT)
        st.plotly_chart(fig2d, use_container_width=True, config=PLOTLY_CFG)

    with c2:
        st.markdown('<div class="weld-accent">3D preview (mock)</div>', unsafe_allow_html=True)
        fig3d = pil_to_plotly_figure(img_3d, height=VIEW_HEIGHT)
        st.plotly_chart(fig3d, use_container_width=True, config=PLOTLY_CFG)

    nav_buttons(True, _go_back, _go_next)


def _analysis_table_2d(df):
    cols = ["Preview", "Part_Index", "Weld_Type_2D", "Weld_Side", "Weld_Size", "Weld_Length"]
    existing = [c for c in cols if c in df.columns]
    df_view = df[existing].copy()

    df_view = df_view.rename(
        columns={
            "Preview": "Preview",
            "Part_Index": "Part index",
            "Weld_Type_2D": "Weld type",
            "Weld_Side": "Weld side",
            "Weld_Size": "Weld size",
            "Weld_Length": "Weld length",
        }
    )

    st.dataframe(df_view, use_container_width=True, height=TABLE_HEIGHT)


def _analysis_table_3d(df):
    df_view = df[["Weld_Index", "Part_A", "Part_B"]].copy()
    df_view = df_view.rename(
        columns={
            "Weld_Index": "Weld Index",
            "Part_A": "Part A",
            "Part_B": "Part B",
        }
    )
    st.dataframe(df_view, use_container_width=True, height=TABLE_HEIGHT)


def _screen_analysis():
    _page_header(
        "Analyze (mock)",
        "This page has two sections. Use the tabs below."
    )

    if st.session_state.uploaded_name is None:
        st.warning("No file uploaded. Go back.")
        nav_buttons(False, _go_back, _go_next)
        return

    tab2d, tab3d = st.tabs(["2D", "3D"])

    with tab2d:
        st.markdown('<div class="weld-accent">2D analysis</div>', unsafe_allow_html=True)
        st.write("Click Analyze to generate the weld list for 2D.")

        if st.button("Analyze 2D", type="primary", use_container_width=False, key="analyze_2d"):
            st.session_state.df = mock_analyze_joints("2D")
            st.session_state.mode = "2D"
            st.session_state.analysis_done = True
            st.session_state.corrections_saved = False
            st.markdown('<div class="weld-accent">2D analysis completed</div>', unsafe_allow_html=True)

        if st.session_state.analysis_done and st.session_state.df is not None and st.session_state.mode == "2D":
            _analysis_table_2d(st.session_state.df)

    with tab3d:
        st.markdown('<div class="weld-accent">3D analysis</div>', unsafe_allow_html=True)
        st.write("Click Analyze to generate the weld connections list for 3D.")

        if st.button("Analyze 3D", type="primary", use_container_width=False, key="analyze_3d"):
            st.session_state.df = mock_analyze_joints("3D")
            st.session_state.mode = "3D"
            st.session_state.analysis_done = True
            st.session_state.corrections_saved = False
            st.markdown('<div class="weld-accent">3D analysis completed</div>', unsafe_allow_html=True)

        if st.session_state.analysis_done and st.session_state.df is not None and st.session_state.mode == "3D":
            _analysis_table_3d(st.session_state.df)
            st.write("")
            _render_3d_weld_blocks(st.session_state.df)

    nav_buttons(bool(st.session_state.analysis_done), _go_back, _go_next)


def _screen_visualize():
    _page_header(
        "Visualize welds",
        "2D overlay supports zoom."
    )

    df = st.session_state.df
    if df is None:
        st.warning("No results. Go back and run analysis.")
        nav_buttons(False, _go_back, _go_next)
        return

    if st.session_state.uploaded_bytes is None or st.session_state.uploaded_name is None:
        st.warning("No uploaded drawing found. Go back and upload the drawing.")
        nav_buttons(False, _go_back, _go_next)
        return

    base_img = load_image_from_bytes(st.session_state.uploaded_bytes, st.session_state.uploaded_name)
    overlay = draw_2d_welds_overlay(base_img, df)
    fig = pil_to_plotly_figure(overlay, height=VIEW_HEIGHT)
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)

    nav_buttons(True, _go_back, _go_next)



def _screen_correct():
    _page_header(
        "Correct weld list",
        "Edit directly in the table, then click Save changes."
    )

    df = st.session_state.df
    if df is None:
        st.warning("No results. Go back and run analysis.")
        nav_buttons(False, _go_back, _go_next)
        return

    visible_cols = ["Weld_Index", "Part_A", "Part_B", "Weld_Type", "Status"]
    existing_cols = [c for c in visible_cols if c in df.columns]

    editable = st.data_editor(
        df[existing_cols],
        use_container_width=True,
        num_rows="dynamic",
        height=TABLE_HEIGHT,
        key="edit_table_welds"
    )

    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("Save changes", type="primary", use_container_width=True):
            df_new = df.copy()
            for col in existing_cols:
                df_new[col] = editable[col]
            st.session_state.df = df_new
            st.session_state.corrections_saved = True
            st.markdown('<div class="weld-accent">Saved</div>', unsafe_allow_html=True)

    with c2:
        if not st.session_state.corrections_saved:
            st.info("Save changes to continue.")

    nav_buttons(bool(st.session_state.corrections_saved), _go_back, _go_next)


def _screen_export():
    _page_header(
        "Export",
        "Download the corrected weld list."
    )

    df = st.session_state.df
    if df is None:
        st.warning("No data to export.")
        nav_buttons(False, _go_back, _go_next)
        return

    keep_cols = [c for c in ["Weld_Index", "Part_A", "Part_B", "Weld_Type"] if c in df.columns]
    df_out = df[df.get("Status", "OK") != "Delete"][keep_cols].copy()

    st.dataframe(df_out, use_container_width=True, height=TABLE_HEIGHT)

    csv_bytes = df_out.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv_bytes,
        file_name="weld_list.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("Restart", type="secondary", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    nav_buttons(False, _go_back, _go_next)


def run_wizard():
    _init_state()
    apply_styles()

    labels = ["Upload", "Workflow", "Analyze", "Visualize", "Correct", "Export"]
    total_steps = 6

    step_nav(labels)
    top_progress(st.session_state.step, total_steps)
    st.write("")

    if st.session_state.step == 1:
        _screen_upload()
    elif st.session_state.step == 2:
        _screen_workflow_preview()
    elif st.session_state.step == 3:
        _screen_analysis()
    elif st.session_state.step == 4:
        _screen_visualize()
    elif st.session_state.step == 5:
        _screen_correct()
    else:
        _screen_export()