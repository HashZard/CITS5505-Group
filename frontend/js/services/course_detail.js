import {fetchWithPagination} from '/js/components/common.js';
import {renderRatingChart} from '/js/services/course_charts.js';

let currentReviewPage = 1;
const reviewsPerPage = 5;

// Private message related functionality
let currentRecipient = '';

function getCourseCodeFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("code") || "";
}

async function loadReviews(code, page = 1, perPage = 5) {
    const container = document.querySelector("#reviewSection");
    const loadMoreBtn = document.getElementById("loadMoreBtn");

    try {
        // Mock data
        const mockComments = [
            {
                username: 'alice.smith@student.uwa.edu.au',
                content: 'The course content is very practical, especially the software testing and project management sections. The professor explains clearly, and the assignments are moderately challenging. I recommend reviewing related concepts beforehand to better understand the lectures.',
                created_at: '2024-03-15T14:30:00Z',
                rating: 5
            },
            {
                username: 'john.doe@student.uwa.edu.au',
                content: 'The course projects are challenging but very rewarding. The team collaboration part taught me a lot about communication skills. I recommend choosing reliable teammates and planning project timelines in advance.',
                created_at: '2024-03-14T09:15:00Z',
                rating: 4
            },
            {
                username: 'sarah.wilson@student.uwa.edu.au',
                content: 'The final exam is quite challenging and requires comprehensive review. I recommend taking good notes and participating in discussion sessions. The professor is very approachable and willing to answer questions.',
                created_at: '2024-03-13T16:45:00Z',
                rating: 4
            },
            {
                username: 'michael.brown@student.uwa.edu.au',
                content: 'The course content is up-to-date and follows industry trends. The lab sessions are very helpful, and I recommend completing each experiment carefully. The TAs are professional and patient in answering questions.',
                created_at: '2024-03-12T11:20:00Z',
                rating: 5
            },
            {
                username: 'emma.davis@student.uwa.edu.au',
                content: 'The course workload is moderate but requires good time management. I recommend starting projects early and not leaving them until the last minute. The textbook selection is excellent with rich case studies.',
                created_at: '2024-03-11T10:05:00Z',
                rating: 4
            }
        ];

        // Simulate pagination
        const startIndex = (page - 1) * perPage;
        const endIndex = startIndex + perPage;
        const comments = mockComments.slice(startIndex, endIndex);

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
                        <div class="ml-4 flex items-center">
                            ${Array(5).fill().map((_, i) => `
                                <svg class="w-4 h-4 ${i < comment.rating ? 'text-yellow-400' : 'text-gray-300'}" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                                </svg>
                            `).join('')}
                        </div>
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

let isFavorited = false;

async function toggleFavorite() {
    const code = getCourseCodeFromURL();
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
    const code = getCourseCodeFromURL();
    const res = await fetch('/api/user/profile');
    const data = await res.json();
    const favCodes = data.user.favourite_courses.map(c => c.code);
    isFavorited = favCodes.includes(code);
    updateFavoriteButton();
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
    if (favoriteBtn) favoriteBtn.addEventListener("click", toggleFavorite);

    await checkFavoriteStatus();  // 页面加载时检测当前课程是否已收藏
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
