from model.produto import produto  # Supondo que a classe produto esteja em Model/produto.py

def criar_messenger_card():
    return {
        "type": "info",
        "title": "",
        "subtitle": "",
        "image": {
            "src": {
                "rawUrl": ""
            }
        },
        "actionLink": ""
    }

def criar_custom_card():
    # Exibir nos ambientes padrões, tais como: ambiente de teste do DialogFlow, Slack, etc
    return {
        "card": {
            "title": "",
            "subtitle": "",
            "imageUri": "",
            "buttons": [
                {
                    "text": "botão",
                    "postback": ""
                }
            ]
        }
    }

async def obter_cards_produtos(tipo_card="custom"):
    lista_cards_produtos = []
    produto = produto()
    produtos = await produto.consultar()

    for prdo in produtos:
        if tipo_card == "custom":
            card = criar_custom_card()
            card["card"]["title"] = prdo.nome
            card["card"]["subtitle"] = f"Descrição: {prdo.descricao} \n" \
                                      f"Valor: {prdo.valor} \n" \
                                      f"Prazo para iniciar atendimento: {prdo.tempoInicioAtendimento} \n" \
                                      f"Prazo para solução: {prdo.tempoSolucao}"
            card["card"]["imageUri"] = prdo.urlImagem
            card["card"]["buttons"][0]["postback"] = "https://www.google.com.br/"
        else:
            card = criar_messenger_card()
            card["title"] = prdo.nome
            card["subtitle"] = f"Descrição: {prdo.descricao} \n" \
                               f"Valor: {prdo.valor} \n" \
                               f"Prazo para iniciar atendimento: {prdo.tempoInicioAtendimento} \n" \
                               f"Prazo para solução: {prdo.tempoSolucao}"
            card["image"]["src"]["rawUrl"] = prdo.urlImagem
            card["actionLink"] = "https://www.google.com.br/"

        lista_cards_produtos.append(card)

    return lista_cards_produtos
