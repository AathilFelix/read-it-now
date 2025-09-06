# 🚀 Render Deployment Guide for Read It Now

This guide will help you deploy your Read It Now app on Render.

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be pushed to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **HackClub AI API Key**: Get it from HackClub

## 🎯 Quick Deployment Steps

### Step 1: Prepare Your Repository

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

### Step 2: Create Render Web Service

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**

   **Basic Settings:**

   - **Name**: `read-it-now` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`

   **Build & Deploy:**

   - **Build Command**: `./build.sh`
   - **Start Command**: `./start.sh`

### Step 3: Environment Variables

In the Render dashboard, add these environment variables:

```
HACKCLUB_API_KEY=your_hackclub_api_key_here
HACKCLUB_BASE_URL=https://api.hackclub.com
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your_secure_random_secret_key
PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/.playwright
PYTHONUNBUFFERED=1
```

### Step 4: Deploy

1. **Click "Create Web Service"**
2. **Render will automatically:**
   - Clone your repository
   - Run `./build.sh` (installs dependencies + Playwright)
   - Start your app with `./start.sh`
3. **Your app will be live at:** `https://your-service-name.onrender.com`

## 🔧 Configuration Files Explained

### `build.sh`

- Installs Python dependencies
- Downloads Playwright browsers
- Verifies installation

### `start.sh`

- Sets Render-specific environment variables
- Starts Gunicorn with proper configuration

### `render.yaml` (Optional)

- Infrastructure as Code configuration
- Can be used instead of manual setup

### `requirements.txt`

- All Python dependencies including Playwright
- Optimized for Render deployment

## 🐛 Troubleshooting

### Common Issues:

1. **Build Fails:**

   ```bash
   # Check build.sh permissions
   chmod +x build.sh
   git add . && git commit -m "Fix permissions" && git push
   ```

2. **Playwright Issues:**

   - Render automatically installs browsers during build
   - Check build logs for Playwright installation errors
   - Fallback to requests method is implemented

3. **Memory Issues:**

   - Render Free tier has 512MB RAM limit
   - App is optimized for single worker
   - Consider upgrading plan for heavy usage

4. **Timeout Issues:**
   - Gunicorn timeout set to 120 seconds
   - AI processing can take 15-20 seconds
   - This is normal behavior

### Debugging:

1. **Check Build Logs:**

   - Go to Render Dashboard → Your Service → Logs
   - Look for build errors

2. **Check Runtime Logs:**

   - Monitor application logs for errors
   - Check for ImportError or dependency issues

3. **Test Locally:**

   ```bash
   # Test build script
   ./build.sh

   # Test start script
   ./start.sh
   ```

## 🎉 Success!

Once deployed, your app will be available at:

```
https://your-service-name.onrender.com
```

### Features Available:

- ✅ **Article Summarization**: Paste any URL → Get 1-minute summary
- ✅ **Anti-Bot Protection**: Playwright with fallback to requests
- ✅ **Mobile Friendly**: Responsive design
- ✅ **Auto HTTPS**: Render provides SSL certificates
- ✅ **Auto Scaling**: Handles traffic spikes

## 📊 Monitoring

- **Render Dashboard**: Monitor deployment status, logs, and metrics
- **Health Checks**: App includes `/health` endpoint
- **Error Handling**: Graceful fallbacks for common issues

## 💰 Pricing

- **Free Tier**: 750 hours/month, 512MB RAM, sleeps after 15min inactivity
- **Starter Plan**: $7/month, always on, 512MB RAM
- **Standard Plan**: $25/month, 2GB RAM, better performance

For Read It Now, Free tier is sufficient for testing, Starter for light production use.

## 🔄 Updates

To update your app:

1. Push changes to GitHub
2. Render automatically detects and redeploys
3. Zero-downtime deployments

---

**Your Read It Now app is now production-ready on Render! 🎉**
