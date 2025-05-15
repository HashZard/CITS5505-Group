# UWA Course Evaluation System

A comprehensive platform for University of Western Australia students to discover, rate, and share insights about
courses.

## 📚 Project Overview

The UWA Course Evaluation System is a web application designed to enhance the academic experience by providing a
centralized platform where students can:

- Browse and search for UWA courses and instructors
- View detailed course information including structure, assessment methods, and relative document.
- Read and contribute authentic student reviews and ratings
- Create and share course resources and insights
- Connect with peers through a messaging system

Built with a modern tech stack including Flask, SQLAlchemy, and Tailwind CSS, this platform aims to help students make
informed decisions about their academic journey.

## 🚀 Features

- **User Authentication**: Secure registration and login system
- **Course Discovery**: Browse, search, and filter courses by various criteria
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

### ### 🚀 Local Development Setup

To get started quickly, follow these steps:

1. **Clone the repository**
   ```bash
   git clone https://github.com/HashZard/CITS5505-Group.git
   ```

2. **Navigate to the project directory**
   ```bash
   cd CITS5505-Group
   ```

3. **Run the setup script**
   ```bash
   bash ./deploy/local_deploy/setup.sh
   ```

   For testing purposes, you can run the setup script with the `--env=test` flag to set up a test environment:
   ```bash
   bash ./deploy/local_deploy/setup.sh --env=test
   ```

The application will be available at: [http://localhost:3000](http://localhost:3000)

4. **Generate demo data**
   ```bash
   python3 ./backend/test/generate_demo_data.py
   ```

5. **Test the application with the admin account**
   ```text
   Email:    admin@example.com
   Password: admin2025
   ```

## 📊 Project Structure

```
CITS5505-Group/
├── backend/                # Flask backend
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Utility functions
│   │   └── __init__.py     # App factory
│   ├── test/               # Unit tests
│   │   ├── selenction/     # Test cases for selection
│   │   └── service/        # Test cases for services
│   └── app.db/             # SQLite database
├── frontend/               # Frontend code
│   ├── assets/             # Images and static assets
│   ├── components/         # Reusable UI components
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   ├── pages/              # HTML pages
│   └── index.html          # Main entry point
├── deploy/                 # Deployment configurations
├── migrations/             # Database migrations
├── tests/                  # Test suite
└── requirements.txt        # Python dependencies
```

## 🤝 Contributing

Please see [README_COLLABORATOR.md](README_COLLABORATOR.md) for details on our code of conduct and the process for
submitting pull requests.

## 👥 Authors

CITS5505 - Group13 - University of Western Australia

- Xudong Zhao (24151881)
- Xinghe Wang (24373601)
- Xudong Chen (23778972)
- Areeb Amir (24156417)

## 🙏 Acknowledgments

- UWA School of Computer Science and Software Engineering
- All students who contributed reviews and feedback