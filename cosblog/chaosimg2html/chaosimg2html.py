import os
import sys
import argparse
from PIL import Image

def generate_header_html(model, model_twitter, char, content_title, event_name, event_date):
    header_html = f'''
{model} (<a title="" target="_blank" href="https://x.com/{model_twitter}">@{model_twitter}</a>) <br />
<span class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-1tl8opc">
    <span class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-1tl8opc">{char}</span>
&nbsp;/ {content_title}</span> <br />
{event_date} {event_name} <br /><br />
'''
    return header_html


def generate_image_html(imgtitle, imgdir, cdn, cdn_path, max_width, max_height, max_width_landscape, max_height_landscape):
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
        title = f"{imgtitle}_{os.path.splitext(img_file)[0]}"
        
        # HTMLの生成
        html += f'''
<a href="https://chaos.alicey.dev/share/{cdn_path}/{img_file}" title="{title}" target="_blank">
    <img src="https://chaos.alicey.dev/share/{cdn_path}/{img_file}" width="{new_width}" height="{new_height}" border="0" alt="{title}" hspace="5" class="pict">
</a>
<br/>
'''
    return html

def generate_footer_html(camera, lenz):
    camera_map = {
        "ILCE-7M4": ("Sony α7Ⅳ", "https://amzn.to/3EFX9cp"),
    }
    lenz_map = {
        "SIGMA2470DGDNART": ("Sigma 24-70 DG DN Art", "https://amzn.to/4i8VPO3"),
    }

    camera_name = camera_map.get(camera)[0] if camera in camera_map else camera
    camra_link = camera_map.get(camera)[1] if camera in camera_map else ""
    lenz_name = lenz_map.get(lenz)[0] if lenz in lenz_map else lenz
    lenz_link = lenz_map.get(lenz)[1] if lenz in lenz_map else ""


    footer_html = f'''
<br /><br /><br />
Camera:&nbsp;<a href="{camra_link}" target="_blank" title="">{camera_name}</a>
<br />
Lenz:&nbsp;<a href="{lenz_link}" target="_blank" title="">{lenz_name}</a>
'''
    return footer_html

def main():
    # 引数のパース
    parser = argparse.ArgumentParser(description="Generate HTML for image files with CDN paths.")
    parser.add_argument('imgtitle', help="The title to be used for the images (Must english)")
    parser.add_argument('imgdir', help="The directory containing the image files")
    parser.add_argument('cdn_path', help="The base CDN path for the images")
    
    ## option
    # img
    parser.add_argument('--cdn', type=str, default='https://chaos.alicey.dev/share/', help="CDN url (default: https://chaos.alicey.dev/share/)")
    parser.add_argument('--max_width', type=int, default=480, help="The maximum width for portrait images (default: 480px)")
    parser.add_argument('--max_height', type=int, default=720, help="The maximum height for portrait images (default: 720px)")
    parser.add_argument('--max_width_landscape', type=int, default=720, help="The maximum width for landscape images (default: 720px)")
    parser.add_argument('--max_height_landscape', type=int, default=480, help="The maximum height for landscape images (default: 480px)")
    # header
    parser.add_argument('--model', type=str, default=None, help="The model name (ex: すずら)")
    parser.add_argument('--model_twitter', type=str, default=None, help="The model name for Twitter (ex: suzuran_ro)")
    parser.add_argument('--char', type=str, default=None, help="The character name (ex: 常磐華乃)")
    parser.add_argument('--content_title', type=str, default=None, help="The content title (ex: ハミダシクリエイティブ)")
    parser.add_argument('--event_name', type=str, default=None, help="The event name (ex: AnimeJapan2025)")
    parser.add_argument('--event_date', type=str, default=None, help="The event date (ex: 20250322)")
    # footer
    parser.add_argument('--camera', type=str, default='ILCE-7M4', help="The camera name (ex: ILCE-7M4)")
    parser.add_argument('--lenz', type=str, default='SIGMA2470DGDNART', help="The lens name (ex: SIGMA2470DGDNART)")


    # 引数をパース
    args = parser.parse_args()

    ## HTMLを生成
    # header
    if args.model is not None and args.model_twitter is not None and args.char is not None and args.content_title is not None and args.event_name is not None and args.event_date is not None:
        r = generate_header_html(args.model, args.model_twitter, args.char, args.content_title, args.event_name, args.event_date)
        print(r)
    # image
    r = generate_image_html(args.imgtitle, args.imgdir, args.cdn, args.cdn_path, args.max_width, args.max_height, args.max_width_landscape, args.max_height_landscape)
    print(r)
    # footer
    if args.camera is not None and args.lenz is not None:
        r = generate_footer_html(args.camera, args.lenz)
        print(r)

if __name__ == "__main__":
    main()
