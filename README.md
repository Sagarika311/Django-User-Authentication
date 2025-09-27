# Django Registration & Authentication System

A full-featured **Django boilerplate** for user registration and authentication.
This project provides a ready-to-use system with account creation, email verification, login/logout, password management, and user profile handling — all built with Django 5 and Bootstrap 5.

---

## ✨ Features

* Custom **User model** (`CustomUser`) with username, email, and optional phone number
* **User registration** with email activation link
* **Login** with username, email, or phone number + “Remember me” option
* **Account activation** via email (console backend in development)
* **Password reset** (via email) and password change functionality
* **Resend activation link**
* **Remind username** via email
* **Change email address** with confirmation flow
* Protected **Authorized page** for logged-in users
* Bootstrap 5 templates for a clean UI

---

## 🛠️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/registration-login-system.git
   cd registration-login-system
   ```

2. **Create virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Apply migrations**

   ```bash
   python manage.py makemigrations accounts
   python manage.py migrate
   ```

4. **Create superuser (for Django admin)**

   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**

   ```bash
   python manage.py runserver
   ```

6. Open browser → [http://127.0.0.1:8000/accounts/register/](http://127.0.0.1:8000/accounts/register/)

---

## 📧 Email Setup

* **Development:** uses Django console backend (activation/reset links will print in terminal).
* **Production:** configure SMTP in `settings.py`:

  ```python
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = 'smtp.gmail.com'
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True
  EMAIL_HOST_USER = 'your-email@example.com'
  EMAIL_HOST_PASSWORD = 'your-app-password'
  DEFAULT_FROM_EMAIL = 'Your Site <noreply@yoursite.com>'
  ```

---

## 📂 Project Structure

```
accounts/
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tokens.py
├── views.py
├── urls.py
└── templates/accounts/
    ├── base.html
    ├── register.html
    ├── login.html
    ├── authorized.html
    ├── activation_sent.html
    ├── activation_invalid.html
    ├── resend_activation.html
    ├── remind_username.html
    ├── password_reset_form.html
    ├── password_reset_done.html
    ├── password_reset_confirm.html
    ├── password_reset_complete.html
    ├── password_change_form.html
    └── password_change_done.html
```

---

## 🚀 Future Improvements

* Make email the unique username field (`USERNAME_FIELD = 'email'`)
* Add **two-factor authentication (2FA / OTP)**
* Write **unit tests** for flows (registration, login, password reset, etc.)
* Improve styling with Tailwind CSS or custom design

---

## 📝 License

This project is licensed under the MIT License. Feel free to use, modify, and share.

---

### 👩‍💻 Author

Developed by **Sagarika**.
If you find this project helpful, give it a ⭐ on GitHub!
