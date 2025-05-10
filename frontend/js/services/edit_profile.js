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
    editProfileBtn.addEventListener('click', function() {
        editProfileModal.classList.remove('hidden');
    });
    
    // Hide modal when clicking close button
    closeEditBtn.addEventListener('click', function() {
        editProfileModal.classList.add('hidden');
    });
    
    // Hide modal when clicking cancel button
    cancelEditBtn.addEventListener('click', function() {
        editProfileModal.classList.add('hidden');
    });
    
    // Hide modal when clicking outside
    editProfileModal.addEventListener('click', function(e) {
        if (e.target === editProfileModal) {
            editProfileModal.classList.add('hidden');
        }
    });
    
    // Handle form submission
    editProfileForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form values
        const newName = document.getElementById('nameInput').value;
        const newDepartment = document.getElementById('departmentInput').value;
        
        // Validate inputs
        if (!newName.trim() || !newDepartment.trim()) {
            alert('Please fill in all fields');
            return;
        }
        
        // Update profile display
        document.getElementById('userName').textContent = newName;
        document.getElementById('userDepartment').textContent = newDepartment;
        
        // Show success message
        const successToast = document.getElementById('successToast');
        // Remove hidden class and set opacity to 100% immediately
        successToast.classList.remove('hidden');
        successToast.style.opacity = '1';
        
        // Hide success message after 3 seconds
        setTimeout(() => {
            // Hide immediately
            successToast.classList.add('hidden');
            successToast.style.opacity = '0';
        }, 3000);
        
        // In a real application, you would send an API request here
        // to update the user's profile on the server
        console.log('Profile updated:', {
            name: newName,
            department: newDepartment
        });
        
        // Close the modal
        editProfileModal.classList.add('hidden');
    });
} 