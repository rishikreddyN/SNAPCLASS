import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from src.ui.base_layout import style_background_home
from src.ui.base_layout import style_background_dashboard
from src.ui.base_layout import style_base_layout
from src.components.header import header_home
from src.components.dialog_auto_enroll import auto_enroll_dialog


def main():
    st.set_page_config(
        page_title='SnapClass - Making Attendance Fast using AI',
        page_icon="https://i.ibb.co/YYTYGn5qV/logo.png"
    )

    style_base_layout()
    style_background_home()

    # Initialize session state
    if 'login_state' not in st.session_state:
        st.session_state['login_state'] = None

    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False

    if 'user_role' not in st.session_state:
        st.session_state['user_role'] = None

    # Handle QR code join link
    join_code = st.query_params.get('join-code')

    if join_code:
        if st.session_state['login_state'] != 'student':
            st.session_state['login_state'] = 'student'
            st.rerun()

    # Route pages
    if st.session_state['login_state'] == 'student':
        student_screen()
    elif st.session_state['login_state'] == 'teacher':
        teacher_screen()
    else:
        home_screen()

    # Auto-enroll after student logs in
    if (
        join_code
        and st.session_state.get('is_logged_in')
        and st.session_state.get('user_role') == 'student'
    ):
        auto_enroll_dialog(join_code)


if __name__ == "__main__":
    main()