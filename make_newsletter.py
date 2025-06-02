import feedparser
from datetime import datetime
import pytz

KST = pytz.timezone('Asia/Seoul')
now = datetime.now(KST)
today_str = now.strftime("%Y-%m-%d")
today_kor = now.strftime("%Y년 %m월 %d일")

rss_url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
feed = feedparser.parse(rss_url)

html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>SONG newsletter</title>
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; background: #FFF9E5; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 40px 0; }}
        h1 {{ text-align: center; font-size: 2.5rem; margin-bottom: 0.5em; }}
        .desc {{ text-align: center; color: #666; margin-bottom: 2em; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ background: #fff; border-radius: 12px; margin-bottom: 1em; padding: 1em 1.5em; box-shadow: 0 2px 8px #0001; display: flex; align-items: flex-start; gap: 1em; }}
        .title {{ color: #111; text-decoration: none; font-size: 1.1rem; font-weight: 500; }}
        .title:visited {{ color: #888; }}
        .source {{ color: #1976d2; font-size: 0.95em; margin-left: 0.5em; }}
        .thumb {{ width: 80px; height: 80px; object-fit: cover; border-radius: 8px; flex-shrink: 0; }}
        .footer {{ text-align: center; color: #888; margin-top: 2em; font-size: 0.95em; }}
        .news-content {{ flex: 1; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>SONG newsletter</h1>
        <div class="desc">{today_kor} 구글 최신 뉴스 TOP 10</div>
        <ul>
"""

for entry in feed.entries[:10]:
    title = entry.title
    link = entry.link
    source = entry.get('source', {}).get('title', '언론사')
    # 썸네일 추출 (media_content 또는 media_thumbnail)
    img_url = None
    if 'media_content' in entry and entry.media_content:
        img_url = entry.media_content[0].get('url')
    elif 'media_thumbnail' in entry and entry.media_thumbnail:
        img_url = entry.media_thumbnail[0].get('url')
    html += '<li>'
    if img_url:
        html += f'<img class="thumb" src="{img_url}" alt="뉴스 이미지">'
    html += f'<div class="news-content"><a class="title" href="{link}" target="_blank">{title}</a> <span class="source">{source}</span></div></li>'

html += f"""
        </ul>
        <div class="footer">
            페이지 업데이트 시간: {now.strftime('%Y-%m-%d %H:%M:%S')} (KST)
        </div>
    </div>
</body>
</html>
"""

with open(f"newsletter_{today_str}.html", "w", encoding="utf-8") as f:
    f.write(html)

print("생성 완료:", f"newsletter_{today_str}.html")