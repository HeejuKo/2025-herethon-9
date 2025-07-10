const form = document.getElementById('profileForm');
const nicknameInput = document.getElementById('nickname');
const bioInput = document.getElementById('bio');
const nicknameError = document.getElementById('nicknameError');
const bioError = document.getElementById('bioError');

form.addEventListener('submit', async function(e) {
  e.preventDefault();

  let isValid = true;

  const nickname = nicknameInput.value.trim();
  const bio = bioInput.value.trim();

  if (nickname === "" || nickname.length > 10) {
    nicknameError.textContent = "닉네임이 올바르지 않습니다!";
    isValid = false;
  } else {
    nicknameError.textContent = "";
  }

  if (bio === "" || bio.length > 200) {
    bioError.textContent = "길이가 올바르지 않습니다!";
    isValid = false;
  } else {
    bioError.textContent = "";
  }

  if (!isValid) {
    return;
  }

  // 선택된 역할 불러오기 (세번째 페이지에서 저장한 값)
  const role = localStorage.getItem('role') || 'customer';

  try {
    const response = await fetch('/api/profile/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        nickname,
        bio,
        role
      })
    });

    if (!response.ok) {
      throw new Error('서버 오류가 발생했습니다.');
    }

    const result = await response.json();

    if (result.success) {
      alert('프로필 정보가 저장되었습니다!');
      window.location.href = "complete.html";
    } else {
      alert('저장에 실패했습니다.');
    }
  } catch (error) {
    alert(error.message);
  }
});

// 뒤로가기 버튼 클릭 이벤트
const backButton = document.querySelector('.back-button');
backButton.addEventListener('click', () => {
  window.location.href = "purpose.html";
});
