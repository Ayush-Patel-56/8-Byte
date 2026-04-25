import { initAnimations } from './js/animations.js';
import { initAuth } from './js/signup_signin.js';
import { initDashboard } from './js/dashboard.js';
import { initPublicProfile } from './js/public_profile.js';
import { initCommunity } from './js/community.js';
import { initDirectMessages } from './js/direct_messages.js';

console.log("Main script loaded");

// 1. Initialize Animations (Global - runs on all pages)
initAnimations();

const path = window.location.pathname;

// 2. Initialize Auth (Landing Page Only)
if (path === '/' || path === '/index.html' || path.endsWith('/index.html')) {
    console.log("Initializing auth (Landing Page)...");
    initAuth();
}

// 3. Initialize Dashboard
if (path.endsWith('/dashboard.html') || path.includes('/dashboard/')) {
    console.log("Initializing dashboard...");
    initDashboard();
}

// 4. Initialize Public Profile
if (path.endsWith('/public_profile.html') || path.includes('/u/')) {
    console.log("Initializing Public Profile...");
    initPublicProfile();
}

// 5. Initialize Community
if (path.endsWith('/community.html') || path.includes('/community/')) {
    initCommunity();
}

// 6. Initialize Direct Messages (1:1)
if (path.endsWith('/direct_messages.html') || path.includes('/messages/')) {
    initDirectMessages();
}
