
function dropdown() {
  const dropdownButton = document.getElementById("dropdownButton");
  const dropdownContent = document.getElementById("dropdownMenu");

  dropdownButton.addEventListener("click", () => {
    dropdownContent.classList.toggle("hidden");
  });

  document.addEventListener("click", (event) => {
    const isClickInside = dropdownButton.contains(event.target) || dropdownContent.contains(event.target);
    if (!isClickInside) {
      dropdownContent.classList.add("hidden");
    }

  });
}