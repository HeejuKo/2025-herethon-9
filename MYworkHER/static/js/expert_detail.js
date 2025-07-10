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
    
    const backBtn = document.querySelector(".Back");
    backBtn.addEventListener("click",()=>{
        history.back();
    });

    const reserveBtn = document.querySelector(".Reserve")
    reserveBtn.addEventListener("click",()=>{
        if(!isLogin){
            alert("로그인이 필요합니다.");
            return;
        }
        window.location.href="../pages/reserve.html";
    });

});