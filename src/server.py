import threading
from flask import Flask, render_template, request, jsonify
from main import process_review 
import os
import json

app = Flask(__name__)

# Criação de um evento para sinalizar a conclusão do processamento da revisão
processing_complete = threading.Event()

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/add_review', methods=['POST'])
def add_review():
    try:
        restaurant_name = request.form['restaurantName']
        review_text = request.form['review']

        input_file_path = "./inputs/reviews.json"
        input_path = "./inputs"
        output_path = "./outputs"

        # Se o arquivo JSON já existe, carrega o conteúdo e adiciona a nova revisão
        if os.path.exists(input_file_path):
            with open(input_file_path, 'r') as f:
                data = json.load(f)
                
            # Procura o restaurante no arquivo existente
            found_restaurant = False
            for restaurant_data in data:
                if restaurant_data['restaurant'] == restaurant_name:
                    restaurant_data['reviews'].append({"review": review_text})
                    found_restaurant = True
                    break

            # Se o restaurante não foi encontrado, cria um novo registro para ele
            if not found_restaurant:
                data.append({
                    "restaurant": restaurant_name,
                    "reviews": [{"review": review_text}]
                })
        else:
            # Se o arquivo JSON não existir, cria um novo com o restaurante e a revisão
            data = [{
                "restaurant": restaurant_name,
                "reviews": [{"review": review_text}]
            }]

        # Escreve os dados de volta no arquivo JSON
        with open(input_file_path, 'w') as f:
            json.dump(data, f, indent=4)

        # Chama process_review() em uma nova thread
        threading.Thread(target=process_review_with_event, args=(input_path, output_path)).start()

        # Espera até que o evento de conclusão seja definido (ou seja, o processamento da revisão foi concluído)
        processing_complete.wait()

        # Atualiza a lista de restaurantes após o processamento da revisão
        restaurant_names = list_restaurants()

        # Limpa o evento de conclusão para futuros usos
        processing_complete.clear()

        # Aqui você pode retornar um alerta de sucesso para o front-end, junto com a lista de restaurantes
        return jsonify({'success': True, 'message': 'Revisão adicionada com sucesso!', 'restaurants': restaurant_names})

    except KeyError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

### """
### FIM DO ADD_REVIEW 
### """
    
def process_review_with_event(input_path, output_path):
    # Chama a função de processamento da revisão
    process_review(input_path, output_path)

    # Define o evento de conclusão
    processing_complete.set()


### """
### COMEÇO DO GET_REVIEW/RESTAURANTE 
### """

@app.route('/get_reviews/<restaurant_name>', methods=['GET'])
def get_reviews(restaurant_name):
    # Ler os dados do arquivo JSON no diretório "outputs"
    with open(f"./outputs/{restaurant_name}_results.json", 'r') as f:
        data = json.load(f)

    return jsonify(data)

@app.route('/list_restaurants')
def list_restaurants():
    output_folder = "./outputs"
    restaurant_names = []

    # Itera sobre os arquivos na pasta 'outputs'
    for filename in os.listdir(output_folder):
        if filename.endswith('_results.json'):
            # Remove o sufixo "_results" do nome do arquivo para obter o nome do restaurante
            restaurant_name = filename.replace('_results.json', '')
            restaurant_names.append(restaurant_name)

    return restaurant_names

if __name__ == '__main__':
    app.run(debug=True)
