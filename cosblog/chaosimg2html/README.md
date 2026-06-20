# chaosimg2html

画像ディレクトリからコスブログ用の HTML スニペットを生成する CLI。

サムネ画像 (`<img>`) は軽量な WebP、クリック後の遷移先 (`<a href>`) は元の高解像度画像、という構成で出力する。HTML 自体を軽く保ったまま、原寸でも見せられる。

## 必要環境

- Python 3.9+ (argparse の `BooleanOptionalAction` を利用)
- Pillow

```bash
python3 -m pip install -r requirements.txt
```

## 使い方

```bash
python3 chaosimg2html.py <imgtitle> <imgdir> <cdn_path> [options]
```

### 位置引数

| 引数 | 説明 |
| --- | --- |
| `imgtitle` | 各画像の `alt` / `title` の接頭辞 (英数推奨) |
| `imgdir` | 画像ファイルを入れたローカルディレクトリ |
| `cdn_path` | CDN 上のディレクトリパス (例: `cosbox/20250322_aj`) |

### 主なオプション

| オプション | デフォルト | 説明 |
| --- | --- | --- |
| `--compress` / `--no-compress` | `--compress` (ON) | サムネ WebP を生成し、`<img>` に使う |
| `--cdn` | `https://chaos.alicey.dev/share/` | CDN のベース URL |
| `--max_width` / `--max_height` | 480 / 720 | 縦長画像の HTML 表示サイズ上限 |
| `--max_width_landscape` / `--max_height_landscape` | 720 / 480 | 横長画像の HTML 表示サイズ上限 |

### ヘッダー/フッター用 (任意)

`--model` `--model_twitter` `--char` `--content_title` `--event_name` `--event_date` を全て指定するとモデル情報のヘッダーが、`--camera` `--lenz` (デフォルト値あり) でフッターが付く。

## `--compress` の挙動

`--compress` (デフォルト) で実行すると、`imgdir` 内の各画像について以下が行われる。

- 表示サイズの **2倍** (Retina 対応) に縮小した **WebP** を同じディレクトリに保存
- ファイル名は `<元のbasename>_small.webp` (例: `ALC00109.jpg` → `ALC00109_small.webp`)
- 既存サムネは毎回上書き
- 再実行時は `*_small.webp` をフィルタで除外するため、二重圧縮にはならない

生成された HTML:

```html
<a href="https://chaos.alicey.dev/share/cosbox_test/ALC00109.jpg" ...>
    <img src="https://chaos.alicey.dev/share/cosbox_test/ALC00109_small.webp" width="480" height="720" ...>
</a>
```

`--no-compress` を付けると、サムネを作らず `src` も元画像になる (従来挙動)。

## 実行例

```bash
# 標準 (圧縮あり)
python3 chaosimg2html.py suzura_aj2025 ./img2 cos/20250322AJ/suzura

# ヘッダー/フッター込み
python3 chaosimg2html.py suzura_aj2025 ./img2 cos/20250322AJ/suzura \
    --model すずら --model_twitter suzuran_ro \
    --char 常磐華乃 --content_title ハミダシクリエイティブ \
    --event_name AnimeJapan2025 --event_date 20250322

# 圧縮なし
python3 chaosimg2html.py suzura_aj2025 ./img2 cos/20250322AJ/suzura --no-compress
```

## デプロイ手順 (運用メモ)

1. 上記コマンドで HTML を生成し、出力をブログ記事に貼り付ける
2. `imgdir` の中身 (元画像 + `_small.webp`) をまるごと CDN の `cdn_path` にアップロード
