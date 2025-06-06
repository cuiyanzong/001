from flask import Flask, request, send_file, render_template, jsonify
from rembg import remove
from io import BytesIO
from PIL import Image, ImageOps
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    print("🎯 收到请求 /remove-bg")
    file = request.files['image']
    mode = request.form.get('mode', 'remove')
    print(f"✅ 收到文件: {file.filename}")
    input_bytes = file.read()

    try:
        if mode == 'remove':
            print("🚀 调用 rembg 去除背景...")
            output_bytes = remove(input_bytes)
            output_image = Image.open(BytesIO(output_bytes)).convert("RGBA")
        else:
            input_image = Image.open(BytesIO(input_bytes)).convert("RGBA")
            if mode == 'grayscale':
                print("🎨 应用灰度处理...")
                output_image = ImageOps.grayscale(input_image).convert("RGBA")
            elif mode == 'invert':
                print("🎨 应用颜色反转...")
                r, g, b, a = input_image.split()
                rgb_image = Image.merge("RGB", (r, g, b))
                inverted = ImageOps.invert(rgb_image)
                output_image = Image.merge("RGBA", (*inverted.split(), a))
            else:
                return jsonify({'error': 'Invalid mode'}), 400

        img_io = BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        print("✅ 处理完成，返回图像。")

        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        print(f"❌ 处理错误: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
