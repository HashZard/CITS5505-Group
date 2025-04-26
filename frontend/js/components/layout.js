document.addEventListener('DOMContentLoaded', () => {
    fetch('/components/header.html')
        .then(res => res.text())
        .then(html => {
            document.getElementById('header').innerHTML = html;
            // Re-bind the logo click event after header is loaded
            document.getElementById('logoImage').addEventListener('click', function() {
                window.location.href = '/index.html';
            });
        });

    fetch('/components/footer.html')
        .then(res => res.text())
        .then(html => {
            document.getElementById('footer').innerHTML = html;
        });
});