document.addEventListener("DOMContentLoaded", ()=>{
    
    const header = document.createElement("template");

    header.innerHTML = `<header>
    <div class="left_head">
        <img id="menu_btn" src="../../Assets/Components/Menu_Button_White.png">
        <img id="logo" src="../../Assets/LOGO/LOGO_forDarkBG.png">
    </div>

    <div class="nav_head">
        <button id="close_menu_btn"> <pre>🞀    Close Menu</pre> </button>
        <a href="#"> Catalog </a>
        <a id="shopbyanime_btn"> 🢖 Shop By Anime </a>
        <div class="shopbyanime_inner">
            <h3>Shop by Anime </h3>
            <ul>
                <li>One Piece</li>
                <li>Jujutsu Kaisen</li>
                <li>Chainsaw Man</li>
                <li>Hunter X Hunter</li>
                <li>Attack On Titan</li>
                <li>Naruto</li>
                <li>Bleach</li>
                <li>Dragon Ball Z</li>
                <li>Demon Slayer</li>
                <li>Solo Leveling</li>
            </ul>
        </div>
        <a id="shopbytype_btn"> 🢖 Shop By Type </a>
        <div class="shopbytype_inner">
            <h3>Shop by Type </h3>
            <ul>
                <li>T-Shirts</li>
                <li>Hoodies</li>
                <li>Caps</li>
                <li>Key Chains</li>
                <li>Rings</li>
                <li>Posters</li>
                <li>Stickers</li>
                <li>Sweatshirts</li>
            </ul>
        </div>
        <a href="#"> Review </a>
        <a href="#"> Contact Us </a>
    </div>
    
    <div class="right_head">
        <button onclick="location.href='../Sign_In_Page/signing.html'" id="signin_btn"> Sign In </button>
    </div>
</header>

<style>

/* U N I V E R S A L   D E S I G N I N G  */

body {
   background-color: #1a1a1a;
   margin: 0px;
   
}

* {
    font-family: Poppins;
}

button {
    cursor: pointer;
    &:active {
        scale: 0.95;
        
        transition: all 0.1s  ease-in-out;
    }
}


a {
    text-decoration: none;
    cursor: pointer;
}

::-webkit-scrollbar {display: none;}


/* Designing Header  */

header {
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    align-items: center;
    padding: 7px 20px;
}

    /* Left side of Header  */
.left_head {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-items: center;
    gap: 10px;
}

#logo {
    height: 55px
}

#menu_btn {
    height: 30px;
    display: none;
    cursor: pointer;
}

#close_menu_btn {

    display: none;
    padding: 7px 15px;
    font-size: medium;
    white-space: nowrap;
    border-radius: 20px;
    background-color: transparent;
    color: white;
    border: none;
    font-weight: bold;
    
    
    
    &:active {
        box-shadow: 0 0 0 1px white;
        
    }
    & > pre {
        margin: 0px;
    }
}

    /* Navigation Menu in Desktop */
.nav_head {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    white-space: nowrap;
    gap: 35px;
    

    & > a {
        color: white;
        font-weight: 500;
        
    }
}

#signin_btn {
    padding: 7px 15px;
    border: none;
    background-color: #D60000;
    color: white;
    border-radius: 10px;
    white-space: nowrap;
    font-weight: 700;
    
}

/* Shop By ------  >>  Overlay Designing  */

.shopbyanime_inner, .shopbytype_inner {
    color: white;
    position: absolute;
    display: none;
    
    width: 90%;
    left:  5%;
    right: 5%;
    top: 60px;
    padding: 30px;
    box-sizing: border-box;
    background-color: #1f1f1f;
    border-radius: 50px;

    & > h3 {
        margin: 0px 20px;
        font-size: x-large;
    }
    & > ul {
        max-height: 200px;
        width:fit-content;
        column-gap: 70px;
        row-gap: 10px;
        list-style: none;
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
        & > li {
            cursor: pointer;
           
        }
    }
}



/* M O B I L E      U I      D E S I G N I N G */

@media screen and (max-width: 900px) {
    

    #menu_btn, #close_menu_btn {
        display : inline-block
    }

    .nav_head {
        display: none;
        position:absolute;
        flex-direction: column;
        top: 0px;
        left: 0px;
        padding: 20px 40px 50px 30px;
        gap: 15px;
        background-color: #161616a6;
        backdrop-filter: blur(10px);

        max-height: fit-content;
        min-height: 100%;
        
        
        

        
    }

    .shopbyanime_inner, .shopbytype_inner {
        display: none;
        position: static;
        background-color: transparent;
        padding: 0px;

        & > h3 {
            display: none;
        }

        & > ul {
            flex-wrap: nowrap;
            max-height: none;
            padding-left: 20px;
            margin: 0px;
            row-gap: 7px;
            & > li {
                font-size: 15px;
                color: rgb(233, 233, 233)
            }
        }
    }
}
</style>
`

    document.body.appendChild(header.content);



    
    
});



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


