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
except ImportError as e:
    print(f"Error: Could not import required modules: {e}")
    sys.exit(1)

app = Flask(__name__)

def extract_and_summarize(url):
    """Extract article and return title, content, and 1-minute summary"""
    try:
        print(f"🔄 Processing: {url}")

        # Get HTML content using human behavior simulation
        html_content = get_html_with_human_behavior(url)

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

if __name__ == '__main__':
    app.run(debug=True)
