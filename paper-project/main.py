from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfReader
from article_service.app.agent import run_langchain
from langchain.globals import set_debug
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')


@app.route('/get_newsList', methods=['POST'])
def selectNewsList():
    # url = "https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=020"
    data = request.form.get('data1') 
    url = data
    data_list = []
    titleList = []
    hrefList =  []
    imgList = []

    # 웹 페이지 가져오기
    response = requests.get(url)
    # 가져온 HTML을 BeautifulSoup으로 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 클래스명이 type06_headline인 기사 제목 가져오기
    titles = soup.select('.type06_headline a')
    images = soup.select('.type06_headline img')

    # 타이틀 변수에 저장
    i =  0
    for title in titles:
        titleList.append(title.text.strip())
        i +=1

    # 공백 제거
    titleList = [title for title in titleList if title != ""]
    # print('-----------------------------------')


    # href 변수에 저장
    i =  0
    for link in titles:
        # 링크의 href 속성 가져오기
        href = link['href']
        hrefList.append(href)
        i +=1
    # 중복 제거 순서 유지
    hrefList = list(OrderedDict.fromkeys(hrefList))
    # print('-----------------------------------')

    i =  0
    # 이미지 변수에 저장
    for img in images:
        # 이미지의 소스 URL 가져오기
        src = img['src']
        imgList.append(src)
        # print(imgList)
        i +=1
    # print('-----------------------------------')

    for i in range(len(titleList)):
        item = { 'title' : titleList[i], 'href': hrefList[i], 'img' : imgList[i]}
        data_list.append(item)

    # print(data_list)
    return data_list










# @app.route('/', methods=['GET', 'POST'])
# def upload_pdf():
#     # post 요청
#     if request.method == 'POST':
#         # 업로드된 파일 가져오기
#         uploaded_file = request.files['pdf_file']
#         # 파일이 있다면,
#         if uploaded_file.filename != '': 
#             # 텍스트 추출 함수 호 출
#             pdf_text = extract_text_from_pdf(uploaded_file)

#             ### 전처리 코드가 들어가야됨 ###
#             pdf_text = run_langchain("요약해줘", pdf_text)



#             # result.html 렌더링처리(pdf_text 값을 담아서 뿌려준다.)
#             return render_template('result.html', pdf_text=pdf_text)
        
#     # upload 파일 렌더링 
#     return render_template('upload.html')



# # 텍스트 호출 함수 정의
# def extract_text_from_pdf(pdf_file):
#     pdf_text = ''
#     # PdfReader 객체 생성
#     pdf_reader = PdfReader(pdf_file)
    
#     # pdf 페이지만큼 반복문
#     for page in pdf_reader.pages:

#         # 텍스트 추출
#         pdf_text += page.extract_text()
#     return pdf_text


# GET 요청 sample code
# ex) http://127.0.0.1:5000/api/get_example?name=taegeun (파라메터 한 개)
# ex) http://127.0.0.1:5000/api/get_example?name=taegeun&&age=26 (파라메터 한 개 이상일 떄,)
@app.route('/api/get_example', methods=['GET'])
def get_example():
    # 리퀘스트 문자열에서 'name' 매개변수를 가져옴
    name = request.args.get('name')
    age = request.args.get('age')
    return jsonify({'message': f'너의 이름은, {name}, {age}! (get 방식).'})


# POST 요청 sample code
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
