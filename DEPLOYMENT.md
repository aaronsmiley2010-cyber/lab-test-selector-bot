# Deploying Veterinary PIMS to Heroku

## Quick Deploy (One-Click)

Click the button below to deploy directly to Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/aaronsmiley2010-cyber/lab-test-selector-bot/tree/claude/create-page-011CV4wHnCmFw66F1CBenEN8)

## Manual Deployment Steps

### Prerequisites
1. A Heroku account (free tier works fine) - Sign up at https://heroku.com
2. Git installed on your local machine
3. Heroku CLI installed - https://devcenter.heroku.com/articles/heroku-cli

### Deployment Instructions

#### Step 1: Install Heroku CLI (if not already installed)
```bash
# On Mac
brew tap heroku/brew && brew install heroku

# On Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli

# On Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### Step 2: Login to Heroku
```bash
heroku login
```

#### Step 3: Clone the repository (if you haven't already)
```bash
git clone https://github.com/aaronsmiley2010-cyber/lab-test-selector-bot.git
cd lab-test-selector-bot
git checkout claude/create-page-011CV4wHnCmFw66F1CBenEN8
```

#### Step 4: Create a Heroku app
```bash
heroku create your-veterinary-pims
```

Replace `your-veterinary-pims` with your desired app name (must be unique across Heroku).

#### Step 5: Deploy to Heroku
```bash
git push heroku claude/create-page-011CV4wHnCmFw66F1CBenEN8:main
```

#### Step 6: Open your PIMS
```bash
heroku open
```

Then navigate to `/pims/` on your Heroku URL.

### Your PIMS URLs

After deployment, your PIMS will be available at:
- **Main Dashboard:** `https://your-app-name.herokuapp.com/pims/`
- **AI Symptom Analyzer:** `https://your-app-name.herokuapp.com/pims/ai/symptom-analyzer`
- **New Patient:** `https://your-app-name.herokuapp.com/pims/patient/new`
- **Reports:** `https://your-app-name.herokuapp.com/pims/reports/dashboard`

### Environment Variables (Optional)

The PIMS works without any environment variables. If you want to enable the Slack integration:

```bash
heroku config:set SLACK_BOT_TOKEN=your-token-here
heroku config:set SLACK_SIGNING_SECRET=your-secret-here
```

### Monitoring Your App

View logs:
```bash
heroku logs --tail
```

Check app status:
```bash
heroku ps
```

### Troubleshooting

**App not starting?**
```bash
heroku logs --tail
```

**Need to restart?**
```bash
heroku restart
```

**Want to scale dynos?**
```bash
heroku ps:scale web=1
```

### Free Tier Limitations

Heroku's free tier (Eco dynos) includes:
- 1000 free dyno hours per month
- App sleeps after 30 minutes of inactivity
- Wakes up automatically when accessed (may take a few seconds)

### Upgrading to Paid Plan

For production use, consider upgrading:
```bash
heroku ps:type hobby
```

## Alternative: Deploy from GitHub

1. Go to your Heroku Dashboard
2. Click "New" → "Create new app"
3. Connect to GitHub and select this repository
4. Choose the `claude/create-page-011CV4wHnCmFw66F1CBenEN8` branch
5. Click "Deploy Branch"

## Post-Deployment

Once deployed, you can:
1. Access the PIMS at your Heroku URL
2. Create patient profiles
3. Use AI features
4. Add medical records
5. Generate reports

The PIMS is fully functional and ready to use immediately after deployment!

## Support

If you encounter any issues during deployment, check:
- Heroku logs: `heroku logs --tail`
- Heroku status page: https://status.heroku.com/
- This repository's issues page
