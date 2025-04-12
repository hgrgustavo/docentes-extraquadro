class DataTablesHandler {
  constructor() {
    this.initializeTables();
  }

  initializeTables() {
    $("#table_history").DataTable({
      language: {
        search: "Filtrar:",
        info: "_START_ de _END_ resultados",
        lengthMenu: "_MENU_ resultados por página",
      },




    });
  }
}

$(document).ready(() => {
  new DataTablesHandler();
});

