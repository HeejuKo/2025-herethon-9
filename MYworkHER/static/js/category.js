document.addEventListener("DOMContentLoaded", ()=>{

    const categoryImages = document.querySelectorAll(".Category div");
    const subsBox = document.querySelector(".Subs");
    const subCategoryData = {
        C1: [
            { name: "에어컨 수리", count: 120 },
            { name: "세탁기 수리", count: 82 },
            { name: "정수기 설치", count: 67 },
        ],
        C2: [
            { name: "요가", count: 95 },
            { name: "헬스", count: 103 },
            { name: "필라테스", count: 77 },
        ],
    };

    function makeSubcategories(categoryClass){
        const subs = subCategoryData[categoryClass];
        subsBox.innerHTML="";

        subs.forEach((sub)=>{
            const subItem = document.createElement("div");
            subItem.className="SubItem";

            subItem.innerHTML = `
                <span class="name">${sub.name}</span>
                <span class="subCount">전문가 <span class="count">${sub.count}명</span></span>
            `;

            subItem.addEventListener("click", ()=>{
                const params = new URLSearchParams({
                category: categoryClass,
                name: sub.name,
                count: sub.count
            });
                window.location.href = `../pages/category_expert.html?${params.toString()}`
            })
            subsBox.appendChild(subItem);
        });
    
    }

    function categoryClick(category){
        categoryImages.forEach((el)=> el.classList.add("faded"));
        category.classList.remove("faded");

        const categoryClass = category.classList[0];
        makeSubcategories(categoryClass);
    }

    categoryImages.forEach((categoryDiv) => {
        categoryDiv.addEventListener("click", () => {
            categoryClick(categoryDiv);
        })
    })
    
    const urlParams = new URLSearchParams(window.location.search);
    const selectCategory = urlParams.get("category")||"C1";

    const targetCategory = Array.from(categoryImages).find(div=>div.classList[0]===selectCategory);
    categoryClick(targetCategory||categoryImages[0]);
  
});