import subprocess

def executar_comando(comando):
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True, shell=True)
        print("----- SAIDA DO PROCESSO -----\n")
        print(resultado.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
        print(f"Saída de erro: {e.stderr}")

# Exemplo de uso
comando = "dir"
executar_comando(comando)