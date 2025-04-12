class DataTablesHandler {
  constructor() {
    this.initializeTables();
  }

  initializeTables() {
    $("#table_history").DataTable();
    // Adicione aqui outras inicializações para diferentes tabelas, se necessário
  }
}

// Instanciar a classe quando o DOM estiver pronto
$(document).ready(() => {
  new DataTablesHandler();
});

