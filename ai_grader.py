# from flask import Flask, request, jsonify
# import requests

# app = Flask(__name__)

# GEMINI_API_KEY = "AIzaSyCjkMcW81IOJjSOj0QzPxw1-8AjeSxJw64"
# GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# @app.route('/grade', methods=['POST'])
# def grade():
#     data = request.get_json()
#     question = data.get('question', '')
#     answer = data.get('answer', '')

#     prompt = f"""Bạn là giáo viên. Hãy chấm bài học sinh như một giám khảo chuyên nghiệp.
#     Đề bài: {question}
#     Bài làm học sinh: {answer}
    
#     Hãy trả về theo định dạng:
#     Điểm: x/10
#     Nhận xét: ..."""

#     response = requests.post(GEMINI_URL, json={
#         "contents": [{"parts": [{"text": prompt}]}]
#     })

#     try:
#         result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
#     except Exception:
#         result = "Không thể chấm bài (lỗi AI)"

#     return jsonify({"result": result})

# if __name__ == '__main__':
#     app.run(port=5000)

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyDEcVqdViepruNXNYL04wbo3j_om1pyg4w"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
@app.route('/grade', methods=['POST'])
def grade():
    data = request.get_json()
    question = data.get('question', '')
    answer = data.get('answer', '')
    criteria = data.get('criteria', '')

    prompt = f"""Bạn là giáo viên. Hãy chấm bài học sinh như một giám khảo chuyên nghiệp.
Đề bài: {question}
Tiêu chí chấm: {criteria if criteria else 'chấm tự do'}
Bài làm học sinh: {answer}

Hãy trả về theo định dạng:
Điểm: x/10
Nhận xét: ...
"""

    print("📥 Prompt gửi Gemini:")
    print(prompt)

    try:
        response = requests.post(GEMINI_URL, json={
            "contents": [{"parts": [{"text": prompt}]}]
            
        })
        print(response.status_code)
        print(response.text)
        print("📤 Gemini response (raw):")
        print(response.text)

        json_response = response.json()
        result = json_response["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"result": result})

    except Exception as e:
        print("❌ Lỗi khi xử lý Gemini response:")
        print(str(e))
        return jsonify({"result": "Không thể chấm bài (lỗi AI nội bộ)"}), 500


if __name__ == '__main__':
    app.run(port=5000)