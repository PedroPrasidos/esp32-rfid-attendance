import paho.mqtt.client as mqtt
import json
from datetime import datetime

#Dados de exemplo

alunos_autorizados = {
    "A3B72F91": "Pedro Prasidos",
    "9BF44CC1": "Maria Oliveira",
    "4A2B8C9F": "Lucas Mendes",
    "11223344": "Ana Clara Souza",
    "7F8E9D0A": "Gabriel Santos",
    "C4D5E6F7": "Juliana Costa",
    "B1A2C3D4": "Rafael Almeida",
    "55667788": "Fernanda Lima",
    "E9F8A7B6": "Matheus Rocha",
    "3C4D5E6F": "Camila Ferreira",
    "8899AABB": "Bruno Carvalho",
    "D1E2F3A4": "Larissa Ribeiro",
    "6789ABCD": "Thiago Martins",
    "F0E1D2C3": "Beatriz Gomes",
    "1A2B3C4D": "Vinícius Araújo",
}

uids_presentes = []
lista_presenca = []


def ao_conectar(client, userdata, flags, reason_code, properties):
    
    #Estabelecimento de conexão
    
    if reason_code == 0:
        print("Conexão Estabelecida com o Broker.")
        client.subscribe("pucpr/presenca/sala1")
    else:
        print("Falha na conexão com o broker!")
        
        
        

def ao_receber(client, userdata, msg):
    
    data_hora_atual = datetime.now()
    
    #Lógica de Controle
    
    try:
        
        conteudo = msg.payload.decode("utf-8") #Por padrão já usa utf-8, sem precisar colocá-lo explicitamente.

        dados = json.loads(conteudo) #Devolve o formato de dicionário

        uid = dados["uid"]
        dispositivo = dados["device_id"]
                        
        if uid in alunos_autorizados:
            
            nome_aluno = alunos_autorizados[uid]

            if uid not in uids_presentes:
                                    
                lista_presenca.append({
                    "nome": nome_aluno,
                    "uid": uid,
                    "dispositivo": dispositivo,
                    "data": data_hora_atual.strftime("%d/%m/%Y"),
                    "horario": data_hora_atual.strftime("%H:%M:%S")
                })
                
                uids_presentes.append(uid)
                
                print(f"[{data_hora_atual.strftime("%H:%M:%S")}] {nome_aluno} - Presença registrada com sucesso!")
                
            else:
                print(f"[{data_hora_atual.strftime("%H:%M:%S")}] {nome_aluno} - Presença já registrada anteriormente!")
                
        else:
            print(f"[{data_hora_atual.strftime("%H:%M:%S")}] UID Desconhecido!")
            
        print(f"\n{"=" * 10} LISTA DE PRESENÇA {"=" * 10}\n\n{lista_presenca}\n\nALUNOS REGISTRADOS = {len(alunos_autorizados)} | ALUNOS PRESENTES = {len(lista_presenca)} | ALUNOS FALTANTES = {len(alunos_autorizados) - len(lista_presenca)}\n\n{"=" * 20}\n")

    except (json.JSONDecodeError, KeyError, TypeError):
        
        print("Mensagem inválida!")
        
        


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = ao_conectar
client.connect("broker.emqx.io", 1883)

client.on_message = ao_receber

print("AGUARDANDO LEITURAS...")

client.loop_forever()