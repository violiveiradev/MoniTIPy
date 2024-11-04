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

    if(!button.nextElementSibling.classList.contains('show')){
        closeAllSubMenus();
    }

    button.nextElementSibling.classList.toggle('show');
    button.classList.toggle('rotate');

    if(sidebar.classList.contains('close')){
        sidebar.classList.toggle('close');
        toggleButton.classList.toggle('rotate');
    }
}

function closeAllSubMenus(){
    Array.from(sidebar.getElementsByClassName('show')).forEach(ul => {
        ul.classList.remove('show');
        ul.previousElementSibling.classList.remove('rotate');
    });
}

function toggleTheme() {
    const isLightTheme = document.body.classList.toggle('light-theme');
    
    // Atualiza o texto do botão conforme o tema
    themeToggleButton.querySelector('span').textContent = isLightTheme ? 'Modo Escuro' : 'Modo Claro';

    // Salva a preferência no localStorage
    localStorage.setItem('theme', isLightTheme ? 'light' : 'dark');
}