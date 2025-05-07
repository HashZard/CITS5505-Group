document.addEventListener("DOMContentLoaded", async () => {
    await loadUserProfile();
});

async function loadUserProfile() {
    try {
        const response = await fetch("/api/user/profile");
        const result = await response.json();

        if (!result.success) {
            alert("Failed to load profile.");
            return;
        }

        const user = result.user;
        document.querySelector(".custom-heading").textContent = user.nickname || user.email;
        document.querySelector(".typography-default").textContent = "Student ID: " + (user.student_id || "N/A");
        document.querySelectorAll(".typography-default")[1].textContent = user.email;
        document.querySelectorAll(".typography-default")[2].textContent = user.field || "N/A";

        const favCoursesContainer = document.querySelector(".grid.grid-cols-1");
        favCoursesContainer.innerHTML = "";

        user.favourite_courses.forEach(course => {
            const div = document.createElement("div");
            div.className = "card card-hover hover-scale";
            div.innerHTML = `
                <img src="/assets/images/course-placeholder.jpg" alt="Course Image" class="w-full h-48 object-cover">
                <div class="p-4">
                    <h3 class="middle-heading">${course.name}</h3>
                    <div class="flex items-center mb-2">
                        <div class="flex items-center text-yellow-400">
                            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                            </svg>
                            <span class="ml-1">${course.avg_rating || "N/A"}</span>
                        </div>
                        <span class="typography-default px-4">(${course.review_count || 0} reviews)</span>
                    </div>
                    <a class="custom-small-btn w-full block text-center"  href="/pages/service/course_details_page.html?code=${course.code}">
                        View Details
                    </a>
                </div>
            `;
            favCoursesContainer.appendChild(div);
        });
    } catch (error) {
        console.error("Error loading profile:", error);
        alert("Error loading profile.");
    }
}
