export function initLogoutFeature() {
    const logoutBtn = document.getElementById('logoutBtn');
    const logoutModal = document.getElementById('logoutModal');
    const cancelLogout = document.getElementById('cancelLogout');
    const confirmLogout = document.getElementById('confirmLogout');

    if (!logoutBtn || !logoutModal || !cancelLogout || !confirmLogout) {
        console.error('Required DOM elements for logout functionality not found');
        return;
    }

    logoutBtn.addEventListener('click', () => {
        logoutModal.classList.remove('hidden');
    });

    cancelLogout.addEventListener('click', () => {
        logoutModal.classList.add('hidden');
    });

    logoutModal.addEventListener('click', (e) => {
        if (e.target === logoutModal) {
            logoutModal.classList.add('hidden');
        }
    });

    confirmLogout.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/logout', {
                method: 'POST',
                credentials: 'include'
            });
            const data = await res.json();
            if (!data.success) throw new Error("Logout failed");

            // 清除 cookie（保险起见）
            const cookies = document.cookie.split("; ");
            for (const cookie of cookies) {
                const eqPos = cookie.indexOf("=");
                const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
                document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            }

            window.location.href = "/pages/auth/login.html";

        } catch (err) {
            alert("Logout failed. Please try again.");
            console.error("Logout error:", err);
        }
    });
}
