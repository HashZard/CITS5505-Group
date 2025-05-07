import {fetchWithPagination} from '/js/components/common.js';
import {renderRatingChart} from '/js/services/course_charts.js';

let currentReviewPage = 1;
const reviewsPerPage = 5;

function getCourseCodeFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("code") || "";
}

async function loadReviews(code, page = 1, perPage = 5) {
    const container = document.querySelector("#reviewSection");
    const loadMoreBtn = document.getElementById("loadMoreBtn");

    try {
        const res = await fetch(`/api/courses/${code}/comments?page=${page}&per_page=${perPage}`);
        const result = await res.json();

        if (!result.success || !result.data) {
            alert("Failed to load comments");
            return;
        }

        const comments = result.data.data;
        if (comments.length === 0 && page === 1) {
            container.innerHTML = "<p class='text-gray-500'>No reviews yet.</p>";
            loadMoreBtn.style.display = "none";
            return;
        }

        comments.forEach(comment => {
            const div = document.createElement("div");
            div.className = "custom-box-dashed";
            div.innerHTML = `
                <div class="flex items-center mb-4 border-b border-gray-200 pb-4">
                    <span class="text-gray-600">${comment.username}</span>
                    <span class="mx-4">•</span>
                    <span class="text-gray-600">${new Date(comment.created_at).toLocaleDateString()}</span>
                </div>
                <p class="typography-default leading-relaxed">${comment.content}</p>
            `;
            container.appendChild(div);
        });

        if (comments.length < perPage) {
            loadMoreBtn.style.display = "none";
        } else {
            loadMoreBtn.style.display = "block";
        }
    } catch (err) {
        console.error("Error loading comments:", err);
        alert("Error loading comments.");
    }
}

async function loadCourseDetails() {
    const code = getCourseCodeFromURL();
    if (!code) {
        alert('No course code provided.');
        return;
    }

    try {
        const response = await fetch(`/api/courses/detail?code=${encodeURIComponent(code)}`);
        const result = await response.json();

        if (result.success) {
            const course = result.data;
            document.querySelector('h1.custom-heading').textContent = course.name;
            document.querySelector('p.middle-heading').textContent = course.code;
            document.querySelector('p.typography-default').textContent = course.description || 'No description available.';
            document.body.dataset.courseId = course.id;
        } else {
            alert(result.message || 'Failed to load course details');
        }
    } catch (error) {
        console.error(error);
        alert('Error loading course details.');
    }
}

async function submitRating() {
    const input = document.getElementById("ratingInput");
    const rating = parseInt(input.value.trim());
    if (isNaN(rating) || rating < 1 || rating > 5) {
        alert("Please enter a valid rating from 1 to 5.");
        return;
    }

    try {
        const courseCode = getCourseCodeFromURL();
        const response = await fetch(`/api/courses/${courseCode}/rate`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({rating})
        });

        const result = await response.json();
        if (result.success) {
            alert("Rating submitted!");
            input.disabled = true;
            document.getElementById("submitRatingBtn").disabled = true;
        } else {
            alert("Failed to submit rating: " + result.message);
        }
    } catch (err) {
        console.error(err);
        alert("Error while submitting rating.");
    }
}

async function submitComment() {
    const textarea = document.getElementById("reviewContent");
    const content = textarea.value.trim();
    if (!content) {
        alert("Please write something before submitting your comment.");
        return;
    }

    try {
        const courseCode = getCourseCodeFromURL();
        const response = await fetch(`/api/courses/${courseCode}/comment`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({content})
        });

        const result = await response.json();
        if (result.success) {
            alert("Your comment was submitted!");
            textarea.value = "";
            currentReviewPage = 1;
            document.querySelector("#reviewSection").innerHTML = "";
            await loadReviews(courseCode, currentReviewPage, reviewsPerPage);
        } else {
            alert("Failed to submit comment: " + result.message);
        }
    } catch (err) {
        console.error(err);
        alert("Error while submitting comment.");
    }
}

async function addToFavorites() {
    const code = getCourseCodeFromURL();
    try {
        const res = await fetch(`/api/courses/${code}/favorite`, {method: "POST"});
        const result = await res.json();
        if (result.success) {
            alert("Added to favorites!");
        } else {
            alert(result.message || "Failed to add to favorites");
        }
    } catch (err) {
        console.error("Error adding to favorites:", err);
        alert("Network error");
    }
}


async function loadRatingChart() {
    const code = getCourseCodeFromURL();
    const ctx = document.getElementById("ratingChart")?.getContext("2d");
    if (!ctx || !code) return;

    try {
        const res = await fetch(`/api/courses/${code}/ratings/distribution`);
        const result = await res.json();
        if (result.success) {
            renderRatingChart(ctx, result.data);
        } else {
            console.error("Failed to load chart data:", result.message);
        }
    } catch (err) {
        console.error("Error fetching rating data:", err);
    }
}

export async function initCourseDetailPage() {
    await loadCourseDetails();

    const ratingBtn = document.getElementById("submitRatingBtn");
    const commentBtn = document.getElementById("submitReviewBtn");
    const loadMoreBtn = document.getElementById("loadMoreBtn");
    const favoriteBtn = document.getElementById("favoriteBtn");

    const courseCode = getCourseCodeFromURL();

    if (ratingBtn) ratingBtn.addEventListener("click", submitRating);
    if (commentBtn) commentBtn.addEventListener("click", submitComment);
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener("click", async () => {
            currentReviewPage++;
            await loadReviews(courseCode, currentReviewPage, reviewsPerPage);
        });
    }
    if (favoriteBtn) favoriteBtn.addEventListener("click", addToFavorites);


    await loadReviews(courseCode, currentReviewPage, reviewsPerPage);
    await loadRatingChart();
}
