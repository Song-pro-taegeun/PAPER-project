from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfReader
import langchain
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from article_service.app.tools.summary import reject_summarize, summarize
import asyncio

langchain.debug = True
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')


@app.route('/get_newsList', methods=['POST'])
async def selectNewsList():
    # url = "https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=020"
    # 1. ajax data 받아오기!!!!
    data = request.form.get('data1') 
    url = data
    
    # 뉴스 오브젝트 배열~~!!(제목, 이미지, 이동 태그, 전체내용, 요약데이터(덕형이형 부분))
    data_list = []

    # 타이틀 받아오는 배열
    titleList = []
    # 이동 태그 받아오는 배열
    hrefList =  []
    # 이미지 받아오는 배열
    imgList = []
    # 본문 받아오는 배열
    realContentList = []
    
    # 요약하는 배열 덕형이형 요 배열에 담으삼
    summaryList = []

    # 1. 뉴스 리스트 페이지 가져오기
    response = requests.get(url)

    # 2. 가져온 HTML을 BeautifulSoup으로 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 3. 클래스명이 type06_headline인 기사 제목 가져오기
    titles = soup.select('.type06_headline a')
    images = soup.select('.type06_headline img')
    # print(soup)

    # 4. 타이틀 배열에 저장
    # i =  0
    for title in titles:
        titleList.append(title.text.strip())
        # i +=1

    # 공백 제거
    titleList = [title for title in titleList if title != ""]
    # print('-----------------------------------')

    # 5. 이동링크인 href 배열에 저장
    # i =  0
    for link in titles:
        # 링크의 href 속성 가져오기
        href = link['href']
        hrefList.append(href)
        # i +=1
    # 중복 제거 순서 유지
    hrefList = list(OrderedDict.fromkeys(hrefList))
    # print('-----------------------------------')

    # 6. 이미지 배열에 저장
    # 임시 예외처리 : 이미지가 없는 언론사에서 에러 발생
    # i =  0
    if(len(images) == 10):
        for img in images:
            # 이미지의 소스 URL 가져오기
            src = img['src']
            imgList.append(src)
            # i +=1
    else :
        for i in range(10):
            imgList.append('')
    # print(imgList)
    # print('imgList##########################')
    # print('-----------------------------------')

    # 7. 본문 내용 구하기 (각 이동태그 별 상세페이지 스크래핑 각각 태우기)
    realContentList = realContentsList(hrefList)
    # print(realContentList)



    ###################################################
    ############### 이덕형 작성부분 시작 ################
    ###################################################
    # 8. 요약 데이터 담기
    # realContentList -> summaryList 요약 내용채우기
    # 덕형이형 요 부분에 요약 태워야함 summaryList 이 배열에 담아야함
    # 본문은 realContentList이 배열에 10개가 담아져 있을거임.
    # for문 돌면서 담아야함.

    # async 처리를 통해 비동기로 요약 요청
    run_func=[]
    for content in realContentList:
        if content=="태그가 다릅니다.":
            run_func.append(reject_summarize())
        else:
            run_func.append(summarize(content))
    summaryList = await asyncio.gather(*run_func)

    # 테스트용 (원문과 요약 동시출력할 수 있도록 처리)
    real_sum=[]
    for r,s in zip(realContentList,summaryList):
        real_sum.append("======원문======<br>" + r + "<br><br>======요약======<br>" + s)
    ###################################################
    ############### 이덕형 작성부분 끝 ################
    ###################################################




    # 찐막 : 리턴 데이터에 가져온 데이터들을 오브젝트로 저장
    for i in range(len(titleList)):
        # 원문 출력
        # item = { 'title' : titleList[i], 'href': hrefList[i], 'img' : imgList[i], 'content' : realContentList[i]}
        # 요약문 출력
        # item = { 'title' : titleList[i], 'href': hrefList[i], 'img' : imgList[i], 'content' : summaryList[i]}
        # 원문+요약문 출력
        item = { 'title' : titleList[i], 'href': hrefList[i], 'img' : imgList[i], 'content' : real_sum[i]}
        # item = { 'title' : titleList[i], 'href': hrefList[i], 'img' : imgList[i]}
        data_list.append(item)

    # print(data_list)
    return data_list


def realContentsList(hrefList):
    dataList = []
    for href in hrefList:
        url = href
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # article 태그의 아이디가 dic_arear것만
        dic_area_element = soup.find('article', {'id': 'dic_area'})
        if dic_area_element:
            # 스트링만 뽑아낸다(html 태그 제외)
            text_content = ' '.join(dic_area_element.stripped_strings)
            dataList.append(text_content)
            print("성공!")
        else:
            print("태그 요소를 찾을 수 없어 예외처리!!!")
            dataList.append('태그가 다릅니다.')
    return dataList
    





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


# # GET 요청 sample code
# # ex) http://127.0.0.1:5000/api/get_example?name=taegeun (파라메터 한 개)
# # ex) http://127.0.0.1:5000/api/get_example?name=taegeun&&age=26 (파라메터 한 개 이상일 떄,)
# @app.route('/api/get_example', methods=['GET'])
# def get_example():
#     # 리퀘스트 문자열에서 'name' 매개변수를 가져옴
#     name = request.args.get('name')
#     age = request.args.get('age')
#     return jsonify({'message': f'너의 이름은, {name}, {age}! (get 방식).'})


# # POST 요청 sample code
# # http://127.0.0.1:5000/api/post_example

# # post json 매개변수~~~
# # {
# #    "name": "태근"
# # }
# @app.route('/api/post_example', methods=['POST'])
# def post_example():
#     # POST 요청에서 JSON 데이터를 추출
#     data = request.get_json()
    
#     name = data['name']
#     return jsonify({'message': f'너의 이름은 : , {name}! (post 방식)'})


if __name__ == '__main__':
    app.run()
