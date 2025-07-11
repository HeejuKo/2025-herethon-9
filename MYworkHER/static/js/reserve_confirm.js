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
            const expertId = reviseBtn.dataset.expertId;
            // 세션에 저장된 값이 이미 있으므로 expert_id만 넘김
            window.location.href = `/matching/${expertId}/edit/`;  // edit_matching 뷰를 호출
        });
    }

    const reserveConfirmContainer = document.querySelector(".ReserveConfirm");
    const completeContainer = document.querySelector(".Complete");

    // 예액 완료 여부 확인
    const isComplete = document.body.dataset.complete === "true";

    if (isComplete) {
        // 예약 완료 상태 : 확인 화면 숨기고 완료 화면만 보이게
        reserveConfirmContainer.style.display = "none";
        completeContainer.style.display = "flex";
    } else {
        // 예약 전 : 확인 화면만 보이고 완료 화면은 숨김
        reserveConfirmContainer.style.display = "block";
        completeContainer.style.display = "none";
    }

    const homeBtn = document.querySelector(".C_Home");
    if(homeBtn){
            homeBtn.addEventListener("click",()=>{
            window.location.href="../index.html";
        });
    }
    
});