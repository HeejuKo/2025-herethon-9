const photoEditBtn = document.getElementById('photoEditBtn');
const photoModal = document.getElementById('photoModal');
const uploadBtn = document.getElementById('uploadBtn');
const deleteBtn = document.getElementById('deleteBtn');
const cancelBtn = document.getElementById('cancelBtn');
const hiddenFileInput = document.getElementById('hiddenFileInput');
const profilePhoto = document.getElementById('profilePhoto');

const form = document.getElementById('profileForm');
const confirmModal = document.getElementById('confirmModal');
const confirmYes = document.getElementById('confirmYes');
const confirmNo = document.getElementById('confirmNo');

const nicknameInput = document.getElementById('nickname');
const phoneInput = document.getElementById('phone');
const emailInput = document.getElementById('email');
const bioTextarea = document.getElementById('bio');

let isDirty = false;

// 값 변경 체크
[nicknameInput, phoneInput, emailInput, bioTextarea, hiddenFileInput].forEach(input => {
  input.addEventListener('input', () => {
    isDirty = true;
  });
});

// 프로필 사진 수정 아이콘 클릭
photoEditBtn.addEventListener('click', () => {
  photoModal.style.display = 'flex';
});

// 모달 취소
cancelBtn.addEventListener('click', () => {
  photoModal.style.display = 'none';
});

// 업로드 버튼
uploadBtn.addEventListener('click', () => {
  hiddenFileInput.click();
});

// 파일 선택 시 미리보기
hiddenFileInput.addEventListener('change', () => {
  const file = hiddenFileInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = e => {
      profilePhoto.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
  photoModal.style.display = 'none';
  isDirty = true;
});

// 삭제 버튼
deleteBtn.addEventListener('click', () => {
  hiddenFileInput.value = '';
  profilePhoto.src = '../assets/img/profile.svg';
  photoModal.style.display = 'none';
  isDirty = true;
});

// 링크 이동 가로채기 (네비가 늦게 로드되는 문제 해결)
setTimeout(() => {
  document.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', e => {
      console.log("✅ 클릭됨", link.getAttribute('href'));
      if (isDirty) {
        console.log("✅ isDirty = true, 모달 열기");
        e.preventDefault();
        const href = link.getAttribute('href');
        confirmModal.style.display = 'flex';

        confirmYes.onclick = () => {
          console.log("✅ 네 클릭: 저장");
          isDirty = false;
          confirmModal.style.display = 'none';
          form.submit();
        };

        confirmNo.onclick = () => {
          console.log("✅ 아니오 클릭: 이동");
          isDirty = false;
          confirmModal.style.display = 'none';
          if (href) {
            window.location.href = href;
          }
        };
      }
    });
  });
}, 1000);
