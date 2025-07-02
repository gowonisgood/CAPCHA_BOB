from flask import Flask, request, send_file, jsonify, session, render_template
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, string, os, math

app = Flask(__name__)
app.secret_key = os.urandom(24)

def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_captcha_image(text):
    width, height = 160, 60
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    # 다양한 폰트 시도 (없으면 기본)
    try:
        font = ImageFont.truetype('arial.ttf', 36)
    except:
        font = ImageFont.load_default()
    # 랜덤 라인
    for _ in range(8):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        d.line(((x1, y1), (x2, y2)), fill=(random.randint(100,200),random.randint(100,200),random.randint(100,200)), width=2)
    # 랜덤 점
    for _ in range(120):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        d.point((x, y), fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    # 글자 그리기 (각 글자마다 위치/각도/색 랜덤)
    for i, char in enumerate(text):
        font_size = random.randint(28, 38)
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except:
            font = ImageFont.load_default()
        angle = random.uniform(-30, 30)
        x = 20 + i*26 + random.randint(-3, 3)
        y = random.randint(5, 18)
        char_img = Image.new('RGBA', (40, 50), (255,255,255,0))
        char_draw = ImageDraw.Draw(char_img)
        char_color = (random.randint(0,120), random.randint(0,120), random.randint(0,120))
        char_draw.text((5, 5), char, font=font, fill=char_color)
        char_img = char_img.rotate(angle, resample=Image.BICUBIC, expand=1)
        img.paste(char_img, (x, y), char_img)
    # 블러 등 후처리 효과
    img = img.filter(ImageFilter.SMOOTH)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

@app.route('/')
def index_route():
    return render_template('index.html')

@app.route('/captcha')
def captcha():
    text = generate_captcha_text()
    session['captcha'] = text
    img_io = generate_captcha_image(text)
    return send_file(img_io, mimetype='image/png')

@app.route('/verify', methods=['POST'])
def verify():
    user_input = request.json.get('captcha', '')
    real = session.get('captcha', '')
    return jsonify({'success': user_input.upper() == real})

if __name__ == '__main__':
    app.run(debug=True) 