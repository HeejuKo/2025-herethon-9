document.addEventListener("DOMContentLoaded", ()=>{
    
const urlParams = new URLSearchParams(window.location.search);

    const categoryClass = urlParams.get("category");
    const categoryMap ={
        C1: "가전/수리",
        C2: "헬스/스포츠",
        C3: "컨설팅/비지니스",
        C4: "생활/라이프",
    };
    const category = categoryMap[categoryClass];
    const name = urlParams.get("name");
    const count = urlParams.get("count");

    const categoryImages = document.querySelectorAll(".Category div");

    categoryImages.forEach((el)=> el.classList.add("faded"));

    const selectCategory = document.querySelector(`.Category .${categoryClass}`);
    if(selectCategory){
        selectCategory.classList.remove("faded");
    }

    const resultText = document.querySelector(".ResultText");

    if(resultText){
        resultText.innerHTML=`
        <span class="BlueText">${category}</span>
        <span class="BlackText">></span>
        <span class="BlueText">${name}</span>
        <span class="BlackText"> 에 해당하는 </span>
        <span class="BlueText">${count}</span>
        <span class="BlackText">명의 전문가가 있습니다.</span>
    `;
    }

    const seoulDistricts = [
        "강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", 
        "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구",
        "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"
    ];

    const regionList = document.getElementById("RegionList");

    if(regionList){
        const regionTop = document.createElement("div");
        regionTop.className="RegionTop";

        const allLabel = document.createElement("label");
        allLabel.classList.add("custom-checkbox");

        const allInput = document.createElement("input");
        allInput.className="checkbox";
        allInput.type="checkbox";
        allInput.id = "checkAll";

        const allSpan = document.createElement("span");
        allSpan.className="checkmark";
        
        const allText = document.createElement("span");
        allText.className="checkbox-label";
        allText.textContent="서울시 전체";

        allLabel.appendChild(allInput);
        allLabel.appendChild(allSpan);
        allLabel.appendChild(allText);

        regionTop.appendChild(allLabel);

        const line = document.createElement("div");
        line.className="RegionLine";
        

        const regionGrid = document.createElement("div");
        regionGrid.className="RegionGrid";

        seoulDistricts.forEach((district)=> {
            const label = document.createElement("label");
            label.className="custom-checkbox";

            const input = document.createElement("input");
            input.className = "checkbox";
            input.type = "checkbox";
            input. value = district;

            const span = document.createElement("span");
            span.className = "checkmark";

            const textSpan = document.createElement("span");
            textSpan.className="checkbox-label";
            textSpan.textContent = district;

            input.addEventListener("change", ()=> {
                textSpan.style.color = input.checked ? "#0D5BDA" : "#000";
                textSpan.style.fontWeight = input.checked ? "600" : "400";

                updateRegionButtonStyle();
            })

            label.appendChild(input);
            label.appendChild(span);
            label.appendChild(textSpan);

            regionGrid.appendChild(label);
        });

        regionList.appendChild(regionTop);
        regionList.appendChild(line);
        regionList.appendChild(regionGrid);

        allInput.addEventListener("change", ()=> {
            const checkboxes = regionList.querySelectorAll(`input[type="checkbox"]:not(#checkAll)`);
            checkboxes.forEach((cb)=>
                cb.checked=allInput.checked
            );
            
            const labels = document.querySelectorAll(".custom-checkbox");
            labels.forEach((label)=>{
                const input = label.querySelector(`input[type=checkbox]`);
                const labelText = label.querySelector(".checkbox-label");
                if(labelText){
                    labelText.style.color = allInput.checked ? "#0D5BDA" : "#000";
                    labelText.style.fontWeight = allInput.checked ? "600" : "400";
                }

            });

            const allText = allLabel.querySelector(".checkbox-label");
            if(allText){
                allText.style.color = allInput.checked  ? "#0D5BDA" : "#000";
                allText.style.fontWeight = allInput.checked  ? "600" : "400";

                updateRegionButtonStyle();
             }

        });
        
    }

    const regionBtn = document.querySelector(".Region");
    const regionCheck = document.querySelector(".Regioncheck");

    regionBtn.addEventListener("click",()=>{
        if(regionCheck.style.display==="none"||regionCheck.style.display===""){
            regionCheck.style.display = "block";
        }else{
            regionCheck.style.display = "none";
        }
    })

    const workChoice=["1년 이하", "1년~3년", "3년~5년", "5년 이상"];
    const workList = document.querySelector(".WorkCheck");

    if(workList){
        const workTop = document.createElement("div");
        workTop.className = "WorkTop";

        const topLabel = document.createElement("label");
        topLabel.className = "custom-checkbox";

        const topInput = document.createElement("input");
        topInput.className = "checkbox";
        topInput.type="checkbox";

        const topCheckmark = document.createElement("span");
        topCheckmark.className = "checkmark";

        const topText = document.createElement("span");
        topText.className = "checkbox-label";
        topText.textContent="경력 무관";
        
        topInput.addEventListener("change", () => {
            topText.style.color = topInput.checked ? "#0D5BDA" : "#000";
            topText.style.fontWeight = topInput.checked ? "600" : "400";

            updateWorkButtonStyle();
        })

        topLabel.appendChild(topInput);
        topLabel.appendChild(topCheckmark);
        topLabel.appendChild(topText);
        workTop.appendChild(topLabel);
        workList.appendChild(workTop);

        const workLine = document.createElement("div");
        workLine.className = "WorkLine";
        workList.appendChild(workLine);

        workChoice.forEach((choice) => {
            const label = document.createElement("label");
            label.className = "custom-checkbox";

            const input = document.createElement("input");
            input.className = "checkbox";
            input.type="checkbox";
            input.value = choice;

            const checkmark = document.createElement("span");
            checkmark.className = "checkmark";

            const textSpan = document.createElement("span");
            textSpan.className="checkbox-label";
            textSpan.textContent = choice;

            input.addEventListener("change", () => {
                textSpan.style.color = input.checked ? "#0D5BDA" : "#000";
                textSpan.style.fontWeight = input.checked ? "600" : "400";
                updateWorkButtonStyle();
            })

            label.appendChild(input);
            label.appendChild(checkmark);
            label.appendChild(textSpan);

            workList.appendChild(label);
        });
    }

    const workBtn = document.querySelector(".Work");
    const workCheck = document.querySelector(".WorkCheck");

    workBtn.addEventListener("click", ()=>{
        if(workCheck.style.display==="none"||workCheck.style.display===""){
            workCheck.style.display = "flex";
        }else{
            workCheck.style.display="none";
        }

    });


    const badgeList = document.querySelector(".BadgeCheck");

    if(badgeList){
        const badgeTop = document.createElement("div");
        badgeTop.className = "BadgeTop";

        const topLabel = document.createElement("label");
        topLabel.className = "custom-checkbox";

        const topInput = document.createElement("input");
        topInput.className = "checkbox";
        topInput.type="checkbox";

        const topCheckmark = document.createElement("span");
        topCheckmark.className = "checkmark";

        const topText = document.createElement("span");
        topText.className = "checkbox-label";
        topText.textContent="전체";

        topLabel.appendChild(topInput);
        topLabel.appendChild(topCheckmark);
        topLabel.appendChild(topText);
        badgeTop.appendChild(topLabel);
        badgeList.appendChild(badgeTop);

        const badgeLine = document.createElement("div");
        badgeLine.className="BadgeLine";
        badgeList.appendChild(badgeLine);

        const label = document.createElement("label");
        label.className = "custom-checkbox";

        const input = document.createElement("input");
        input.className = "checkbox";
        input.type = "checkbox";
        
        const checkmark = document.createElement("span");
        checkmark.className = "checkmark";
    
        const textSpan = document.createElement("span");
        textSpan.className="checkbox-label";
        textSpan.textContent = "인증배지 보유";

        input.addEventListener("change", ()=> {
            textSpan.style.color = input.checked ? "#0D5BDA" : "#000";
            textSpan.style.fontWeight = input.checked ? "600" : "400";

            updateBadgeButtonStyle();
        });

        label.appendChild(input);
        label.appendChild(checkmark);
        label.appendChild(textSpan);
        badgeList.appendChild(label);

        const badgeBtn = document.querySelector(".Badge");
        const badgeCheck = document.querySelector(".BadgeCheck");

        badgeBtn.addEventListener("click",()=>{
            if(badgeCheck.style.display==="none"||badgeCheck.style.display===""){
                badgeCheck.style.display = "block";
            }else{
                badgeCheck.style.display = "none";
            }
        })
    }

    function updateRegionButtonStyle() {
        const regionBtn = document.querySelector(".Region");
        const checkedBoxes = document.querySelectorAll(`#RegionList input[type="checkbox"]:checked`);

        if(checkedBoxes.length>0){
            regionBtn.style.color="#0D5BDA";
        }else{
            regionBtn.style.color = "#000";
        }
    }

    function updateWorkButtonStyle() {
        const workBtn = document.querySelector(".Work");
        const checkedBoxes = document.querySelectorAll(`.WorkCheck input[type=checkbox]:checked`);

        if(checkedBoxes.length>0){
            workBtn.style.color="#0D5BDA";
        }else{
            workBtn.style.color="#000";
        }
    }

    function updateBadgeButtonStyle(){
        const badgeBtn = document.querySelector(".Badge");
        const checkedBoxes = document.querySelectorAll(`.BadgeCheck input[type=checkbox]:checked`);

        if(checkedBoxes.length>0){
            badgeBtn.style.color="#0D5BDA";
        }else{
            badgeBtn.style.color="#000";
        }
        
    }

    const experts = [
        {
            nickname: "전문가 닉네임",
            introduce: "한줄소개 한줄소개 한줄소개",
            description: "업무설명 업무설명업무설명 업무설명업무설명 업무설명...",
            hasBadge: true
        },
        {
            nickname: "홍길동 전문가",
            introduce: "10년차 운동전문가",
            description: "헬스트레이닝, 요가, 필라테스, 운동 루틴 설계 및 식단 코칭",
            hasBadge: false
        },
        {
            nickname: "김영희 전문가",
            introduce: "가전 수리 경력 15년",
            description: "에어컨, 세탁기, 냉장고 수리 전문. 친절한 서비스 제공.",
            hasBadge: true
        },
        {
            nickname: "이철수 전문가",
            introduce: "비즈니스 컨설팅 전문가",
            description: "스타트업 경영 전략, 마케팅 플랜, 팀 조직 구조 설계 지원.",
            hasBadge: false
        },
        {
            nickname: "박지은 전문가",
            introduce: "생활 코칭 전문가",
            description: "시간 관리, 정리 정돈, 효율적인 일상 루틴 설계 도와드립니다.",
            hasBadge: true
        },
        {
            nickname: "조민수 전문가",
            introduce: "헬스/필라테스 트레이너",
            description: "개인 맞춤 운동 플랜 제공. 체형 교정 및 다이어트 특화.",
            hasBadge: false
        },
        {
            nickname: "정가은 전문가",
            introduce: "정수기 설치 전문가",
            description: "깔끔하고 빠른 설치 보장, 수질 개선 상담까지 함께.",
            hasBadge: true
        }

    ];

    const expertContainer = document.querySelector(".ExpertBoxes");

    let isShowAll = false;
    const defaultShowNum=5;

    function makeExperts(experts){
        expertContainer.innerHTML ="";

        const showExperts = isShowAll ? experts: experts.slice(0,defaultShowNum)

        showExperts.forEach((expert)=>{
            const box = document.createElement("div");
            box.className = "ExpertBox";

            const profileImg = document.createElement("img");
            profileImg.className="img";
            profileImg.src = "../assets/img/profile.svg";
            profileImg.alt = "profile";
            profileImg.width= 74;
            
            const expertInfo = document.createElement("div");
            expertInfo.className = "ExpertInfo";
            
            const nicknameDiv = document.createElement("div");
            nicknameDiv.className ="NicknameDiv";

            const nickname = document.createElement("div");
            nickname.className = "Nickname";
            nickname.textContent = expert.nickname;
            
            nicknameDiv.appendChild(nickname);

            if(expert.hasBadge){
                const badge = document.createElement("img");
                badge.src="../assets/img/badgeicon.svg";
                badge.alt="badge"
                badge.width=33;
                badge.className="BadgeIcon"
                nicknameDiv.appendChild(badge);
            }

            const introduce = document.createElement("div");
            introduce.className="Introduce";
            introduce.textContent=expert.introduce;

            const description = document.createElement("div");
            description.className = "Description";
            description.textContent = expert.description;

            expertInfo.appendChild(nicknameDiv);
            expertInfo.appendChild(introduce);
            expertInfo.appendChild(description);
            
            box.appendChild(profileImg);
            box.appendChild(expertInfo);
            
            box.addEventListener("click",()=>{
                window.location.href="./expert_detail.html?name="+encodeURIComponent(expert.nickname);
            })
            expertContainer.appendChild(box);
        });
    }

  

    makeExperts(experts);

    const showCount = document.querySelector(".Count");
    showCount.textContent=count;

    const showAllBtn = document.querySelector(".ShowAllBtn");
    showAllBtn.addEventListener("click", () => {
        isShowAll = isShowAll ? false :  true;
        makeExperts(experts);
    })
}); 