document.addEventListener('DOMContentLoaded', async () => {
    await injectHeaderAndFooter();
    await checkLoginRedirect();
});

async function injectHeaderAndFooter() {
    try {
        // 加载 header
        const headerHTML = await fetch('/components/header.html').then(res => res.text());
        document.getElementById('header').innerHTML = headerHTML;

        // 加载 footer
        const footerHTML = await fetch('/components/footer.html').then(res => res.text());
        document.getElementById('footer').innerHTML = footerHTML;

        // 绑定 logo 跳转
        const logo = document.getElementById('logoImage');
        if (logo) {
            logo.addEventListener('click', () => {
                window.location.href = '/index.html';
            });
        }

        // 搜索绑定（桌面 + 移动）
        setupSearchEvents('header-search-input', 'header-search-btn');
        setupSearchEvents('header-search-input-mobile', 'header-search-btn-mobile');
    } catch (error) {
        console.error('Failed to load header/footer:', error);
    }
}

function setupSearchEvents(inputId, btnId) {
    const input = document.getElementById(inputId);
    const btn = document.getElementById(btnId);

    if (input) {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                jumpToSearch(inputId);
            }
        });
    }

    if (btn) {
        btn.addEventListener('click', () => {
            jumpToSearch(inputId);
        });
    }
}

function jumpToSearch(inputId) {
    const input = document.getElementById(inputId);
    const keyword = input ? input.value.trim() : '';
    if (keyword) {
        window.location.href = `/pages/service/course_search_result.html?keyword=${encodeURIComponent(keyword)}`;
    }
}

async function checkLoginRedirect() {
    const whitelist = ["/pages/auth/login.html", "/pages/auth/register.html", "/index.html"];
    const currentPath = window.location.pathname;

    const isWhitelisted = whitelist.some(path => currentPath.startsWith(path));
    if (isWhitelisted) return;

    try {
        const res = await fetch('/api/user/check_login');
        if (res.status !== 200) throw new Error("Not logged in");

        const data = await res.json();
        if (!data.logged_in) {
            redirectToLogin();
        }
        // ✅ hide login and signup buttons(if they exist)
        const loginBtn = document.getElementById("loginBtn");
        if (loginBtn) {
            loginBtn.style.visibility = "hidden";
        }
        const signupBtn = document.getElementById("signupBtn");
        if (signupBtn) {
            signupBtn.style.visibility = "hidden";
        }
        document.body.classList.remove('invisible');
        document.dispatchEvent(new CustomEvent('LayoutReady'));
    } catch (err) {
        console.warn('Login check failed or not logged in:', err);
        redirectToLogin();
    }
}

function redirectToLogin() {
    const currentUrl = window.location.pathname + window.location.search + window.location.hash;
    const loginUrl = "/pages/auth/login.html?next=" + encodeURIComponent(currentUrl);
    window.location.href = loginUrl;
}
