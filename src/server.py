from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/add_review', methods=['POST'])
def add_review():
    try:
        restaurant_name = request.form['restaurantName']
        review_text = request.form['review']

        input_file_path = "./inputs/reviews.json"

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

        # Aqui você pode retornar um alerta de sucesso para o front-end
        return jsonify({'success': True, 'message': 'Revisão adicionada com sucesso!'})
    except KeyError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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

    return jsonify(restaurant_names)

if __name__ == '__main__':
    app.run(debug=True)
