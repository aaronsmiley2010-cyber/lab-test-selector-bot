# Veterinary PIMS Deployment - Render

## Deploy to Render (Free Tier Available)

Render offers a free tier that's perfect for this PIMS!

### Step-by-Step Deployment

1. **Create a Render account**: https://render.com/
   - Sign up with GitHub (recommended) or email

2. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select repository: `lab-test-selector-bot`
   - Branch: `claude/create-page-011CV4wHnCmFw66F1CBenEN8`

3. **Configure the service**:
   - **Name**: `veterinary-pims` (or your choice)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:flask_app`
   - **Plan**: Free

4. **Deploy**:
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Your PIMS will be available at: `https://veterinary-pims.onrender.com/pims/`

### Free Tier Limitations
- App spins down after 15 minutes of inactivity
- Takes 30-60 seconds to wake up when accessed
- 750 hours/month free (plenty for testing)

### Environment Variables (Optional)
If you want Slack integration:
- `SLACK_BOT_TOKEN`: (leave empty)
- `SLACK_SIGNING_SECRET`: (leave empty)
