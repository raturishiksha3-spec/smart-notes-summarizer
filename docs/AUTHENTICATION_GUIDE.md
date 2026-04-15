# Authentication System Guide

## Overview

The Smart Notes Summarizer now includes a complete authentication system with login and registration pages that users must pass through before accessing the main application.

## Implementation Details

### Backend (Flask)

#### Database
- **Database**: SQLite (`smart_notes.db`)
- **Users Table**: Stores user credentials with hashed passwords
- **Sessions**: In-memory session storage with token-based authentication

#### API Endpoints

##### 1. Register User
```
POST /api/register
Content-Type: application/json

Request Body:
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}

Response:
{
  "success": true,
  "message": "Registration successful",
  "user": {
    "user_id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "token": "session_token_here"
}
```

**Validation Rules**:
- Name: Minimum 2 characters
- Email: Valid email format, unique in database
- Password: Minimum 6 characters

##### 2. Login User
```
POST /api/login
Content-Type: application/json

Request Body:
{
  "email": "john@example.com",
  "password": "password123"
}

Response:
{
  "success": true,
  "message": "Login successful",
  "user": {
    "user_id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "token": "session_token_here"
}
```

#### Security Features
- **Password Hashing**: SHA-256 hashing for password storage
- **Session Tokens**: Cryptographically secure tokens (32 bytes, URL-safe)
- **Session Expiration**: 24-hour session lifetime
- **Email Uniqueness**: Prevents duplicate accounts

### Frontend (React)

#### Components

##### 1. Login.jsx
- Email and password input fields
- Form validation
- Error handling and display
- Link to registration page
- Calls `onLogin()` callback on success

##### 2. Register.jsx
- Name, email, password, and confirm password fields
- Password matching validation
- Error handling
- Link to login page
- Calls `onRegister()` callback on success

##### 3. Updated App.jsx
- Conditional rendering based on auth state
- Shows login/register if not authenticated
- Shows main app if authenticated
- Logout functionality
- Persistent sessions (localStorage)

#### Authentication Flow

```
1. User opens app → Login page shown
2. User clicks "Sign up" → Registration page shown
3. User registers → Account created → Logged in automatically
4. OR User logs in → Session created → Logged in
5. User session stored in localStorage
6. App checks localStorage on load → Auto-login if session exists
7. User clicks logout → Session cleared → Back to login
```

## How to Use

### For Users

1. **First Time Users**:
   - Visit http://localhost:3000
   - Click "Sign up" link
   - Fill in name, email, and password
   - Click "Create Account"
   - Automatically logged in

2. **Returning Users**:
   - Visit http://localhost:3000
   - Enter email and password
   - Click "Sign In"
   - If session exists, logged in automatically

3. **Logging Out**:
   - Click "Logout" button in header
   - Session cleared and redirected to login

### For Developers

#### Testing Endpoints

**Register a user:**
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"password123"}'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**Test User Credentials:**
- Email: test@example.com
- Password: password123

#### Database Management

**Initialize database:**
```bash
cd backend
python init_db.py
```

**Reset database:**
```bash
cd backend
python init_db.py --reset
```

**Add sample data:**
Uncomment the `add_sample_data()` call in `init_db.py`

## Security Notes

### Current Implementation
- Basic authentication suitable for development
- Password hashing with SHA-256
- Session tokens stored in-memory
- localStorage for client-side persistence

### Production Recommendations

1. **Password Security**:
   - Upgrade to bcrypt or Argon2
   - Add password strength requirements
   - Implement password reset functionality

2. **Session Management**:
   - Use Redis for session storage
   - Implement token refresh mechanism
   - Add CSRF protection

3. **API Security**:
   - Add rate limiting
   - Implement HTTPS
   - Add request validation middleware
   - Use JWT tokens instead of session tokens

4. **Database**:
   - Migrate to PostgreSQL for production
   - Add database connection pooling
   - Implement backup strategy

5. **Additional Features**:
   - Email verification
   - Two-factor authentication (2FA)
   - Account lockout after failed attempts
   - Password history tracking

## Project Structure

```
backend/
├── app.py              # Main Flask app with auth endpoints
├── init_db.py          # Database initialization
├── smart_notes.db      # SQLite database (generated)
└── uploads/            # File uploads directory

frontend/
├── src/
│   ├── App.jsx         # Main app with auth routing
│   ├── Login.jsx       # Login component
│   ├── Register.jsx    # Registration component
│   └── main.jsx        # Entry point
├── package.json
└── vite.config.js
```

## Troubleshooting

### Common Issues

**"Email already registered"**
- Email is already in the database
- Use a different email or reset the database

**"Invalid email or password"**
- Check credentials are correct
- Ensure account exists

**Database errors**
- Run `python init_db.py` to create tables
- Check `smart_notes.db` file exists

**Session not persisting**
- Check browser localStorage is enabled
- Clear localStorage and re-login

**Port already in use**
- Backend: Check port 5000
- Frontend: Check port 3000
- Kill existing processes or change ports

## Future Enhancements

- [ ] User profile page
- [ ] Edit profile functionality
- [ ] Password reset via email
- [ ] Social login (Google, Facebook)
- [ ] Remember me functionality
- [ ] Account deletion
- [ ] Admin dashboard
- [ ] User roles and permissions
- [ ] Activity logging

---

**Made with ❤️ by Smart Notes Squad**

