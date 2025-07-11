const photoEditBtn = document.getElementById('photoEditBtn');
const photoModal = document.getElementById('photoModal');
const uploadBtn = document.getElementById('uploadBtn');
const deleteBtn = document.getElementById('deleteBtn');
const cancelBtn = document.getElementById('cancelBtn');
let hiddenFileInput = document.getElementById('hiddenFileInput');
const profilePhoto = document.getElementById('profilePhoto');
const deleteProfileFlag = document.getElementById('deleteProfileFlag');


const form = document.getElementById('profileForm');
const confirmModal = document.getElementById('confirmModal');
const confirmYes = document.getElementById('confirmYes');
const confirmNo = document.getElementById('confirmNo');

const nicknameInput = document.getElementById('nickname');
const phoneInput = document.getElementById('phone');
const emailInput = document.getElementById('email');
const bioTextarea = document.getElementById('bio');

const openModalBtn = document.querySelector('.save-button');

let isDirty = false;


// 값 변경 체크
[nicknameInput, phoneInput, emailInput, bioTextarea, hiddenFileInput].forEach(input => {
  input.addEventListener('input', () => {
    isDirty = true;
  });
});

document.querySelectorAll('.label-edit-icon').forEach((icon) => {
  icon.addEventListener('click', () => {
    const container = icon.closest('.info-block, .bio-block');
    const input = container.querySelector('input, textarea');
    if (input) {
      input.removeAttribute('readonly');  
      input.focus();
      const length = input.value.length;
      input.setSelectionRange(length, length); 
    }
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
function attachChangeListenerToInput(input) {
  input.addEventListener('change', () => {
    const file = input.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = e => {
        profilePhoto.src = e.target.result;
      };
      reader.readAsDataURL(file);
      deleteProfileFlag.value = "false"; 
    }
    photoModal.style.display = 'none';
    isDirty = true;
  });
}

// 초기 연결
attachChangeListenerToInput(hiddenFileInput);

// 삭제 버튼
deleteBtn.addEventListener('click', () => {
  const newInput = hiddenFileInput.cloneNode(true);
  hiddenFileInput.parentNode.replaceChild(newInput, hiddenFileInput);
  hiddenFileInput = newInput;
  attachChangeListenerToInput(hiddenFileInput);

  profilePhoto.src = "/static/img/basic_profile.svg";
  deleteProfileFlag.value = "true";
  photoModal.style.display = 'none';
  isDirty = true;
});


openModalBtn.addEventListener('click', () => {
  confirmModal.style.display = 'flex';
});

confirmYes.addEventListener('click', () => {
  confirmModal.style.display = 'none';
});

confirmNo.addEventListener('click', () => {
  confirmModal.style.display = 'none'; 
});