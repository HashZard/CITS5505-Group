export function initFileUpload({
                                   fileInputId,
                                   descInputId,
                                   uploadBtnId = null,
                                   formId = null,
                                   fileListId,
                                   uploadUrl,
                                   onSuccess = null
                               } = {}) {
    const fileInput = document.getElementById(fileInputId);
    const descInput = document.getElementById(descInputId);
    const form = formId ? document.getElementById(formId) : null;
    const uploadBtn = uploadBtnId ? document.getElementById(uploadBtnId) : null;
    const fileList = fileListId ? document.getElementById(fileListId) : null;

    if (!fileInput || !descInput || (!uploadBtn && !form)) {
        console.error("Upload elements not found:", fileInputId, descInputId, uploadBtnId || formId);
        return;
    }

    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        if (fileList) {
            fileList.textContent = file ? file.name : "";
        }
    });

    const handleSubmit = async (e) => {
        if (e) e.preventDefault();

        const file = fileInput.files[0];
        const description = descInput.value.trim();

        if (!file) {
            alert("Please select a file to upload.");
            return;
        }

        if (!description) {
            alert("Please enter a description.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("description", description);

        try {
            const res = await fetch(uploadUrl, {
                method: "POST",
                body: formData
            });

            const result = await res.json();
            if (result.success) {
                alert("✅ Upload successful!");
                fileInput.value = "";
                descInput.value = "";
                if (fileList) fileList.textContent = "";
                if (typeof onSuccess === "function") onSuccess(result.file);
            } else {
                alert("❌ Upload failed: " + result.message);
            }
        } catch (err) {
            console.error("Upload error:", err);
            alert("❌ Network error during file upload.");
        }
    };

    if (form) {
        form.addEventListener("submit", handleSubmit);
    } else if (uploadBtn) {
        uploadBtn.addEventListener("click", handleSubmit);
    }
}
