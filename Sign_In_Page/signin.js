document.addEventListener('DOMContentLoaded', ()=>{

    const lefthyper = document.querySelector("#left_hyper");
    const righthyper = document.querySelector("#right_hyper");
    const middletext = document.querySelector("#middletext");
    const confirmpass_holder = document.querySelector(".Confirm_Password_Holder");
    const uporin = document.querySelector("#main_title_switch_item");
    const submitbtn = document.querySelector("#Submit");
    
    function switch_to_signin () {
        
        uporin.textContent = "IN";
        confirmpass_holder.style.display = "none";
        middletext.textContent = "Or Sign In Using";
        lefthyper.textContent = "Register Here";
        righthyper.textContent = "Forgot Password?";
        submitbtn.value = "Login";
        document.querySelector("#Confirm").removeAttribute("required");
        lefthyper.onclick = switch_to_signup;
    
    }
    
    function switch_to_signup () {
        document.querySelector("#Confirm").setAttribute("required",'');
        uporin.textContent = "UP";
        confirmpass_holder.style.display = "flex";
        middletext.textContent = "Or Sign Up Using";
        lefthyper.textContent = "Login Here";
        righthyper.textContent = "Need Help?";
        submitbtn.value = "Sign Up";
        lefthyper.onclick = switch_to_signin;
    
    }

    lefthyper.onclick = switch_to_signin;
        
    
    const pass = document.querySelector("#Password");
    const confirmpass = document.querySelector("#Confirm")

    const passvisibility = document.querySelector("#passvisibility");
    const confirmpassvisibility = document.querySelector("#confirmpassvisibility");
    
    function pass_vb_switch(ele, btn){
        if (ele.type == "password") {
            ele.type = "text";
            btn.src = "..\\Assets\\Components\\Eye_crossed_icon.png";
        } else {
            ele.type = "password";
            btn.src = "..\\Assets\\Components\\Eye_icon.png";
        }
    }

    passvisibility.onclick = ()=>{
        pass_vb_switch(pass, passvisibility)
    };
    confirmpassvisibility.onclick = ()=>{
        pass_vb_switch(confirmpass, confirmpassvisibility)
    }

})
