import os
import requests
from flask import Flask, render_template, abort, send_file, Response, request
from config import Config
from cachetools import cached, TTLCache
from urllib.parse import quote

app = Flask(__name__)
app.config.from_object(Config)

# Cache for structured multi-dimensional table data (lives 45 minutes because S3 links expire in 1 hour)
data_cache = TTLCache(maxsize=1, ttl=45 * 60)

@cached(cache=data_cache)
def fetch_bitable_records():
    token = app.config['NOTION_TOKEN']
    database_id = app.config['DATABASE_ID']
    if token == "***" or database_id == "***":
        print("Notion credentials missing.")
        return []

    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    records = []
    has_more = True
    next_cursor = None

    while has_more:
        data = {"page_size": 100}
        if next_cursor:
            data["start_cursor"] = next_cursor
            
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                print(f"Failed to fetch records. Status code: {response.status_code}, error: {response.text}")
                break
                
            result = response.json()
            items = result.get('results', [])
            records.extend(items)
            
            has_more = result.get('has_more', False)
            next_cursor = result.get('next_cursor')
        except Exception as e:
            print(f"Exception while fetching records: {e}")
            break

    formatted_records = []
    for item in records:
        props = item.get('properties', {})
        
        def get_rich_text(field_data):
            if not field_data: return ""
            rich_text_array = field_data.get('title', []) if 'title' in field_data else field_data.get('rich_text', [])
            return "".join([t.get('plain_text', '') for t in rich_text_array])

        # Attempt to get an image URL
        image_url = None
        
        # 1. Try to get page cover
        cover = item.get('cover')
        if cover:
            if cover.get('type') == 'file':
                image_url = cover.get('file', {}).get('url')
            elif cover.get('type') == 'external':
                image_url = cover.get('external', {}).get('url')
                
        # 2. Fallback to properties if no cover
        if not image_url:
            files_prop = props.get('Image', {}) or props.get('Files & media', {})
            files = files_prop.get('files', [])
            if files and len(files) > 0:
                first_file = files[0]
                if first_file.get('type') == 'file':
                    image_url = first_file.get('file', {}).get('url')
                elif first_file.get('type') == 'external':
                    image_url = first_file.get('external', {}).get('url')
        
        title_text = get_rich_text(props.get('Name', {}))
        
        record = {
            'id': item.get('id'),
            'title': title_text[:50] + "..." if len(title_text) > 50 else (title_text or '未命名'),
            'prompt': title_text,
            'image_token': image_url
        }
        
        formatted_records.append(record)

    return formatted_records


@app.route('/')
def index():
    records = fetch_bitable_records()
        
    return render_template(
        'index.html',
        articles=records,
        total_count=len(records)
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
