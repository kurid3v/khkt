# submissions/api.py
import requests

def grade_with_ai(problem_text, answer, criteria=""):
    prompt = f"""Bạn là giáo viên. Hãy chấm bài học sinh như một giám khảo chuyên nghiệp.
Đề bài: {problem_text}
Tiêu chí chấm: {criteria if criteria else 'Chấm theo cảm nhận chung của giáo viên'}
Bài làm học sinh: {answer}
Tiêu chí chấm: {criteria if criteria else 'chấm tự do'}
Hãy trả về theo định dạng:
Điểm: x/10
Nhận xét: ..."""

    res = requests.post("http://127.0.0.1:5000/grade", json={
        "question": problem_text,
        "answer": answer,
        "criteria": criteria
    })
    
    try:
        return res.json()["result"]
    except:
        return "Không thể chấm bài (lỗi AI)"


