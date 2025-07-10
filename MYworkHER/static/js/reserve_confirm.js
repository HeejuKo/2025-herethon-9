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

    const saved = localStorage.getItem("reservationData");
    if(!saved){
        alert("예약 정보가 없습니다.");
        return;
    }

    const data=JSON.parse(saved);
    const dayContainer = document.querySelector(".ChoiceDay");

    data.dates.forEach(date => {
        const [year, month, day] = date.split("-");
        const formatted = `${year}년 ${parseInt(month)}월 ${parseInt(day)}일`;

        const dateDiv = document.createElement("div");
        dateDiv.className = "SelectedDate";
        dateDiv.textContent = formatted;
        dayContainer.appendChild(dateDiv);

       
    });

    const timeContainer = document.querySelector(".TimeBtnBox");
    data.times.forEach(time => {
        const timeDiv = document.createElement("div");
        timeDiv.className="TimeBtn";
        timeDiv.textContent = time;

        timeContainer.appendChild(timeDiv);
    });

    const requestContainer = document.querySelector(".RequestText");
    requestContainer.textContent=data.request;


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