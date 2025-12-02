# 🗺️CampXplore: Smart Campus Navigation & Feedback System 🚀

[![GitHub language count](https://img.shields.io/github/languages/count/RishikaYashwini/campXplore)](https://github.com/RishikaYashwini/campXplore)
[![GitHub last commit](https://img.shields.io/github/last-commit/RishikaYashwini/campXplore)](https://github.com/RishikaYashwini/campXplore)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
[![Deployed Status](https://img.shields.io/badge/Deployed-Live_on_Render-brightgreen)](https://campxplore.onrender.com)
[![Version](https://img.shields.io/badge/Version-v0.2-blue)](https://github.com/RishikaYashwini/campXplore/releases/tag/v0.2)

> **CampXplore** is a comprehensive, production-ready system designed to digitize campus management. It features smart navigation using **Dijkstra's shortest path algorithm**, a robust **complaint tracking system**, and a **role-based analytics dashboard**. Built using the modern **PERN stack** (PostgreSQL, Flask, React, Python).

## ✨ Key Features (Version 0.2)

We've built a scalable application focusing on security, performance, and user experience, including full Dark Mode support and responsive design.

| Feature Category | Icon | Description | Status |
| :--- | :--- | :--- | :--- |
| **Smart Navigation** | 🗺️ | Interactive map (Leaflet.js) with precise shortest path calculation between any two buildings. | **✅ Complete** |
| **Complaint Management** | 📩 | Digital submission, status tracking (Open, In Progress, Resolved), and full admin management. | **✅ Complete** |
| **Feedback System** | ⭐ | 5-star rating system and comment submission for campus facilities. | **✅ Complete** |
| **Admin Dashboard** | 📊 | Comprehensive analytics dashboard with charts (Chart.js) showing complaint statistics and feedback trends. | **✅ Complete** |
| **Security & Access** | 🔒 | Role-based access control (Student/Faculty/Admin) and secure password hashing. | **✅ Complete** |
| **Theming** | 🌙 | Perfect Dark Mode support across all pages with a beautiful purple theme. | **✅ Complete** |

---

## ⚡ Live Application Access (Interactive)

Experience the live application deployed on Render. 

| Role | Access Link | Credentials (Try Me) |
| :--- | :--- | :--- |
| **Live Site URL** | [https://campxplore.onrender.com](https://campxplore.onrender.com) | N/A |
| **Admin** | Login Page | **Email:** `admin@drait.edu.in` **Password:** `admin123` |
| **Student** | Login Page | **Email:** `rishika@drait.edu.in` **Password:** `student123` |

> **Note:** The Admin account provides full CRUD access for complaints, user management, and the Analytics Dashboard.

---

## 💻 Tech Stack (Why It's Scalable)

CampXplore is built using a modern, decoupled architecture with a strong focus on maintainability and performance.

### Frontend (React Static Site)

* **React.js:** Single Page Application (SPA) architecture.
* **Maps:** **Leaflet.js** for interactive campus maps.
* **Charts:** Chart.js for data visualization on the Admin Dashboard.
* **API:** Axios with `withCredentials: true` for secure session management.

### Backend (Flask Web Service)

* **Framework:** **Flask** (Python).
* **Database:** **PostgreSQL** with comprehensive schema (Role, Building, Path, Complaint, Feedback tables).
* **ORM:** SQLAlchemy.
* **Algorithms:** **Dijkstra's** shortest path algorithm implemented in `utils/algorithms.py`.
* **Deployment:** Gunicorn WSGI server.

---

## ⚙️ Installation & Development Setup

Follow these steps to get a local copy of the project running for development.

### 1. Prerequisites

* Python 3.8+
* Node.js (LTS recommended)
* **PostgreSQL** (running locally)
* Git

### 2. Backend Setup (`backend/`)

```bash
# 1. Clone the repository and navigate to the backend
git clone [https://github.com/RishikaYashwini/campXplore.git](https://github.com/RishikaYashwini/campXplore.git)
cd campxplore/backend

# 2. Setup Python Environment
python3 -m venv venv
source venv/bin/activate # Use 'venv\Scripts\activate' on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create and Initialize Database (Your PostgreSQL server must be running)
# Run your custom data migration script to load waypoints and paths, or:
# createdb campxplore
# python init_db.py 

# 5. Set Environment Variables (.env file)
# Example (must match your local PostgreSQL setup):
# SECRET_KEY=your-secret-key-here
# DATABASE_URL=postgresql://campxplore_user:campxplore_pass@localhost:5432/campxplore

# 6. Start the Flask API
python app.py
# API runs on: http://localhost:5000
```

### 3. Frontend Setup (`frontend/`)

```bash
# 1. Navigate to the frontend directory
cd ../frontend

# 2. Install Node dependencies
npm install

# 3. Set Environment Variable (.env.local file)
# The frontend must point to the local backend API
# REACT_APP_API_URL=http://localhost:5000

# 4. Start the React app
npm start
# App opens on: http://localhost:3000
```

---

## 🛠️ Deployment Configuration (Render)

This project is deployed to Render using a decoupled architecture for maximum scalability and easy maintenance.

### Backend Deployment: Deployed as a Python Web Service.

* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `gunicorn --bind 0.0.0.0:$PORT app:app`

### Frontend Deployment: Deployed as a Static Site.

* **Build Command:** `npm run build`
* **Publish Directory:** `build`

### Database: Hosted via Render PostgreSQL instance.

---

## 🤝 Contribution

Feel free to fork the repository and contribute! We are currently planning CampXplore v0.3, which will include features like User Profile Management and Notifications.

* Fork the Project.
* Create your Feature Branch (git checkout -b feature/AmazingFeature).
* Commit your Changes (git commit -m 'Add some AmazingFeature').
* Push to the Branch (git push origin feature/AmazingFeature).
* Open a Pull Request.

---

**Project developed by:** Rishika Yashwini | **License:** MIT
