class Fixes {
  constructor(formId) {
    this.form = document.getElementById(formId);
    this.applyFixes();
  }

  applyFixes() {
    if (!this.form) {
      console.error("Form não encontrado!");
      return;
    }

    // applying fixes
    this.removeSelectDashes();
  }

  removeSelectDashes() {
    try {
      document.addEventListener("DOMContentLoaded", () => {
        let select = document.getElementById("pf_ou_pj");
        if (select && select.options.length > 0) {
          select.remove(0);

          console.log("Dashes removidos com sucesso!");
        } else {
          console.error("O elemento select não foi encontrado ou está vazio.");
        }
      });
    }
    catch (error) {
      console.error("Erro ao reomver o elemento: ", error.messsage || error);
    }
  }
}

const fixes = new Fixes("professor-form");

