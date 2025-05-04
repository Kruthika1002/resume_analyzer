document.addEventListener('DOMContentLoaded', function() {
    // File input enhancement
    const fileInput = document.getElementById('resume');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                // You could add visual feedback here
                console.log(`File selected: ${fileName}`);
            }
        });
    }
    
    // Form validation
    const form = document.querySelector('.upload-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('resume');
            
            if (!fileInput.files || fileInput.files.length === 0) {
                e.preventDefault();
                alert('Please select a resume file to upload.');
                return;
            }
            
            const allowedExtensions = ['.pdf', '.docx', '.doc'];
            const fileName = fileInput.files[0].name;
            const fileExtension = fileName.substring(fileName.lastIndexOf('.')).toLowerCase();
            
            if (!allowedExtensions.includes(fileExtension)) {
                e.preventDefault();
                alert('Please upload a PDF or DOCX file.');
                return;
            }
            
            // Add a loading state
            const submitButton = document.querySelector('.submit-btn');
            submitButton.textContent = 'Analyzing...';
            submitButton.disabled = true;
        });
    }
    
    // Collapsible sections on results page
    const sectionHeadings = document.querySelectorAll('.analysis-section h2');
    sectionHeadings.forEach(heading => {
        heading.addEventListener('click', () => {
            const section = heading.parentElement;
            section.classList.toggle('collapsed');
        });
    });
});