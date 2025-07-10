window.addEventListener('DOMContentLoaded', () => {
  fetch('../components/admin-navbar.html')
    .then(res => res.text())
    .then(html => {

      document.getElementById('navbar').innerHTML = html;


      const logoutBtn = document.querySelector(".logout-btn");
      if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
          window.location.href = "../pages/login.html";
        });
      }
    });
});
