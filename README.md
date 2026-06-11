# SnapClass 🎓📸

SnapClass is an AI-powered classroom attendance management system that automates attendance tracking using facial recognition and voice verification. The platform allows teachers to create classrooms, enroll students, capture classroom photos, and automatically mark attendance using machine learning models.

---

## 🚀 Features

### 👨‍🏫 Teacher Features
- Teacher Registration & Login
- Create and Manage Subjects
- View Enrolled Students
- Track Attendance Records
- Attendance Analytics Dashboard

### 👨‍🎓 Student Features
- Student Registration & Login
- Join Subjects
- View Attendance Percentage
- Access Subject Information

### 🤖 AI Features
- Face Recognition for Student Identification
- Voice Recognition for Additional Verification
- Automated Attendance Marking
- Classroom Photo Processing
- Real-Time Attendance Reports

---

## 🏗️ System Architecture

```text
Teacher
   │
   ▼
Streamlit Frontend
   │
   ▼
Business Logic Layer
   │
   ▼
Supabase Database
   │
   ▼
AI Processing Pipeline
 ├── Face Recognition
 ├── Voice Recognition
 └── Attendance Engine
```

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Database
- Supabase

### AI / Machine Learning
- OpenCV
- Face Recognition Models
- Speech Recognition Models
- NumPy
- Pandas

### Authentication
- Supabase Authentication

### Deployment
- Streamlit Cloud / VPS

---

## 📂 Project Structure

```text
SNAPCLASS/
│
├── src/
│   ├── components/
│   ├── database/
│   ├── screens/
│   ├── utils/
│   └── models/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/SNAPCLASS.git
cd SNAPCLASS
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

FACE_MODEL_PATH=path_to_face_model
VOICE_MODEL_PATH=path_to_voice_model
```

---

## ▶️ Running the Project

Start the application using:

```bash
streamlit run app.py
```

After successful startup, open:

```text
http://localhost:8501
```

in your browser.

---

## 📊 Future Enhancements

- Real-time classroom monitoring
- Multi-camera attendance support
- Mobile Application
- AI-generated attendance insights
- Student performance analytics
- Cloud deployment
- LLM-powered classroom assistant

---

## 🎯 Use Cases

- Schools
- Colleges
- Coaching Centers
- Training Institutes
- Corporate Training Programs

---

## 👥 Contributors

### Rishik Reddy
Founder & Developer

---

## 📜 License

This project is developed for educational and research purposes.

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub.

```
⭐ Star the repository to support the project.
```
