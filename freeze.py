import os
from app import app, fetch_bitable_records
from flask import render_template

def freeze():
    with app.app_context():
        # Fetch the data
        records = fetch_bitable_records()
        
        # Render the template
        rendered = render_template(
            'index.html',
            articles=records,
            total_count=len(records)
        )
        
        # Save to index.html
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(rendered)
            
    print("Successfully frozen Flask app to index.html")

if __name__ == '__main__':
    freeze()
