# 🧩 Command Interpreter

Um **interpretador de comandos programável**, criado para agilizar
testes e executar funções dinamicamente enquanto o programa está em
execução.

------------------------------------------------------------------------

## ⚙️ Sintaxe

O interpretador segue uma sintaxe simples.\
Cada comando individual é **separado por ponto e vírgula (`;`)**.

Um comando é composto por: - **Comando principal** --- o nome do comando
a ser executado; - **Argumentos** --- iniciados por `/`.

O comando principal e seus argumentos são **encerrados com `$`**, e o
comando completo termina com `;`.

**Exemplos:**

    comando-a$;
    print$ /hello world!$ ;

------------------------------------------------------------------------

## ➕ Adicionando Comandos

Para adicionar novos comandos personalizados ao interpretador, utilize o
método:

``` python
commandCreate(command_key, function, args_name_n_types)
```

### Parâmetros

  ---------------------------------------------------------------------------------
  Parâmetro                    Tipo                    Descrição
  ---------------------------- ----------------------- ----------------------------
  `command_key`                `str`                   Palavra-chave que identifica
                                                       o comando no interpretador.

  `function`                   `Callable`              Função que será executada ao
                                                       chamar o comando.

   `args_name_n_types`          `dict[str, ArgsType]`   Dicionário com os nomes e
                                                       tipos dos argumentos
                                                       esperados.
                                                       
  ---------------------------------------------------------------------------------

> **Nota:** O número de argumentos registrados em `commandCreate()` deve
> corresponder exatamente ao número de parâmetros da função associada.

------------------------------------------------------------------------

## 🧱 Tipos de Argumentos (`ArgsType`)

Os tipos de argumentos determinam como o interpretador deve tratar cada
parâmetro.\
Eles são definidos na classe `ArgsType`:

  -----------------------------------------------------------------------
  Tipo                    Descrição
  ----------------------- -----------------------------------------------
  `INTEGER`               Argumento numérico (int).

  `TEXT`                  Argumento textual (str).

  `ENUM`                  Argumento numérico restrito a um conjunto de
                          valores predefinidos.
                          
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## ▶️ Executando Comandos

A execução de comandos é feita pelo método:

``` python
execCommand(input: str) -> Status
```

### Parâmetros

  ------------------------------------------------------------------------
  Parâmetro                    Tipo           Descrição
  ---------------------------- -------------- ----------------------------
  `input`                      `str`          Linha de comando(s) a ser
                                              interpretada e executada.

  ------------------------------------------------------------------------

### Retorno

Retorna um valor da enumeração `Status`, indicando o resultado da
execução:

  Status                        Significado
  ----------------------------- ------------------------------------------
  `SUCEFULL`                    Execução concluída com sucesso.\
  `FAILURE`                     Falha genérica.\
  `ARGUMENTS_MISSING_OR_LEFT`   Quantidade incorreta de argumentos.\
  `ARGUMENTS_TYPE_ERROR`        Tipo de argumento inválido.\
  `END_FLAG_MISSING`            Delimitador de fim (`$`) ausente.\
  `COMMAND_NOT_FOUND`           Comando inexistente.\
  `MAIN_COMMAND_EXPECTED`       Faltando comando principal.\
  `SEMICOLON_MISSING`           Comando não termina com ponto e vírgula.\

  ------------------------------------------------------------------------

## 💬 Retorno de Função

O resultado da última execução de comando é armazenado em:

``` python
Interpreter.last_command_return
```

> Recomenda-se que todas as funções chamadas retornem **strings**, para
> que o valor possa ser exibido ou manipulado posteriormente.

------------------------------------------------------------------------

## 📦 Comandos Padrão

O interpretador vem com dois comandos internos:

  --------------------------------------------------------------------------------------------------
  Comando                               Função
  ------------------------------------- ------------------------------------------------------------
  `help$;`                              Imprime a lista de comandos disponíveis, no
                                        formato:`<br>`{=html}`command_key <arg_type: arg_name>...`

  `test$;`                              Executa um teste básico para verificar se o interpretador
                                        está funcionando corretamente.
                                        
  --------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## 💡 Exemplo de Uso

``` python
from cmd_5E import Interpreter, ArgsType

def soma(a: int, b: int):
    return str(a + b)

main = Interpreter()
main.commandCreate("soma", soma, {"a": ArgsType.INTEGER, "b": ArgsType.INTEGER})

print(main.execCommand("soma$ /10$ /5$ ;"))
print(main.last_command_return)  # -> "15"
```
