# UWA Course Evaluation System

A comprehensive platform for University of Western Australia students to discover, rate, and share insights about courses and instructors.

## 📚 Project Overview

The UWA Course Evaluation System is a web application designed to enhance the academic experience by providing a centralized platform where students can:

- Browse and search for UWA courses and instructors
- View detailed course information including structure, assessment methods, and difficulty levels
- Read and contribute authentic student reviews and ratings
- Create and share course resources and insights
- Connect with peers through a messaging system

Built with a modern tech stack including Flask, SQLAlchemy, and Tailwind CSS, this platform aims to help students make informed decisions about their academic journey.

## 🚀 Features

- **User Authentication**: Secure registration and login system
- **Course Discovery**: Browse, search, and filter courses by various criteria
- **Instructor Profiles**: View instructor information, teaching styles, and ratings
- **Course Reviews**: Read and write detailed course reviews with ratings
- **Score Structure Visualization**: Interactive charts showing assessment breakdowns
- **Responsive Design**: Fully functional on both desktop and mobile devices
- **User Profiles**: Personalized profiles with favorite courses and contribution history
- **Messaging System**: Private communication between users

## 🛠️ Technology Stack

### Frontend
- HTML5, CSS3, JavaScript
- Tailwind CSS for responsive design
- Chart.js for data visualization

### Backend
- Flask (Python web framework)
- SQLAlchemy ORM
- SQLite database (development)

### Tools & Utilities
- Flask-Migrate for database migrations
- Nginx for local deployment

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- Pip (Python package manager)
- Git

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/HashZard/CITS5505-Group.git
cd uwa-course-evaluation
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
export FLASK_APP=backend/app/app.py
export FLASK_ENV=development
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. Start the development server:
```bash
# Start Flask backend (port 8000)
flask run --port=8000

# In a separate terminal, serve the frontend (requires Nginx)
# Or use the setup script:
bash deploy/local_deploy/setup.sh
```

Access the application at http://localhost:3000

## 📊 Project Structure

```
uwa-course-evaluation/
├── backend/                # Flask backend
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── __init__.py     # App factory
├── frontend/               # Frontend code
│   ├── assets/             # Images and static assets
│   ├── components/         # Reusable UI components
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── pages/              # HTML pages
├── deploy/                 # Deployment configurations
├── migrations/             # Database migrations
├── tests/                  # Test suite
└── requirements.txt        # Python dependencies
```

## 🧪 Testing

Run the test suite with:

```bash
# run units test
python -m unittest discover -s backend/test/service
```

## 🤝 Contributing

Please see [README_COLLABORATOR.md](README_COLLABORATOR.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

CITS5505 - Group13 - University of Western Australia
- Xudong Zhao (24151881)
- Xinghe Wang (24373601)
- Xudong Chen (23778972)
- Areeb Amir (24156417)

## 🙏 Acknowledgments

- UWA School of Computer Science and Software Engineering
- All students who contributed reviews and feedback