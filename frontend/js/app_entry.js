import '/js/components/layout.js';

document.addEventListener('LayoutReady', async () => {
    const path = window.location.pathname;

    if (window.location.pathname.includes('/profile.html')) {
        await import('/js/services/profile.js');
    } else if (path.startsWith('/pages/service/course_search_result.html')) {
        await import('/js/services/search.js');
    } else if (path.startsWith('/pages/service/course_details_page.html')) {
        await import('/js/services/course_details.js');
    }
    // 你可以继续加更多页面和对应逻辑模块
});
