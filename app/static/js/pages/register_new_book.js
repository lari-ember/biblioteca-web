/**
 * Register New Book - Confirmation Modal & Duplicate Detection
 *
 * Features:
 * - Book summary confirmation
 * - Duplicate detection with similarity scoring
 * - Modal overlay with form validation
 */

let currentFormData = null;

// ════════════════════════════════════════════════════════════════════════════
// INITIALIZATION
// ════════════════════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');
    if (!registerForm) return;

    // Intercept form submission
    registerForm.addEventListener('submit', function(e) {
        // Only prevent default for initial check
        if (e.submitter && e.submitter.getAttribute('data-skip-check') !== 'true') {
            e.preventDefault();

            // Validate form before showing confirmation
            const validationErrors = validateFormFields();
            if (validationErrors.length > 0) {
                displayValidationErrors(validationErrors);
                return;
            }

            checkForDuplicatesAndShowConfirmation();
        }
    });

    // Remove error highlighting when user starts typing
    const formFields = registerForm.querySelectorAll('.form-control, .form-select');
    formFields.forEach(field => {
        field.addEventListener('input', function() {
            this.classList.remove('validation-error');
            // Remove error message if it exists
            clearValidationErrors();
        });

        field.addEventListener('change', function() {
            this.classList.remove('validation-error');
            clearValidationErrors();
        });
    });
});

// ════════════════════════════════════════════════════════════════════════════
// FORM VALIDATION
// ════════════════════════════════════════════════════════════════════════════

/**
 * Validate form fields
 * @returns {Array} Array of validation error messages
 */
function validateFormFields() {
    const errors = [];

    // Get form fields
    const titleEl = document.getElementById('title');
    const authorEl = document.getElementById('author');
    const publisherEl = document.getElementById('publisher');
    const yearEl = document.getElementById('year');
    const pagesEl = document.getElementById('pages');
    const genreEl = document.getElementById('genre');
    const readEl = document.getElementById('read');
    const statusEl = document.getElementById('status');
    const formatEl = document.getElementById('format');
    const isbnEl = document.getElementById('isbn');

    const title = titleEl ? titleEl.value.trim() : '';
    const author = authorEl ? authorEl.value.trim() : '';
    const publisher = publisherEl ? publisherEl.value.trim() : '';
    const year = yearEl ? yearEl.value : '';
    const pages = pagesEl ? pagesEl.value : '';
    const genre = genreEl ? genreEl.value.trim() : '';
    const read = readEl ? readEl.value : '';
    const status = statusEl ? statusEl.value : '';
    const format = formatEl ? formatEl.value : '';
    const isbn = isbnEl ? isbnEl.value.trim() : '';

    // Validation rules
    if (!title) {
        errors.push('Title is required');
    }

    if (!author) {
        errors.push('Author is required');
    }

    if (!publisher) {
        errors.push('Publisher is required');
    }

    if (!year) {
        errors.push('Year is required');
    } else if (isNaN(year) || year < 1000 || year > new Date().getFullYear() + 5) {
        errors.push('Year must be a valid number');
    }

    if (!pages) {
        errors.push('Pages is required');
    } else if (isNaN(pages) || pages < 1) {
        errors.push('Pages must be a valid number greater than 0');
    }

    if (!genre) {
        errors.push('Genre is required');
    }

    if (!read) {
        errors.push('Reading Status is required');
    }

    if (!status) {
        errors.push('Availability is required');
    }

    if (!format) {
        errors.push('Format is required');
    }

    // Validate ISBN if provided
    if (isbn) {
        if (!validateISBNFormat(isbn)) {
            errors.push('Invalid ISBN format');
        }
    }

    return errors;
}

/**
 * Validate ISBN format
 */
function validateISBNFormat(isbn) {
    const clean = isbn.replace(/[-\s]/g, '').toUpperCase();

    if (clean.length === 10) {
        let sum = 0;
        for (let i = 0; i < 10; i++) {
            const c = clean[i];
            const v = (c === 'X' && i === 9) ? 10 : parseInt(c);
            if (isNaN(v)) return false;
            sum += (10 - i) * v;
        }
        return sum % 11 === 0;
    } else if (clean.length === 13 && /^\d{13}$/.test(clean)) {
        let sum = 0;
        for (let i = 0; i < 12; i++) {
            sum += parseInt(clean[i]) * (i % 2 === 0 ? 1 : 3);
        }
        return (10 - (sum % 10)) % 10 === parseInt(clean[12]);
    }

    return clean.length === 0; // Allow empty ISBN
}

/**
 * Display validation errors to user
 */
function displayValidationErrors(errors) {
    // Clear previous errors
    clearValidationErrors();

    // Clear previous field highlighting
    document.querySelectorAll('.validation-error').forEach(el => {
        el.classList.remove('validation-error');
    });

    // Highlight invalid fields
    highlightInvalidFields();

    // Create error container
    const errorContainer = document.createElement('div');
    errorContainer.className = 'validation-errors-alert';
    errorContainer.setAttribute('role', 'alert');

    const errorHeader = document.createElement('h4');
    errorHeader.innerHTML = '<ion-icon name="alert-circle-outline" aria-hidden="true" class="me-2"></ion-icon>Please fix the following errors:';
    errorContainer.appendChild(errorHeader);

    const errorList = document.createElement('ul');
    errors.forEach(error => {
        const li = document.createElement('li');
        li.textContent = error;
        errorList.appendChild(li);
    });
    errorContainer.appendChild(errorList);

    // Insert error container at the top of the form
    const registerForm = document.getElementById('register-form');
    registerForm.insertBefore(errorContainer, registerForm.firstChild);

    // Scroll to error
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Auto-remove after 10 seconds
    setTimeout(() => {
        if (errorContainer.parentNode) {
            errorContainer.remove();
        }
    }, 10000);
}

/**
 * Highlight invalid form fields
 */
function highlightInvalidFields() {
    const title = document.getElementById('title');
    const author = document.getElementById('author');
    const publisher = document.getElementById('publisher');
    const year = document.getElementById('year');
    const pages = document.getElementById('pages');
    const genre = document.getElementById('genre');
    const read = document.getElementById('read');
    const status = document.getElementById('status');
    const format = document.getElementById('format');

    // Check each field and add error class if empty
    if (title && !title.value.trim()) title.classList.add('validation-error');
    if (author && !author.value.trim()) author.classList.add('validation-error');
    if (publisher && !publisher.value.trim()) publisher.classList.add('validation-error');
    if (year && !year.value) year.classList.add('validation-error');
    if (pages && !pages.value) pages.classList.add('validation-error');
    if (genre && !genre.value.trim()) genre.classList.add('validation-error');
    if (read && !read.value) read.classList.add('validation-error');
    if (status && !status.value) status.classList.add('validation-error');
    if (format && !format.value) format.classList.add('validation-error');
}

/**
 * Clear validation errors
 */
function clearValidationErrors() {
    const existingErrors = document.querySelector('.validation-errors-alert');
    if (existingErrors) {
        existingErrors.remove();
    }
}

// ════════════════════════════════════════════════════════════════════════════
// CONFIRMATION MODAL FUNCTIONS
// ════════════════════════════════════════════════════════════════════════════

/**
 * Check for duplicates and show confirmation modal
 */
function checkForDuplicatesAndShowConfirmation() {
    const form = document.getElementById('register-form');

    // Collect book data from form
    const bookData = {
        title: document.getElementById('title').value,
        author: document.getElementById('author').value,
        isbn: document.getElementById('isbn').value,
        year: document.getElementById('year').value,
        publisher: document.getElementById('publisher').value,
        pages: document.getElementById('pages').value,
        genre: document.getElementById('genre').value,
        country_of_origin: document.getElementById('country_of_origin').value,
        original_language: document.getElementById('original_language').value,
        read: document.getElementById('read').value,
        status: document.getElementById('status').value,
        format: document.getElementById('format').value,
        cover_url: document.getElementById('cover_url').value,
        openlibrary_key: document.getElementById('openlibrary_key').value,
    };

    // Store form data for later submission
    currentFormData = bookData;

    // Check for duplicates via AJAX
    fetch('/check_duplicates', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: bookData.title,
            author: bookData.author,
            isbn: bookData.isbn
        })
    })
    .then(response => response.json())
    .then(data => {
        // Populate confirmation modal with book data
        populateConfirmationModal(bookData, data.duplicates || []);
        // Show the modal
        document.getElementById('confirmation-modal').style.display = 'flex';
    })
    .catch(error => {
        console.error('Error checking duplicates:', error);
        // Show error but allow confirmation anyway
        alert('Error checking for similar books. Please review before confirming.');
        populateConfirmationModal(bookData, []);
        document.getElementById('confirmation-modal').style.display = 'flex';
    });
}

/**
 * Populate the confirmation modal with book data
 */
function populateConfirmationModal(bookData, duplicates) {
    // Populate book summary
    document.getElementById('confirm-title').textContent = bookData.title || '—';
    document.getElementById('confirm-author').textContent = bookData.author || '—';
    document.getElementById('confirm-isbn').textContent = bookData.isbn || '—';
    document.getElementById('confirm-year').textContent = bookData.year || '—';
    document.getElementById('confirm-publisher').textContent = bookData.publisher || '—';
    document.getElementById('confirm-pages').textContent = bookData.pages ? `${bookData.pages} pages` : '—';

    // Show/hide duplicates section
    const duplicatesSection = document.getElementById('duplicates-section');
    const duplicatesList = document.getElementById('duplicates-list');

    if (duplicates.length > 0) {
        duplicatesSection.style.display = 'block';
        duplicatesList.innerHTML = '';

        duplicates.forEach(dup => {
            const dupItem = createDuplicateItem(dup);
            duplicatesList.appendChild(dupItem);
        });
    } else {
        duplicatesSection.style.display = 'none';
    }
}

/**
 * Create a duplicate item element
 */
function createDuplicateItem(duplicate) {
    const div = document.createElement('div');
    div.className = 'duplicate-item';

    // Calculate similarity class
    let similarityClass = 'similarity-low';
    if (duplicate.similarity >= 80) similarityClass = 'similarity-high';
    else if (duplicate.similarity >= 50) similarityClass = 'similarity-medium';

    const coverHtml = duplicate.cover_url
        ? `<img src="${escapeHtmlDup(duplicate.cover_url)}" alt="${escapeHtmlDup(duplicate.title)}" loading="lazy">`
        : '<div style="display: flex; align-items: center; justify-content: center; color: var(--reg-text-muted);">No Cover</div>';

    const readStatusLabel = {
        'want_to_read': 'Want to Read',
        'unread': 'Unread',
        'reading': 'Reading',
        'read': 'Read'
    }[duplicate.read_status] || duplicate.read_status;

    div.innerHTML = `
        <div class="duplicate-cover">${coverHtml}</div>
        <div class="duplicate-info">
            <h5>${escapeHtmlDup(duplicate.title)}</h5>
            <p><strong>${escapeHtmlDup(duplicate.author)}</strong></p>
            <p>${duplicate.year || 'Year unknown'}</p>
            ${duplicate.isbn ? `<p>ISBN: ${escapeHtmlDup(duplicate.isbn)}</p>` : ''}
            <span class="duplicate-badge">${readStatusLabel}</span>
        </div>
        <div class="similarity-score">
            <div class="similarity-badge ${similarityClass}">${duplicate.similarity}%</div>
            <small>Match</small>
        </div>
    `;

    return div;
}

/**
 * Escape HTML special characters
 */
function escapeHtmlDup(str) {
    const div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
}

/**
 * Close confirmation modal
 */
function closeConfirmationModal() {
    document.getElementById('confirmation-modal').style.display = 'none';
    currentFormData = null;
}

/**
 * Confirm and submit the form
 */
function confirmAndSubmit() {
    const form = document.getElementById('register-form');

    // Create a hidden submit button to skip the check on re-submission
    if (!document.getElementById('hidden-submit-btn')) {
        const hiddenBtn = document.createElement('button');
        hiddenBtn.id = 'hidden-submit-btn';
        hiddenBtn.type = 'submit';
        hiddenBtn.setAttribute('data-skip-check', 'true');
        hiddenBtn.style.display = 'none';
        form.appendChild(hiddenBtn);
    }

    // Trigger the hidden submit button to bypass our check
    document.getElementById('hidden-submit-btn').click();
}

// Close modal when clicking outside of it
document.addEventListener('click', function(event) {
    const modal = document.getElementById('confirmation-modal');
    const modalContent = document.querySelector('.modal-content');

    if (modal && modal.style.display === 'flex' &&
        !modalContent.contains(event.target)) {
        closeConfirmationModal();
    }
});

