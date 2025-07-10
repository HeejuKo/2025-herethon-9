document.addEventListener("DOMContentLoaded", () => {
  const loginSection = document.getElementById("loginSection");
  const alarm = document.querySelector(".Alarm");

  const isLogin = false; // 백엔드에서 받아오기
  const unreadChat = true; // 백엔드에서 받아오기

  if (loginSection) {
    if (isLogin) {
      const logoutDiv = document.createElement("div");
      logoutDiv.textContent = "로그아웃";
      logoutDiv.className = "Logout";
      loginSection.replaceWith(logoutDiv);
    } else {
      loginSection.style.display = "inline-flex";
    }
  }

  if (alarm) {
    alarm.style.display = isLogin && unreadChat ? "block" : "none";
  }
});
