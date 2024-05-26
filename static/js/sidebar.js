const onResize = () => {

    const nav = document.querySelector('nav.sidebar');
    const forceSidebar = nav.classList.contains('force-sidebar');
    const navButton = document.querySelector('header nav .sidebar-button');

    if(forceSidebar || document.body.clientWidth < 800){ // Sidebar view
        if(!nav.hasClass('hamburger')){ // Back to the Hamburger view
            globalNav.animate({left: -400}, 0);
            globalNav.addClass('nav-hide'); // Add hide nav info
            nav.addClass('hamburger'); // Add condensed nav info
        }

    }else{ // Header view
        globalNav.animate({left: 400}, 0);
        navButton.removeClass('hamburger');

    }
}

window.addEventListener('resize', onResize)
onResize()
