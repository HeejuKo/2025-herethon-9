const cards = document.querySelectorAll('.card');
const doneButton = document.getElementById('doneButton');

let selectedRole = null;

cards.forEach(card => {
  card.addEventListener('click', () => {
    cards.forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
    selectedRole = card.dataset.role;
  });
});

doneButton.addEventListener('click', () => {
  if (!selectedRole) {
    alert('가입 목적을 선택해 주세요.');
    return;
  }

  // 로컬 스토리지에 역할 저장 (원하면)
  localStorage.setItem('role', selectedRole);

  // 다음 페이지 이동
  window.location.href = "profile.html";
});

// 뒤로가기 버튼 클릭 이벤트
const backButton = document.querySelector('.back-button');
backButton.addEventListener('click', () => {
  window.location.href = "verify.html";
});
