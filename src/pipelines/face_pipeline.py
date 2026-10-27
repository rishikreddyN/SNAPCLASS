import streamlit as st

import dlib 
import numpy as np
import face_recognition_models

from sklearn.svm import SVC

from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    detecter=dlib.get_frontal_face_detector()


    sp= dlib.shape_predictor(
        face_recognition_models.pose_predictor_five_point_model_location()
    )

    facerec=dlib.face_recognition_model_v1(

        face_recognition_models.face_recognition_model_location()
    )
    return detecter,sp,facerec 

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 0)

    if len(faces) == 0:
        return []

    encodings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        encodings.append(np.array(face_descriptor))

    return encodings
@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding, dtype=np.float64))
            y.append(student.get('student_id'))

    if len(X) == 0:
        return None

    clf = None
    if len(set(y)) >= 2:
        try:
            clf = SVC(kernel='linear', class_weight='balanced')
            clf.fit(X, y)
        except Exception:
            clf = None

    return {'clf': clf, 'X': X, 'y': y}

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()

    return bool(model_data)

def predict_attendance(class_image_np, threshold=0.45):
    encodings = get_face_embeddings(class_image_np)

    detected_student = {}

    model_data = get_trained_model()

    if not model_data or not model_data.get('X') or len(model_data['X']) == 0:
        return detected_student, [], len(encodings)
    
    x_train = np.array(model_data['X'])
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        encoding = np.array(encoding, dtype=np.float64)

        # Compute Euclidean distance to all enrolled embeddings in database
        distances = np.linalg.norm(x_train - encoding, axis=1)
        best_idx = int(np.argmin(distances))
        best_match_score = float(distances[best_idx])
        predicted_id = int(y_train[best_idx])

        # A threshold of 0.45 cleanly separates same person (<0.40) from wrong/different persons (>0.50)
        if best_match_score <= threshold:
            detected_student[predicted_id] = True 

    return detected_student, all_students, len(encodings)