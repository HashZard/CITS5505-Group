(async () => {
    await loadUserProfile();
    await loadMessages();
    initMessagesSidebar();
    initEditProfileFeature();
})();

async function loadUserProfile() {
    try {
        const response = await fetch("/api/user/profile");
        const result = await response.json();

        if (!result.success) {
            alert("Failed to load profile.");
            return;
        }

        const user = result.user;
        document.getElementById("userName").textContent = user.name || user.email;
        document.getElementById("studentId").textContent = "Student ID: " + (user.student_id || "N/A");
        document.getElementById("userEmail").textContent = user.email;
        document.getElementById("userDepartment").textContent = user.department || "N/A";

        const favCoursesContainer = document.getElementById("favCoursesContainer");
        favCoursesContainer.innerHTML = "";

        if (user.favourite_courses.length === 0) {
            favCoursesContainer.innerHTML = '<p class="text-gray-500 col-span-3 text-center">No favorite courses yet.</p>';
            return;
        }

        user.favourite_courses.forEach(course => {
            const div = document.createElement("div");
            div.className = "course-card glass-card h-[400px] flex flex-col border border-gray-200 rounded-2xl hover:border-primary-blue hover:shadow-lg transition-all duration-300";
            div.innerHTML = `
                <div class="overflow-hidden rounded-t-2xl">
                    <img src="/assets/images/course-placeholder.jpg" alt="${course.name}" class="w-full h-48 object-cover">
                </div>
                <div class="course-card-content flex-1 flex flex-col p-4">
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="middle-heading line-clamp-2">${course.name}</h3>
                    </div>
                    <div class="flex items-center mb-4 rating-stars">
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                        </svg>
                        <span class="ml-1">${course.avg_rating || "N/A"}</span>
                        <span class="typography-default px-2 text-gray-600">(${course.review_count || 0} reviews)</span>
                    </div>
                    <a class="custom-small-btn btn-full-width hover-up mt-auto"
                       href="/pages/service/course_details_page.html?code=${course.code}">
                        View Details
                    </a>
                </div>
            `;
            favCoursesContainer.appendChild(div);
        });

        // 设置初始值给编辑表单
        document.getElementById('nameInput').value = user.name || '';
        document.getElementById('departmentInput').value = user.field || '';

    } catch (error) {
        console.error("Error loading profile:", error);
        alert("Error loading profile.");
    }
}

function initEditProfileFeature() {
    const editProfileBtn = document.getElementById('editProfileBtn');
    const editProfileModal = document.getElementById('editProfileModal');
    const closeEditBtn = document.getElementById('closeEditBtn');
    const cancelEditBtn = document.getElementById('cancelEditBtn');
    const editProfileForm = document.getElementById('editProfileForm');

    if (!editProfileBtn || !editProfileModal || !closeEditBtn || !cancelEditBtn || !editProfileForm) {
        console.error('Missing DOM elements for edit profile');
        return;
    }

    editProfileBtn.addEventListener('click', () => {
        editProfileModal.classList.remove('hidden');
    });

    closeEditBtn.addEventListener('click', () => {
        editProfileModal.classList.add('hidden');
    });

    cancelEditBtn.addEventListener('click', () => {
        editProfileModal.classList.add('hidden');
    });

    editProfileModal.addEventListener('click', (e) => {
        if (e.target === editProfileModal) {
            editProfileModal.classList.add('hidden');
        }
    });

    editProfileForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const newName = document.getElementById('nameInput').value.trim();
        const newDepartment = document.getElementById('departmentInput').value.trim();

        if (!newName || !newDepartment) {
            alert("Please fill in all fields.");
            return;
        }

        try {
            const res = await fetch('/api/user/profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: newName,
                    department: newDepartment
                })
            });

            const data = await res.json();
            if (!data.success) {
                alert("Update failed: " + (data.message || "Unknown error"));
                return;
            }

            document.getElementById("userName").textContent = newName;
            document.getElementById("userDepartment").textContent = newDepartment;

            const toast = document.getElementById("successToast");
            toast.classList.remove("hidden");
            toast.style.opacity = "1";
            setTimeout(() => {
                toast.classList.add("hidden");
                toast.style.opacity = "0";
            }, 3000);

            editProfileModal.classList.add('hidden');

        } catch (err) {
            console.error("Update error:", err);
            alert("Server error while updating profile.");
        }
    });
}

async function loadMessages() {
    const messagesContainer = document.getElementById('messagesContainer');
    const messageBtn = document.getElementById('messageBtn');
    if (!messagesContainer) {
        console.error('Messages container not found');
        return;
    }

    try {
        // This should call the backend API to get the message list
        const res = await fetch('/api/user/message/inbox');
        const result = await res.json();

        if (!result.success || !Array.isArray(result.messages)) {
            messagesContainer.innerHTML = '<p class="text-gray-500 text-center py-4">No messages</p>';
            return;
        }

        const messages = result.messages;

        // Update unread indicator
        const hasUnreadMessages = messages.some(message => !message.isRead);
        const unreadDot = messageBtn.querySelector('.bg-red-500');
        if (unreadDot) {
            unreadDot.style.display = hasUnreadMessages ? 'block' : 'none';
        }

        // Clear existing content
        messagesContainer.innerHTML = '';

        // Add messages
        messages.forEach(message => {
            const messageDiv = document.createElement('div');
            messageDiv.className = `custom-box-dashed hover:bg-gray-50 transition-colors duration-200 p-3 cursor-pointer ${!message.isRead ? 'bg-blue-50' : ''}`;
            messageDiv.innerHTML = `
                <div class="flex flex-col mb-2">
                    <div class="flex items-center justify-between">
                        <span class="text-gray-600 font-medium truncate">${message.sender}</span>
                        ${!message.isRead ? '<span class="w-2 h-2 bg-blue-500 rounded-full"></span>' : ''}
                    </div>
                    <span class="text-gray-500 text-sm">${new Date(message.timestamp).toLocaleDateString()}</span>
                </div>
                <div class="message-content hidden">
                    <p class="typography-default text-sm text-gray-600 mb-3">${message.content}</p>
                    <div class="reply-section hidden">
                        <textarea class="w-full p-2 border border-gray-300 rounded-lg text-sm mb-2" placeholder="Enter your reply..."></textarea>
                        <div class="flex justify-end gap-2">
                            <button class="custom-small-btn cancel-reply">Cancel</button>
                            <button class="custom-small-btn send-reply">Send</button>
                        </div>
                    </div>
                    <button class="text-blue-500 text-sm hover:text-blue-600 reply-btn">Reply</button>
                </div>
            `;

            // Add click event
            messageDiv.addEventListener('click', (e) => {
                // If clicking reply button or reply area, don't trigger message expansion
                if (e.target.closest('.reply-section') || e.target.closest('.reply-btn')) {
                    return;
                }

                const contentDiv = messageDiv.querySelector('.message-content');
                contentDiv.classList.toggle('hidden');

                // Mark as read
                if (!message.isRead) {
                    message.isRead = true;
                    messageDiv.classList.remove('bg-blue-50');
                    const unreadDot = messageDiv.querySelector('.bg-blue-500');
                    if (unreadDot) {
                        unreadDot.remove();
                    }

                    // Update button unread indicator
                    const hasRemainingUnread = messages.some(m => !m.isRead);
                    const buttonUnreadDot = messageBtn.querySelector('.bg-red-500');
                    if (buttonUnreadDot) {
                        buttonUnreadDot.style.display = hasRemainingUnread ? 'block' : 'none';
                    }
                }
            });

            // Add reply button events
            const replyBtn = messageDiv.querySelector('.reply-btn');
            const replySection = messageDiv.querySelector('.reply-section');
            const cancelBtn = messageDiv.querySelector('.cancel-reply');
            const sendBtn = messageDiv.querySelector('.send-reply');

            replyBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                replySection.classList.remove('hidden');
                replyBtn.classList.add('hidden');
            });

            cancelBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                replySection.classList.add('hidden');
                replyBtn.classList.remove('hidden');
            });

            sendBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                const replyContent = messageDiv.querySelector('textarea').value;
                if (replyContent.trim()) {
                    // This should call the backend API to send the reply
                    console.log('Sending reply:', replyContent);
                    // Clear input and hide reply section
                    messageDiv.querySelector('textarea').value = '';
                    replySection.classList.add('hidden');
                    replyBtn.classList.remove('hidden');
                }
            });

            messagesContainer.appendChild(messageDiv);
        });

        // If no messages, show prompt
        if (messages.length === 0) {
            messagesContainer.innerHTML = '<p class="text-gray-500 text-center py-4">No messages</p>';
        }
    } catch (error) {
        console.error('Error loading messages:', error);
        messagesContainer.innerHTML = '<p class="text-gray-500 text-center py-4">Failed to load messages. Please try again later.</p>';
    }
}

// Initialize private message sidebar functionality
function initMessagesSidebar() {
    const messageBtn = document.getElementById('messageBtn');
    const messageContainer = document.getElementById('messageContainer');
    const closeMessageBtn = document.getElementById('closeMessageBtn');

    if (messageBtn && messageContainer && closeMessageBtn) {
        // Open message panel
        messageBtn.addEventListener('click', () => {
            messageContainer.classList.remove('hidden');
            // Add animation effect
            const messagePanel = messageContainer.querySelector('div');
            messagePanel.style.transform = 'translateY(0)';
            messagePanel.style.opacity = '1';
        });

        // Close message panel
        const closePanel = () => {
            const messagePanel = messageContainer.querySelector('div');
            messagePanel.style.transform = 'translateY(20px)';
            messagePanel.style.opacity = '0';
            setTimeout(() => {
                messageContainer.classList.add('hidden');
            }, 300);
        };

        closeMessageBtn.addEventListener('click', closePanel);

        // Close panel when clicking background
        messageContainer.addEventListener('click', (e) => {
            if (e.target === messageContainer) {
                closePanel();
            }
        });
    }
}
