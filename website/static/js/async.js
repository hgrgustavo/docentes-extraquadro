class Async {
  constructor() {
    this.showUserAvatar();
    this.deleteContract();
    this.downloadContract();

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

  deleteContract() {
    document.addEventListener("DOMContentLoaded", () => {
      document.querySelectorAll("a.hover\\:text-red-700").forEach((anchor) => {
        anchor.addEventListener("click", (event) => {
          event.preventDefault();
          const row = event.target.closest("tr[id]");

          if (!row) {
            console.error("Linha não encontrada!");
            return;
          }

          const row_id = row.id;

          if (confirm(`Deseja excluir o contrato Nº${row_id}?`)) {
            fetch(`excluir/${row_id}/`, {
              method: "DELETE",
              headers: {
                "X-CSRFToken": this.getCSRFToken(),
                "Content-Type": "application/json",
              },
            })
              .then((response) => response.json())
              .then((data) => {
                if (data.message === "success") {
                  const table_body = document.getElementById("table_body");

                  if (table_body) {
                    row.parentNode.removeChild(row);
                  }
                } else {
                  console.error("Falha ao excluir o contrato.");
                }
              })
              .catch((error) => {
                console.error("Erro ao excluir linha: " + error);
              });
          }
        });
      });
    });
  }

  downloadContract() {
    document.addEventListener("DOMContentLoaded", () => {
      document.querySelectorAll("a.hover\\:text-orange-700").forEach((anchor) => {
        const row = anchor.closest("tr[id]");

        if (!row) {
          console.error("Linha não encontrada!");
          return;
        }

        const row_id = row.id;

        fetch(`download/${row_id}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": this.getCSRFToken(),
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(`Erro HTTP: ${response.status}`);
            }

            return response.json();
          })
          .then((data) => {
            if (data.message === "success" && data.link) {
              anchor.setAttribute("href", data.link);
              anchor.setAttribute("target", "_blank");
              anchor.setAttribute("rel", "noopener noreferrer");

            }
          })
          .catch(error => {
            alert(`Erro no download: ${error}`);
          })
      })
    })
  }
}

const async = new Async();
