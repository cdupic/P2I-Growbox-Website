const onResize = () => {

    const nav = document.querySelector('#sidebar');
    const navButton = document.querySelector('header .sidebar-button');
    const overlay = document.querySelector('#overlay');

    if(document.body.clientWidth < 800){ // Sidebar view
        if(!navButton.classList.contains('active')){
            navButton.classList.add('active');
        }
        if(!nav.classList.contains('overlayed')){
            nav.classList.add('overlayed');
        }
    }else{ // Full view
        if(navButton.classList.contains('active')){
            navButton.classList.remove('active');
        }
        if(nav.classList.contains('overlayed')){
            nav.classList.remove('overlayed');
        }
        if(nav.classList.contains('active')){
            nav.classList.remove('active');
        }
        if(overlay.classList.contains('active')){
            overlay.classList.remove('active');
        }
    }
}

const onToggleMenu = () => {
    const nav = document.querySelector('#sidebar')
    const overlay = document.querySelector('#overlay');

    if(nav.classList.contains('active')){
        nav.classList.remove('active');
        overlay.classList.remove('active');
    }else{
        nav.classList.add('active');
        overlay.classList.add('active');
    }
}

const onLoad = () => {
    onResize();
    const nav = document.querySelector('#sidebar');
    nav.classList.remove('to-init')

    const navButton = document.querySelector('header .sidebar-button');
    navButton.addEventListener('click', onToggleMenu)

    const overlay = document.querySelector('#overlay');
    overlay.addEventListener('click', onToggleMenu)
}

window.addEventListener('resize', onResize)
window.addEventListener('load', onLoad)
