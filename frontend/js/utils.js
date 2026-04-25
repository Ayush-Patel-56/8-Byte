// ─────────────────────────────────────────────────────────────────────────────
// Re-export API_BASE from config so all other modules import from utils.js
// (no circular deps — config.js has no imports)
// ─────────────────────────────────────────────────────────────────────────────
export { API_BASE } from './config.js';

// GLOBAL UTILITY: LOADING STATE MANAGEMENT
export function setButtonLoading(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        button.dataset.originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Loading...';
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText || button.innerHTML;
    }
}

// GLOBAL UTILITY: TOAST NOTIFICATIONS
export function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 px-6 py-4 rounded-xl shadow-2xl z-50 transform transition-all duration-300 ease-out glass-card border ${type === 'success'
        ? 'border-green-500/30 bg-green-500/10'
        : type === 'error'
            ? 'border-red-500/30 bg-red-500/10'
            : 'border-blue-500/30 bg-blue-500/10'
        }`;

    const icon = type === 'success'
        ? '<i class="fas fa-check-circle text-green-400"></i>'
        : type === 'error'
            ? '<i class="fas fa-exclamation-circle text-red-400"></i>'
            : '<i class="fas fa-info-circle text-blue-400"></i>';

    toast.innerHTML = `
        <div class="flex items-center gap-3">
            ${icon}
            <span class="text-white font-medium">${message}</span>
        </div>
    `;

    // Initial state for animation
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';

    document.body.appendChild(toast);

    // Trigger animation
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    }, 10);

    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// GLOBAL UTILITY: LOGOUT
export const logout = () => {
    localStorage.clear();
    window.location.href = '/index.html';
};

// GLOBAL UTILITY: AUTHENTICATED FETCH
// Automatically prepends API_BASE to relative URLs (e.g. '/api/profile/' → full Azure URL)
export async function authFetch(url, options = {}) {
    // Resolve relative API paths to absolute Azure backend URL
    if (url.startsWith('/')) {
        url = API_BASE + url;
    }

    let token = localStorage.getItem('access');
    if (!token) {
        logout();
        return Promise.reject("No token");
    }

    // Inject Header
    options.headers = options.headers || {};
    if (!options.headers['Authorization']) {
        options.headers['Authorization'] = `Bearer ${token}`;
    }

    let response = await fetch(url, options);

    // Handle 401 (Unauthorized/Expired)
    if (response.status === 401) {
        console.warn("Access token expired. Refreshing...");
        const refresh = localStorage.getItem('refresh');

        if (!refresh) {
            logout();
            return response;
        }

        try {
            const refreshRes = await fetch(`${API_BASE}/api/token/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh })
            });

            if (refreshRes.ok) {
                const data = await refreshRes.json();
                localStorage.setItem('access', data.access);

                // Retry original request with NEW token
                options.headers['Authorization'] = `Bearer ${data.access}`;
                response = await fetch(url, options);
            } else {
                console.error("Session expired completely.");
                logout();
            }
        } catch (err) {
            console.error("Refresh failed:", err);
            logout();
        }
    }
    return response;
}
