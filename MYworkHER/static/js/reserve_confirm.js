document.addEventListener("DOMContentLoaded", ()=>{
    const loginSection = document.getElementById("loginSection");
    const alarm = document.querySelector(".Alarm");

    const isLogin = true; //백에서 받아와야함
    const unreadChat = true; // 백에서 받아와야함

    if(loginSection){
        if(isLogin) {
            const logoutDiv = document.createElement("div");
            logoutDiv.textContent="로그아웃";
            logoutDiv.className = "Logout";
            loginSection.replaceWith(logoutDiv);
        }
        else{
            loginSection.style.display = "inline-flex";
        }
    }

    if(alarm){
        alarm.style.display = isLogin&&unreadChat ? "block" : "none";
    }

    const reviseBtn = document.querySelector(".Revise");
    if(reviseBtn){
        reviseBtn.addEventListener("click",()=>{
            window.location.href="../pages/reserve.html";
        });
    }

    const reserveConfirmContainer = document.querySelector(".ReserveConfirm");
    const completeContainer = document.querySelector(".Complete");

    const submitBtn = document.querySelector(".Submit");
    if(submitBtn){
        submitBtn.addEventListener("click",()=>{
            reserveConfirmContainer.style.display="none";
            completeContainer.style.display="flex";
        });
    }

    const homeBtn = document.querySelector(".C_Home");
    if(homeBtn){
            homeBtn.addEventListener("click",()=>{
            window.location.href="../index.html";
        });
    }
    
});