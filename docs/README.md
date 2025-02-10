# Maestro USB API
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://shields.io/) [![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## Overview / Visão Geral
Este repositório contém todo o código-fonte para comunicação entre o portal ITDM e o Maestro via conexão USB.

This repository contains all the source code for communication between the ITDM portal and Maestro via USB connectio

## 📂 Project Structure / Estrutura do Projeto

```
📦 projeto-nome / project-name
 ┣ 📂 docs                     # Project documentation / Documentação do projeto
 ┣ 📂 src                      # Main source code / Código-fonte principal
 ┣ 📂 templates                # Templates for file or page generation / Templates para geração de arquivos ou páginas 
 ┣ 📂 tests                    # Automated tests / Testes automatizados
 ┣ 📄 .gitignore               # Files and directories ignored by Git / Arquivos e diretórios ignorados pelo Git
 ┣ 📄 CHANGELOG.md             # Project change history / Histórico de mudanças do projeto
 ┣ 📄 Dockerfile               # Docker containerization setup / Configuração para containerização via Docker
 ┣ 📄 Makefile                 # Common task automation / Automação de tarefas comuns
 ┣ 📄 PULL_REQUEST_TEMPLATE.md # Pull request template / Template para pull requests
 ┣ 📄 explicação_pastas.txt    # Description of directories and files / Descrição dos diretórios e arquivos
 ┣ 📄 pyproject.toml           # Project configuration for PEP 518 (Python) / Configuração do projeto para PEP 518 (Python)
 ┣ 📄 requirements.txt         # Project dependencies for pip installation / Dependências do projeto para instalação via pip
 ┗ 📄 setup.py                 # Project installation script / Script de instalação do projeto
```

## 🚀 How to Set Up and Run / Como Configurar e Executar 

### Prerequisites / Pré-requisitos
- Ensure you have installed:
    - Python 3.9+
    - Docker (optional, for container execution) / (opcional, para execução via container)

### Installation / Intalação

1. Clone the repository / Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/projeto-nome.git
    ```
2. Create a virtual enviroment and activate it / Crie um ambiente virtual e ative-o:
    ```sh
    python -m venv venv
    source venv/bin/activate # Linux/MacOS
    venv/Scripts/Activate # Windows
    ```
3. Install dependencies / Instale as depêndencias:
    ```sh
    pip install -r requirements.txt
    ```

### Running the project / Executando o projeto

```sh
python src/main/py
```

### Running tests / Rodando os testes
```sh
pytest tests/
```

## 🛠️ Development / Desenvolvimento

### Code Style / Estilo de Código
- This project follows PEP 8. Use Black for automatic formatting:
- Este projeto segue a PEP 8. Utilize o Black para formatação automática:
```sh
black src/
```

### Gerenciamento de Dependências / Dependency Management
- We use `requirements.txt` and `pyproject.toml`. To add new dependencies:
- Utilizamos `requirements.txt` e `pyproject.toml`. Para adicionar novas dependências:
```sh
pip install nome-da-biblioteca / library-name
pip freeze > requirements.txt
```

## 📖 Documentation / Documentação 
- Documentation is available in the `docs` directory. To contribute to the documentation, follow the guidelines in `docs/CONTRIBUTING.md`.

- A documentação está disponível no diretório `docs`. Para contribuir com a documentação, siga as diretrizes dentro de `docs/CONTRIBUTING.md`.

## 📜 License / Licença 
- Este projeto é licenciado sob a [MIT License](LICENSE).

- This project is licensed under the [MIT License](LICENSE).

---