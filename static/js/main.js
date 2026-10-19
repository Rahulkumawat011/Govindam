// Main JavaScript logic for Govindam Enterprises

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Initialize AOS (Animate On Scroll)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            mirror: false
        });
    }

    // 2. Initialize Swiper for testimonials slider
    if (typeof Swiper !== 'undefined') {
        new Swiper('.testimonial-swiper', {
            slidesPerView: 1,
            spaceBetween: 24,
            loop: true,
            autoplay: {
                delay: 4000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            breakpoints: {
                768: {
                    slidesPerView: 2,
                },
                1024: {
                    slidesPerView: 3,
                }
            }
        });
    }

    // 3. Sticky Navbar shadow/blur transition
    const navbar = document.querySelector('.main-navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('shadow');
                navbar.style.padding = '0.5rem 0';
            } else {
                navbar.classList.remove('shadow');
                navbar.style.padding = '0.8rem 0';
            }
        });
    }

    // 4. Counter Ticker Animation using Intersection Observer
    const counters = document.querySelectorAll('.count-num');
    if (counters.length > 0) {
        const runCounter = (counter) => {
            const target = parseInt(counter.getAttribute('data-target'));
            let count = 0;
            const speed = target / 50; // duration division
            
            const updateCount = () => {
                count += speed;
                if (count < target) {
                    counter.innerText = Math.floor(count);
                    setTimeout(updateCount, 25);
                } else {
                    counter.innerText = target;
                }
            };
            updateCount();
        };

        const counterObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    runCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }

    // 5. AJAX Form Submission and Validation Helper
    const setupAjaxForm = (formId, submitBtnId) => {
        const form = document.getElementById(formId);
        const submitBtn = document.getElementById(submitBtnId);
        
        if (!form || !submitBtn) return;
        
        const spinner = submitBtn.querySelector('.spinner-border');
        const btnText = submitBtn.querySelector('span:not(.spinner-border)');
        const submitIcon = submitBtn.querySelector('i');

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Reset previous validation errors
            form.querySelectorAll('.invalid-feedback').forEach(el => {
                el.innerText = '';
                el.style.display = '';
            });
            form.querySelectorAll('.form-control, .form-select').forEach(el => el.classList.remove('is-invalid'));

            const formData = new FormData(form);
            
            // Set loading state
            submitBtn.disabled = true;
            if (spinner) spinner.classList.remove('d-none');
            if (btnText) btnText.innerText = 'Submitting...';
            if (submitIcon) submitIcon.classList.add('d-none');

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errData => { throw errData; });
                }
                return response.json();
            })
            .then(data => {
                form.reset();
                form.classList.remove('was-validated');

                if (data.whatsapp_url) {
                    Swal.fire({
                        title: 'Inquiry Submitted Successfully!',
                        text: data.message || 'Thank you! Your quote request has been saved successfully.',
                        icon: 'success',
                        showCancelButton: true,
                        confirmButtonColor: '#25d366',
                        cancelButtonColor: '#0b2e59',
                        confirmButtonText: '<i class="fa-brands fa-whatsapp me-2"></i> Chat on WhatsApp (+91 96807 11542)',
                        cancelButtonText: 'Close'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.open(data.whatsapp_url, '_blank');
                        }
                    });
                } else {
                    Swal.fire({
                        title: 'Submitted Successfully!',
                        text: data.message,
                        icon: 'success',
                        confirmButtonColor: '#0b2e59',
                        confirmButtonText: 'OK'
                    });
                }
            })
            .catch(error => {
                console.error('Submission error:', error);
                
                if (error && error.errors) {
                    let firstInvalidField = null;

                    // Populate validation errors inline
                    Object.keys(error.errors).forEach(field => {
                        const errorMsg = error.errors[field];
                        const errorContainer = form.querySelector(`[id$="-${field}"]`) ||
                                               form.querySelector(`#error-${field}`) ||
                                               form.querySelector(`.invalid-feedback`);
                        const inputField = form.querySelector(`[name="${field}"]`);
                        
                        if (errorContainer) {
                            errorContainer.innerText = errorMsg;
                            errorContainer.style.display = 'block';
                        }
                        if (inputField) {
                            inputField.classList.add('is-invalid');
                            if (!firstInvalidField) firstInvalidField = inputField;
                        }
                    });
                    
                    if (firstInvalidField) {
                        firstInvalidField.focus();
                    }
                    
                    Swal.fire({
                        title: 'Form Validation Error',
                        text: 'Please check the highlighted fields below.',
                        icon: 'warning',
                        confirmButtonColor: '#0b2e59'
                    });
                } else {
                    Swal.fire({
                        title: 'Oops!',
                        text: 'An unexpected connection error occurred. Please try again later.',
                        icon: 'error',
                        confirmButtonColor: '#0b2e59'
                    });
                }
            })
            .finally(() => {
                // Restore submit button state
                submitBtn.disabled = false;
                if (spinner) spinner.classList.add('d-none');
                if (btnText) {
                    if (submitBtnId === 'heroSubmitBtn') {
                        btnText.innerText = 'Request Quote';
                    } else if (submitBtnId === 'bottomSubmitBtn') {
                        btnText.innerText = 'Send Bulk RFQ Inquiry';
                    } else {
                        btnText.innerText = 'Send B2B Message';
                    }
                }
                if (submitIcon) submitIcon.classList.remove('d-none');
            });
        });
    };
 
    // Initialize forms
    setupAjaxForm('heroRequestForm', 'heroSubmitBtn');
    setupAjaxForm('bottomRequestForm', 'bottomSubmitBtn');
    setupAjaxForm('contactPageForm', 'contactSubmitBtn');
    setupAjaxForm('modalRequestForm', 'modalSubmitBtn');

    // 3D Interactive Mouse Tilt for Hero Quick Inquiry Form Card
    const heroCard = document.querySelector('#hero-quote-form .request-form-card');
    const heroContainer = document.getElementById('hero-quote-form');
    
    if (heroCard && heroContainer) {
        heroContainer.style.perspective = '1200px';
        
        heroCard.addEventListener('mousemove', function(e) {
            const rect = heroCard.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            const rotateX = (-y / rect.height) * 12;
            const rotateY = (x / rect.width) * 12;
            
            heroCard.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        heroCard.addEventListener('mouseleave', function() {
            heroCard.style.transform = 'rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        });
    }

    // 6. Gallery Lightbox Modal Handling
    const lightboxTriggers = document.querySelectorAll('.lightbox-trigger');
    const lightboxModalEl = document.getElementById('lightboxModal');
    
    if (lightboxTriggers.length > 0 && lightboxModalEl) {
        const lightboxModal = new bootstrap.Modal(lightboxModalEl);
        const lightboxImage = document.getElementById('lightboxImage');
        const lightboxTitle = document.getElementById('lightboxTitle');
        const lightboxCategory = document.getElementById('lightboxCategory');

        lightboxTriggers.forEach(trigger => {
            trigger.addEventListener('click', function() {
                const src = this.getAttribute('data-img-src');
                const title = this.getAttribute('data-img-title');
                const category = this.getAttribute('data-img-cat');

                if (src.startsWith('SVG_')) {
                    // Load fallback SVGs or colored blocks for simulated items
                    let svgMarkup = '';
                    let bgColor = '#2b5876';
                    let iconClass = 'fa-tower-broadcast';
                    
                    if (src === 'SVG_TOWER') { bgColor = 'linear-gradient(135deg, #2b5876 0%, #4e4376 100%)'; iconClass = 'fa-tower-broadcast'; }
                    else if (src === 'SVG_SUBSTATION') { bgColor = 'linear-gradient(135deg, #141e30 0%, #243b55 100%)'; iconClass = 'fa-circle-nodes'; }
                    else if (src === 'SVG_CABLING') { bgColor = 'linear-gradient(135deg, #0f2027 0%, #203a43 100%)'; iconClass = 'fa-bolt'; }
                    else if (src === 'SVG_METERING') { bgColor = 'linear-gradient(135deg, #e65c00 0%, #f9d423 100%)'; iconClass = 'fa-chart-line'; }
                    else if (src === 'SVG_SOLAR') { bgColor = 'linear-gradient(135deg, #3a7bd5 0%, #3a6073 100%)'; iconClass = 'fa-solar-panel'; }
                    else if (src === 'SVG_FEEDER') { bgColor = 'linear-gradient(135deg, #1d976c 0%, #93f9b9 100%)'; iconClass = 'fa-plug-circle-bolt'; }

                    lightboxImage.style.display = 'none';
                    
                    // Create simulated illustration box
                    let illustrationBox = document.getElementById('lightboxIllustrationBox');
                    if (!illustrationBox) {
                        illustrationBox = document.createElement('div');
                        illustrationBox.id = 'lightboxIllustrationBox';
                        lightboxImage.parentNode.insertBefore(illustrationBox, lightboxImage);
                    }
                    illustrationBox.style.display = 'flex';
                    illustrationBox.style.height = '350px';
                    illustrationBox.style.borderRadius = '8px';
                    illustrationBox.style.background = bgColor;
                    illustrationBox.style.alignItems = 'center';
                    illustrationBox.style.justifyContent = 'center';
                    illustrationBox.style.flexDirection = 'column';
                    illustrationBox.className = 'shadow-2xl';
                    illustrationBox.innerHTML = `<i class="fa-solid ${iconClass} fa-6x text-white-50 mb-3"></i><p class="text-white-50 font-weight-bold">Govindam Enterprises Project Site Image</p>`;
                } else {
                    // Standard image loading
                    const illustrationBox = document.getElementById('lightboxIllustrationBox');
                    if (illustrationBox) illustrationBox.style.display = 'none';
                    lightboxImage.style.display = 'inline-block';
                    lightboxImage.src = src;
                }

                lightboxTitle.innerText = title;
                lightboxCategory.innerText = category;
                
                lightboxModal.show();
            });
        });
    }

});

// Global 3D Quick Inquiry Modal Toggle Handler
window.toggle3DInquiryModal = function() {
    const modal = document.getElementById('quickInquiry3DModal');
    if (!modal) return;

    if (modal.classList.contains('d-none')) {
        modal.classList.remove('d-none');
        setTimeout(() => {
            modal.classList.add('show');
        }, 10);
    } else {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.classList.add('d-none');
        }, 450);
    }
};
