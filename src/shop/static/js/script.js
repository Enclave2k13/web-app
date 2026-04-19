// Выпадающее меню в сайдбаре
const arrow = document.getElementById('dropdownArrow');
const dropdownMenu = document.getElementById('dropdownMenu');

if (arrow && dropdownMenu) {
    arrow.addEventListener('click', function() {
        dropdownMenu.classList.toggle('hidden-menu');
    });
}