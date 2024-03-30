document.addEventListener("DOMContentLoaded",()=>{
    // MOBILE MENU 

    const mobile_menu = document.querySelector(".nav_head");
    const mobile_menu_open_btn = document.querySelector("#menu_btn");
    const mobile_menu_close_btn = document.querySelector("#close_menu_btn");
    const body = document.querySelector("body");

    function toggle_nav(){
        if (mobile_menu.style.display == "flex") {
            mobile_menu.style.display = "none";
            
        } else {
            mobile_menu.style.display = "flex";
            
        }
    }
    
    mobile_menu_open_btn.onclick = toggle_nav;
    mobile_menu_close_btn.onclick = toggle_nav;

    // DESKTOP SHOPBY 

    const shopbyanime_btn = document.querySelector("#shopbyanime_btn");
    const shopbytype_btn = document.querySelector("#shopbytype_btn");
    const shopbyanime_overlay = document.querySelector(".shopbyanime_inner");
    const shopbytype_overlay = document.querySelector(".shopbytype_inner");

    shopbyanime_overlay.style.display = "none";
    shopbytype_overlay.style.display = "none";

    function close_overlay (ov) {

        ov.style.display = "none"
    }

    function open_overlay (ov, otherOV) {
        console.log("HI")
        if (window.innerWidth >= 901){close_overlay(otherOV);}
        
        ov.style.display = "block";
    }

    shopbyanime_btn.onclick = ()=>{
        if (shopbyanime_overlay.style.display == "none" ) {
            open_overlay(shopbyanime_overlay, shopbytype_overlay)
        } else {close_overlay(shopbyanime_overlay)}
        
    } 
    shopbytype_btn.onclick = ()=>{
        if (shopbytype_overlay.style.display == "none") {
            open_overlay(shopbytype_overlay, shopbyanime_overlay)
        } else {close_overlay(shopbytype_overlay)}
        
    } 
    

    // WINDOW LISTENSERS 
    
    window.addEventListener("click", (MouseEvent)=>{
        if (!shopbyanime_overlay.contains(MouseEvent.target) && !shopbytype_overlay.contains(MouseEvent.target) && !shopbyanime_btn.contains(MouseEvent.target) && !shopbytype_btn.contains(MouseEvent.target) && window.innerWidth >= 901) {
            close_overlay(shopbyanime_overlay);
            close_overlay(shopbytype_overlay);
        }

        if (MouseEvent.target != mobile_menu_open_btn && MouseEvent.target != mobile_menu && !mobile_menu.contains(MouseEvent.target) && window.innerWidth <= 900) {
            mobile_menu.style.display = "none";
        }
    })

    window.onresize = ()=>{
        if (window.innerWidth >= 901) {
            mobile_menu.style.display = "flex"
        } else {mobile_menu.style.display = "none"}

        close_overlay(shopbyanime_overlay);
        close_overlay(shopbytype_overlay);
    }
})