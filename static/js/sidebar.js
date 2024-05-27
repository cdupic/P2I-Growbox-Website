const onResize = () => {

    const nav = document.querySelector('#sidebar');
    const navButton = document.querySelector('header .sidebar-button');

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
    }
}

const onToggleMenu = () => {
    const nav = document.querySelector('#sidebar')
    if(nav.classList.contains('active')){
        nav.classList.remove('active');
    }else{
        nav.classList.add('active');
    }
}

const onLoad = () => {
    onResize();
    const navButton = document.querySelector('header .sidebar-button');
    navButton.addEventListener('click', onToggleMenu)
}

window.addEventListener('resize', onResize)
window.addEventListener('load', onLoad)
