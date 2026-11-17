# SupriDesk — Gestão de Solicitações Internas

Sistema desktop desenvolvido em Python para cadastrar e acompanhar solicitações internas de materiais.

## Requisitos
- Python 3.10 ou superior
- Tkinter/ttk (normalmente incluído na instalação do Python)
- sqlite3 e csv (bibliotecas padrão do Python)

Não há dependências externas.

## Como executar
1. Baixe ou clone este repositório.
2. Abra o terminal na pasta do projeto.
3. Execute:

```bash
python main.py
```

O banco `solicitacoes.db` é criado automaticamente na primeira execução.

## Funcionalidades
- Cadastro de setor, material, quantidade e prioridade (Normal/Alta).
- Geração automática de ID, data/hora e status inicial Pendente.
- Validação de campos obrigatórios e quantidade inteira positiva.
- Persistência dos registros em SQLite.
- Fluxo controlado: Pendente → Em atendimento → Atendida.
- Pesquisa por setor ou material e filtro por status.
- Limpeza dos filtros.
- Exportação de todo o histórico para CSV com cabeçalho.

## Estrutura do projeto
- `main.py`: inicialização da aplicação.
- `interface.py`: janela, formulário, tabela e ações.
- `database.py`: criação e operações no banco SQLite.
- `regras.py`: validações e regras de transição de status.
- `testes.py`: testes automatizados das regras e do banco.

## Testes
Para executar os testes automatizados:

```bash
python -m unittest testes.py
```

Testes mínimos solicitados na atividade:
1. Cadastrar TI / Mouse USB / 5 / Alta e conferir status Pendente.
2. Tentar cadastrar Administrativo / Papel A4 / 0 / Normal; o cadastro deve ser recusado.
3. Fazer Pendente → Em atendimento → Atendida e tentar repetir a conclusão; a repetição deve ser bloqueada.
4. Fechar e reabrir o sistema; o registro deve permanecer no banco SQLite.
5. Pesquisar Mouse ou TI, filtrar por Atendida e exportar o histórico CSV.

## Uso de inteligência artificial
Uma ferramenta de inteligência artificial foi utilizada como apoio na elaboração inicial da estrutura e do código. O projeto deve ser revisado, executado e compreendido pelo estudante, que é responsável por validar o funcionamento e explicar suas decisões.

## Observação
O arquivo `solicitacoes.db` é gerado automaticamente e não precisa ser enviado ao repositório.
