# 📸 Instagram Clone — Backend API

A backend REST API replicating core Instagram functionality, built with Django and Django REST Framework. Covers user authentication, post management, media handling, and real SMS/email verification flows.

---

## 🚀 Features

- **User registration & authentication** — JWT-based login, token refresh
- **Phone & email verification** — OTP via Twilio SMS + email templates
- **User profiles** — profile creation, update, avatar upload
- **Posts** — create, read, update, delete (full CRUD)
- **Media handling** — image uploads via Pillow
- **Secure configuration** — environment variables with python-decouple
- **PostgreSQL** database with psycopg2

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 4.2 |
| API | Django REST Framework |
| Auth | JWT (djangorestframework-simplejwt) |
| Database | PostgreSQL (psycopg2) |
| Media | Pillow |
| SMS | Twilio |
| Config | python-decouple |
| Phone validation | phonenumbers |

---

## 📁 Project Structure

```
Instagram_clone/
├── users/              # User model, registration, auth, profiles
├── post/               # Post model, CRUD endpoints
├── shared/             # Shared utilities and helpers
├── media/              # Uploaded media files
├── templates/
│   └── email/          # Email verification templates
├── .env                # Environment variables (not committed)
├── requirements.txt    # Dependencies
└── manage.py
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Azamatjohn/Instagram_clone.git
cd Instagram_clone
```

### 2. Create a virtual environment
```bash
pip install pipenv
pipenv shell
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

DB_NAME=instagram_clone
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_number

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Start the development server
```bash
python manage.py runserver
```

---

## 🔑 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/register/` | Register a new user |
| POST | `/users/login/` | Login and receive JWT tokens |
| POST | `/users/token/refresh/` | Refresh access token |
| POST | `/users/verify/phone/` | Verify phone via OTP (Twilio) |
| POST | `/users/verify/email/` | Verify email address |

### Users
| Method | Endpoint | Description |
|---|---|---|
| GET | `/users/profile/<id>/` | Get user profile |
| PUT | `/users/profile/<id>/` | Update user profile |

### Posts
| Method | Endpoint | Description |
|---|---|---|
| GET | `/post/` | List all posts |
| POST | `/post/` | Create a new post |
| GET | `/post/<id>/` | Get a specific post |
| PUT | `/post/<id>/` | Update a post |
| DELETE | `/post/<id>/` | Delete a post |

---

## 🔐 Authentication

All protected endpoints require a JWT access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

## 📋 Requirements

See [requirements.txt](requirements.txt) for the full list of dependencies.

Key packages:
- `Django==4.2.24`
- `djangorestframework==3.16.1`
- `djangorestframework_simplejwt==5.5.1`
- `psycopg2==2.9.10`
- `pillow==11.3.0`
- `twilio==9.8.0`
- `python-decouple==3.8`
- `phonenumbers==9.0.13`

---

## 👤 Author

**Azamatjon Abdulazizov**
- LinkedIn: [azamatjon-abdulazizov](https://linkedin.com/in/azamatjon-abdulazizov)
- GitHub: [@Azamatjohn](https://github.com/Azamatjohn)
- Email: abdulazizovjohn@gmail.com
