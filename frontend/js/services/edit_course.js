/**
 * Course editing and voting functionality
 */

export function initCourseEditingFeatures() {
    const editCourseBtn = document.getElementById('editCourseBtn');
    const editCourseModal = document.getElementById('editCourseModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const cancelEditBtn = document.getElementById('cancelEditBtn');
    const editCourseForm = document.getElementById('editCourseForm');
    const proposedChangesCard = document.getElementById('proposedChangesCard');
    const voteUpBtn = document.getElementById('voteUpBtn');
    
    if (!editCourseBtn || !editCourseModal || !closeModalBtn || !cancelEditBtn || 
        !editCourseForm || !proposedChangesCard || !voteUpBtn) {
        console.error('Required DOM elements not found for course editing features');
        return;
    }
    
    // Modal control
    editCourseBtn.addEventListener('click', () => {
        editCourseModal.classList.remove('hidden');
    });
    
    closeModalBtn.addEventListener('click', () => {
        editCourseModal.classList.add('hidden');
    });
    
    cancelEditBtn.addEventListener('click', () => {
        editCourseModal.classList.add('hidden');
    });
    
    // Form submission
    editCourseForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get values from form
        const lecturer = document.getElementById('lecturerInput').value;
        const examStructure = document.getElementById('examStructureInput').value;
        const courseDetails = document.getElementById('courseDetailsInput').value;
        
        if (!lecturer || !examStructure || !courseDetails) {
            alert('Please fill in all fields');
            return;
        }
        
        // Update proposed changes card
        document.getElementById('proposedLecturer').textContent = lecturer;
        document.getElementById('proposedExamStructure').textContent = examStructure;
        document.getElementById('proposedDetails').textContent = courseDetails;
        
        // Show the proposed changes card
        proposedChangesCard.classList.remove('hidden');
        
        // Close the modal
        editCourseModal.classList.add('hidden');
    });
    
    // Voting functionality
    initVotingSystem(voteUpBtn);
}

function initVotingSystem(voteUpBtn) {
    let voteCount = 0;
    let hasVoted = false;
    
    const voteCountElement = document.getElementById('voteCount');
    const votersCountElement = document.getElementById('votersCount');
    const voteBarElement = document.getElementById('voteBar');
    
    if (!voteCountElement || !votersCountElement || !voteBarElement) {
        console.error('Voting elements not found');
        return;
    }
    
    voteUpBtn.addEventListener('click', () => {
        if (!hasVoted) {
            voteCount++;
            hasVoted = true;
            
            // Update display
            voteCountElement.textContent = voteCount;
            votersCountElement.textContent = voteCount;
            
            // Update progress bar (max is 20 votes)
            const percentage = Math.min((voteCount / 20) * 100, 100);
            voteBarElement.style.width = `${percentage}%`;
            
            // Change button appearance
            voteUpBtn.classList.add('bg-gray-300');
            voteUpBtn.disabled = true;
        }
    });
} 