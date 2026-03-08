import os
from app import app, fetch_bitable_records
from flask import render_template

def freeze():
    # Set the sub-path for GitHub Pages
    repo_name = 'ai-prompt-gallery'
    app.config['APPLICATION_ROOT'] = f'/{repo_name}/'
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    
    with app.app_context():
        # Use a test request context with the repo name as the base
        with app.test_request_context(base_url=f'https://localhost/{repo_name}/'):
            # Fetch the data
            records = fetch_bitable_records()
            
            # Render the template
            rendered = render_template(
                'index.html',
                articles=records,
                total_count=len(records)
            )
            
            # Optional: Ensure static paths are relative for maximum compatibility
            # However, with APPLICATION_ROOT and base_url, it should generate /repo/static/...
            
            # Save to index.html
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(rendered)
            
    print(f"Successfully frozen Flask app to index.html with path prefix /{repo_name}/")

if __name__ == '__main__':
    freeze()
