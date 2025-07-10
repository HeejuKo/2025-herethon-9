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
    for (let hour = 9; hour <= 20; hour++) {
        const formattedHour = hour.toString().padStart(2, '0');
        allTime.push(`${formattedHour}:00`);
    }

    const selectedTimes = JSON.parse(document.getElementById("timesInput")?.value
        ? `["${document.getElementById("timesInput").value.split(',').join('","')}"]`
        : "[]");

    const timeContainer = document.querySelector(".TimeBtnBox");
    const timesInput = document.getElementById("timesInput");

    timeContainer.innerHTML = ""; // 기존 버튼 제거 (중복 방지)

    allTime.forEach(time => {
        const btn = document.createElement("button");
        btn.textContent = time;
        btn.className = "TimeBtn";
        btn.type = "button";

        // 예약을 수정할 경우 이전에 선택했던 시간들이 반영됨
        if (selectedTimes.includes(time)) {
            btn.classList.add("selected");
        }

        // 클릭 시 toggle 및 hidden input 갱신
        btn.addEventListener("click", () => {
            btn.classList.toggle("selected");

            const selected = Array.from(document.querySelectorAll('.TimeBtn.selected'))
                .map(b => b.textContent);

            if (timesInput) {
                timesInput.value = selected.join(",");
            }
        });

        timeContainer.appendChild(btn);
    });

    // 최초 로드 시 input 값 업데이트
    if (timesInput) {
        timesInput.value = selectedTimes.join(",");
    }



    
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