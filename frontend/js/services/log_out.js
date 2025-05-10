/**
 * Logout functionality for the user profile page
 */

export function initLogoutFeature() {
    const logoutBtn = document.getElementById('logoutBtn');
    const logoutModal = document.getElementById('logoutModal');
    const cancelLogout = document.getElementById('cancelLogout');
    const confirmLogout = document.getElementById('confirmLogout');
    
    // Check if elements exist
    if (!logoutBtn || !logoutModal || !cancelLogout || !confirmLogout) {
        console.error('Required DOM elements for logout functionality not found');
        return;
    }
    
    // Show logout confirmation modal
    logoutBtn.addEventListener('click', function() {
        logoutModal.classList.remove('hidden');
    });
    
    // Hide modal on cancel
    cancelLogout.addEventListener('click', function() {
        logoutModal.classList.add('hidden');
    });
    
    // Also hide modal when clicking outside
    logoutModal.addEventListener('click', function(e) {
        if (e.target === logoutModal) {
            logoutModal.classList.add('hidden');
        }
    });
    
    // Handle logout confirmation
    confirmLogout.addEventListener('click', function() {
        // Clear any auth tokens from localStorage
        localStorage.removeItem('authToken');
        localStorage.removeItem('userInfo');
        
        // Show success message
        alert('You have been successfully logged out');
        
        // Redirect to home or login page
        window.location.href = '/';
    });
} 