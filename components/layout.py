import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.0rem;
            padding-bottom: 2rem;
            animation: fadein 220ms ease-in-out;
        }

        @keyframes fadein {
            from { opacity: 0; transform: translateY(6px); }
            to   { opacity: 1; transform: translateY(0px); }
        }

        [data-testid="stAppViewContainer"] {
            background: rgb(255, 255, 255);
        }

        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stToolbar"] { visibility: hidden; height: 0px; }
        footer { visibility: hidden; height: 0px; }

        .weld-card {
            background: rgba(232, 245, 255, 0.95);
            border: 1px solid rgba(10, 80, 170, 0.14);
            border-radius: 16px;
            padding: 16px 18px;
            box-shadow: 0 10px 24px rgba(10, 80, 170, 0.08);
        }

        .weld-subtle { color: rgba(12, 26, 52, 0.72); font-size: 0.96rem; }
        .weld-title  { font-size: 2.05rem; font-weight: 850; margin-bottom: 4px; color: rgba(12, 26, 52, 0.95); }

        .weld-accent {
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(0, 102, 204, 0.14);
            color: rgba(0, 75, 160, 0.98);
            font-weight: 700;
            font-size: 0.9rem;
            margin-top: 6px;
        }

        div[data-testid="stButton"] button {
            border-radius: 999px;
            padding: 0.58rem 0.95rem;
            border: 1px solid rgba(10, 80, 170, 0.20);
            transition: transform 120ms ease, box-shadow 120ms ease;
        }

        div[data-testid="stButton"] button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 18px rgba(10, 80, 170, 0.12);
        }

        div[data-testid="stButton"] button[kind="primary"] {
            background: linear-gradient(180deg, rgba(0, 102, 204, 1) 0%, rgba(0, 86, 179, 1) 100%);
            border: 1px solid rgba(0, 86, 179, 0.9);
            color: white;
        }

        .step-arrow {
            text-align: center;
            font-size: 22px;
            font-weight: 900;
            color: rgba(0, 86, 179, 0.55);
            padding-top: 8px;
        }

        div[data-testid="stVerticalBlock"]:has(#nav_stepper_marker) {
            background: rgba(232, 245, 255, 0.95);
            border: 1px solid rgba(10, 80, 170, 0.14);
            border-radius: 18px;
            padding: 10px 12px;
            box-shadow: 0 10px 24px rgba(10, 80, 170, 0.06);
            margin-bottom: 14px;
        }

        [data-testid="stFileUploader"] button { display: none; }

        [data-testid="stFileUploader"] {
            background: rgba(232, 245, 255, 0.55);
            border: 1px solid rgba(10, 80, 170, 0.14);
            border-radius: 16px;
            padding: 12px 12px 6px 12px;
            box-shadow: 0 10px 24px rgba(10, 80, 170, 0.06);
        }

        [data-testid="stFileUploader"] section { border-radius: 14px; }
        [data-testid="stFileUploader"] small { color: rgba(12, 26, 52, 0.65); }

        /* Make Streamlit tabs large and visible (2D / 3D) */
        div[data-testid="stTabs"] button {
            font-size: 1.05rem;
            font-weight: 800;
            padding: 12px 18px;
            border-radius: 999px;
            border: 1px solid rgba(10, 80, 170, 0.18);
            margin-right: 10px;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            background: linear-gradient(180deg, rgba(0, 102, 204, 1) 0%, rgba(0, 86, 179, 1) 100%);
            color: white;
            border: 1px solid rgba(0, 86, 179, 0.9);
        }

        div[data-testid="stTabs"] {
            margin-top: 6px;
            margin-bottom: 10px;
        }

        /* 3D weld blocks UI */
        .weld3d-group {
          border-radius: 12px;
          overflow: hidden;
          border: 1px solid rgba(10, 80, 170, 0.18);
          box-shadow: 0 10px 20px rgba(10, 80, 170, 0.06);
          margin-bottom: 14px;
        }

        .weld3d-header {
          background: rgba(0, 150, 220, 0.95);
          color: white;
          font-weight: 900;
          text-align: center;
          padding: 14px 12px;
          font-size: 1.1rem;
        }

        .weld3d-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 10px;
          padding: 8px 10px;
          background: white;
        }

        .weld3d-chip {
          flex: 1;
          border-radius: 6px;
          border: 2px solid rgba(10, 80, 170, 0.25);
          padding: 10px 12px;
          font-size: 1.05rem;
          font-weight: 700;
          text-align: center;
          background: white;
        }

        .weld3d-chip.bad {
          background: rgba(255, 52, 97, 0.95);
          color: black;
          border: 2px solid rgba(255, 52, 97, 0.95);
        }

        .weld3d-check {
          width: 38px;
          height: 38px;
          border-radius: 999px;
          background: rgba(63, 167, 70, 0.95);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-size: 22px;
          font-weight: 900;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def top_progress(step: int, total_steps: int):
    st.write(f"Step {step} of {total_steps}")
    if total_steps > 1:
        st.progress((step - 1) / (total_steps - 1))


def step_nav(labels):
    current = int(st.session_state.get("step", 1))
    n = len(labels)

    with st.container():
        st.markdown('<div id="nav_stepper_marker"></div>', unsafe_allow_html=True)

        widths = []
        for idx in range(n):
            widths.append(1.6)
            if idx < n - 1:
                widths.append(0.25)

        cols = st.columns(widths, vertical_alignment="center")

        col_i = 0
        for i, label in enumerate(labels, start=1):
            with cols[col_i]:
                is_active = (i == current)
                btn_type = "primary" if is_active else "secondary"

                if st.button(
                    f"{label}",
                    disabled=is_active,
                    type=btn_type,
                    use_container_width=True,
                    key=f"nav_{i}"
                ):
                    st.session_state.step = i
                    st.rerun()

            col_i += 1

            if i < n:
                with cols[col_i]:
                    st.markdown('<div class="step-arrow">›</div>', unsafe_allow_html=True)
                col_i += 1


def nav_buttons(can_next: bool, on_back, on_next):
    c1, c2, c3 = st.columns([1, 1, 6])

    with c1:
        disabled_back = bool(st.session_state.get("step", 1) == 1)
        if st.button("Back", disabled=disabled_back, type="secondary"):
            on_back()
            st.rerun()

    with c2:
        if st.button("Next", disabled=(not can_next), type="primary"):
            on_next()
            st.rerun()

    with c3:
        st.write("")