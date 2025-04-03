class Fixes {
  constructor() {
    this.removeSelectDashes();
    this.dropdownClick();
  }

  removeSelectDashes() {
    document.addEventListener("DOMContentLoaded", () => {
      const select = document.getElementById("pf_ou_pj");
      if (select && select.options.length > 0) {
        select.remove(0);
        console.log("Dashes removidos com sucesso!");
      } else {
        console.error("O elemento select não foi encontrado ou está vazio.");
      }
    })

  }

  dropdownClick() {
    document.addEventListener("DOMContentLoaded", () => {
      const button = document.getElementById("menu-button");
      const dropdown = document.getElementById("dropdown");

      button.addEventListener("click", (event) => {
        event.stopPropagation();
        dropdown.classList.toggle("hidden");
      });
    })
  }
}

const fixes = new Fixes();

