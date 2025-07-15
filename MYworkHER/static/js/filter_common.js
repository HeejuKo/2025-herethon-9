// document.addEventListener("DOMContentLoaded", function () {
//   // ✅ 모달 toggle
//   const toggleModal = (btnSelector, modalSelector, displayType = "block") => {
//     const btn = document.querySelector(btnSelector);
//     const modal = document.querySelector(modalSelector);
//     if (!btn || !modal) return;

//     btn.addEventListener("click", () => {
//       const isOpen = modal.style.display === displayType;
//       document.querySelectorAll(".Regioncheck, .WorkCheck, .BadgeCheck").forEach(el => el.style.display = "none");
//       modal.style.display = isOpen ? "none" : displayType;
//     });
//   };

//   toggleModal(".Region", ".Regioncheck");
//   toggleModal(".Work", ".WorkCheck", "flex");
//   toggleModal(".Badge", ".BadgeCheck");

//   // ✅ 상호 배제 체크박스 처리 (UI 상태만)
//   document.querySelectorAll('#expert-filter-form input[type="checkbox"]').forEach((checkbox) => {
//     checkbox.addEventListener('change', () => {
//       const name = checkbox.name;
//       const value = checkbox.value;

//       if (name === "badge_all" && checkbox.checked) {
//         document.getElementById("badge_true").checked = false;
//       }
//       if (name === "badge" && checkbox.checked) {
//         document.getElementById("badge_all").checked = false;
//       }

//       if (name === "experience" && value === "all") {
//         document.querySelectorAll('input[name="experience"][value]:not([value="all"])').forEach(cb => cb.checked = false);
//       }
//       if (name === "experience" && value !== "all" && checkbox.checked) {
//         const noneCb = document.querySelector('input[name="experience"][value="all"]');
//         if (noneCb) noneCb.checked = false;
//       }

//       if (name === "region" && value === "all" && checkbox.checked) {
//         document.querySelectorAll('input[name="region"][value]:not([value="all"])').forEach(cb => cb.checked = false);
//       }
//       if (name === "region" && value !== "all" && checkbox.checked) {
//         const allCb = document.querySelector('input[name="region"][value="all"]');
//         if (allCb) allCb.checked = false;
//       }
//     });
//   });

//   // ✅ 🔍 버튼 클릭 시 URL 갱신
//   const searchBtn = document.querySelector(".FilterSearch") || document.querySelector(".Search");
//   if (searchBtn) {
//     searchBtn.addEventListener('click', (e) => {
//       e.preventDefault();
//       const form = document.getElementById('expert-filter-form');
//       const formData = new FormData(form);
//       const url = new URL(window.location.href.split('?')[0]);

//       for (const [key, value] of formData.entries()) {
//         url.searchParams.append(key, value);
//       }
//       window.location.href = url.toString();
//     });
//   }
// });

// 모달 열고 닫기
  const toggleModal = (btnSelector, modalSelector, displayType = "block") => {
    const btn = document.querySelector(btnSelector);
    const modal = document.querySelector(modalSelector);

    btn.addEventListener("click", () => {
      if (!modal) return;
      const isOpen = modal.style.display === displayType;
      document.querySelectorAll(".Regioncheck, .WorkCheck, .BadgeCheck").forEach(el => el.style.display = "none");
      modal.style.display = isOpen ? "none" : displayType;
    });
  };

  toggleModal(".Region", ".Regioncheck");
  toggleModal(".Work", ".WorkCheck", "flex");
  toggleModal(".Badge", ".BadgeCheck");

  // DOM이 로드되면 필터 관련 이벤트 연결
  document.addEventListener("DOMContentLoaded", function () {
    // 🔹 인증배지: 전체 vs 인증보유 충돌 방지
    const badgeAll = document.getElementById("badge_all");
    const badgeTrue = document.getElementById("badge_true");

    if (badgeAll && badgeTrue) {
      badgeAll.addEventListener("change", () => {
        if (badgeAll.checked) badgeTrue.checked = false;
      });

      badgeTrue.addEventListener("change", () => {
        if (badgeTrue.checked) badgeAll.checked = false;
      });
    }

    // 🔹 지역 필터: 서울시 전체 vs 개별 구
    const seoulAllCheckbox = document.querySelector('input[name="seoul_all"]');
    const regionCheckboxes = document.querySelectorAll('input[name="region"][value]');

    if (seoulAllCheckbox) {
      seoulAllCheckbox.addEventListener("change", () => {
        if (seoulAllCheckbox.checked) {
          regionCheckboxes.forEach(cb => cb.checked = false);
        }
      });
    }

    regionCheckboxes.forEach(cb => {
      cb.addEventListener("change", () => {
        if (cb.checked && seoulAllCheckbox?.checked) {
          seoulAllCheckbox.checked = false;
        }
      });
    });

    // 🔹 경력 필터: 경력 무관 vs 상세 조건
    const experienceNoneCheckbox = document.querySelector('input[name="experience"][value="none"]');
    const experienceDetailCheckboxes = document.querySelectorAll('input[name="experience"][value]:not([value="none"])');

    if (experienceNoneCheckbox) {
      experienceNoneCheckbox.addEventListener("change", () => {
        if (experienceNoneCheckbox.checked) {
          experienceDetailCheckboxes.forEach(cb => cb.checked = false);
        }
      });
    }

    experienceDetailCheckboxes.forEach(cb => {
      cb.addEventListener("change", () => {
        if (cb.checked && experienceNoneCheckbox?.checked) {
          experienceNoneCheckbox.checked = false;
        }
      });
    });
  });

  // 카테고리 박스 생성 및 하위 카테고리 토글
  const categoryInfo = {
    appliance: {
      imgSrc: "/static/img/main_C1.svg",
      alt: "repair",
      className: "C1"
    },
    health: {
      imgSrc: "/static/img/main_C2.svg",
      alt: "sports",
      className: "C2"
    },
    business: {
      imgSrc: "/static/img/main_C3.svg",
      alt: "consulting",
      className: "C3"
    },
    lifestyle: {
      imgSrc: "/static/img/main_C4.svg",
      alt: "life",
      className: "C4"
    }
  };

  function createCategoryBox(key) {
    const info = categoryInfo[key];
    if (!info) return;

    const wrapper = document.createElement('div');
    wrapper.className = "category-box";

    wrapper.onclick = () => {
      const url = `/category/?category=${key}`;
      window.location.href = url;
    };

    wrapper.innerHTML = `
      <div class="Category">
        <div class="${info.className}">
          <img id="img-${key}" src="${info.imgSrc}" alt="${info.alt}" width="222.516px" />
        </div>
      </div>
    `;
    return wrapper;
  }

  const categories = ['appliance', 'health', 'business', 'lifestyle'];
  const container = document.getElementById('categoryContainer');

  categories.forEach(key => {
    const box = createCategoryBox(key);
    container.appendChild(box);
  });

  const urlParams = new URLSearchParams(window.location.search);
  const selectedCategory = urlParams.get("category") || "appliance";
  toggleSub(selectedCategory);

  function toggleSub(key) {
    document.querySelectorAll('.subcategory-list').forEach(el => {
      el.style.display = 'none';
    });

    const target = document.getElementById('sub-' + key);
    if (target) {
      target.style.display = 'block';
    }

    categories.forEach(catKey => {
      const img = document.getElementById('img-' + catKey);
      if (img) {
        img.style.opacity = (catKey === key) ? '1' : '0.2';
      }
    });
  }