const form = document.getElementById('signup-form');
const idInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const passwordConfirmInput = document.getElementById('passwordConfirm');
const phoneInput = document.getElementById('phone');
const emailInput = document.getElementById('email');
const submitButton = document.getElementById('submit-button');

const idError = document.getElementById('id-error');
const passwordError = document.getElementById('password-error');
const contactError = document.getElementById('contact-error');


// 터치 상태
let touched = {
  id: false,
  password: false,
  passwordConfirm: false,
  phone: false,
  email: false,
};


function validate() {
  let idValid = true;
  let passwordValid = true;
  let contactValid = true;

  // ID
  const idValue = idInput.value.trim();
  if (touched.id) {
    if (!/^[a-zA-Z0-9]{6,20}$/.test(idValue)) {
      idError.textContent = '아이디가 올바르지 않습니다!';
      idValid = false;
    } else {
      idError.textContent = '';
    }
  } else {
    idError.textContent = '';
    idValid = false;
  }

  // Password
  const pwValue = passwordInput.value.trim();
  const pwConfirmValue = passwordConfirmInput.value.trim();
  if (touched.password || touched.passwordConfirm) {
    if (!/^(?=.*[a-zA-Z])(?=.*\d).{8,20}$/.test(pwValue)) {
      passwordError.textContent = '비밀번호가 올바르지 않습니다!';
      passwordValid = false;
    } else if (pwValue !== pwConfirmValue) {
      passwordError.textContent = '비밀번호가 일치하지 않습니다!';
      passwordValid = false;
    } else {
      passwordError.textContent = '';
    }
  } else {
    passwordError.textContent = '';
    passwordValid = false;
  }

  // Contact
  const phoneValue = phoneInput.value.trim();
  const emailValue = emailInput.value.trim();
  let phoneValid = false;
  let emailValid = false;

  if (touched.phone) {
    if (/^\d{11}$/.test(phoneValue)) {
      phoneValid = true;
    } else {
      phoneValid = false;
    }
  }

  if (touched.email) {
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailValue)) {
      emailValid = true;
    } else {
      emailValid = false;
    }
  }

  // 연락처 검증 로직: 둘 다 유효해야 통과
  if (!touched.phone && !touched.email) {
    contactError.textContent = '';
    contactValid = false;
  } else if (!phoneValid && !emailValid) {
    contactError.textContent = '휴대폰 번호와 이메일을 올바르게 입력해주세요!';
    contactValid = false;
  } else if (!phoneValid) {
    contactError.textContent = '휴대폰 번호를 올바르게 입력해주세요!';
    contactValid = false;
  } else if (!emailValid) {
    contactError.textContent = '이메일을 올바르게 입력해주세요!';
    contactValid = false;
  } else {
    contactError.textContent = '';
    contactValid = true;
  }

  // 버튼 상태
  if (idValid && passwordValid && contactValid) {
    submitButton.disabled = false;
    submitButton.classList.add('enabled');
  } else {
    submitButton.disabled = true;
    submitButton.classList.remove('enabled');
  }
}

// 터치 처리
function markTouched(field) {
  touched[field] = true;
  validate();
}

// 입력 이벤트
idInput.addEventListener('input', validate);
passwordInput.addEventListener('input', validate);
passwordConfirmInput.addEventListener('input', validate);
emailInput.addEventListener('input', validate);
phoneInput.addEventListener('input', () => {
  // 숫자만 입력 + 11자리 제한
  phoneInput.value = phoneInput.value.replace(/\D/g, '').slice(0, 11);
  validate();
});

// 포커스 아웃 시 터치 처리
idInput.addEventListener('blur', () => markTouched('id'));
passwordInput.addEventListener('blur', () => markTouched('password'));
passwordConfirmInput.addEventListener('blur', () => markTouched('passwordConfirm'));
phoneInput.addEventListener('blur', () => markTouched('phone'));
emailInput.addEventListener('blur', () => markTouched('email'));

// // 제출 이벤트
// form.addEventListener('submit', function(e) {
//   e.preventDefault();
//   validate(); // 마지막 검증

//   if (submitButton.disabled === false) {
//     // 페이지 이동
//     window.location.href = "verify.html";
//   } else {
//     alert('입력값을 다시 확인해주세요.');
//   }
// });

