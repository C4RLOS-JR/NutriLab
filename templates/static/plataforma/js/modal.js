$('#alterarPaciente').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Botão que acionou o modal
  var id = button.data('id') // Extrair informações de atributos data-*
  var nome = button.data('nome')
  var sexo = button.data('sexo')
  var idade = button.data('idade')
  var email = button.data('email')
  var telefone = button.data('telefone')
  
  var modal = $(this)
  modal.find('.modal-title').text('Alterar dados de ' + nome)
  modal.find('#id_paciente').val(id)
  modal.find('#nome_paciente').val(nome)
  modal.find('#sexo_paciente').val(sexo)
  modal.find('#idade_paciente').val(idade)
  modal.find('#email_paciente').val(email)
  modal.find('#telefone_paciente').val(telefone)
})

$('#excluirPaciente').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Botão que acionou o modal
  var id = button.data('id') // Extrair informações de atributos data-*
  var nome = button.data('nome')

  var modal = $(this)
  modal.find('.modal-title').text('Deseja excluir "' + nome + '" da lista?')
  modal.find('#id_paciente').val(id)
})

$('#excluirOpcao').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Botão que acionou o modal
  var id = button.data('id') // Extrair informações de atributos data-*

  var modal = $(this)
  modal.find('.modal-title').text('Deseja excluir essa opção?')
  modal.find('#id_opcao').val(id)
})

$('#excluirRefeicao').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Botão que acionou o modal
  var id = button.data('id') // Extrair informações de atributos data-*

  var modal = $(this)
  modal.find('.modal-title').text('Deseja excluir essa refeição?')
  modal.find('#id_refeicao').val(id)
})