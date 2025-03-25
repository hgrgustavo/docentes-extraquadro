class Fixes {
  constructor(formId) {
    this.form = document.getElementById(formId);
    document.addEventListener("DOMContentLoaded", () => {
      this.applyFixes();
    });
  }

  applyFixes() {
    if (!this.form) {
      console.error("Form não encontrado!");
      return;
    }

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
    const menuButton = document.getElementById("menu-button");
    const dropdown = document.querySelector(".origin-top-right");

    if (!menuButton || !dropdown) {
      console.error("Elementos do dropdown não foram encontrados.");
      return;
    }

    menuButton.addEventListener("click", () => {
      const isExpanded = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", !isExpanded);
      dropdown.classList.toggle("hidden");
    });
  }
}

const fixes = new Fixes("professor-form");

