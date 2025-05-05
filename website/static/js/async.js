class Async {
  constructor() {
    this.showUserAvatar();
    this.deleteContract();
    this.downloadContract();
    this.uploadTeacherPhoto();

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
            console.error("Table row not found.");
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
                }
              })
              .catch((error) => {
                console.error(`Error while deleting row: ${error}`);
              });
          }
        });
      });
    });
  }

  downloadContract() {
    document.addEventListener("DOMContentLoaded", () => {
      document.querySelectorAll("a.hover\\:text-yellow-700").forEach((anchor) => {
        const row = anchor.closest("tr[id]");

        if (!row) {
          console.error("Table row not found");
          return;
        }

        const row_id = row.id;

        fetch(`download/${row_id}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": this.getCSRFToken(),
            "Content-Type": "application/json",
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(`HTTP Error: ${response.status}`);
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
            alert(`Download links attribution error: ${error}`);
          })
      })
    })
  }

  uploadTeacherPhoto() {
    document.addEventListener("DOMContentLoaded", () => {
      document.querySelectorAll("input.sr-only").forEach((input) => {
        const targetDiv = input.closest("div[id]");

        if (!targetDiv) {
          throw new DOMException("Target div not found.", "NotFoundError");
        }

        const id = targetDiv.id;

        if (!id) {
          throw new DOMException("Teacher id not found.", "NotFoundError");
        }

        const label = targetDiv.querySelector("label");

        if (!label) {
          throw new DOMException("Label not found.", "NotFoundError");
        }

        label.setAttribute("for", `input_${id}`);
        input.setAttribute("name", `teacher_${id}`);
        input.setAttribute("id", `input_${id}`)

        input.addEventListener("change", (event) => {
          const photo = event.target.files[0];
          const formData = new FormData();

          formData.append("file", photo);

          fetch(`upload/teacher_photo/${id}/`, {
            method: "POST",
            headers: { "X-CSRFToken": this.getCSRFToken() },
            body: formData,
          })
            .then(response => response.json())
            .then((data) => {
              if (data.status === "success" && data.photo_url.match(/^https:\/\/lh3\.googleusercontent\.com\/d\//)) {
                localStorage.setItem(`teacher_${id}_photo`, data.photo_url);

              }
            })
            .catch(error => {
              alert(`Teacher photo upload error, because ${error}`);
            })
        })
        let cachedPhoto = localStorage.getItem(`teacher_${id}_photo`);

        if (cachedPhoto) {
          targetDiv.classList.add(`bg-[url(${cachedPhoto})]`);

        }
      })
    })

  }
}

const async = new Async();
