# Personal Color Analysis API & PDF Generator (Pro Edition)

An automated microservice engine built with FastAPI, OpenCV (ITA° dermatological skin analysis), rembg (background removal), WeasyPrint (multi-page PDF dossier generation), and SMTP email delivery.

Designed for seamless deployment on **Render.com** (Free Docker Web Service) and integration with **WordPress** (WPForms or shortcode).

---

## Features

- **Dermatological Skin Analysis**: Calculates Individual Typology Angle (ITA°), warmth index, value, and contrast scores using OpenCV face detection & LAB color space.
- **12 Sub-Season Seasonal Palettes**:
  - Spring: Light Spring, Warm Spring, Bright Spring
  - Summer: Light Summer, Cool Summer, Soft Summer
  - Autumn: Soft Autumn, Warm Autumn, Dark Autumn
  - Winter: Dark Winter, Cool Winter, Bright Winter
- **Luxury Multi-Page PDF Dossiers**: Generates 3-page customized PDF reports featuring client cutouts, 12 swatch codes (Hex + names), metal/jewelry recommendations, makeup advice, and colors to avoid.
- **Background Removal**: Integrates `rembg` for automated background removal with fallback.
- **FastAPI Webhook**: Asynchronous background pipeline execution (`POST /webhook/analyze`) for instant form submission responses.

---

## Deployment Guide: GitHub to Render.com

### Step 1: Push Project to GitHub

1. Open your terminal in this project directory (`color_analysis_backend`).
2. Run the following commands:

```bash
git init
git add .
git commit -m "Initial commit - Personal Color Analysis Pro API"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/color-analysis-backend.git
git push -u origin main
```

---

### Step 2: Deploy on Render.com (Free Tier)

1. Log into your [Render.com](https://render.com) dashboard.
2. Click **New +** -> **Web Service**.
3. Connect your GitHub account and select your `color-analysis-backend` repository.
4. Render will detect the `Dockerfile` automatically (or select **Runtime: Docker**).
5. Set the **Region** (e.g. Oregon).
6. Under **Environment Variables**, add:
   - `SMTP_USER`: Your Gmail / SMTP email address (e.g. `yourname@gmail.com`)
   - `SMTP_PASS`: Your Gmail App Password (generated from Google Account Security -> App Passwords)
   - `ALLOWED_ORIGIN`: Your WordPress domain (e.g. `https://color-analysis.shop` or `*`)
7. Click **Create Web Service**.

Once deployed, Render will provide a live URL such as:
`https://color-analysis-backend.onrender.com`

---

## WordPress Integration Guide

### Option A: WPForms Integration

1. Copy the code from `wordpress_integration.php`.
2. Update line 10 with your live Render URL:
   ```php
   define('COLOR_ANALYSIS_API_URL', 'https://color-analysis-backend.onrender.com/webhook/analyze');
   ```
3. Paste the contents into your theme's `functions.php` file or use the **Code Snippets** plugin in WordPress.

### Option B: Built-in Shortcode `[color_analysis_form]`

Simply place the shortcode `[color_analysis_form]` on any page, post, or Elementor widget in your WordPress site! It renders a responsive, high-converting upload form that sends data directly to your Render backend.

---

## Local Development & Testing

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run local test pipeline:
   ```bash
   python test_pipeline.py
   ```
3. Launch FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
4. Access interactive API docs at `http://127.0.0.1:8000/docs`.
