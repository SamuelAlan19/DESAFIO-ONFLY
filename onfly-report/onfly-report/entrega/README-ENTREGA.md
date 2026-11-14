# Entrega — Consolidador de reservas de hotel (Onfly)

## Resumo

O CLI entregava números errados por **cinco defeitos independentes**, todos em código (os dados estão corretos,
como o README já indicava). Os cinco foram corrigidos com mudanças pequenas e localizadas, sem alterar
comando, argumentos, schema do relatório, testes fornecidos ou os CSVs de dados.

## Defeitos corrigidos

| # | Arquivo | Defeito | Causa raiz (uma frase) |
|---|---------|---------|------------------------|
| 1 | `services/status_policy.py` | NO_SHOW entrava nos totais | `is_billable` usava `status != "CANCELLED"`, deixando passar `NO_SHOW`; o correto é `status == "CONFIRMED"`. |
| 2 | `services/stay_calculator.py` | Noites negativas/erradas na virada de mês | O cálculo subtraía `checkout.day - checkin.day` (só o dia do mês) em vez de subtrair as datas completas. |
| 3 | `services/currency_converter.py` | Valor em BRL errado e impreciso | Dividia pela taxa em vez de multiplicar e passava por `float`, perdendo exatidão decimal. |
| 4 | `services/report_builder.py` | `top_hotels` mostrava os hotéis **menos** rentáveis | A ordenação era crescente por valor; o correto é decrescente, com desempate por `hotel_id` crescente. |
| 5 | `repositories/csv_reservation_repository.py` | Relatório real ignorava 100 das 300 reservas | O leitor interrompia a leitura na 200ª linha (`if len(rows) == 200: break`), descartando o resto sem aviso. |

### Correções aplicadas

1. `return status == "CONFIRMED"`
2. `return (checkout - checkin).days * rooms`
3. `return amount * rates[currency]` (apenas `Decimal`, arredondamento só na serialização)
4. `key=lambda item: (-item[1]["amount"], item[0])`
5. Remoção do `break` aos 200 registros.

O defeito 5 **não é detectado por nenhum dos testes fornecidos** (todos usam poucas linhas); foi encontrado
conferindo o tamanho do CSV real (300 linhas) contra o que o leitor devolvia. Ele só aparece no arquivo
completo e, sozinho, alteraria todos os totais do relatório final.

## Como investiguei

1. Montei a estrutura descrita no README e rodei os testes **antes de corrigir**: 5 de 5 falhavam.
   O resumo da amostra do README já mostrava o sintoma de um defeito (`Noites: -33`).
2. Li cada módulo confrontando-o com a seção "Regras de negócio" do README (status, noites, câmbio,
   exatidão, ordenação). Cada regra violada levou a um defeito (1 a 4).
3. Como o README avisa que a amostra cobre "apenas parte dos cenários", procurei defeitos fora dos testes:
   perfilei o CSV real (linhas, status, moedas, espaços, duplicidades, nomes de hotel) e comparei com o que o
   leitor devolvia, o que revelou o defeito 5.
4. Corrigi, e validei por três caminhos independentes (ver abaixo).
5. Escrevi testes novos que travam os defeitos não cobertos e confirmei, reintroduzindo cada bug, que os
   testes realmente falham quando o defeito volta.

## Como validar

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

pytest -q

PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json

PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json
```

## Resultados

**Amostra de validação do README (`exemplo-validacao.csv`)** — idêntica ao esperado em todos os campos:
12 reservas, 9 confirmadas, 2 canceladas, 1 no-show, 28 noites, `7566.00` BRL, média `270.21`;
`by_month` (2025-01: 8 / 25 / 6684.00; 2025-02: 1 / 3 / 882.00) e `top_hotels` (H01, H02, H12, H10, H09).

**Dataset completo (`reservas_hoteis.csv`)**, conferido contra um recálculo independente feito fora do código do projeto:

| Campo | Valor |
|-------|-------|
| total_reservations | 300 |
| confirmed / cancelled / no_show | 235 / 31 / 34 |
| total_room_nights | 1347 |
| total_amount_brl | 396170.00 |
| average_nightly_rate_brl | 294.11 |
| top_hotels | H06, H10, H12, H07, H11 |

**Testes:** 13 testes (5 fornecidos, sem alteração + 8 adicionais em `tests/test_extra_regressions.py`),
todos aprovados.

> **Nota de transparência sobre o `pytest`:** o ambiente em que as correções foram desenvolvidas não tinha
> `pytest` instalado nem acesso à internet. Os 13 testes foram executados com um executor mínimo que chama as
> mesmas funções de teste (os testes fornecidos não foram modificados). A execução com o `pytest` oficial deve
> ser feita e colada abaixo antes da entrega:
>
> ```
> (colar aqui a saída real de `pytest -q`)
> ```

## Testes adicionais (`tests/test_extra_regressions.py`)

Leitura sem truncamento (250 linhas), desempate do ranking por `hotel_id`, limite de `--top`, exclusão de
CANCELLED/NO_SHOW de `by_month` e `top_hotels`, noites na virada de ano com vários quartos, arredondamento
half-up só na serialização, média `"0.00"` sem noites faturáveis e código de saída 2 para arquivo ausente.
