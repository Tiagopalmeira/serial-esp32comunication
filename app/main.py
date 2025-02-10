from fastapi import FastAPI, Body
from typing import Dict

app = FastAPI()

# Variável global que armazenará a configuração
stored_config: Dict = {}

def update_config(modifications: Dict) -> Dict:
    """
    Atualiza a configuração global com as modificações recebidas.
    """
    global stored_config
    stored_config.update(modifications)
    return stored_config

@app.post("/maestro_config")
async def create_maestro_config(data: Dict = Body(...)):
    """
    GET /maestro_config
    Recebe um JSON (serializado no corpo da requisição) e o armazena na variável global,
    retornando-o na resposta.
    
    **Exemplo de corpo da requisição:**
    {
        "param1": "valor1",
        "param2": 123,
        "param3": true
    }
    """
    global stored_config
    stored_config = data  # Armazena o JSON recebido
    return stored_config

@app.get("/maestro_config")
async def get_maestro_config(data: Dict = Body(...)):
    """
    GET /maestro_config
    Recebe um JSON (serializado no corpo da requisição) e o armazena na variável global,
    retornando-o na resposta.
    
    **Exemplo de corpo da requisição:**
    {
        "param1": "valor1",
        "param2": 123,
        "param3": true
    }
    """
    return stored_config

@app.put("/maestro_config")
async def put_maestro_config(modifications: Dict = Body(...)):
    """
    PUT /maestro_config
    Recebe um JSON contendo as modificações desejadas para certas chaves do config
    e atualiza o stored_config com essas modificações. Em seguida, retorna o config atualizado.
    
    **Exemplo de corpo da requisição:**
    {
        "param2": 456,
        "param3": false
    }
    """
    updated_config = update_config(modifications)
    return updated_config

@app.post("/json")
async def post_json(new_json: Dict = Body(...)):
    """
    POST /json
    Recebe um JSON deserializado (por exemplo, enviado por um front-end) e verifica se há
    alguma modificação em relação ao JSON originalmente recebido via GET /x_config.
    
    Se houver alterações, as modificações são encaminhadas para atualizar o config (ou seja,
    são aplicadas via a mesma lógica do PUT /x_config) e o config atualizado é retornado.
    Caso não haja alteração, informa que não houve modificação.
    
    **Exemplo de corpo da requisição:**
    {
        "param1": "novo_valor",
        "param2": 456
    }
    """
    global stored_config
    modifications = {}
    
    # Verifica, para cada chave do JSON recebido, se o valor difere do armazenado
    for key, value in new_json.items():
        if stored_config.get(key) != value:
            modifications[key] = value

    if modifications:
        updated_config = update_config(modifications)
        return {"status": "updated", "updated_config": updated_config}
    else:
        return {"status": "no modification detected", "config": stored_config}
