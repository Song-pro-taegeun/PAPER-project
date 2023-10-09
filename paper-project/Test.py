from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
count = 1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/paper/analysis')
def analysis():
    return render_template('main.html')



# GET 요청
# ex) http://127.0.0.1:5000/api/get_example?name=taegeun (파라메터 한 개)
# ex) http://127.0.0.1:5000/api/get_example?name=taegeun&&age=26 (파라메터 한 개 이상일 떄,)
@app.route('/api/get_example', methods=['GET'])
def get_example():
    # 리퀘스트 문자열에서 'name' 매개변수를 가져옴
    name = request.args.get('name')
    age = request.args.get('age')
    return jsonify({'message': f'너의 이름은, {name}, {age}! (get 방식).'})


# POST 요청
# http://127.0.0.1:5000/api/post_example

# post json 매개변수~~~
# {
#    "name": "태근"
# }
@app.route('/api/post_example', methods=['POST'])
def post_example():
    # POST 요청에서 JSON 데이터를 추출
    data = request.get_json()
    
    name = data['name']
    return jsonify({'message': f'너의 이름은 : , {name}! (post 방식)'})


if __name__ == '__main__':
    app.run()
