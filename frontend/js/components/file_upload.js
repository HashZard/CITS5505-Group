        // Form validation and file upload handling
        document.getElementById('createCourseForm').addEventListener('submit', function(e) {
            e.preventDefault();
            // Add form submission logic here
        });

        // File upload handling
        const fileUpload = document.getElementById('fileUpload');
        const fileList = document.getElementById('fileList');
        
        fileUpload.addEventListener('change', function(e) {
            fileList.innerHTML = '';
            Array.from(this.files).forEach(file => {
                const fileItem = document.createElement('div');
                fileItem.className = 'flex items-center gap-2 mt-2';
                fileItem.innerHTML = `
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    <span>${file.name}</span>
                `;
                fileList.appendChild(fileItem);
            });
        });

        // Drag and drop functionality
        const dropZone = document.querySelector('.border-dashed');
        
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('border-purple-blue-600');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('border-purple-blue-600');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('border-purple-blue-600');
            const files = e.dataTransfer.files;
            fileUpload.files = files;
            const event = new Event('change');
            fileUpload.dispatchEvent(event);
        });