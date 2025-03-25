class Async {
  constructor() {
    this.showUserAvatar();
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

  // implementar um meio de salvar imagem em cache
}

const async = new Async();
