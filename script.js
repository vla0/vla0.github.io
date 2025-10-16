// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Copy BibTeX function
function copyBibtex() {
    const bibtex = `@article{goyal2025vla0,
  title={VLA-0: Building State-of-the-Art VLAs with Zero Modification},
  author={Goyal, Ankit and Hadfield, Hugo and Yang, Xuning and Bulkis, Valts and Ramos, Fabio},
  journal={arXiv preprint arXiv:2510.13054},
  year={2025}
}`;
    
    navigator.clipboard.writeText(bibtex).then(function() {
        const copyBtn = document.querySelector('.copy-btn');
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<span class="copy-icon">✓</span> Copied!';
        copyBtn.style.background = '#10b981';
        copyBtn.style.color = 'white';
        
        setTimeout(function() {
            copyBtn.innerHTML = originalText;
            copyBtn.style.background = 'white';
            copyBtn.style.color = 'var(--text-dark)';
        }, 2000);
    }).catch(function(err) {
        console.error('Failed to copy: ', err);
        alert('Failed to copy BibTeX. Please copy manually.');
    });
}

// Scroll reveal animation
function scrollReveal() {
    const reveals = document.querySelectorAll('.scroll-reveal');
    
    reveals.forEach(element => {
        const windowHeight = window.innerHeight;
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < windowHeight - elementVisible) {
            element.classList.add('revealed');
        }
    });
}

window.addEventListener('scroll', scrollReveal);

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Convert PDF to image for comparison figure
window.addEventListener('DOMContentLoaded', function() {
    const comparisonImg = document.getElementById('comparison-img');
    if (comparisonImg) {
        const pdfPath = comparisonImg.src;
        
        // Check if the browser can display PDF, if not try to show a different figure
        if (pdfPath.endsWith('.pdf')) {
            // Try to load an alternative figure if PDF doesn't work
            comparisonImg.onerror = function() {
                // Try other figure formats
                const altFormats = [
                    'data/figures/comp_fig_horizontal.pdf',
                    'data/figures/SimpleVLAComp.pdf',
                    'data/figures/arch_fig.pdf'
                ];
                
                let currentIndex = altFormats.indexOf(pdfPath);
                if (currentIndex < altFormats.length - 1) {
                    comparisonImg.src = altFormats[currentIndex + 1];
                }
            };
        }
    }
    
    // Initialize scroll reveal for elements already in view
    scrollReveal();
});

// Add animation classes to sections as they scroll into view
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
        }
    });
}, observerOptions);

// Observe all cards and major elements
document.addEventListener('DOMContentLoaded', function() {
    const elementsToObserve = document.querySelectorAll(
        '.comparison-card, .method-card, .highlight-card, .stat-card, .resource-link'
    );
    
    elementsToObserve.forEach(el => {
        el.classList.add('scroll-reveal');
        observer.observe(el);
    });
});

// Video lazy loading optimization
document.addEventListener('DOMContentLoaded', function() {
    const videos = document.querySelectorAll('video');
    
    const videoObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const video = entry.target;
                if (video.paused) {
                    // Autoplay hero video, LIBERO animation, and real-world video
                    if (video.autoplay || video.classList.contains('libero-animation') || video.classList.contains('realworld-video')) {
                        video.play().catch(e => console.log('Video autoplay prevented:', e));
                    }
                }
            } else {
                const video = entry.target;
                // Pause videos when they leave viewport
                if (!video.paused && (video.autoplay || video.classList.contains('libero-animation') || video.classList.contains('realworld-video'))) {
                    video.pause();
                }
            }
        });
    }, { threshold: 0.5 });
    
    videos.forEach(video => {
        videoObserver.observe(video);
    });
});

// Table responsive handling
window.addEventListener('DOMContentLoaded', function() {
    const tables = document.querySelectorAll('.results-table');
    tables.forEach(table => {
        // Add touch scrolling hint for mobile
        if (window.innerWidth < 768) {
            const container = table.parentElement;
            container.style.cursor = 'grab';
            
            let isDown = false;
            let startX;
            let scrollLeft;
            
            container.addEventListener('mousedown', (e) => {
                isDown = true;
                container.style.cursor = 'grabbing';
                startX = e.pageX - container.offsetLeft;
                scrollLeft = container.scrollLeft;
            });
            
            container.addEventListener('mouseleave', () => {
                isDown = false;
                container.style.cursor = 'grab';
            });
            
            container.addEventListener('mouseup', () => {
                isDown = false;
                container.style.cursor = 'grab';
            });
            
            container.addEventListener('mousemove', (e) => {
                if (!isDown) return;
                e.preventDefault();
                const x = e.pageX - container.offsetLeft;
                const walk = (x - startX) * 2;
                container.scrollLeft = scrollLeft - walk;
            });
        }
    });
});

// Highlight active navigation link
window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a');
    
    let currentSection = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.scrollY >= (sectionTop - 100)) {
            currentSection = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + currentSection) {
            link.classList.add('active');
        }
    });
});

