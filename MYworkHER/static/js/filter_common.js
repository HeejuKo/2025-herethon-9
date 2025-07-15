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