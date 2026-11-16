(function () {
    var grid = document.getElementById('pub-grid');
    var button = document.getElementById('pub-more');
    if (!grid || !button) {
        return;
    }
    var label = button.textContent;
    button.addEventListener('click', function () {
        var expanded = grid.classList.toggle('is-expanded');
        button.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        button.textContent = expanded ? 'Show less' : label;
    });
})();
