import requests
import json

def getAllAccounts():
    response = requests.get("http://localhost:8080/contas")
    contas = response.json()
    return contas

def formatarClientes(dicionaryList):
    clientesFormatado = {}

    for cliente in dicionaryList:
        
    # clientes = {"Jennifer":{"numConta":"02312540","cpf":"002025","ispb":bancos_ispb["Agibank"],"numAgencia":"1254"}}
        clientesFormatado[cliente["cliente"]["nome"]] = {"numConta":cliente["numConta"],
                                                    "cpf":cliente["cliente"]["cpf"],
                                                    "ispb":cliente["ispb"],
                                                    "numAgencia":cliente["numAgencia"]}
        print(clientesFormatado)
        print("                ")
    return clientesFormatado;



def sendRequest(TransacaoPayLoad:dict):
    requests.post(url="http://localhost:8080/transacoes", data=TransacaoPayLoad)

ContasCliente = getAllAccounts()

# clientes = {"Jennifer":{"numConta":"02312540","cpf":"002025","ispb":bancos_ispb["Agibank"],"numAgencia":"1254"}}

clientes = formatarClientes(ContasCliente)
print(clientes.keys())