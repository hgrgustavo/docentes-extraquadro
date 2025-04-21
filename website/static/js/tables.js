/* DataTables requires jquery */
import { deleteContract } from "./async.js"

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

        emptyTable: "Não há contratos disponíveis",
        infoEmpty: "Nenhum resultado",
        zeroRecords: "Registros não encontrados",
      },
    });
  }
}

$(document).ready(() => {
  new DataTablesHandler();
});

