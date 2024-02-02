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

    const expand_element = (parent,element, display) => {
        
        element.style.display = display;
        element.style.height = 'auto'; // Set height to auto temporarily
        const computedHeight = window.getComputedStyle(element).getPropertyValue('height'); // Get computed height
        element.style.height = '0px'; 

        setTimeout(() => {
            element.style.height = computedHeight; 
            parent.textContent = parent.textContent.replace('+', '-');
        }, 200); 
        
    };
    
    const contract_element = (parent, element)=>{
        
        element.style.height = '0px';
        setTimeout(()=>{
            parent.textContent = parent.textContent.replace('-', '+');
            element.style.display = 'none';
        }, 200)
    };

    shopbytype_btn.addEventListener('click', ()=>{
        if (shopbytype_content.style.display == 'flex') {
            contract_element(shopbytype_btn ,shopbytype_content);
        } else {expand_element(shopbytype_btn ,shopbytype_content, 'flex')}
    });
    shopbyanime_btn.addEventListener('click', ()=>{
        if (shopbyanime_content.style.display == 'flex') {
            contract_element(shopbyanime_btn, shopbyanime_content);
        } else {expand_element(shopbyanime_btn, shopbyanime_content, 'flex')}
    })

})