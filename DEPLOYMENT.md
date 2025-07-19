# 🚀 Deployment Guide

This guide covers various deployment options for the AI Revision Agent.

## 📋 Prerequisites

- Python 3.8+
- OpenRouter API key
- Git (for repository cloning)

## 🖥️ Local Development

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/your-username/ai-revision-agent.git
cd ai-revision-agent

# Run automated setup
python setup.py

# Edit .env file with your API key
# OPENROUTER_API_KEY=your_actual_key_here

# Test the installation
python 3_Agent_Code/test_runner.py
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your API key

# Run CLI version
python 3_Agent_Code/cli_interface.py

# Run web version
streamlit run streamlit_app.py
```

## ☁️ Cloud Deployment

### Streamlit Cloud (Recommended for Web App)

1. **Fork the repository** on GitHub
2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Connect your GitHub account**
4. **Deploy from your fork**:
   - Repository: `your-username/ai-revision-agent`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
5. **Add secrets** in Streamlit Cloud dashboard:
   ```toml
   OPENROUTER_API_KEY = "your_actual_api_key_here"
   ```

### Heroku Deployment

1. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```

2. **Add Procfile**:
   ```bash
   echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set OPENROUTER_API_KEY=your_actual_key_here
   ```

4. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Railway Deployment

1. **Connect GitHub repository** at [Railway](https://railway.app)
2. **Add environment variables**:
   - `OPENROUTER_API_KEY`: your actual API key
3. **Railway will auto-deploy** from your repository

### Docker Deployment

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .
   EXPOSE 8501

   CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0"]
   ```

2. **Build and run**:
   ```bash
   docker build -t ai-revision-agent .
   docker run -p 8501:8501 -e OPENROUTER_API_KEY=your_key ai-revision-agent
   ```

## 🔧 Environment Configuration

### Required Environment Variables
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Optional Environment Variables
```bash
OPENROUTER_HTTP_REFERER=your_app_name
OPENROUTER_X_TITLE=AI Revision Agent
```

## 🧪 Testing Deployment

### Health Check Endpoints
- **CLI Test**: `python 3_Agent_Code/test_runner.py`
- **Web Test**: Visit `/` on your deployed URL
- **API Test**: Check if topics load in the sidebar

### Common Issues

1. **API Key Not Found**:
   - Ensure `OPENROUTER_API_KEY` is set correctly
   - Check environment variable spelling

2. **Import Errors**:
   - Verify all dependencies in `requirements.txt`
   - Check Python version compatibility

3. **Streamlit Issues**:
   - Clear browser cache
   - Check Streamlit logs for errors

## 📊 Monitoring

### Streamlit Cloud
- Built-in logs and metrics
- Resource usage monitoring
- Automatic restarts

### Heroku
- Use `heroku logs --tail` for real-time logs
- Monitor dyno usage in dashboard

### Custom Monitoring
```python
# Add to your app for basic monitoring
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log usage statistics
logger.info(f"User generated summary for: {topic}")
```

## 🔒 Security Considerations

1. **API Key Security**:
   - Never commit API keys to repository
   - Use environment variables or secrets management
   - Rotate keys regularly

2. **Rate Limiting**:
   - Implement request throttling for production
   - Monitor API usage

3. **Input Validation**:
   - Sanitize user inputs
   - Implement proper error handling

## 📈 Scaling

### Horizontal Scaling
- Use load balancers for multiple instances
- Implement session persistence if needed

### Performance Optimization
- Cache frequently requested summaries
- Implement async processing for multiple topics
- Use CDN for static assets

## 🆘 Troubleshooting

### Common Commands
```bash
# Check Python version
python --version

# Verify dependencies
pip list

# Test imports
python -c "import streamlit; print('Streamlit OK')"

# Check environment variables
python -c "import os; print(os.getenv('OPENROUTER_API_KEY', 'NOT_SET'))"
```

### Support Resources
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Project Issues](https://github.com/your-username/ai-revision-agent/issues)

---

**Happy Deploying! 🚀**