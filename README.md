# Pipeline IPCA — IBGE

Pipeline de dados em Python que extrai o **IPCA (inflação oficial do Brasil) por região metropolitana** da API SIDRA do IBGE, guarda o dado bruto e entrega uma versão tratada, com tipos corretos e nomes padronizados, pronta para análise.

O objetivo é praticar os fundamentos de engenharia de dados em um projeto de ponta a ponta: extração de API com tratamento de falhas, organização em camadas, formato colunar e código modular executável fora do notebook.

## Arquitetura

```
API SIDRA / IBGE  (tabela 7060 — IPCA por região metropolitana)
        │
        │  src/extrair.py      requisição HTTP, validação do status, resposta vazia
        ▼
dados/bronze/ipca_regiao.parquet     dado cru, exatamente como veio da API
        │
        │  src/transformar.py  conversão de tipos, seleção de colunas, snake_case
        ▼
dados/silver/ipca_regiao.parquet     dado tratado, com schema definido
```

O `main.py` orquestra as etapas em ordem: extrair → gravar bronze → transformar → gravar silver.

## Stack

Python · requests · pandas · Parquet (pyarrow) · pathlib · Git

## Estrutura do projeto

```
pipeline-ipca-ibge/
├── main.py              # ponto de entrada: executa o pipeline
├── src/
│   ├── extrair.py       # buscar_sidra(): consome a API SIDRA
│   ├── transformar.py   # transformar_sidra(): tipos, seleção e renomeação
│   └── carregar.py      # carregar(): grava Parquet na camada indicada
├── notebooks/
│   └── exploracao_api.ipynb   # exploração da API e desenvolvimento das funções
├── requirements.txt
└── .gitignore           # dados/ não é versionado: é gerado pelo pipeline
```

## Como executar

Requer Python 3.9 ou superior.

```bash
git clone https://github.com/AntonioPradoJr/pipeline-ipca-ibge.git
cd pipeline-ipca-ibge
pip install -r requirements.txt
python main.py
```

Ao final, os arquivos são criados em `dados/bronze/` e `dados/silver/`.

## Schema da camada silver

| Coluna | Tipo | Descrição |
|---|---|---|
| `data` | datetime | Mês de referência (primeiro dia do mês) |
| `val` | float | Variação mensal do IPCA, em % |
| `regiao_2020_id` | texto | Código da região metropolitana |
| `regiao_2020` | texto | Nome da região metropolitana |
| `variavel_id` | texto | Código da variável no SIDRA |
| `variavel` | texto | Nome da variável |
| `item_id` | texto | Código do item (geral, grupo, subgrupo...) |
| `item` | texto | Nome do item |
| `nivel_id` | texto | Código do nível territorial |
| `unidade_medida_id` | texto | Código da unidade de medida |

## Decisões técnicas

**Camadas bronze e silver.** O dado bruto é gravado antes de qualquer transformação. Se uma regra de tratamento estiver errada, é possível corrigir e reprocessar a partir do bronze, sem chamar a API de novo.

**Parquet em vez de CSV.** O Parquet guarda o schema junto com os dados: `val` continua numérico e `data` continua data ao ler o arquivo. Em CSV, tudo voltaria como texto. Por ser colunar e comprimido, também ocupa menos espaço e permite ler apenas as colunas necessárias.

**Erro da API × ausência de dados.** São situações diferentes e tratadas de forma diferente:
- Status HTTP diferente de 200 (ex.: tabela ou parâmetro inválido): o pipeline **falha** com a mensagem retornada pelo IBGE.
- Resposta sem dados (ex.: mês ainda não divulgado): o pipeline **avisa e não grava**, para não sobrescrever um arquivo válido com um vazio.

**Timeout nas requisições.** Toda chamada à API tem limite de 30 segundos, para que uma API instável não deixe o processo travado indefinidamente.

**Execução idempotente.** Cada execução sobrescreve os arquivos da camada. Rodar o pipeline uma ou várias vezes produz o mesmo resultado, sem duplicar dados.

**Separação de responsabilidades.** Cada etapa (extrair, transformar, carregar) é uma função em seu próprio módulo, recebendo e devolvendo DataFrames. Isso facilita testar, reutilizar e orquestrar as etapas.

## Limitações atuais

- A transformação é específica da tabela 7060 (IPCA por região metropolitana).
- Os parâmetros da consulta (tabela, variável, período, nível) estão fixos no `main.py`.
- Cada execução busca os últimos 12 meses e sobrescreve o arquivo; ainda não há histórico incremental.

## Próximos passos

- [ ] Retry com backoff para falhas temporárias da API (5xx e timeout)
- [ ] Logging estruturado no lugar de `print`
- [ ] Carga incremental: buscar apenas os meses novos, usando os metadados da tabela
- [ ] Testes automatizados com `pytest`
- [ ] Containerização com Docker e orquestração com Airflow

## Fonte dos dados

[SIDRA — Sistema IBGE de Recuperação Automática](https://sidra.ibge.gov.br/tabela/7060), tabela 7060: IPCA — variação mensal, acumulada no ano, acumulada em 12 meses e peso mensal, para o índice geral, grupos, subgrupos, itens e subitens (a partir de janeiro/2020). O pipeline usa a variável 63 (variação mensal) no nível de região metropolitana.
