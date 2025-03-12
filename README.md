# Projeto MaestroAPI-ITDM

## Estrutura de Pastas

```plaintext
/projeto
 ├── application.py
 ├── itdm_interface.py
 ├── /core
 │    ├── communication.py
 │    └── terminalui.py
 └── /commands
      ├── command.py
      └── rfid_command.py
```

## Classes

- **application.py**  
    - Arquivo principal da aplicação.  
    - Tenta estabelecer a conexão com o STM32, aguarda o modo interativo, exibe o menu e permite enviar comandos.

- **itdm_interface.py**  
    - Interface externa para puxar gatilhos via botões do itdm.
    - Exemplo: `WriteRFID()` envia o comando RFID sem interagir diretamente com a comunicação.

- **core/communication.py**  
    - Gerencia a conexão serial e a thread de escuta.  
    - Processa as mensagens recebidas e executa a lógica do comando pendente.

- **core/terminalui.py**  
    - Exibe mensagens e status no terminal.  
    - Trata interações com o usuário (inputs, menus etc.).

- **commands/command.py**  
    - Classe abstrata para comandos de mensagens.  
    - Define métodos `send()`, `on_validate()` e `on_receive()`.

- **commands/rfid_command.py**  
    - Exemplo concreto de comando.  
    - Envia comandos para configurar RFID e valida se a resposta contém `"successful"`.

## Uso do Sistema de Commands

1. Crie um novo arquivo na pasta `/commands` e herde de `Command`.
2. Implemente `send()`, `on_validate()` e `on_receive()`.
3. Para enviar a mensagem use:

   ```python
   comm.send(SuaClasseDeMensagem())
   ```

## Como Executar
1. Instale Python 3.x e as bibliotecas pyserial e keyboard.
2. Navegue até a pasta raiz (onde está o application.py) e execute:

```plaintext
python application.py
```

Se a conexão for estabelecida, aguarde a ativação do modo interativo pelo CLI da STM32, ou as intruções para ativar.
Caso falhe, escolha entre reconectar ou sair.

## Proximos Passos

1. Validar um modelo/fluxo de trocar de mensagens.
2. Através da classe ITDMInterface, criar pontos de funcão acionados através da conexão com o ITDM.