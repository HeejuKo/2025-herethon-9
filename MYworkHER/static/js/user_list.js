// 무한 스크롤 예제 (더미)
let loading = false;

window.addEventListener("scroll", () => {
  if (loading) return;
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
    loading = true;
    // 실제로는 AJAX로 추가 데이터 로드
    const list = document.getElementById("userList");
    for (let i = 0; i < 3; i++) {
      const li = document.createElement("li");
      li.className = "user-card";
      li.innerHTML = `
        <a href="#">
          <span class="status status-pending">인증 대기</span>
          <span class="user-info">아이디 (닉네임)</span>
          <img src="../assets/img/search-icon.svg" alt="상세보기" class="search-icon">
        </a>`;
      list.appendChild(li);
    }
    setTimeout(() => {
      loading = false;
    }, 500);
  }
});
