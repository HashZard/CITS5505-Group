// index.js

document.addEventListener("DOMContentLoaded", () => {
    setupEmailTooltip();
    fetchLatestCourses();
    fetchTopRankedCourses();
});

function setupEmailTooltip() {
    const btn = document.getElementById("joinNowBtn");
    const tooltip = document.getElementById("emailTooltip");

    if (!btn || !tooltip) return;

    btn.addEventListener("click", () => {
        tooltip.classList.remove("hidden");

        // 自动隐藏 tooltip（例如 2 秒后）
        setTimeout(() => {
            tooltip.classList.add("hidden");
        }, 2000);
    });
}

async function fetchLatestCourses() {
    try {
        const response = await fetch("/api/courses/latest?sort=limit=3");
        const data = await response.json();

        if (data.success && Array.isArray(data.courses)) {
            renderCourses(data.courses);
        } else {
            console.error("Invalid data format from server:", data);
        }
    } catch (error) {
        console.error("Failed to fetch featured courses:", error);
    }
}

function renderCourses(courses) {
    const container = document.getElementById("featuredCourses");
    if (!container) return;

    container.innerHTML = "";

    courses.forEach(course => {
        const isPending = course.status === "PENDING";


        const card = document.createElement("div");
        card.className = "course-card glass-card h-[400px] flex flex-col border border-gray-200 rounded-2xl hover:border-primary-blue hover:shadow-lg transition-all duration-300";
        card.innerHTML = `
            <div class="overflow-hidden rounded-t-2xl">
                <img src="/assets/images/course-placeholder.jpg" alt="${course.name}" class="w-full h-48 object-cover">
            </div>
            <div class="course-card-content flex-1 flex flex-col p-4">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="middle-heading line-clamp-2">${course.name}</h3>
                    <span class="tag ml-2 flex-shrink-0">${course.status || "New"}</span>
                </div>
                <p class="text-gray-700 text-sm line-clamp-2 mb-4">${course.description}</p>
                ${isPending ? `
                    <div class="flex items-center mb-4 text-gray-600 text-sm">
                        <span>👍 ${course.agree_votes ?? 0}</span>
                        <span class="mx-2">|</span>
                        <span>👎 ${course.disagree_votes ?? 0}</span>
                    </div>
                ` : ''}
                <a class="custom-small-btn btn-full-width hover-up mt-auto"
                   href="/pages/service/course_details_page.html?code=${encodeURIComponent(course.code)}">
                    View Details
                </a>
            </div>
        `;
        container.appendChild(card);
    });
}

async function fetchTopRankedCourses() {
    try {
        const response = await fetch("/api/courses/top-rated");
        const data = await response.json();

        if (data.success && Array.isArray(data.courses)) {
            renderTopCourses(data.courses);
        } else {
            console.error("Invalid top-rated courses response:", data);
        }
    } catch (err) {
        console.error("Failed to fetch top-rated courses:", err);
    }
}

function renderTopCourses(courses) {
    const container = document.getElementById("rankingList");
    container.innerHTML = "";

    courses.forEach((course, index) => {
        const li = document.createElement("li");
        li.className = "flex items-center justify-between hover-up py-4 px-6";

        const rating = parseFloat(course.avg_rating).toFixed(1);
        const stars = renderStars(rating);

        li.innerHTML = `
            <div class="flex items-center">
                <span class="text-lg font-bold text-primary-blue mr-3">${index + 1}</span>
                <div>
                    <a href="/pages/service/course_details_page.html?code=${encodeURIComponent(course.code)}"
                       class="middle-heading hover:text-primary-blue transition-all duration-300 ease-in-out hover:scale-105 inline-block">
                        ${course.name}
                    </a>
                    <div class="flex items-center mt-1">
                        <div class="flex text-yellow-400">${stars}</div>
                        <span class="ml-2 text-sm text-gray-600">(${rating})</span>
                    </div>
                </div>
            </div>
            <div class="flex items-center gap-4">
                <span class="text-gray-600">Votes: ${course.rating_count}</span>
            </div>
        `;
        container.appendChild(li);
    });
}

function renderStars(rating) {
    const fullStars = Math.round(rating); // round to nearest int
    return Array.from({length: 5}, (_, i) => `
        <svg class="w-4 h-4" fill="${i < fullStars ? 'currentColor' : 'none'}" stroke="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81
            l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0
            l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57
            -.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
    `).join('');
}
