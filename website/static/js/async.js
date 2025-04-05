class Async {
  constructor() {
    this.showUserAvatar();
    this.generatePDF();
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

}

const async = new Async();
