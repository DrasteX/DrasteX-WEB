document.addEventListener("DOMContentLoaded",()=>{
    const scrl_right_scroller = document.querySelector(".right_control_scroller");
    const scrl_left_scroller = document.querySelector(".left_control_scroller");
    const scrl_content_scroller = document.querySelector(".scroller_content");
    scrl_right_scroller.addEventListener("mousedown",()=>{
        scrl_content_scroller.scrollLeft += 200;
    })
    
    scrl_left_scroller.addEventListener("mousedown",()=>{
        scrl_content_scroller.scrollLeft -= 200;
    })
})