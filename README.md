# Sistema Inteligente de Gestão Acadêmica

Projeto desenvolvido para o desafio de Algoritmos Avançados — 2º ano TDS.

## Funcionalidades

- Cadastro de alunos com bloqueio de matrículas duplicadas;
- Registro e validação de quatro notas, com média automática;
- Registro de aulas e faltas, com cálculo de frequência;
- Situação acadêmica: aprovado, recuperação, reprovado ou reprovado por frequência;
- Consulta por matrícula;
- Relatórios com média da turma, maiores e menores médias, contagem por situação e baixa frequência;
- Ranking decrescente e identificação dos três melhores alunos;
- Registro de nota de recuperação e atualização automática da média;
- Detecção de inconsistências e tratamento de entradas inválidas.

## Como executar

Requer Python 3.10 ou superior.

```bash
python sistema_academico.py
```

## Como executar os testes

```bash
python -m unittest discover -s tests -v
```

## Organização

A classe `Aluno` concentra os dados e regras calculadas de média, frequência, situação e inconsistências. A classe `SistemaAcademico` gerencia o conjunto de alunos e as operações do sistema. A função `executar_menu` fornece a interface interativa de console.

## Decisões para uso em uma instituição maior

Para atender centenas de usuários, a solução poderia evoluir para uma API com autenticação e permissões, banco de dados relacional com transações, auditoria de alterações, validações no servidor, testes de integração, backups automáticos, logs, paginação de relatórios e uma interface web. Também seria importante separar as camadas de apresentação, regras de negócio e persistência, além de proteger dados pessoais conforme a LGPD.
