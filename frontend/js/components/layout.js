document.addEventListener('DOMContentLoaded', () => {
    fetch('/components/header.html')
        .then(res => res.text())
        .then(html => {
            document.getElementById('header').innerHTML = html;
            // Re-bind the logo click event after header is loaded
            if(document.getElementById('logoImage')){
                document.getElementById('logoImage').addEventListener('click', function() {
                    window.location.href = '/index.html';
                });
            }
            // Bind search input and button events after header is loaded
            function jumpToSearchResult(inputId) {
                const input = document.getElementById(inputId);
                const keyword = input ? input.value.trim() : '';
                window.location.href = `/pages/service/course_search_result.html?keyword=${encodeURIComponent(keyword)}`;
            }
            // Desktop
            if(document.getElementById('header-search-input')){
                document.getElementById('header-search-input').addEventListener('keydown', function(e) {
                    if (e.key === 'Enter') {
                        jumpToSearchResult('header-search-input');
                    }
                });
            }
            if(document.getElementById('header-search-btn')) {
                document.getElementById('header-search-btn').addEventListener('click', function() {
                    jumpToSearchResult('header-search-input');
                });
            }
            // Mobile
            if(document.getElementById('header-search-input-mobile')){
                document.getElementById('header-search-input-mobile').addEventListener('keydown', function(e) {
                    if (e.key === 'Enter') {
                        jumpToSearchResult('header-search-input-mobile');
                    }
                });
            }
            if(document.getElementById('header-search-btn-mobile')){
                document.getElementById('header-search-btn-mobile').addEventListener('click', function() {
                    jumpToSearchResult('header-search-input-mobile');
                });
            }
        });

    fetch('/components/footer.html')
        .then(res => res.text())
        .then(html => {
            document.getElementById('footer').innerHTML = html;
        });
});