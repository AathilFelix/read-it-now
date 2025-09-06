from flask import Flask, render_template, request, jsonify
import sys
import io
import os
from contextlib import redirect_stdout, redirect_stderr

# Import the working scraping components
try:
    from main import get_html_with_human_behavior
    from hackclub_ai import get_hackclub_ai
    from langchain_core.messages import HumanMessage
    from bs4 import BeautifulSoup
    import re
    import requests
except ImportError as e:
    print(f"Error: Could not import required modules: {e}")
    sys.exit(1)

app = Flask(__name__)

# Production configuration for Render
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-render')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

def get_html_fallback(url):
    """Fallback method using requests when Playwright fails on Render"""
    print("🔄 Using requests fallback method...")
    
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    
    for i, ua in enumerate(user_agents):
        try:
            headers = {
                'User-Agent': ua,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            print(f"🔄 Trying user agent {i+1}...")
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                print(f"✅ Success with requests method!")
                return response.text
                
        except Exception as e:
            print(f"❌ Requests attempt {i+1} failed: {e}")
            continue
    
    return None

def extract_and_summarize(url):
    """Extract article and return title, content, and 1-minute summary - Render optimized"""
    try:
        print(f"🔄 Processing: {url}")

        # Try Playwright first, fall back to requests if it fails
        html_content = None
        try:
            html_content = get_html_with_human_behavior(url)
        except Exception as e:
            print(f"❌ Playwright failed: {e}")
            print("🔄 Falling back to requests...")
            html_content = get_html_fallback(url)

        if not html_content:
            return {"error": "Failed to access the article. The site might have strong anti-bot protection."}

        # AI-powered content extraction
        llm = get_hackclub_ai()

        extraction_prompt = f"""Extract content from this news article: {url}

        The HTML contains an article. Extract:
        1. Article title (look for h1, h2, or meta og:title)
        2. Main article content (look for article, div with content/story classes, or paragraph tags)

        Only output Python code that sets 'title' and 'content' variables as strings.
        """

        response = llm.invoke([HumanMessage(content=extraction_prompt)])
        generated_code = response.content.strip()

        # Clean the generated code
        generated_code = re.sub(r'<think>.*?</think>', '', generated_code, flags=re.DOTALL)
        if '```python' in generated_code:
            generated_code = generated_code.split('```python')[1].split('```')[0]
        elif '```' in generated_code:
            generated_code = generated_code.split('```')[1].split('```')[0]
        generated_code = generated_code.strip()

        # Execute the extraction
        exec_namespace = {
            'BeautifulSoup': BeautifulSoup,
            'html_content': html_content,
            'soup': BeautifulSoup(html_content, 'html.parser'),
            'url': url
        }

        exec(generated_code, exec_namespace)

        title = exec_namespace.get('title', '')
        content = exec_namespace.get('content', '')

        # Fallback extraction if AI didn't work well
        if len(str(content)) < 100:
            soup = BeautifulSoup(html_content, 'html.parser')
            title = title or (soup.find('title') and soup.find('title').get_text().strip()) or "Article"
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 10])

        if len(str(content)) < 50:
            return {"error": "Could not extract sufficient content from the article."}

        # Generate 1-minute summary
        summary_prompt = f"""Create a concise 1-minute summary of this article that captures the key points:

        Title: {title}
        Content: {content[:4000]}

        Write 2-3 short paragraphs that someone can read in about 1 minute.
        """

        summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
        summary = re.sub(r'<think>.*?</think>', '', summary_response.content, flags=re.DOTALL).strip()

        return {
            "title": title,
            "content": content,
            "summary": summary,
            "url": url
        }

    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}

@app.route('/')
def home():
    """Homepage for Read It Now - Article Summarizer"""
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    """API endpoint to extract and summarize an article"""
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'success': False, 'error': 'URL is required'})

        # Extract and summarize the article
        result = extract_and_summarize(url)

        if 'error' in result:
            return jsonify({'success': False, 'error': result['error']})

        return jsonify({
            'success': True,
            'title': result['title'],
            'summary': result['summary'],
            'url': result['url']
        })

    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})

@app.route('/summary')
def summary():
    """Display the article summary"""
    return render_template('summary.html')

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy', 'service': 'read-it-now'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print("📖 Starting Read It Now server...")
    print(f"🚀 Visit: http://localhost:{port}")
    print("💡 Turn any article into a 1-minute summary!")
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=port)
