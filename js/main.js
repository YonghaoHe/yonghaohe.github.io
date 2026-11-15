// Navbar scroll effect
window.addEventListener('scroll', function () {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 2px 16px rgba(0, 0, 0, 0.08)';
    } else {
        navbar.style.boxShadow = 'none';
    }
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        var target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Publications: papers before 2025 stay in the page until View more.
(function () {
    var list = document.getElementById('publications-list');
    var button = document.getElementById('publications-more');
    if (!list || !button) {
        return;
    }
    var earlier = list.querySelectorAll('.publication-item--earlier');
    if (!earlier.length) {
        button.hidden = true;
        return;
    }
    button.addEventListener('click', function () {
        var expanded = list.classList.toggle('is-expanded');
        button.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        button.textContent = expanded ? 'Show less' : 'View more';
        earlier.forEach(function (item) {
            item.setAttribute('aria-hidden', expanded ? 'false' : 'true');
        });
        if (!expanded) {
            var rect = button.getBoundingClientRect();
            if (rect.top < 72 || rect.bottom > window.innerHeight) {
                button.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }
    });
})();
