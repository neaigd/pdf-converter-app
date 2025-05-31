document.addEventListener('DOMContentLoaded', () => {
    const pdfFileElement = document.getElementById('pdfFile');
    const fileNameElement = document.getElementById('fileName');
    const convertBtn = document.getElementById('convertBtn');
    const progressBarElement = document.getElementById('progressBar');
    const statusMessageElement = document.getElementById('statusMessage');
    const downloadLinkElement = document.getElementById('downloadLink');

    let selectedFile = null;

    // --- Configuration ---
    // IMPORTANT: Set this URL to where your backend API is running.
    // For local development, this is typically http://localhost:8000.
    // If you deploy the backend to a different server, update this URL.
    const API_BASE_URL = 'http://localhost:8000';
    // --- End Configuration ---

    pdfFileElement.addEventListener('change', (event) => {
        selectedFile = event.target.files[0];
        if (selectedFile) {
            fileNameElement.textContent = selectedFile.name;
            statusMessageElement.textContent = `File "${selectedFile.name}" selected. Ready to convert.`;
            statusMessageElement.className = '';
            downloadLinkElement.classList.add('disabled');
            downloadLinkElement.removeAttribute('href');
            downloadLinkElement.removeAttribute('download');
            resetProgressBar();
        } else {
            fileNameElement.textContent = 'Click to choose a PDF file';
            selectedFile = null;
        }
    });

    convertBtn.addEventListener('click', async () => {
        if (!selectedFile) {
            updateStatus('Please select a PDF file first.', true);
            return;
        }

        const outputFormat = document.querySelector('input[name="outputFormat"]:checked').value;
        if (!outputFormat) {
            updateStatus('Please select an output format.', true);
            return;
        }

        convertBtn.disabled = true;
        convertBtn.textContent = 'Converting...';
        downloadLinkElement.classList.add('disabled');
        downloadLinkElement.removeAttribute('href');
        updateStatus(`Uploading ${selectedFile.name}...`, false);
        setProgressBar(10);

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            // 1. Upload the file
            const uploadResponse = await fetch(`${API_BASE_URL}/upload/`, {
                method: 'POST',
                body: formData,
            });

            setProgressBar(30);

            if (!uploadResponse.ok) {
                const errorData = await uploadResponse.json().catch(() => ({ detail: "Upload failed with no specific error message." }));
                throw new Error(`Upload failed: ${uploadResponse.status} ${errorData.detail || uploadResponse.statusText}`);
            }

            const uploadResult = await uploadResponse.json();
            updateStatus(`File uploaded. Now converting to ${outputFormat}...`, false);
            setProgressBar(50);

            // 2. Trigger conversion
            const convertResponse = await fetch(`${API_BASE_URL}/convert/?filename=${encodeURIComponent(uploadResult.filename)}&output_format=${outputFormat}`, {
                method: 'POST',
            });

            setProgressBar(75);

            if (!convertResponse.ok) {
                const errorData = await convertResponse.json().catch(() => ({ detail: "Conversion failed with no specific error message." }));
                throw new Error(`Conversion failed: ${convertResponse.status} ${errorData.detail || convertResponse.statusText}`);
            }

            const convertResult = await convertResponse.json();
            setProgressBar(100);
            updateStatus(convertResult.message || 'File converted successfully!', false, true);

            // 3. Enable download
            const downloadUrl = `${API_BASE_URL}/download/${encodeURIComponent(convertResult.output_file)}`;
            downloadLinkElement.href = downloadUrl;
            downloadLinkElement.setAttribute('download', convertResult.output_file);
            downloadLinkElement.classList.remove('disabled');
            downloadLinkElement.textContent = `Download ${convertResult.output_file}`;

        } catch (error) {
            console.error('Conversion process error:', error);
            updateStatus(`Error: ${error.message}`, true);
            resetProgressBar();
        } finally {
            convertBtn.disabled = false;
            convertBtn.textContent = '✨ Convert File';
        }
    });

    function updateStatus(message, isError = false, isSuccess = false) {
        statusMessageElement.textContent = message;
        statusMessageElement.className = isError ? 'error' : (isSuccess ? 'success' : '');
    }

    function setProgressBar(percentage) {
        progressBarElement.style.width = `${percentage}%`;
        progressBarElement.textContent = `${percentage}%`;
    }

    function resetProgressBar() {
        setProgressBar(0);
    }

    // Initial state for download link
    downloadLinkElement.classList.add('disabled');
});
