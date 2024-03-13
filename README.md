
# Criando um Recurso no Portal Language Studio Azure

## Ideia do Projeto:

O projeto utiliza a API Language Studio da Azure para processar textos de reviews de restaurantes, permitindo a extração e análise de sentimentos. Isso facilita a compreensão das opiniões dos clientes e a avaliação da reputação de diferentes restaurantes com base em seus reviews. O projeto atualmente é capaz de extrair os reviews e analisar os sentimentos associados a eles.

Para utilizar as APIs de processamento de linguagem do Azure, é necessário criar um recurso no portal `https://language.cognitive.azure.com`. Aqui está um guia passo a passo:

### 1. Acessar o Portal:

* Acesse o portal `language.cognitive.azure.com` usando sua conta Microsoft.
* Se for sua primeira vez, aceite os termos de serviço e a política de privacidade.

### 2. Criar um Recurso:

* Clique no botão **+ Criar Recurso**.
* Na caixa de pesquisa, digite "Language Studio" e selecione o resultado.
* Preencha os seguintes campos:

    - **Nome do Recurso:** Insira um nome único para o seu recurso.
    - **Assinatura:** Selecione a assinatura do Azure que deseja usar.
    - **Grupo de Recursos:** Crie um novo grupo de recursos ou selecione um existente.
    - **Localização:** Selecione a região mais próxima de você.

* Clique em **Criar**. Aguarde alguns minutos enquanto o recurso é criado.

### 3. Obter Chave de Acesso:

* Navegue até o seu recurso no portal language studio. (https://language.cognitive.azure.com/tryout/sentiment)
* Na seção **Ccopie a chave de acesso e o ponto de extremidade. Você precisará deles para usar as APIs de processamento de linguagem.
* Certifique-se de salvar essas informações em um local seguro.

![Chaves da API Azure Vision](https://raw.githubusercontent.com/VicLira/azure-analyze-sentiment-with-opinion-mining/main/src/imgs-readme/next-steps.png)

### Rodar

* Para rodar esse projeto é necessário clonar o repositório
* Ir até a pasta src
* E rodar o comando python server.py or python3 server.py

![Projeto](https://raw.githubusercontent.com/VicLira/azure-analyze-sentiment-with-opinion-mining/main/src/imgs-readme/project.png)


### Recursos Adicionais:

* Quickstart: Azure Language Studio v1.0 Read: [quickstart](https://learn.microsoft.com/pt-br/azure/ai-services/language-service/sentiment-opinion-mining/quickstart?tabs=windows)

### Resolução de Problemas (insights):

* Durante o desenvolvimento, eu tentei ir um pouco além e montar um servidor simples em python com flask para conseguir além de extrair sentimentos e emoções de restaurantes que já estão no json, o usuario poder adicionar reviews que também serão analisadas, independente de linguagem.

**Este foi o guia que utilizei para criar um recurso no portal Language Studio Azure e começar a usar as APIs de processamento de linguagem.**

**Obrigado pela atenção! Se tiver dúvidas, entre em contato através do meu e-mail: victor.liracarlos@gmail.com**





