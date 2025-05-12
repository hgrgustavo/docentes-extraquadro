class Fixes {
  constructor() {
    this.removeSelectDashes();
    this.dropdownClick();
    this.selectConstraint();
    this.cpfMask();
    this.cnpjMask();
  }

  removeSelectDashes() {
    document.addEventListener("DOMContentLoaded", () => {
      document.querySelectorAll("select").forEach(select => {
        select.options.length > 0 ? select.remove(0) : console.error(
          `O elemento select (${select.name || select.id}) não foi encontrado ou está vazio.`);
      });
    });
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

  // Constraints
  constraintInputField(field_id) {
    field_id.readOnly = true;
    field_id.ariaReadOnly = true;
    field_id.required = false;
    field_id.setAttribute("placeholder", "bloqueado");
  }

  releaseInputField(field_id) {
    field_id.required = true;
    field_id.ariaRequired = true;
    field_id.readOnly = false;
    field_id.ariaReadOnly = false;
    field_id.setAttribute("placeholder", "obrigatório");
  }

  selectConstraint() {
    document.addEventListener("DOMContentLoaded", () => {
      const selectElement = document.getElementById("pf_ou_pj");
      const cnpjInput = document.getElementById("cnpj");
      const cpfInput = document.getElementById("cpf");

      if (!selectElement || !cnpjInput || !cpfInput) {
        console.error("Erro: Elementos do formulário não encontrados.");
        return;
      }

      selectElement.addEventListener("change", () => {
        const currentSelection = selectElement.selectedOptions[0];

        switch (currentSelection) {
          case selectElement.options[0]:
            this.constraintInputField(cnpjInput);
            this.releaseInputField(cpfInput);

            break;

          case selectElement.options[1]:
            this.constraintInputField(cpfInput);
            this.releaseInputField(cnpjInput);

            break;

          default:
            console.error("Seleção inválida");
        }
      });

      if (selectElement) {
        selectElement.dispatchEvent(new Event("change"));
      }
    });
  }

  // Masks   
  cpfMask() {
    const cpfInput = document.getElementById("cpf");
    cpfInput.addEventListener("input", (event) => {
      let cpf = event.target.value;


      cpf = cpf.replace(/\D/g, "");

      cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
      cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
      cpf = cpf.replace(/(\d{3})(\d{1,2})$/, "$1-$2");


      event.target.value = cpf;
    });
  }

  cnpjMask() {
    const cnpjInput = document.getElementById("cnpj");
    cnpjInput.addEventListener("input", (event) => {
      let cnpj = event.target.value;

      cnpj = cnpj.replace(/\D/g, "");

      cnpj = cnpj.replace(/(\d{2})(\d)/, "$1.$2");
      cnpj = cnpj.replace(/(\d{3})(\d)/, "$1.$2");
      cnpj = cnpj.replace(/(\d{3})(\d)/, "$1/$2");
      cnpj = cnpj.replace(/(\d{4})(\d)/, "$1-$2");

      event.target.value = cnpj;
    })
  }
}

const fixes = new Fixes();

