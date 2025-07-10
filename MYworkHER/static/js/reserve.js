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

    const choiceBtn = document.querySelector(".ChoiceBtn");
    const datePicker = document.getElementById("datePicker");
    const choiceDayBox = document.querySelector(".ChoiceDay");

    const selectedDates = new Set();

    choiceBtn.addEventListener("click",()=>{
        datePicker.style.display="flex";
        datePicker.click();
    });

    datePicker.addEventListener("change", () => {
        const selectedDate = datePicker.value;
        if(!selectedDate) return;

        datePicker.style.display="none";

        if(selectedDates.has(selectedDate)){
            alert("이미 선택된 날짜입니다.");
            return;
        }

        selectedDates.add(selectedDate);

        const [year,month,day] = selectedDate.split("-");
        const formmatedDate =`${year}년 ${parseInt(month)}월 ${parseInt(day)}일`;
       

        const dateDiv = document.createElement("div");
        dateDiv.className="SelectedDate";
        dateDiv.textContent=formmatedDate;

        dateDiv.addEventListener("click",()=>{
            const confirmDelete = confirm("이 날짜를 삭제할까요?");
            if(confirmDelete){
                selectedDates.delete(selectedDate);
                dateDiv.remove();
            }
        });
        
        choiceDayBox.insertBefore(dateDiv,choiceBtn);
    });

    const allTime = [];

    for(let hour=9;hour<=20;hour++){
        const formmatedHour = hour.toString().padStart(2,'0');
        allTime.push(`${formmatedHour}:00`);
    }

    const timeContainer = document.querySelector(".TimeBtnBox");
    allTime.forEach(time=>{
        const btn = document.createElement("button");
        btn.textContent=time;
        btn.className="TimeBtn";
        btn.type = "button"; // 새로고침 방지

        btn.addEventListener("click",()=>{
           btn.classList.toggle("selected");
        })

        timeContainer.append(btn);
    });

    
    const reserveBtn = document.querySelector(".ReserveBtn");
    
    reserveBtn.addEventListener("click",()=>{
        const requestText = document.querySelector(".Request").value;
        const selectedTimes=Array.from(document.querySelectorAll(".TimeBtn.selected")).map(btn=>btn.textContent);
        const expertId = document.querySelector("input[name='expert_id']")?.value;

        if(selectedDates.size===0){
            alert("예약할 날짜를 최소 한 개 이상 선택해주세요.");
            return;
        }

        if(selectedTimes.length===0){
            alert("예약할 시간을 최소 한 개 이상 선택해 주세요.");
            return;
        }

        if (!expertId) {
            alert("전문가 정보가 누락되었습니다.");
            return;
        }

        // hidden input에 값 채워 넣기
        document.getElementById("datesInput").value = Array.from(selectedDates).join(",");
        document.getElementById("timesInput").value = selectedTimes.join(",");

        // form 제출
        document.getElementById("matchingForm").submit();
    })
  
});