# Declaração de uso de IA

## Ferramenta e modelo

- **Ferramenta:** Claude (Anthropic), via interface de chat (claude.ai / app), com ambiente de execução de código.
- **Modelo:** Claude Sonnet 5.5.

## O que a IA fez

- Leu o enunciado e todo o código-fonte fornecido e o confrontou com as regras de negócio do README.
- Identificou os cinco defeitos (status, noites, câmbio, ordenação do ranking e corte em 200 linhas) e propôs/aplicou as correções.
- Escreveu os testes adicionais (`tests/test_extra_regressions.py`) e validou o resultado contra a amostra do
  README e contra um recálculo independente do dataset completo.
- Redigiu o rascunho do `README-ENTREGA.md` e desta declaração.

## O que eu fiz

- Selecionei e enviei os arquivos do desafio e defini a tarefa para a IA.
- Revisei as explicações de cada defeito e das correções, e me apropriei delas.
- Executei/executarei o `pytest` oficial na minha máquina, publiquei o repositório no GitHub e fiz a entrega.

> Ajuste os itens acima para refletir fielmente o que você de fato fez antes de entregar.
