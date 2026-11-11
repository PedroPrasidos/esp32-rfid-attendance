# 📡 Sistema Ciberfísico de Presença por RFID (Core: Hardware & Backend)

Repositório dedicado aos módulos de **Aquisição Física (Firmware ESP32 + RC522)** e **Transporte/Lógica de Controle (Backend Python + MQTT)** do projeto de extensão de chamada escolar automatizada.

---

## 🎯 Sobre o Projeto

O sistema automatiza o registro de presença de alunos por meio de identificação por radiofrequência (RFID)[cite: 1]. Ao aproximar um cartão ou tag do leitor físico, o identificador único (**UID**) é capturado pelo microcontrolador, transmitido via rede utilizando o protocolo **MQTT** e processado pelo backend em Python, que valida a identidade do estudante, filtra leituras duplicadas e consolida o estado atual da turma[cite: 1, 2, 5].

---

## 🏗️ Arquitetura de Comunicação (Módulos 1 e 2)

```text
+-----------------------------------------------------------------------+
| 1. CAMADA FÍSICA / PUBLICAÇÃO (Publisher)                             |
|                                                                       |
|  [Tag RFID] ──(SPI)──> [Leitor RC522 + ESP32]  (Cenário Real)         |
|  [publisher.py] ──(Disparo a cada 3s)          (Simulador de Testes)  |
+-----------------------------------+-----------------------------------+
                                    |
                                    | Wi-Fi / MQTT (JSON Payload)
                                    | Tópico: pucpr/presenca/sala1
                                    v
+-----------------------------------------------------------------------+
| 2. TRANSPORTE DE MENSAGENS (Broker MQTT)                              |
|                                                                       |
|  Host: broker.emqx.io | Porta: 1883                                   |
+-----------------------------------+-----------------------------------+
                                    |
                                    | Assinatura (Subscribe)
                                    v
+-----------------------------------------------------------------------+
| 3. LÓGICA DE CONTROLE E ESTADO (Backend Python - subscribe.py)        |
|                                                                       |
|  1. Decodifica e valida o JSON recebido                               |
|  2. Verifica se o UID consta no dicionário `alunos_autorizados`       |
|  3. Evita duplicidade consultando `uids_presentes`                    |
|  4. Registra presença com data/hora em `lista_presenca`               |
+-----------------------------------------------------------------------+
