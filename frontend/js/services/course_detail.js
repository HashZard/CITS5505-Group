import {fetchWithPagination} from '/js/components/common.js';
import {renderRatingChart} from '/js/services/course_charts.js';

let currentReviewPage = 1;
const reviewsPerPage = 5;

// Private message related functionality
let currentRecipient = '';

function getCourseCode() {
    const params = new URLSearchParams(window.location.search);
    const codeFromUrl = params.get("code");
    if (codeFromUrl) return codeFromUrl;

    const el = document.getElementById("courseCode");
    if (el) return el.dataset.code || el.textContent.trim() || "";

    return "";
}

async function loadReviews(code, page = 1, perPage = 5) {
    const container = document.querySelector("#reviewSection");
    const loadMoreBtn = document.getElementById("loadMoreBtn");

    try {
        const res = await fetch(`/api/courses/${code}/comments?page=${page}&per_page=${perPage}`);
        const result = await res.json();

        if (!result.success || !result.data) {
            container.innerHTML = "<p class='text-gray-500'>No reviews yet.</p>";
            console.error("Failed to load comments:", result.message);
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
            div.className = "custom-box-dashed mb-4";
            div.innerHTML = `
                <div class="flex items-center mb-4 border-b border-gray-200 pb-4">
                    <div class="flex items-center">
                        <span class="text-gray-600 font-medium">${comment.username}</span>
                        <span class="mx-4">•</span>
                        <span class="text-gray-500">${new Date(comment.created_at).toLocaleDateString()}</span>
                    </div>
                    <button class="ml-auto custom-small-btn hover-up" onclick="window.openMessageModal('${comment.username}')">
                        <svg class="w-4 h-4 mr-1 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                        </svg>
                        Send Message
                    </button>
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
        alert("Failed to load reviews.");
    }
}

async function loadCourseDetails() {
    const code = getCourseCode();
    if (!code) {
        alert('No course code provided.');
        return;
    }

    try {
        const response = await fetch(`/api/courses/detail?code=${encodeURIComponent(code)}`);
        const result = await response.json();

        if (result.success) {
            const course = result.data;
            document.getElementById("courseName").textContent = course.name;
            document.getElementById("courseCode").textContent = course.code;
            document.getElementById("courseDescription").textContent = course.description || "No description available.";
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
        const courseCode = getCourseCode();
        const response = await fetch(`/api/courses/${courseCode}/rate`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({rating})
        });

        const result = await response.json();
        if (result.success) {
            alert("Rating submitted!");
            await loadRatingChart();
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
        const courseCode = getCourseCode();
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

let isFavorited = false;

async function toggleFavorite() {
    const code = getCourseCode();
    try {
        const res = await fetch(`/api/courses/${code}/favorite`, {
            method: "POST"
        });
        const result = await res.json();

        if (result.success) {
            isFavorited = result.status === "added";
            updateFavoriteButton();
        } else {
            alert(result.message || "操作失败");
        }
    } catch (err) {
        console.error("Toggle favorite error:", err);
        alert("网络错误");
    }
}

function updateFavoriteButton() {
    const favoriteBtn = document.getElementById("favoriteBtn");
    if (!favoriteBtn) return;

    if (isFavorited) {
        favoriteBtn.classList.add("bg-red-500", "text-white");
        favoriteBtn.innerHTML = `
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 
                    2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 
                    2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 
                    22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 
                    11.54L12 21.35z"/>
            </svg> Remove from Favorites`;
    } else {
        favoriteBtn.classList.remove("bg-red-500", "text-white");
        favoriteBtn.innerHTML = `
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4.318 6.318a4.5 4.5 0 000 
                    6.364L12 20.364l7.682-7.682a4.5 
                    4.5 0 00-6.364-6.364L12 
                    7.636l-1.318-1.318a4.5 4.5 0 
                    00-6.364 0z"/>
            </svg> Add to Favorites`;
    }
}

async function checkFavoriteStatus() {
    const code = getCourseCode();
    const res = await fetch('/api/user/profile');
    const data = await res.json();
    const favCodes = data.user.favourite_courses.map(c => c.code);
    isFavorited = favCodes.includes(code);
    updateFavoriteButton();
}

async function loadCourseFiles(courseCode) {
    const container = document.getElementById("materialList");
    container.innerHTML = ""; // clear previous content

    try {
        const res = await fetch(`/api/courses/${courseCode}/files`);
        const result = await res.json();

        if (!result.success || !result.files.length) {
            container.innerHTML = "<p class='text-gray-500'>No materials uploaded yet.</p>";
            return;
        }

        result.files.forEach(file => {
            const div = document.createElement("div");
            div.className = "p-3 border border-gray-200 rounded-lg shadow-sm bg-white";

            div.innerHTML = `
                <div class="grid grid-cols-4 gap-4 text-sm text-gray-600 mb-1 items-center">
                    <span class="font-semibold text-blue-700 truncate">${file.filename}</span>
                    <span class="truncate">Uploader: ${file.uploader}</span>
                    <span class="truncate">Uploaded: ${file.uploaded_at}</span>
                    <a href="/api/courses/${courseCode}/files/download/${file.filename}" download class="custom-small-btn hover-up justify-self-end whitespace-nowrap">
                        Download
                    </a>
                </div>
            
                <p class="text-sm text-gray-700 col-span-4">${file.description}</p>
            `;


            container.appendChild(div);
        });

    } catch (err) {
        console.error("Error loading course files:", err);
        container.innerHTML = "<p class='text-red-500'>Failed to load course materials.</p>";
    }
}

async function loadRatingChart() {
    const code = getCourseCode();
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

    const courseCode = getCourseCode();

    if (ratingBtn) ratingBtn.addEventListener("click", submitRating);
    if (commentBtn) commentBtn.addEventListener("click", submitComment);
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener("click", async () => {
            currentReviewPage++;
            await loadReviews(courseCode, currentReviewPage, reviewsPerPage);
        });
    }
    if (favoriteBtn) favoriteBtn.addEventListener("click", toggleFavorite);

    await checkFavoriteStatus();  // check if the course is already favorited
    await loadCourseFiles(courseCode);  // Load course files
    await loadReviews(courseCode, currentReviewPage, reviewsPerPage);
    await loadRatingChart();
}

// Private message related functionality
function openMessageModal(recipient) {
    currentRecipient = recipient;
    const modal = document.getElementById('messageModal');
    const recipientInput = document.getElementById('recipientInput');
    recipientInput.value = recipient;
    modal.classList.remove('hidden');
}

function closeMessageModal() {
    const modal = document.getElementById('messageModal');
    modal.classList.add('hidden');
    document.getElementById('messageInput').value = '';
    currentRecipient = '';
}

// Initialize private message functionality
function initMessageFeature() {
    const messageModal = document.getElementById('messageModal');
    const closeMessageBtn = document.getElementById('closeMessageBtn');
    const cancelMessageBtn = document.getElementById('cancelMessageBtn');
    const messageForm = document.getElementById('messageForm');

    if (!messageModal || !closeMessageBtn || !cancelMessageBtn || !messageForm) {
        console.error('Required DOM elements for message functionality not found');
        return;
    }

    // Close button events
    closeMessageBtn.addEventListener('click', closeMessageModal);
    cancelMessageBtn.addEventListener('click', closeMessageModal);

    // Close modal when clicking outside
    messageModal.addEventListener('click', (e) => {
        if (e.target === messageModal) {
            closeMessageModal();
        }
    });

    // Handle form submission
    messageForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const messageContent = document.getElementById('messageInput').value.trim();
        if (!messageContent) {
            alert('Please enter a message');
            return;
        }

        try {
            // This should call the backend API to send the message
            // Using mock data for now
            console.log('Sending message:', {
                recipient: currentRecipient,
                content: messageContent
            });

            alert('Message sent successfully!');
            closeMessageModal();
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Failed to send message. Please try again later.');
        }
    });
}

// Initialize private message functionality when page loads
document.addEventListener('DOMContentLoaded', () => {
    initMessageFeature();
});

// Expose openMessageModal function to window object
window.openMessageModal = function (recipient) {
    currentRecipient = recipient;
    const modal = document.getElementById('messageModal');
    const recipientInput = document.getElementById('recipientInput');
    recipientInput.value = recipient;
    modal.classList.remove('hidden');
};
