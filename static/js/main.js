/* ===================================================
   StudySync – Client-Side Interactivity
   =================================================== */

document.addEventListener('DOMContentLoaded', () => {

    // ── Mobile Sidebar Toggle ──
    const mobileToggle = document.querySelector('.mobile-toggle');
    const sidebar = document.querySelector('.sidebar');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            sidebarOverlay.classList.toggle('active');
        });
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            sidebarOverlay.classList.remove('active');
        });
    }

    // ── Auto-dismiss flash messages ──
    const flashMessages = document.querySelectorAll('.flash-msg');
    flashMessages.forEach((msg) => {
        setTimeout(() => {
            msg.style.display = 'none';
        }, 4000);
    });

    // ── Animated Progress Bars ──
    const progressBars = document.querySelectorAll('.progress-bar-fill');
    if (progressBars.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const width = bar.getAttribute('data-width');
                    bar.style.width = width + '%';
                }
            });
        }, { threshold: 0.2 });

        progressBars.forEach((bar) => {
            bar.style.width = '0%';
            observer.observe(bar);
        });
    }

    // ── Animated Progress Ring (Attendance) ──
    const progressRing = document.querySelector('.progress-ring-fill');
    if (progressRing) {
        const radius = progressRing.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;
        const percentage = parseFloat(progressRing.getAttribute('data-percentage')) || 0;

        progressRing.style.strokeDasharray = circumference;
        progressRing.style.strokeDashoffset = circumference;

        setTimeout(() => {
            const offset = circumference - (percentage / 100) * circumference;
            progressRing.style.strokeDashoffset = offset;
        }, 300);
    }

    // ── Dynamic CGPA Semester Inputs ──
    const semesterCountInput = document.getElementById('semester-count');
    const semesterInputsContainer = document.getElementById('semester-inputs');
    const generateBtn = document.getElementById('generate-inputs-btn');

    if (generateBtn && semesterCountInput && semesterInputsContainer) {
        generateBtn.addEventListener('click', () => {
            const count = parseInt(semesterCountInput.value);
            if (isNaN(count) || count < 1 || count > 8) {
                alert('Please enter a valid number of semesters (1-8)');
                return;
            }

            semesterInputsContainer.innerHTML = '';

            for (let i = 1; i <= count; i++) {
                const group = document.createElement('div');
                group.className = 'semester-input-group';
                group.innerHTML = `
                    <label>Sem ${i}</label>
                    <input type="number" name="sgpa_${i}" min="0" max="10" step="0.01"
                           placeholder="SGPA" required class="form-control">
                `;
                semesterInputsContainer.appendChild(group);
            }

            // Show submit button
            const submitBtn = document.getElementById('cgpa-submit-btn');
            if (submitBtn) submitBtn.style.display = 'inline-flex';

            // Add hidden input for semester count
            let hiddenInput = document.getElementById('total-semesters-hidden');
            if (!hiddenInput) {
                hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'total_semesters';
                hiddenInput.id = 'total-semesters-hidden';
                semesterInputsContainer.appendChild(hiddenInput);
            }
            hiddenInput.value = count;
        });
    }

    // ── Edit Task Modal ──
    const editBtns = document.querySelectorAll('.edit-task-btn');
    const editModal = document.getElementById('edit-task-modal');
    const closeModalBtns = document.querySelectorAll('.close-modal');

    editBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
            const taskId = btn.getAttribute('data-id');
            const title = btn.getAttribute('data-title');
            const subject = btn.getAttribute('data-subject');
            const priority = btn.getAttribute('data-priority');
            const dueDate = btn.getAttribute('data-due');

            document.getElementById('edit-task-id').value = taskId;
            document.getElementById('edit-title').value = title;
            document.getElementById('edit-subject').value = subject;
            document.getElementById('edit-priority').value = priority;
            document.getElementById('edit-due-date').value = dueDate;

            editModal.classList.add('active');
        });
    });

    closeModalBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.modal-overlay').forEach((m) => {
                m.classList.remove('active');
            });
        });
    });

    // Close modal on overlay click
    document.querySelectorAll('.modal-overlay').forEach((overlay) => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.classList.remove('active');
            }
        });
    });

    // ── Delete Confirmation ──
    const deleteForms = document.querySelectorAll('.delete-task-form');
    deleteForms.forEach((form) => {
        form.addEventListener('submit', (e) => {
            if (!confirm('Are you sure you want to delete this task?')) {
                e.preventDefault();
            }
        });
    });

    // ── Live Date/Time ──
    const datetimeEl = document.querySelector('.datetime');
    if (datetimeEl) {
        const updateDateTime = () => {
            const now = new Date();
            const options = {
                weekday: 'short',
                day: '2-digit',
                month: 'short',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                hour12: true
            };
            datetimeEl.textContent = now.toLocaleDateString('en-IN', options);
        };
        updateDateTime();
        setInterval(updateDateTime, 30000);
    }

    // ── Animate stat counters ──
    const statValues = document.querySelectorAll('.stat-value[data-count]');
    statValues.forEach((el) => {
        const target = parseFloat(el.getAttribute('data-count'));
        const isDecimal = el.getAttribute('data-decimal') === 'true';
        const suffix = el.getAttribute('data-suffix') || '';
        let current = 0;
        const duration = 1200;
        const steps = 40;
        const increment = target / steps;
        const interval = duration / steps;

        const counter = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(counter);
            }
            el.textContent = (isDecimal ? current.toFixed(2) : Math.round(current)) + suffix;
        }, interval);
    });
});
