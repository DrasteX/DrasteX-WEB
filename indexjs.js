// Navigation Menu SCRIPTING
document.addEventListener('DOMContentLoaded', ()=>{
    // Mobile Navigation Menu Scripting
    const menu_container = document.querySelector('.navigation_menu_mob_container');
    const menu_open_btn = document.querySelector('.hammenu_btn');
    const menu_close_btn = document.querySelector('.close_btn');
    const content_container = document.querySelector('.content');

    const close_menu_fn = ()=>{
        menu_container.style.width = '0px';
        setTimeout(()=>{
            menu_container.style.display = 'none';
            content_container.classList.remove('overlay-visible');
            content_container.style.filter = 'brightness(1)';
        }, 200)
    }

    const open_menu_fn = ()=>{
        
        menu_container.style.display = 'flex';
        setTimeout(()=>{
            menu_container.style.width = '236px';
            content_container.classList.add('overlay-visible');
            content_container.style.filter = 'brightness(0.6)';
            
        }, 200)
    }

    menu_open_btn.onclick = open_menu_fn;
    menu_close_btn.onclick = close_menu_fn;

    window.onresize = close_menu_fn;

    document.addEventListener('click',(event)=>{
        const isClickInsideMenu = event.target.closest('.navigation_menu_mob_container') !== null;
        const isClickInsideButton = event.target.closest('.hammenu_btn') !== null || event.target.closest('.close_btn') !== null;
        
        if (!isClickInsideMenu && !isClickInsideButton) {
            close_menu_fn();
        }
    });

    const shopbytype_btn = document.querySelector('.shopbytype_title_mob');
    const shopbyanime_btn = document.querySelector('.shopbyanime_title_mob');

    const shopbytype_content = document.querySelector('.shopbytype_content_mob');
    const shopbyanime_content = document.querySelector('.shopbyanime_content_mob');

    const expand_element_mobile = (parent,element, display) => {
        
        element.style.display = display;
        element.style.height = 'auto'; 
        const computedHeight = window.getComputedStyle(element).getPropertyValue('height'); // Get computed height
        element.style.height = '0px'; 

        setTimeout(() => {
            element.style.height = computedHeight; 
            parent.textContent = parent.textContent.replace('+', '-');
        }, 200); 
        
    };
    
    const contract_element_mobile = (parent, element)=>{
        
        element.style.height = '0px';
        setTimeout(()=>{
            parent.textContent = parent.textContent.replace('-', '+');
            element.style.display = 'none';
        }, 200)
    };

    shopbytype_btn.addEventListener('click', ()=>{
        if (shopbytype_content.style.display == 'flex') {
            contract_element_mobile(shopbytype_btn ,shopbytype_content);
        } else {expand_element_mobile(shopbytype_btn ,shopbytype_content, 'flex')}
    });
    shopbyanime_btn.addEventListener('click', ()=>{
        if (shopbyanime_content.style.display == 'flex') {
            contract_element_mobile(shopbyanime_btn, shopbyanime_content);
        } else {expand_element_mobile(shopbyanime_btn, shopbyanime_content, 'flex')}
    })

    // DESKTOP NAV SETUP
    const shopby_container_desk = document.querySelector('.shopby_container_desktop');

    const shopbyanime_desk_btn = document.querySelector('.ShopByAnime_head');
    const shopbytype_desk_btn = document.querySelector('.ShopByType_head');

    const shopbyanime_container = document.querySelector('.shopbyanime_container_desk');
    const shopbytype_container = document.querySelector('.shopbytype_container_desk');

    const expand_element_desk = (btn, target) => {
        shopby_container_desk.style.display = "grid";
        target.style.display = "flex";
        setTimeout(() => {
            btn.textContent = btn.textContent.replace('+', '-');
            shopby_container_desk.style.height = "230px";
        }, 200);
    };

    const contract_element_desk = (btn, target) => {
        shopby_container_desk.style.height = "0px";
        setTimeout(() => {
            btn.textContent = btn.textContent.replace('-', '+');
            shopby_container_desk.style.display = "none";
            target.style.display = "none";
        }, 200);
    };

    const handle_click_outside_desk = (event) => {
        const isClickInsideContainersOrButtons = event.target.closest('.shopby_container_desktop') !== null || 
                                                event.target.closest('.ShopByAnime_head') !== null ||
                                                event.target.closest('.ShopByType_head') !== null;
                                                
        if (!isClickInsideContainersOrButtons && shopby_container_desk.style.display === "grid") {
            contract_element_desk(shopbyanime_desk_btn, shopbyanime_container);
            contract_element_desk(shopbytype_desk_btn, shopbytype_container);
        }
    };

    document.addEventListener('click', handle_click_outside_desk);

    
    shopbyanime_desk_btn.addEventListener('click', () => {
        if (shopbyanime_container.style.display === "flex") {
            contract_element_desk(shopbyanime_desk_btn, shopbyanime_container);
        } else {
            if (shopbytype_container.style.display === "flex") {
                contract_element_desk(shopbytype_desk_btn, shopbytype_container);
                setTimeout(()=>{
                    expand_element_desk(shopbyanime_desk_btn, shopbyanime_container);
                }, 200)
            } else {
                expand_element_desk(shopbyanime_desk_btn, shopbyanime_container);
            }
            
        }
    });

    shopbytype_desk_btn.addEventListener('click', () => {
        if (shopbytype_container.style.display === "flex") {
            contract_element_desk(shopbytype_desk_btn, shopbytype_container);
        } else {
            if (shopbyanime_container.style.display === "flex") {
                contract_element_desk(shopbyanime_desk_btn, shopbyanime_container);
                setTimeout(()=>{
                    expand_element_desk(shopbytype_desk_btn, shopbytype_container);
                }, 200)
            } else {expand_element_desk(shopbytype_desk_btn, shopbytype_container);}
            
        }
    });

    
});

document.addEventListener("DOMContentLoaded", function() {
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;
    
    function showSlide(n) {
        slides[currentSlide].style.left = '-100%';
        slides[n].style.left = '0';
        currentSlide = n;
        updateDots();
    }
    
    function nextSlide() {
        let next = (currentSlide + 1) % slides.length;
        showSlide(next);
    }
    
    function prevSlide() {
        let prev = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(prev);
    }
    
    function updateDots() {
        const dots = document.querySelectorAll('.dot');
        dots.forEach((dot, index) => {
            if (index === currentSlide) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }
    
    document.querySelectorAll('.next_slide').forEach(button => {
        button.addEventListener('click', nextSlide);
    });
    
    document.querySelectorAll('.prev_slide').forEach(button => {
        button.addEventListener('click', prevSlide);
    });
    
    document.querySelectorAll('.dot').forEach(dot => {
        dot.addEventListener('click', () => {
            showSlide(Array.from(dot.parentNode.children).indexOf(dot));
        });
    });
});


document.addEventListener("DOMContentLoaded", function() {
    // Hide the loading screen
    document.querySelector('.loading-screen').style.display = 'none';
    // Show the website content
    document.querySelector('.content').style.display = '';
});
