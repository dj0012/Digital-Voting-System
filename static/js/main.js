// Toast Notification Helper
function showToast(message, type = 'info', duration = 4000) {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    // Choose appropriate emoji/icon based on type
    let icon = '🔔';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '❌';
    
    toast.innerHTML = `
        <span style="margin-right: 10px;">${icon} ${message}</span>
        <span class="close-toast" style="cursor: pointer; opacity: 0.6; font-weight: bold; margin-left: 15px;">&times;</span>
    `;
    
    container.appendChild(toast);
    
    // Handle close button click
    toast.querySelector('.close-toast').addEventListener('click', () => {
        toast.style.transform = 'translateX(120%)';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 350);
    });
    
    // Auto-remove toast
    setTimeout(() => {
        if (toast.parentNode) {
            toast.style.transform = 'translateX(120%)';
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 350);
        }
    }, duration);
}

// Global loader overlays
function showLoader(text = 'Processing...') {
    let overlay = document.getElementById('loaderOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loaderOverlay';
        overlay.className = 'loader-overlay';
        overlay.innerHTML = `
            <div class="spinner"></div>
            <p style="color: var(--text-muted); font-size: 14px; font-weight: 500;">${text}</p>
        `;
        // Insert at the form level or container level
        const container = document.querySelector('.glass-container') || document.body;
        container.appendChild(overlay);
    } else {
        overlay.querySelector('p').textContent = text;
        overlay.style.display = 'block';
    }
}

function hideLoader() {
    const overlay = document.getElementById('loaderOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}
