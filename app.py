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
    # header_home()
    style_base_layout()
    style_background_home()
    style_background_home()
    if 'login_state' not in st.session_state:
        st.session_state['login_state'] = None 
    if st.session_state['login_state']=='student':
        student_screen()
    elif st.session_state['login_state']=='teacher':
        teacher_screen()
    else:
        home_screen()
    join_code = st.query_params.get('join-code')

    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()

        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)



if __name__ == "__main__":
    main()