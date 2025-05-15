class Async {
  constructor() {
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

  deleteContract() {
    document.addEventListener("DOMContentLoaded", () => {
      document.querySelectorAll("a.hover\\:text-red-700").forEach((anchor) => {
        anchor.addEventListener("click", (event) => {
          event.preventDefault();
          const row = event.target.closest("tr[id]");

          if (!row) {
            throw new DOMException("Row not found.", "NotFoundError");
          }

          const row_id = row.id;

          if (confirm(`Excluir contrato Nº${row_id}?`)) {
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

                  if (!table_body) {
                    throw new DOMException("Table not found.", "NotFoundError");
                  }


                  row.style.transition = "opacity 0.5s";
                  row.style.opacity = "0";

                  setTimeout(() => row.parentNode.removeChild(row), 500);
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
      document.querySelectorAll("a.hover\\:text-yellow-700[data-contract-id]").forEach((anchor) => {
        const id = anchor.getAttribute("data-contract-id");

        if (!id) {
          throw new DOMException("ID not found.", "NotFoundError");
        }

        fetch(`download/${id}/`, {
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
              console.log(data.link);
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
