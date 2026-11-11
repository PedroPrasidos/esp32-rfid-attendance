import paho.mqtt.client as mqtt
import json
import time
import random

# Lista com alguns UIDs cadastrados e alguns desconhecidos para testar todos os cenários
uids_teste = [
    "A3B72F91", # Pedro Prasidos
    "9BF44CC1", # Maria Oliveira
    "4A2B8C9F", # Lucas Mendes
    "11223344", # Ana Clara Souza
    "7F8E9D0A", # Gabriel Santos
    "FFFFFFFF", # Cartão Desconhecido 1
    "00000000"  # Cartão Desconhecido 2
]

def ao_conectar(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conexão MQTT aceita pelo broker!")
    else:
        print(f"Conexão recusada: {reason_code}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = ao_conectar
client.connect("broker.emqx.io", 1883)

# Inicia o loop em segundo plano para manter a conexão ativa
client.loop_start()

time.sleep(1) #Evitar que o print de conexão aceita apareça primeiro (evitando queima de largada)

while True:
    # 1. Criamos o dicionário Python sorteando um UID da lista
    dados = {
        "device_id": "SALA_01",
        "uid": random.choice(uids_teste)
    }

    # 2. Transformamos o dicionário em texto JSON (str)
    mensagem_json = json.dumps(dados)

    # 3. Publicamos o texto JSON no tópico
    client.publish("pucpr/presenca/sala1", mensagem_json)
    print(f"Mensagem enviada: {mensagem_json}")

    time.sleep(3)