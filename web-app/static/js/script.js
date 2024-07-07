
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.querySelector('input[type="file"]');
    fileInput.addEventListener('change', function () {
        if (fileInput.files.length > 0) {
            document.querySelector('button[type="submit"]').disabled = false;
        }
    });
});
