document.addEventListener("DOMContentLoaded", ()=>{
    const submitBtn = document.querySelector(".Submit");
    const withdrawBtn = document.querySelector(".Withdraw");
    submitBtn.addEventListener("click",()=>{
        submitBtn.style.border="2px solid #00B333";
        submitBtn.style.background="#FFF"
        submitBtn.style.color="#00B333"
        submitBtn.textContent="인증 해제"
        withdrawBtn.style.display="none";

        const user = mockData[currentIndex];
        user.isVerified = user.isVerified ? false : true;
        renderUser(user);
    });

    const mockData = [
    { nickname: "user1", email: "a@a.com", phone: "010-1234-0001", isVerified: false },
    { nickname: "user2", email: "b@b.com", phone: "010-1234-0002", isVerified: true },
    { nickname: "user3", email: "c@c.com", phone: "010-1234-0003", isVerified: false },
    { nickname: "user4", email: "d@d.com", phone: "010-1234-0004", isVerified: true },
    { nickname: "user5", email: "e@e.com", phone: "010-1234-0005", isVerified: false },
    ];

    function renderUser(data){
        document.querySelector(".Nickname").textContent=data.nickname;
        document.getElementById("email").textContent = data.email
        document.getElementById("phoneNum").textContent = data.phone;

        if(data.isVerified){
            submitBtn.style.border="2px solid #00B333";
            submitBtn.style.background="#FFF"
            submitBtn.style.color="#00B333"
            submitBtn.textContent="인증 해제"
            withdrawBtn.style.display="none";
        }else{
            submitBtn.textContent="인증 승인";
            submitBtn.style.border="none";
            submitBtn.style.background="#00B333";
            submitBtn.style.color="#FFF"
            withdrawBtn.style.display="inline-flex";
        }
    }

    const backBtn = document.querySelector(".Back");
    const nextBtn = document.querySelector(".Next");

    let currentIndex=0;

    backBtn.addEventListener("click",()=>{
        if(currentIndex>0){
            currentIndex--;
            renderUser(mockData[currentIndex]);
        }
    });

    nextBtn.addEventListener("click",()=>{
        if(currentIndex<mockData.length-1){
            currentIndex++;
            renderUser(mockData[currentIndex]);
        }
    });

    renderUser(mockData[currentIndex]);

});