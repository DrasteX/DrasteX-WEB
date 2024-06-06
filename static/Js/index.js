document.addEventListener("DOMContentLoaded",()=>{
    function Scroll_Functionality(scroller, left, right){
        right.addEventListener("mousedown",()=>{
            scroller.scrollLeft += 200;
        })
        
        left.addEventListener("mousedown",()=>{
            scroller.scrollLeft -= 200;
        })
    }
    console.log('h')

    const scrollers = document.querySelectorAll(".scroller_content")
    for (elements of scrollers) {
        if(elements.children.length < 1) {
            elements.parentElement.parentElement.style.display = "none"
        }
        
    }

    // NEW RELEASES
    Scroll_Functionality(document.getElementById("NEW_RELEASES_SCROLLER"), document.getElementById("NEW_RELEASES_LEFT"), document.getElementById("NEW_RELEASES_RIGHT"));
    // FEATURED PRODUCTS
    Scroll_Functionality(document.getElementById("FEATURED_PRODUCTS_SCROLLER"), document.getElementById("FEATURED_PRODUCTS_LEFT"), document.getElementById("FEATURED_PRODUCTS_RIGHT"));
    // SHOP BY ANIME
    Scroll_Functionality(document.getElementById("SHOP_BY_ANIME_SCROLLER"), document.getElementById("SHOP_BY_ANIME_LEFT"), document.getElementById("SHOP_BY_ANIME_RIGHT"));
    // SHOP BY TYPE
    Scroll_Functionality(document.getElementById("SHOP_BY_TYPE_SCROLLER"), document.getElementById("SHOP_BY_TYPE_LEFT"), document.getElementById("SHOP_BY_TYPE_RIGHT"));
})