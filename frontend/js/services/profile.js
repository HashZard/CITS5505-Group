document.addEventListener("DOMContentLoaded", async () => {
    await loadUserProfile();
    await loadMessages();
    initMessagesSidebar();
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

async function loadMessages() {
    const messagesContainer = document.getElementById('messagesContainer');
    const messageBtn = document.getElementById('messageBtn');
    if (!messagesContainer) {
        console.error('Messages container not found');
        return;
    }

    try {
        // This should call the backend API to get the message list
        // Using mock data for now
        const mockMessages = [
            {
                id: 1,
                sender: 'alice.smith@student.uwa.edu.au',
                content: 'Hi! I saw your experience sharing in the CITS5505 course review. I have some questions about project development. How did your team handle requirement changes?',
                timestamp: '2024-03-15T14:30:00Z',
                isRead: false
            },
            {
                id: 2,
                sender: 'prof.david@uwa.edu.au',
                content: 'Thank you for your course feedback. We are adjusting the course content based on student suggestions, and your input is valuable. If you have any specific suggestions, feel free to continue the discussion.',
                timestamp: '2024-03-14T09:15:00Z',
                isRead: true
            },
            {
                id: 3,
                sender: 'john.doe@student.uwa.edu.au',
                content: 'Hey! I noticed you\'re also taking CITS5502. Would you like to team up for the final project? I\'m familiar with frontend development and looking for a backend developer.',
                timestamp: '2024-03-13T16:45:00Z',
                isRead: false
            },
            {
                id: 4,
                sender: 'study.group@uwa.edu.au',
                content: 'Reminder: CITS5505 study group discussion this Saturday at 2 PM in Library 3rd floor. Topic: "Software Testing Strategies". All are welcome!',
                timestamp: '2024-03-12T11:20:00Z',
                isRead: true
            },
            {
                id: 5,
                sender: 'course.admin@uwa.edu.au',
                content: 'Your course review has been approved by the administrator. Thank you for your detailed feedback, it\'s very helpful for other students.',
                timestamp: '2024-03-11T10:05:00Z',
                isRead: true
            },
            {
                id: 6,
                sender: 'sarah.wilson@student.uwa.edu.au',
                content: 'Hi! I saw your course notes, they\'re very detailed. May I reference your project report? I\'ll make sure to cite the source.',
                timestamp: '2024-03-10T15:30:00Z',
                isRead: false
            }
        ];

        // Update unread indicator
        const hasUnreadMessages = mockMessages.some(message => !message.isRead);
        const unreadDot = messageBtn.querySelector('.bg-red-500');
        if (unreadDot) {
            unreadDot.style.display = hasUnreadMessages ? 'block' : 'none';
        }

        // Clear existing content
        messagesContainer.innerHTML = '';
        
        // Add messages
        mockMessages.forEach(message => {
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
                    const hasRemainingUnread = mockMessages.some(m => !m.isRead);
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
        if (mockMessages.length === 0) {
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
