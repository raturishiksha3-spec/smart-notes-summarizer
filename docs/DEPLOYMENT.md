# 🚀 Deployment Guide for Smart Notes Summarizer

This guide covers deployment options for both backend and frontend of the Smart Notes Summarizer application.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Deployment](#backend-deployment)
   - [Render](#deploy-backend-on-render)
   - [Heroku](#deploy-backend-on-heroku)
   - [Railway](#deploy-backend-on-railway)
3. [Frontend Deployment](#frontend-deployment)
   - [Vercel](#deploy-frontend-on-vercel)
   - [Netlify](#deploy-frontend-on-netlify)
4. [Docker Deployment](#docker-deployment)
5. [Environment Variables](#environment-variables)
6. [Post-Deployment](#post-deployment)

---

## Prerequisites

- GitHub account
- Git installed locally
- Project repository on GitHub
- Domain name (optional)

---

## Backend Deployment

### Deploy Backend on Render

**Render** is recommended for Python Flask applications with free tier support.

#### Steps:

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the backend directory

3. **Configure Service**
   ```
   Name: smart-notes-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **Set Environment Variables**
   ```
   SECRET_KEY=your-production-secret-key
   FLASK_ENV=production
   DATABASE_PATH=/opt/render/project/src/smart_notes.db
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (may take 10-15 minutes for first deployment)
   - Note your backend URL: `https://smart-notes-backend.onrender.com`

---

### Deploy Backend on Heroku

#### Steps:

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from heroku.com/cli
   ```

2. **Login and Create App**
   ```bash
   heroku login
   cd backend
   heroku create smart-notes-backend
   ```

3. **Add Buildpack**
   ```bash
   heroku buildpacks:set heroku/python
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set FLASK_ENV=production
   ```

5. **Create Procfile** (in backend directory)
   ```
   web: gunicorn app:app
   ```

6. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

---

### Deploy Backend on Railway

#### Steps:

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**
   - Railway auto-detects Python
   - Set environment variables in dashboard
   - Railway provides HTTPS URL automatically

---

## Frontend Deployment

### Deploy Frontend on Vercel

**Vercel** is optimized for React applications and offers seamless deployment.

#### Steps:

1. **Install Vercel CLI** (optional)
   ```bash
   npm install -g vercel
   ```

2. **Deploy via Dashboard**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository
   - Select frontend directory

3. **Configure Build Settings**
   ```
   Framework Preset: Vite
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Set Environment Variables**
   ```
   VITE_API_URL=https://your-backend-url.onrender.com/api
   ```

5. **Deploy**
   - Click "Deploy"
   - Get your production URL: `https://smart-notes.vercel.app`

#### Alternative: Deploy via CLI

```bash
cd frontend
vercel
# Follow prompts
vercel --prod  # Deploy to production
```

---

### Deploy Frontend on Netlify

#### Steps:

1. **Create Netlify Account**
   - Go to [netlify.com](https://netlify.com)
   - Sign up with GitHub

2. **Deploy from Git**
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub
   - Select repository

3. **Configure Build Settings**
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/dist
   ```

4. **Set Environment Variables**
   - Go to Site settings → Environment variables
   - Add: `VITE_API_URL=https://your-backend-url.onrender.com/api`

5. **Deploy**
   - Click "Deploy site"
   - Get your URL: `https://smart-notes.netlify.app`

---

## Docker Deployment

### Using Docker Compose

1. **Build and Run**
   ```bash
   docker-compose up --build -d
   ```

2. **Check Status**
   ```bash
   docker-compose ps
   ```

3. **View Logs**
   ```bash
   docker-compose logs -f
   ```

4. **Stop Services**
   ```bash
   docker-compose down
   ```

### Deploy to Cloud with Docker

#### AWS ECS / Azure Container Instances / GCP Cloud Run

1. **Build Image**
   ```bash
   docker build -t smart-notes-backend:latest ./backend
   docker build -t smart-notes-frontend:latest ./frontend
   ```

2. **Push to Container Registry**
   ```bash
   # AWS ECR
   aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.region.amazonaws.com
   docker tag smart-notes-backend:latest <account>.dkr.ecr.region.amazonaws.com/smart-notes:backend
   docker push <account>.dkr.ecr.region.amazonaws.com/smart-notes:backend
   ```

3. **Deploy to Service**
   - Follow cloud provider's container deployment guide

---

## Environment Variables

### Backend (.env)

```env
# Production Settings
SECRET_KEY=<generate-strong-random-key>
FLASK_ENV=production
DATABASE_PATH=/path/to/persistent/storage/smart_notes.db

# Model Settings
SUMMARIZATION_MODEL=facebook/bart-large-cnn
QA_MODEL=t5-base

# Server
HOST=0.0.0.0
PORT=5000

# CORS
CORS_ORIGINS=https://your-frontend-domain.com
```

### Frontend (.env.production)

```env
VITE_API_URL=https://your-backend-domain.com/api
```

### Generate Secret Key

```python
# Python
import secrets
print(secrets.token_hex(32))
```

---

## Post-Deployment

### 1. Test API Endpoints

```bash
# Health check
curl https://your-backend-url.com/api/health

# Test registration
curl -X POST https://your-backend-url.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","password":"test123"}'
```

### 2. Monitor Application

- Set up error tracking (Sentry, Rollbar)
- Monitor uptime (UptimeRobot, Pingdom)
- Check logs regularly

### 3. Set Up Custom Domain (Optional)

#### Vercel
- Go to Project Settings → Domains
- Add custom domain
- Update DNS records

#### Render
- Go to Settings → Custom Domain
- Follow DNS configuration instructions

### 4. Enable HTTPS

- Most platforms (Vercel, Netlify, Render) provide free SSL certificates automatically
- For custom setups, use Let's Encrypt

### 5. Database Backup

For production SQLite:
```bash
# Backup
sqlite3 smart_notes.db ".backup backup.db"

# Restore
sqlite3 smart_notes.db ".restore backup.db"
```

Consider upgrading to PostgreSQL for production:
- Render PostgreSQL (free tier)
- ElephantSQL
- AWS RDS

---

## Troubleshooting

### Backend Issues

**Problem:** Models not loading
- **Solution:** Increase memory/RAM allocation in hosting platform
- Models require ~2-4GB RAM

**Problem:** Slow response times
- **Solution:** 
  - Enable model caching
  - Use smaller models (distilbart, t5-small)
  - Add Redis caching layer

**Problem:** Database locked errors
- **Solution:** 
  - Migrate to PostgreSQL for concurrent access
  - Use connection pooling

### Frontend Issues

**Problem:** API calls failing
- **Solution:** 
  - Check CORS settings
  - Verify API URL in environment variables
  - Check network tab in browser DevTools

**Problem:** Build fails
- **Solution:**
  - Clear node_modules and reinstall
  - Check Node.js version compatibility
  - Review build logs for specific errors

---

## Performance Optimization

### Backend
1. **Add Redis caching** for API responses
2. **Use Gunicorn workers**: `gunicorn -w 4 -k gthread --threads 2 app:app`
3. **Implement request queuing** for heavy AI operations
4. **Use CDN** for static assets

### Frontend
1. **Enable lazy loading** for components
2. **Optimize bundle size** with code splitting
3. **Add service worker** for PWA
4. **Compress images** and assets

---

## Security Checklist

- [ ] Change all default passwords and keys
- [ ] Enable HTTPS everywhere
- [ ] Set up rate limiting on API
- [ ] Implement input validation
- [ ] Add CSRF protection
- [ ] Regular security audits
- [ ] Keep dependencies updated
- [ ] Set secure HTTP headers
- [ ] Implement proper authentication
- [ ] Add logging and monitoring

---

## Support

For deployment issues:
- Check platform-specific documentation
- Review application logs
- Contact: smartnotessquad@example.com

---

**Last Updated:** October 2025  
**Maintained by:** Smart Notes Squad