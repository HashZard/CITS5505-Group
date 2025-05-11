/**
 * Edit profile functionality for the user profile page
 */

export function initEditProfileFeature() {
    const editProfileBtn = document.getElementById('editProfileBtn');
    const editProfileModal = document.getElementById('editProfileModal');
    const closeEditBtn = document.getElementById('closeEditBtn');
    const cancelEditBtn = document.getElementById('cancelEditBtn');
    const editProfileForm = document.getElementById('editProfileForm');

    // Check if elements exist
    if (!editProfileBtn || !editProfileModal || !closeEditBtn ||
        !cancelEditBtn || !editProfileForm) {
        console.error('Required DOM elements for edit profile functionality not found');
        return;
    }

    // Current values - get from profile display
    const currentName = document.getElementById('userName').textContent;
    const currentDepartment = document.getElementById('userDepartment').textContent;

    // Set initial form values
    document.getElementById('nameInput').value = currentName;
    document.getElementById('departmentInput').value = currentDepartment;

    // Show edit profile modal
    editProfileBtn.addEventListener('click', function () {
        editProfileModal.classList.remove('hidden');
    });

    // Hide modal when clicking close button
    closeEditBtn.addEventListener('click', function () {
        editProfileModal.classList.add('hidden');
    });

    // Hide modal when clicking cancel button
    cancelEditBtn.addEventListener('click', function () {
        editProfileModal.classList.add('hidden');
    });

    // Hide modal when clicking outside
    editProfileModal.addEventListener('click', function (e) {
        if (e.target === editProfileModal) {
            editProfileModal.classList.add('hidden');
        }
    });

    // Handle form submission
    editProfileForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const newName = document.getElementById('nameInput').value.trim();
        const newDepartment = document.getElementById('departmentInput').value.trim();

        if (!newName || !newDepartment) {
            alert('Please fill in all fields');
            return;
        }

        fetch('/api/user/profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: newName,
                department: newDepartment
            })
        })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert("Update failed: " + (data.message || "Unknown error"));
                    return;
                }

                // update UI
                document.getElementById('userName').textContent = newName;
                document.getElementById('userDepartment').textContent = newDepartment;

                // 弹出 toast
                const successToast = document.getElementById('successToast');
                successToast.classList.remove('hidden');
                successToast.style.opacity = '1';
                setTimeout(() => {
                    successToast.classList.add('hidden');
                    successToast.style.opacity = '0';
                }, 3000);

                // close modal
                editProfileModal.classList.add('hidden');
            })
            .catch(error => {
                console.error("Error updating profile:", error);
                alert("Server error while updating profile.");
            });
    });

} 