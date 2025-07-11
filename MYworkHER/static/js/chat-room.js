const chatInput = document.getElementById('chatInput');
  const chatForm = document.getElementById('chatForm');

  chatInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();  // 줄바꿈 방지
      chatForm.submit();   // 폼 제출
    }
  });

  // 클라이언트: 희주... 제작자: 진경... RESPECT...