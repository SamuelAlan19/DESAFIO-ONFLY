# CHALLENGE ONFLY  

Prezados, boa tarde.
Estimo que estejam bem!

Segue repositório destinado a resolução do desafio proposto pela Onfly.

```Haja visto minha maior atuação na área de Produtos, gostaria de destacar a utilização de IA para resolução do desafio proposto.``` 
 
# CAUSA RAIZ EM UMA FRASE POR DEFEITO

1. Status: NO_SHOW entrava no faturamento

Arquivo: services/status_policy.py

Causa raiz: a regra de negócio diz “só CONFIRMED é faturável”, mas o código foi escrito como uma lista de exclusão (status != "CANCELLED"), que barra apenas um status. Qualquer outro, como NO_SHOW, passava.

2. Noites: cálculo ignorava mês e ano

Arquivo: services/stay_calculator.py

Causa raiz: o código subtraía checkout.day - checkin.day, ou seja, apenas o número do dia dentro do mês. Entre 30/01 e 02/02 isso dá 2 − 30 = −28, e não 3. A subtração correta é entre as datas completas: (checkout - checkin).days.

3. Câmbio: operação invertida e perda de precisão

Arquivo: services/currency_converter.py

Causa raiz: são dois erros no mesmo ponto.

Operação invertida: o código dividia pela taxa, mas a regra é amount × rate_to_brl. US$ 100 virava ≈ R$ 18 em vez de R$ 542.
Conversão para float: o valor passava por float, que representa decimais de forma aproximada e acumula erro de centavos. A regra do README exige Decimal.

4. Ranking: ordem invertida

Arquivo: services/report_builder.py

Causa raiz: o sorted(...) usava o valor em ordem crescente. Como o código depois pega os primeiros N itens, o “top 5” devolvia os 5 hotéis de menor faturamento. O correto é valor decrescente, com desempate por hotel_id crescente (-valor, hotel_id).

5. Leitura: corte silencioso em 200 linhas

Arquivo: repositories/csv_reservation_repository.py

Causa raiz: o leitor tinha if len(rows) == 200: break, um limite fixo que interrompe a leitura sem erro nem aviso. O CSV real tem 300 reservas, então 100 eram descartadas.

# COMO INVESTIGOU/ABORDOU O PROBLEMA

Após a leitura inicial, foi-se identificada a necessidade de utilização de Inteligência Artificial para resolução deste, sendo assim realizei toda descrição funcional do que eu precisava que fosse obtido através do prompt para que, desta forma, surtisse o resultado esperado!

<img width="1105" height="378" alt="image" src="https://github.com/user-attachments/assets/2c13007f-b7d1-4232-9d07-9c128836cc9e" />


# COMO VALIDAR O RESULTADO DO ```PYTEST```

Após subir os arquivos para o repositório no GutHub, realizei a criação de um ```CODESPACE``` a fim de executar o comando descrito ```pytest -q```. 
* Este qual após executado apresentou sucesso em todas as instâncias.

### [Arquivo /EXPORT](https://github.com/user-attachments/files/34861403/sessao.md)
### [Arquivo DECLARAÇÃO.MD](https://github.com/user-attachments/files/34861424/declaracao.md)

