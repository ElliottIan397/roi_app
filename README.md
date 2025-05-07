# Digitol Link Generator (Flask App)

## Purpose
This web service accepts user input (including an email and a few calculator values), merges it with a baseline, encodes the payload, and returns a working Digitol calculator URL.

## How to Deploy on Render

1. Fork this repo to your GitHub account.
2. Log in to https://render.com and click "New Web Service".
3. Connect your GitHub repo and select this project.
4. Set the **Start Command** to:
   ```
   gunicorn app:app
   ```
5. Leave the **Build Command** blank (Render will install from `requirements.txt`).
6. Click "Deploy" — your app will be live in a few minutes.

## Example POST Body

```
{
  "email": "dealer@example.com",
  "B15": 1000,
  "E46": 12000000,
  "L52": 0.65
}
```

## Response

```
{
  "url": "https://digitolservices.com/ecommerce-deployment-roi?s=..."
}
```