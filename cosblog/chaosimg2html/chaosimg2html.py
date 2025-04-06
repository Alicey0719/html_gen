import os
import sys
import argparse
from PIL import Image

def generate_html(titlename, imgdir, cdn, cdn_path, max_width, max_height, max_width_landscape, max_height_landscape):
    # 画像ディレクトリが存在するかチェック
    if not os.path.isdir(imgdir):
        print(f"Error: The directory '{imgdir}' does not exist.")
        return
    
    # 画像ディレクトリ内のファイル一覧を取得
    img_files = [f for f in os.listdir(imgdir) if os.path.isfile(os.path.join(imgdir, f))]
    
    # 拡張子が画像ファイルのものだけフィルタリング
    img_files = [f for f in img_files if f.lower().endswith(('jpeg', 'jpg', 'png'))]
    
    # 画像ファイルが見つからなかった場合
    if not img_files:
        print(f"No image files found in the directory '{imgdir}'.")
        return

    # 画像ファイルごとにHTMLを生成
    html = ''
    for img_file in img_files:
        img_path = os.path.join(imgdir, img_file)
        
        # 画像を開いてサイズを取得
        with Image.open(img_path) as img:
            width, height = img.size
        
        # 横長と縦長でサイズを変える
        if width > height:  # 横長の場合
            ratio = min(max_width_landscape / width, max_height_landscape / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
        else:  # 縦長の場合
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
        
        # タイトルを作成
        title = f"{titlename}_{os.path.splitext(img_file)[0]}"
        
        # HTMLの生成
        html += f'''
<a href="https://chaos.alicey.dev/share/{cdn_path}/{img_file}" title="{title}" target="_blank">
    <img src="https://chaos.alicey.dev/share/{cdn_path}/{img_file}" width="{new_width}" height="{new_height}" border="0" alt="{title}" hspace="5" class="pict">
</a>
<br/>
'''
    return html

def main():
    # 引数のパース
    parser = argparse.ArgumentParser(description="Generate HTML for image files with CDN paths.")
    
    # 必須引数
    parser.add_argument('titlename', help="The title to be used for the images")
    parser.add_argument('imgdir', help="The directory containing the image files")
    parser.add_argument('cdn_path', help="The base CDN path for the images")
    
    # オプション引数
    parser.add_argument('--cdn', type=str, default='https://chaos.alicey.dev/share/', help="CDN url (default: https://chaos.alicey.dev/share/)")
    parser.add_argument('--max_width', type=int, default=480, help="The maximum width for portrait images (default: 480px)")
    parser.add_argument('--max_height', type=int, default=720, help="The maximum height for portrait images (default: 720px)")
    parser.add_argument('--max_width_landscape', type=int, default=720, help="The maximum width for landscape images (default: 720px)")
    parser.add_argument('--max_height_landscape', type=int, default=480, help="The maximum height for landscape images (default: 480px)")

    # 引数をパース
    args = parser.parse_args()

    # HTMLを生成
    r = generate_html(args.titlename, args.imgdir, args.cdn, args.cdn_path, args.max_width, args.max_height, args.max_width_landscape, args.max_height_landscape)
    print(r)

if __name__ == "__main__":
    main()
