document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Masonry Layout
    const grid = document.querySelector('.masonry-grid');
    if (grid) {
        // Init Masonry
        const msnry = new Masonry(grid, {
            itemSelector: '.masonry-item',
            columnWidth: '.masonry-item',
            percentPosition: true,
            transitionDuration: '0.3s'
        });

        // Layout Masonry after each image loads
        imagesLoaded(grid).on('progress', function () {
            msnry.layout();
        });
    }

    // 2. Copy Prompt Functionality
    const toast = document.getElementById('toast');
    let toastTimeout;

    function showToast() {
        toast.classList.add('show');
        clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            // Prevent event from bubbling up if we add card click modal later
            e.stopPropagation();

            const promptText = btn.getAttribute('data-prompt');
            if (!promptText) return;

            try {
                // Try writing to clipboard
                await navigator.clipboard.writeText(promptText);
                showToast();

                // Visual feedback on button
                const originalHTML = btn.innerHTML;
                btn.innerHTML = '<i class="ph-fill ph-check"></i> Copied!';
                btn.style.background = '#10b981';
                btn.style.borderColor = '#10b981';

                setTimeout(() => {
                    btn.innerHTML = originalHTML;
                    btn.style.background = '';
                    btn.style.borderColor = '';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy text: ', err);
                alert('Copy failed, please copy manually');
            }
        });
    });
});
