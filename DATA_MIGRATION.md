# Data Migration Guide: Local to Railway

This guide explains how to transfer your data (products, sales, orders) from your local computer to your Railway production database.

## Prerequisites

1.  **Railway Project**: You must have a project on Railway with a PostgreSQL database.
2.  **Railway CLI** (Optional but recommended): Or you can use the Railway dashboard.
3.  **Git**: Your code must be pushed to GitHub and connected to Railway.

## Step 1: Prepare Your Data (Local Computer)

Run the following command in your terminal to export your local data to a file named `data.json`. This excludes authentication and content type data to avoid conflicts.

```bash
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data.json
```

## Step 2: Upload Data File

1.  Commit the `data.json` file to your Git repository:

```bash
git add data.json
git commit -m "Add initial data dump"
git push origin main
```

2.  Wait for Railway to redeploy your application.

## Step 3: Load Data on Railway

Once your application is deployed on Railway, you need to run the load command.

### Option A: Using Railway Dashboard

1.  Go to your Railway project dashboard.
2.  Click on your Django service.
3.  Go to the **"Settings"** tab.
4.  Scroll down to **"Deploy"** section.
5.  Find **"Healthcheck Command"** or use the **"Command"** tab to run a one-off command (if available via CLI) or simply use the **"Variables"** tab to ensure `DATABASE_URL` is set.
6.  *Better Method via Dashboard*: Go to the **"Connect"** tab, copy the **"Postgres Connection URL"**. Use a local tool like **pgAdmin** or **DBeaver** to connect to the remote database and restore data, BUT since we have `data.json` in the code, we can use the Django command.

**The Easiest Way (via Railway CLI or Shell):**

If you have Railway CLI installed:
```bash
railway run python manage.py migrate
railway run python manage.py loaddata data.json
```

**Alternative (via Build Command - One time only):**

You can temporarily add the load command to your Start Command in Railway settings, but **remove it after the first run**:

Change Start Command to:
```bash
python manage.py migrate && python manage.py loaddata data.json && gunicorn Point_De_Vente.wsgi
```

**After the deployment finishes and data is loaded, change it back to:**
```bash
python manage.py migrate && gunicorn Point_De_Vente.wsgi
```

## Step 4: Verify

Visit your Railway app URL and check if your products and orders are visible.
