const toggleButton = document.getElementById('toggle-btn');
const sidebar = document.getElementById('sidebar');
const themeToggleButton = document.getElementById('theme-toggle-btn');

// Carregar tema salvo no localStorage
document.body.classList.toggle('light-theme', localStorage.getItem('theme') === 'light');

function toggleSidebar(){
    sidebar.classList.toggle('close');
    toggleButton.classList.toggle('rotate');
    closeAllSubMenus();
}

function toggleSubMenu(button){
    const submenu = button.nextElementSibling;

    if(!submenu.classList.contains('show')){
        closeAllSubMenus();
    }

    submenu.classList.toggle('show');
    button.classList.toggle('rotate');

    submenu.querySelectorAll('a').forEach(link => {
        if (submenu.classList.contains('show')) {
            link.removeAttribute('tabindex');
        } else {
            link.setAttribute('tabindex', '-1');
        }
    });

    if(sidebar.classList.contains('close')){
        sidebar.classList.toggle('close');
        toggleButton.classList.toggle('rotate');
    }
}

function closeAllSubMenus(){
    Array.from(sidebar.getElementsByClassName('show')).forEach(submenu => {
        submenu.classList.remove('show');
        submenu.previousElementSibling.classList.remove('rotate');

        submenu.querySelectorAll('a').forEach(link => {
            link.setAttribute('tabindex', '-1');
        });

    });
}

function toggleTheme() {
    const isLightTheme = document.body.classList.toggle('light-theme');
    
    // Atualiza o texto do botão conforme o tema
    themeToggleButton.querySelector('span').textContent = isLightTheme ? 'Modo Escuro' : 'Modo Claro';

    // Salva a preferência no localStorage
    localStorage.setItem('theme', isLightTheme ? 'light' : 'dark');
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.sub-menu').forEach(submenu => {
        if (!submenu.classList.contains('show')) {
            submenu.querySelectorAll('a').forEach(link => {
                link.setAttribute('tabindex', '-1'); // Ignora links dos submenus ocultos
            });
        }
    });
});

function toggleDetails(row) {
    // Encontra a linha de detalhes logo abaixo da linha principal
    const detailsRow = row.parentElement.nextElementSibling;
    
    // Alterna a exibição da linha de detalhes
    if (detailsRow.style.display === "table-row") {
        detailsRow.style.display = "none";
        row.classList.remove("active");
    } else {
        detailsRow.style.display = "table-row";
        row.classList.add("active");
    }
}
