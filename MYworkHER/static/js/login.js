// 테스트용: 폼 제출 막기 (실제 연동 시 제거)
document.getElementById('login-form').addEventListener('submit', function(e) {
  e.preventDefault();
  alert('로그인 처리 로직 연결 필요');
});
