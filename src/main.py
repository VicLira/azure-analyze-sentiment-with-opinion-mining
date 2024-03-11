# -------------------------------------------------------------------------
# Criado por Victor Lira
# --------------------------------------------------------------------------

"""
FILE: sample_analyze_sentiment_with_opinion_mining.py

DESCRIPTION:
    This sample demonstrates how to analyze sentiment on a more granular level, mining individual
    opinions from reviews (also known as aspect-based sentiment analysis).
    This feature is only available for clients with api version v3.1 and up.

    In this sample, we will be a hotel owner looking for complaints users have about our hotel,
    in the hopes that we can improve people's experiences.

USAGE:
    python sample_analyze_sentiment_with_opinion_mining.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_LANGUAGE_ENDPOINT - the endpoint to your Language resource.
    2) AZURE_LANGUAGE_KEY - your Language subscription key

OUTPUT:
    In this sample we will be a hotel owner going through reviews of their hotel to find complaints.
    I first found a handful of reviews for my hotel. Let's see what we have to improve.

    Let's first see the general sentiment of each of these reviews
    ...We have 1 positive reviews, 2 mixed reviews, and 0 negative reviews.

    Since these reviews seem so mixed, and since I'm interested in finding exactly what it is about my hotel that should be improved, let's find the complaints users have about individual aspects of this hotel

    In order to do that, I'm going to extract the targets of a negative sentiment. I'm going to map each of these targets to the mined opinion object we get back to aggregate the reviews by target.

    Let's now go through the aspects of our hotel people have complained about and see what users have specifically said
    Users have made 1 complaints about 'food', specifically saying that it's 'unacceptable'
    Users have made 1 complaints about 'service', specifically saying that it's 'unacceptable'
    Users have made 3 complaints about 'toilet', specifically saying that it's 'smelly', 'broken', 'dirty'


    Looking at the breakdown, I can see what aspects of my hotel need improvement, and based off of both the number and content of the complaints users have made about my toilets, I need to get that fixed ASAP.
"""


import json


def process_review(input_folder, output_folder) -> None:
    import os
    from dotenv import load_dotenv
    import typing
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    load_dotenv()

    LANGUAGE_END = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    LANGUAGE_KEY = os.environ["AZURE_LANGUAGE_KEY"]

    text_analytics_client = TextAnalyticsClient(
        endpoint=LANGUAGE_END,
        credential=AzureKeyCredential(LANGUAGE_KEY)
    )

    # Verifica se a pasta "outputs" existe e cria se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Lista os arquivos na pasta "inputs"
    files = os.listdir(input_folder)

    all_reviews_data = []  # Lista para armazenar todos os dados das reviews

    for file in files:
        if file.endswith('.json'):
            with open(os.path.join(input_folder, file), 'r') as f:
                data = json.load(f)

                for restaurant_data in data:
                    restaurant_name = restaurant_data['restaurant']
                    reviews = restaurant_data['reviews']

                    # Dicionário para armazenar os resultados das análises de sentimentos e mineração de opinião
                    restaurant_results = {
                        'restaurant_name': restaurant_name,
                        'sentiment_analysis': {},
                        'opinion_mining': {}
                    }

                    for review_data in reviews:
                        review_text = review_data['review']

                        # Realiza a análise de sentimento
                        sentiment = text_analytics_client.analyze_sentiment([review_text])[0].sentiment

                        # Realiza a mineração de opinião
                        opinion_mining = text_analytics_client.analyze_sentiment([review_text], show_opinion_mining=True)[0]

                        # Processa os resultados da mineração de opinião
                        opinions = []
                        for sentence in opinion_mining.sentences:
                            for mined_opinion in sentence.mined_opinions:
                                target = mined_opinion.target.text
                                assessment = mined_opinion.assessments[0].text
                                opinions.append({"target": target, "assessment": assessment})

                        # Adiciona os resultados na estrutura do dicionário
                        restaurant_results['sentiment_analysis'][review_text] = sentiment
                        restaurant_results['opinion_mining'][review_text] = opinions

                    # Adiciona os resultados na estrutura do dicionário
                    all_reviews_data.append(restaurant_results)

    # Escreve os resultados em arquivos na pasta "outputs"
    for restaurant_results in all_reviews_data:
        restaurant_name = restaurant_results['restaurant_name']
        output_file = os.path.join(output_folder, f"{restaurant_name}_results.json")

        # Escreve os resultados em um arquivo JSON na pasta de saída
        with open(output_file, 'w') as out_f:
            json.dump(restaurant_results, out_f, indent=4)


if __name__ == '__main__':
    input_folder = "./src/inputs"
    output_folder = "./src/outputs"
    process_review(input_folder, output_folder)