function abrirDialogo() {
  var html = HtmlService.createHtmlOutputFromFile('Dialogo')
      .setWidth(800)
      .setHeight(600);
  SpreadsheetApp.getUi().showModalDialog(html, 'Painel de Manutenção - Status Real-Time');
}

function obterDadosManutencao() {
  // Acessa a aba onde está o seu CSV/Dados
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var dados = sheet.getDataRange().getValues();
  var cabecalho = dados.shift(); // Remove o cabeçalho
  
  // Mapeia os dados para um formato fácil de ler no HTML
  return dados.map(function(linha) {
    return {
      maquina: linha[0], // Coluna A: Nome da Máquina
      os: linha[1],      // Coluna B: Número da O.S.
      status: linha[2]   // Coluna C: Status (Aberta, Em Execução, Finalizada, etc.)
    };
  });
}
