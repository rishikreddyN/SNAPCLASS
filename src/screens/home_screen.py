

import streamlit as st
from pathlib import Path
from src.components.header import header_home
from src.ui.base_layout import style_base_layout,style_background_home
img_folder = Path(__file__).parent.parent / "img"

teacher=img_folder/"demo"/"snap-teacher.png"
student=img_folder/"demo"/"snap-student.png"
def home_screen():
    
    header_home()
    style_background_home()
    style_base_layout()

    

    col1,col2=st.columns(2)

    with col1:
        st.write("I'm a teacher")
        st.image(str(teacher),width=200)
        if st.button('Teacher Portal',key='home_teacher_portal'):
            st.session_state['login_state']='teacher'
            st.rerun()
    with col2:
        st.write("I'm a student")
        st.image(str(student), width=200)


        if st.button('Student Portal', key='home_student_portal'):
            st.session_state['login_state'] = 'student'
            st.rerun()


    
    