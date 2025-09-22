# KHKT

Dự án Django phục vụ quản lý và chấm bài tập online.

## 🚀 Yêu cầu

- Python 3.10+
- pip, virtualenv
- Git
- (Khuyến nghị) VPS/Server chạy Ubuntu 20.04+  
- Nginx + Gunicorn (cho production)

## ⚙️ Cài đặt local

```bash
git clone git@github.com:kurid3v/khkt.git
cd khkt
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install --no-cache-dir --use-pep517 -r requirements.txt (Ép pip dùng PEP517 build system, bỏ qua setup.py cũ) 

# migrate & collect static
python manage.py migrate
python manage.py collectstatic --noinput

# chạy server dev
python manage.py runserver
python ai_grader.py
