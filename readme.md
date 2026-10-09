# Muscle Gain - Gym Management Website

A modern web application for managing gym memberships, classes, schedules, and more. Designed for gym owners, staff, and members to seamlessly interact and manage gym operations.

## Live Website

[Click here to visit the FRONTEND live site](https://gym-management-client-lilac.vercel.app/)

[Click here to visit the BACKEND live site](https://gym-management-0fmi.onrender.com/)

## Credentials

- User Credentials

        Email: tanvirulislam149@gmail.com
        password: asdfasdf12

- Admin Credentials

        Email: admin@gmail.com
        password: admin

## Features

- Member registration and login
- Admin dashboard for gym management
- Real time notification and chat with admin feature
- Class scheduling and booking
- Membership plans and payments
- Attendance tracking
- Mobile-responsive UI

## Tech Stack

**Frontend:**

- Next.js
- Tailwind CSS
- Redux Toolkit (for state management)

**Backend:**

- Django Rest Framework
- Django channels, Redis
- PostgreSQL
- JWT for authentication
- WebSockets for notification

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/tanvirulislam149/gym_management.git
cd gym_management

# Create a virtual environment
python -m venv gym_env

# Activate the virtual environment
# On Windows:
gym_env\Scripts\activate

# On macOS/Linux:
source gym_env/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

```bash
# For PostgreSQL Database
user=your_user
password=your_password
host=your_host
port=your_port
dbname=your_dbname

# For Sending Email
EMAIL_BACKEND=your_EMAIL_BACKEND
EMAIL_HOST=your_EMAIL_HOST
EMAIL_USE_TLS=your_EMAIL_USE_TLS
EMAIL_PORT=your_EMAIL_PORT
EMAIL_HOST_USER=your_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=your_EMAIL_HOST_PASSWORD

# For Cloudinary Storage
Cloud_name=your_Cloud_name
API_key=your_API_key
API_secret=your_API_secret
CLOUDINARY_URL=your_CLOUDINARY_URL

# URLs
FRONTEND_PROTOCOL=your_FRONTEND_PROTOCOL
FRONTEND_DOMAIN=your_FRONTEND_DOMAIN
FRONTEND_URL=your_FRONTEND_URL
BACKEND_URL=your_BACKEND_URL

# Redis
REDIS_URL=your_REDIS_URL
```

**Deployment:**

- Vercel (Frontend)
- Render (Backend)
