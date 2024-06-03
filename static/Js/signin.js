document.addEventListener('DOMContentLoaded', ()=>{
    document.getElementById("footer_id_for_removing").remove()
    document.getElementById("header_id_for_removing").remove()

    const pass = document.querySelector("#password");
    const confirmpass = document.querySelector("#Confirm")

    const passvisibility = document.querySelector("#passvisibility");
    const confirmpassvisibility = document.querySelector("#confirmpassvisibility");
    
    function pass_vb_switch(ele, btn){
        if (ele.type == "password") {
            ele.type = "text";
            btn.src = "static\\Assets\\Components\\Eye_crossed_icon.png";
        } else {
            ele.type = "password";
            btn.src = "static\\Assets\\Components\\Eye_icon.png";
        }
    }

    passvisibility.onclick = ()=>{
        pass_vb_switch(pass, passvisibility)
    };
    confirmpassvisibility.onclick = ()=>{
        pass_vb_switch(confirmpass, confirmpassvisibility)
    }

    
})
