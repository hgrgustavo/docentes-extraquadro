class Fixes {
  constructor() {
    document.addEventListener("DOMContentLoaded", () => {
      this.applyFixes();
    });
  }

  applyFixes() {
    this.removeSelectDashes();
    this.dropdownClick();
  }

  removeSelectDashes() {
    const select = document.getElementById("pf_ou_pj");
    if (select && select.options.length > 0) {
      select.remove(0);
      console.log("Dashes removidos com sucesso!");
    } else {
      console.error("O elemento select não foi encontrado ou está vazio.");
    }
  }

  dropdownClick() {
    const button = document.getElementById("menu-button");
    const dropdown = document.getElementById("dropdown");

    button.addEventListener("click", (event) => {
      event.stopPropagation();
      dropdown.classList.toggle("hidden");
    });

    document.addEventListener("click", (event) => {
      if (!dropdown.contains(event.target) && !button.contains(event.target)) {
        dropdown.classList.add("hidden");
      }
    });
  }
}

const fixes = new Fixes();

