document.addEventListener("DOMContentLoaded", function () {
  const radioChips = document.querySelectorAll(".radio-chip");

  radioChips.forEach((chip) => {
    const input = chip.querySelector("input[type='radio']");
    input.addEventListener("change", function () {
      radioChips.forEach((c) => c.classList.remove("selected"));
      if (input.checked) {
        chip.classList.add("selected");
      }
    });
  });
});
