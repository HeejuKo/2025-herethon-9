const fileInput = document.getElementById('fileInput');
const confirmButton = document.getElementById('confirmButton');
const uploadBox = document.querySelector('.upload-box');

// 파일 선택 시 미리보기
fileInput.addEventListener('change', () => {
  if (fileInput.files && fileInput.files[0]) {
    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
      uploadBox.innerHTML = `
        <img src="${e.target.result}" alt="신분증 미리보기" class="preview-image" />
      `;
    };
    reader.readAsDataURL(file);
  }
});

// 확인 버튼 클릭
confirmButton.addEventListener('click', () => {
  if (!fileInput.files || fileInput.files.length === 0) {
    alert('신분증 이미지를 업로드해 주세요.');
    return;
  }
  // 인증 성공 후 페이지 이동
  window.location.href = "purpose.html";
});

// 뒤로가기 버튼 클릭
const backButton = document.querySelector('.back-button');
backButton.addEventListener('click', () => {
  window.location.href = "signup.html";
});
