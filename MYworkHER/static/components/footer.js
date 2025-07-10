document.addEventListener("DOMContentLoaded", () => {
  // footer.html을 가져와서 id="footer-container" 자리에 넣기
  fetch("../components/footer.html")
    .then((res) => res.text())
    .then((html) => {
      document.getElementById("footer-container").innerHTML = html;
    });
});
window.addEventListener('scroll', () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
    console.log('맨 아래에 도달 - 데이터 더 불러오기');
    // 여기에 AJAX fetch 코드 작성
  }
});

