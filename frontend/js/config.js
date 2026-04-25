// ─────────────────────────────────────────────────────────────────────────────
// Frontend Configuration
// ─────────────────────────────────────────────────────────────────────────────
// Vanilla JS cannot read .env files directly.
// Edit the values below for local development.
// For Vercel production, these are set in the Vercel Dashboard under
// Project → Settings → Environment Variables.
// ─────────────────────────────────────────────────────────────────────────────

// 🔧 Change this to your real Azure backend URL before deploying
// Local dev:  'http://127.0.0.1:8000'
// Production: 'https://django-user-auth.azurewebsites.net'
export const API_BASE = 'http://127.0.0.1:8000';

// Google OAuth Client ID (public — safe to expose)
export const GOOGLE_CLIENT_ID = '636039070454-73758bnvf06inavu947k86m1ibsh330j.apps.googleusercontent.com';

// Note: AGORA_APP_ID is NOT needed here.
// The backend returns it as part of the /api/call/token/<id>/ response.
// The AGORA_APP_CERTIFICATE stays on the backend ONLY (never expose it).
