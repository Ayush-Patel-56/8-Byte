// ─────────────────────────────────────────────────────────────────────────────
// Frontend Configuration
// ─────────────────────────────────────────────────────────────────────────────
// Vanilla JS cannot read .env files directly.
// Edit the values below for local development.
// For Vercel production, these are set in the Vercel Dashboard under
// Project → Settings → Environment Variables.
// ─────────────────────────────────────────────────────────────────────────────

// 🔧 Dynamic Backend URL Logic
export const API_BASE = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:8000'
    : 'https://8-byte-backend-f0bre8awcafxetgv.canadacentral-01.azurewebsites.net';

// Google OAuth Client ID (public — safe to expose)
export const GOOGLE_CLIENT_ID = '636039070454-73758bnvf06inavu947k86m1ibsh330j.apps.googleusercontent.com';

// Note: AGORA_APP_ID is NOT needed here.
// The backend returns it as part of the /api/call/token/<id>/ response.
// The AGORA_APP_CERTIFICATE stays on the backend ONLY (never expose it).
