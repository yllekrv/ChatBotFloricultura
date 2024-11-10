from dialogflow.funcoes import obter_cards_Produtos
from model.chamado import Chamado
from model.Produto import Produto

class DFController:
    async def processar_intencoes(self, req, resp):
        if req.method == "POST" and req.is_json:
            dados = req.get_json()
            intencao = dados['queryResult']['intent']['displayName']
            origem = dados.get('originalDetectIntentRequest', {}).get('source', '')
            resposta = None
            
            if intencao == 'Default Welcome Intent':
                resposta = await exibir_menu(origem)
            elif intencao == 'SelecaoSuporte':
                resposta = await processar_escolha(dados, origem)
            elif intencao == 'simConcluirDemanda':
                resposta = await registrar_chamado(dados, origem)
            
            return resp.json(resposta)

async def exibir_menu(tipo=''):
    resposta = {
        "fulfillmentMessages": []
    }
    
    tipo = 'custom' if tipo else ''
    
    try:
        cards = await obter_cards_Produtos(tipo)
        
        if tipo == 'custom':
            resposta['fulfillmentMessages'].append({
                "text": {
                    "text": [
                        "Ola! Seja bem-vindo!.\n",                        
                        "Estamos preparados para te ajudar com os seguintes produtos:\n"
                    ]
                }
            })
            resposta['fulfillmentMessages'].extend(cards)
            resposta['fulfillmentMessages'].append({
                "text": {
                    "text": ["Por favor nos informe o que você deseja."]
                }
            })
        else:
            resposta["fulfillmentMessages"].append({
                "payload": {
                    "richContent": [[{
                        "type": "description",
                        "title": "Ola! Seja bem-vindo!.\n",
                        "text": [                            
                            "Estamos preparados para te ajudar com os seguintes produtos:\n"
                        ]
                    }]]
                }
            })
            resposta["fulfillmentMessages"][0]["payload"]["richContent"][0].extend(cards)
            resposta["fulfillmentMessages"][0]["payload"]["richContent"][0].append({
                "type": "description",
                "title": "Por favor nos informe o que você deseja.",
                "text": []
            })
        return resposta

    except Exception as erro:
        if tipo == 'custom':
            resposta['fulfillmentMessages'].append({
                "text": {
                    "text": [
                        "Não foi possível recuperar a lista dos produtos disponíveis.",
                        "Desculpe-nos pelo transtorno!"
                    ]
                }
            })
        else:
            resposta["fulfillmentMessages"].append({
                "payload": {
                    "richContent": [[{
                        "type": "description",
                        "title": "Não foi possível recuperar a lista dos produtos disponíveis.\n",
                        "text": [
                            "Desculpe-nos pelo transtorno!\n"
                        ]
                    }]]
                }
            })
        return resposta

async def processar_escolha(dados, origem):
    resposta = {
        "fulfillmentMessages": []
    }
    
    sessao = dados['session'].split('/')[-1]
    global dados_globais
    if 'dados_globais' not in globals():
        dados_globais = {}
    if sessao not in dados_globais:
        dados_globais[sessao] = {'Produtos': []}

    Produtos_selecionados = dados['queryResult']['parameters']['Produto']
    dados_globais[sessao]['Produtos'].extend(Produtos_selecionados)

    lista_mensagens = []
    for prod in Produtos_selecionados:
        Produto = Produto()
        resultado = await Produto.consultar(prod)
        if resultado:
            lista_mensagens.append(f"✅ {prod} registrado com sucesso!\n")
        else:
            lista_mensagens.append(f"❌ O {prod} não está disponível!\n")

    lista_mensagens.append("Posso te ajudar em algo mais?\n")

    if origem:
        resposta['fulfillmentMessages'].append({
            "text": {
                "text": lista_mensagens
            }
        })
    else:
        resposta["fulfillmentMessages"].append({
            "payload": {
                "richContent": [[{
                    "type": "description",
                    "title": "",
                    "text": lista_mensagens
                }]]
            }
        })
    
    return resposta

async def registrar_chamado(dados, origem):
    sessao = dados['session'].split('/')[-1]
    usuario = {"cpf": "111.111.111-11"}
    lista_de_Produtos = []
    
    Produtos_selecionados = dados_globais[sessao]['Produtos']
    Produto_obj = Produto()
    for prod in Produtos_selecionados:
        busca = await Produto_obj.consultar(prod)
        if busca:
            lista_de_Produtos.append(busca[0])

    chamado = Chamado(0, '', usuario, lista_de_Produtos)
    await chamado.gravar()

    resposta = {
        "fulfillmentMessages": []
    }

    mensagem_chamado = [
        f"Pedido nº {chamado.numero} registrado com sucesso.\n",
        "Anote o número para consulta ou acompanhamento posterior.\n"
    ]
    
    if origem:
        resposta['fulfillmentMessages'].append({
            "text": {
                "text": mensagem_chamado
            }
        })
    else:
        resposta["fulfillmentMessages"].append({
            "payload": {
                "richContent": [[{
                    "type": "description",
                    "title": "",
                    "text": mensagem_chamado
                }]]
            }
        })
    
    return resposta
