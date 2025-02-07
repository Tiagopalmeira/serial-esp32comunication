#include <Arduino.h>
#include "cJSON.h"

bool processJson = false;  // Variável para controlar o estado do LED
bool jsonProcessed = false; // Flag para verificar se o JSON foi processado com sucesso

void setup() {
  Serial.begin(115200);  // Inicia a comunicação serial
  pinMode(2, OUTPUT);    // Configura o pino 2 como saída (LED)
  digitalWrite(2, LOW);  // Garante que o LED comece apagado

  Serial.println("ESP32 iniciada. Aguardando dados JSON...");
}

void loop() {
  if (Serial.available() > 0) {  // Verifica se há dados recebidos
    String receivedData = Serial.readString();  // Lê o dado JSON recebido
    Serial.println("JSON recebido:");
    Serial.println(receivedData);  // Exibe o JSON recebido no Serial Monitor

    // Cria um objeto cJSON a partir da string recebida
    cJSON *json = cJSON_Parse(receivedData.c_str());

    // Verifica se o JSON foi parseado com sucesso
    if (json == NULL) {
      Serial.println("Erro ao ler o JSON");
      jsonProcessed = false;
      digitalWrite(2, LOW);  // Apaga o LED em caso de erro
      return;  // Retorna em caso de erro de deserialização
    }

    // Verifica se a chave "process" existe no JSON
    cJSON *process = cJSON_GetObjectItem(json, "process");

    if (process != NULL && cJSON_IsBool(process)) {
      processJson = cJSON_IsTrue(process);  // Atualiza o valor de processJson
      jsonProcessed = true;
      Serial.println("Chave 'process' encontrada no JSON.");
    } else {
      processJson = false;  // Se a chave não existir, desativa o LED
      jsonProcessed = false;  // Caso não tenha sido válido
      Serial.println("Chave 'process' não encontrada ou não é booleana.");
    }

    // Libera a memória do JSON
    cJSON_Delete(json);
  }

  // Controle do LED de acordo com a variável processJson
  if (jsonProcessed) {
    if (processJson == true) {
      digitalWrite(2, HIGH);  // Acende o LED
      Serial.println("LED ligado: JSON processado com sucesso!");
    } else {
      digitalWrite(2, LOW);   // Apaga o LED
      Serial.println("LED apagado: JSON processado, mas não acionou o processo.");
    }
  } else {
    // Se o JSON não foi processado corretamente, pisca o LED para indicar erro
    for (int i = 0; i < 3; i++) {
      digitalWrite(2, HIGH);  // Acende o LED
      delay(250);              // Aguarda 250ms
      digitalWrite(2, LOW);   // Apaga o LED
      delay(250);              // Aguarda 250ms
    }
    Serial.println("Erro no processamento do JSON.");
  }

  delay(1000);  // Aguarda 1 segundo antes de continuar a leitura
}
