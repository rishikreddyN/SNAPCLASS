import streamlit as st
from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)
from src.pipelines.face_pipeline import predict_attendance 
from src.database.config import supabase
from src.components.dialog_create import create_subject_dialog
from src.components.header import header_dashboard
from src.database.db import check_teacher_exists,create_teacher,teacher_login,get_teacher_subjects
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photos import add_photos_dialog
import numpy as np
from datetime import datetime
from src.components.dialog_attendance import add_photos_dialog

def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_state' not in st.session_state or st.session_state.teacher_login_state == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_state == 'register':
        teacher_screen_register()


def teacher_dashboard():

    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']} !""")
        if st.button("Logout", type='secondary', key='teacher_logout_btn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()
    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else 'tertiary'
        if st.button('Take Attendance', width='stretch', icon=':material/ar_on_you:', key='teacher_tab_attendance', type=type1):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else 'tertiary'
        if st.button('Manage Subjects', width='stretch', icon=':material/book_ribbon:', key='teacher_tab_subjects', type=type2):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else 'tertiary'
        if st.button('Attendance Records', width='stretch', icon=':material/cards_stack:', key='teacher_tab_records', type=type3):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning(
            'You havent created any subjects yet! Please create one to begin!'
        )
        return

    subject_options = {
        f"{s['name']} - {s['subject_code']}": s['subject_id']
        for s in subjects
    }

    col1, col2 = st.columns([3, 1])

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))
    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch', key='teacher_add_photos_btn'):
            add_photos_dialog()

    selected_subject_id=subject_options[selected_subject_label]
    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button(
                'Clear all photos',
                width='stretch',
                type='tertiary',
                icon=':material/delete:'
            ):
                st.session_state.attendance_images = []
                st.rerun()

        with c2:
            has_photos = bool(st.session_state.attendance_images)

            if st.button(
                'Run Face Analysis',
                width='stretch',
                type='secondary',
                icon=':material/analytics:'
            ):
                with st.spinner('Deep scanning classroom photos...'):
                    all_detected_id = {}

                    for idx, img in enumerate(st.session_state.attendance_images):
                        img_np = np.array(img.convert('RGB'))
                        detected, _, _ = predict_attendance(img_np)

                        if detected:
                            for sid in detected.keys():
                                student_id = int(sid)

                                all_detected_id.setdefault(student_id, []).append(
                                    f'Photo {idx+1}'
                                )

                    enrolled_res = (
                        supabase.table('subject_students')
                        .select("*, students(*)")
                        .eq('subject_id',selected_subject_id).execute()
                    enrolled_students=enrolled_res.data

                    if not enrolled_students:
                        st.warning("No students enrolled in this course")
                    else:

                        results, attendance_to_log = [], []

                        current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                        for node in enrolled_students:
                            student = node['students']
                            sources = all_detected_ids.get(int(student['student_id']), [])
                            is_present = len(sources) > 0

                            results.append({
                                "Name": student['name'],
                                "ID": student['student_id'],
                                "Source": ", ".join(sources) if is_present else "—",
                                "Status": "✅ Present" if is_present else "❌ Absent"
                            })

                            attendance_to_log.append({
                                'student_id': student['student_id'],
                                'subject_id': selected_subject_id,
                                'timestamp': current_timestamp,
                                'is_present': bool(is_present)
                            })

                        attendance_result_dialog(
                            pd.DataFrame(results),
                            attendance_to_log
                        )
        with c3:
        if st.button('Use voice Assistant',type='primary',width='stretch',icon=':material/mic:')



def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns(2)

    with col1:
        st.header('Manage Subjects', width='stretch')

    with col2:
        if st.button('Create New Subject', width='stretch', key='teacher_create_subject_btn'):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub['total_students']),
                ("📦", "Classes", sub['total_classes']),
            ]

            def share_btn():
                if st.button(
                    f"Share Code: {sub['name']}",
                    key=f"share_{sub['subject_code']}",
                    icon=":material/share:"
                ):
                    share_subject_dialog(
                        sub['name'],
                        sub['subject_code']
                    )

                st.space()

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )

    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    st.header('Take AI attendance')


def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True


def teacher_screen_login():
    c1, c2 = st.columns(
        [2, 1],
        vertical_alignment="center"
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            key="teacher_login_back_btn"
        ):
            st.session_state["login_state"] = None
            st.rerun()

    st.header(
        "Login using password",
        divider=None
    )

    left, center, right = st.columns([1, 2, 1])

    with center:

        teacher_username = st.text_input(
            "Enter username",
            placeholder="Ex: Rishik Reddy Nalla"
        )

        teacher_pass = st.text_input(
            "Enter password",
            type="password",
            placeholder="Enter password"
        )

        st.divider()

        btn1, btn2 = st.columns(2)

        with btn1:
            if st.button(
                "Login",
                icon=":material/passkey:",
                use_container_width=True,
                key='teacher_login_btn'
            ):
                if login_teacher(teacher_username, teacher_pass):
                    st.toast("Welcome back!", icon="👋")
                    import time
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        with btn2:
            if st.button(
                "First time user",
                type="primary",
                icon=":material/passkey:",
                use_container_width=True,
                key='teacher_first_time_btn'
            ):
                st.session_state.teacher_login_state = "register"
                st.rerun()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username Already exists!"
    if teacher_pass != teacher_pass_confirm:
        return False, "password is not matching"
    try:
        create_teacher(teacher_username, teacher_name, teacher_pass)
        return True, "Registration successful!"
    except Exception as e:
        return False, str(e)


def teacher_screen_register():

    st.title("register")
    c1, c2 = st.columns(
        [2, 1],
        vertical_alignment="center"
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            key="teacher_register_back_btn"
        ):
            st.session_state["login_state"] = None
            st.rerun()

    st.header("Register your teacher profile")

    teacher_username = st.text_input(
        "Enter username",
        key="register_username"
    )
    teacher_name = st.text_input(
        "Enter your full name",
        key="register_name"
    )

    teacher_pass = st.text_input(
        "Enter password",
        type="password",
        key="register_password"
    )
    teacher_pass_confirm = st.text_input(
        "confirm password",
        type="password",
        key="register_confirm_password"
    )

    btn1, btn2 = st.columns(2)

    with btn1:
        if st.button(
            "Login instead",
            icon=":material/passkey:",
            use_container_width=True,
            key='teacher_register_login_instead_btn'
        ):
            st.session_state.teacher_login_state = "login"
            st.rerun()

    with btn2:
        if st.button(
            "Register now",
            type="primary",
            icon=":material/passkey:",
            use_container_width=True,
            key='teacher_register_now_btn'
        ):
            success, msg = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success("Registration successful! 🎉")
                import time
                time.sleep(2)
                st.session_state.teacher_login_state = "login"
                st.rerun()
            else:
                st.error(msg)