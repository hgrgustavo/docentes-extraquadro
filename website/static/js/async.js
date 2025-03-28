class Async {
  constructor() {
    this.showUserAvatar();
  }

  getCSRFToken() {
    const token = document.querySelector("[name=csrfmiddlewaretoken]") ||
      document.querySelector('meta[name="csrf-token"]');

    if (!token) {
      console.warn("CSRF token não encontrado!");
    }

    return token ? token.getAttribute('content') || token.value : '';
  }

  showUserAvatar() {
    document.addEventListener("DOMContentLoaded", () => {
      document.getElementById("file-upload").addEventListener("change", (event) => {
        const file = event.target.files[0];

        if (file && file.type.startsWith("image/")) {
          const reader = new FileReader();

          reader.onload = (e) => {
            const img = document.querySelector(".avatar-preview");
            img.src = e.target.result;
          };

          reader.readAsDataURL(file);
        } else {
          alert("Por favor, selecione um arquivo de imagem válido.");
        }
      });
    });
  }


  async generatePDF() {
    document.getElementById("btn-generatepdf").addEventListener("click", async () => {
      try {
        const urlId = document.getElementById("btn-generatepdf").getAttribute("data-id");
        const response = await fetch(`${urlId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.getCSRFToken(),
          },
        });

        if (!response.ok) {
          throw new Error("Erro ao gerar o PDF");
        }

        const data = await response.json();
        console.log("PDF gerado com sucesso:", data);
        alert("Contrato gerado com sucesso!");

      } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro ao gerar o contrato: ", error);
      }
    });
  }
}

const async = new Async();
