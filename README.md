# 📡 Sistema Ciberfísico de Presença por RFID (Core: Hardware & Backend)

Repositório dedicado aos módulos de **Aquisição Física (Firmware ESP32 + RC522)** e **Transporte/Lógica de Controle (Backend Python + MQTT)** do projeto de extensão de chamada escolar automatizada.

---

## 🎯 Sobre o Projeto

O sistema automatiza o registro de presença de alunos por meio de identificação por radiofrequência (RFID). Ao aproximar um cartão ou tag do leitor físico, o identificador único (**UID**) é capturado pelo microcontrolador, transmitido via rede utilizando o protocolo **MQTT** e processado pelo backend em Python, que valida a identidade do estudante, filtra leituras duplicadas e consolida o estado atual da turma.

---

## 🏗️ Arquitetura de Comunicação (Módulos 1 e 2)

* **1. Camada Física / Publicação (Publisher):**
  * **Cenário Real:** Tag RFID $\rightarrow$ Leitor RC522 + ESP32 (via SPI).
  * **Simulador de Testes:** Script `publisher.py` realizando disparos automáticos a cada 3 segundos.
* **2. Transporte de Mensagens (Broker MQTT):**
  * **Host:** `broker.emqx.io` | **Porta:** `1883`
  * **Tópico:** `pucpr/presenca/sala1`
* **3. Lógica de Controle e Estado (Backend Python - `subscribe.py`):**
  * Decodifica e valida o pacote JSON recebido.
  * Verifica se o UID consta no dicionário `alunos_autorizados`.
  * Evita duplicidade consultando a lista `uids_presentes`.
  * Registra a presença com carimbo de data e hora em `lista_presenca`.

---

## 📂 Estrutura do Repositório

* 📁 **`backend/`**
  * `subscribe.py` — Subscriber MQTT e lógica de controle de presença.
  * `publisher.py` — Simulador de envios MQTT para testes de software sem hardware.
* 📁 **`firmware/`** — Código C/C++ do ESP32 com leitor RC522.
* 📁 **`docs/`**
  * `documentacao_presenca_rfid.pdf` — Documentação técnica e fluxogramas do sistema.
* 📄 **`README.md`** — Documentação principal do repositório.

---

## 📄 Contrato de Dados (Payload MQTT)

A comunicação entre o dispositivo de leitura (ESP32 ou Simulador) e o Backend ocorre através do tópico **`pucpr/presenca/sala1`**. O dispositivo publica apenas os dados brutos de identificação em formato JSON, delegando toda a regra de negócio ao servidor:

    {
      "device_id": "SALA_01",
      "uid": "A3B72F91"
    }

### Regras de Negócio Aplicadas pelo Backend (`subscribe.py`):
* **Validação de Formato:** Mensagens fora do padrão JSON ou sem as chaves obrigatórias (`device_id` e `uid`) são descartadas com segurança via blocos `try/except`.
* **Autenticação de UID:** O UID recebido é confrontado com a base em memória (`alunos_autorizados`). Cartões não cadastrados geram alerta imediato de `UID Desconhecido!`.
* **Controle de Duplicidade (Idempotência):** Caso um aluno já registrado passe o cartão novamente na mesma sessão, o sistema identifica o UID na lista `uids_presentes` e bloqueia o registro duplicado.

---

## 🚀 Como Executar o Ambiente Python

### 1. Pré-requisitos
Certifique-se de ter o **Python 3.x** instalado e instale a biblioteca do cliente MQTT (`paho-mqtt`) no terminal:

    pip install paho-mqtt

### 2. Iniciando o Backend (Subscriber)
Abra um terminal na raiz do projeto e execute o receptor de chamadas:

    python backend/subscribe.py

*O terminal exibirá `Conexão Estabelecida com o Broker.` e aguardará novas leituras em tempo real.*

### 3. Simulando Leituras (Opcional - Sem Hardware)
Caso queira testar o fluxo completo sem o ESP32 em mãos, abra um **segundo terminal** e execute o simulador:

    python backend/publisher.py

*O script sorteará periodicamente (a cada 3 segundos) UIDs cadastrados e UIDs desconhecidos (`FFFFFFFF`, `00000000`), enviando-os ao broker para validar todos os cenários do backend.*

---

## 🛣️ Próximos Passos (Roadmap)

- [x] Definição do contrato JSON e integração via Broker EMQX.
- [x] Implementação da lógica de controle, validação de alunos e bloqueio de duplicidade em Python.
- [x] Criação de simulador de publicação automatizada para testes de estresse.
- [ ] Integração final do código embarcado no ESP32 + RC522 na pasta `firmware/`.
- [ ] Persistência local dos registros de presença em arquivos `.json`.
- [ ] Exposição de rota HTTP/API para consumo pelo painel Frontend (Angular).

---

## 👥 Autores (Módulos de Hardware e Backend)

* **Felipe Lima** — *Aquisição Física, Hardware (ESP32 + RC522) e Publicação MQTT (Aluno 1)*
* **Pedro Prasidos** — *Arquitetura MQTT, Lógica de Controle e Estado do Backend (Aluno 2)*
