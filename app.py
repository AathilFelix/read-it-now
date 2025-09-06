from flask import Flask, render_template, request, jsonify
import sys
import io
import os
import random
from contextlib import redirect_stdout, redirect_stderr

# Import the working scraping components
try:
    from main import get_html_with_human_behavior
    from hackclub_ai import get_hackclub_ai
    from langchain_core.messages import HumanMessage
    from bs4 import BeautifulSoup
    import re
    import requests
    import markdown
    import time
except ImportError as e:
    print(f"Error: Could not import required modules: {e}")
    sys.exit(1)

app = Flask(__name__)

# Production configuration for Render
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-render')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

def get_html_fallback(url):
    """Universal enhanced fallback method using requests with multi-site strategies"""
    print("🔄 Using universal enhanced requests fallback method...")
    
    # Universal user agents that work well across sites
    universal_user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0'
    ]
    
    # Universal referer strategies that work across sites
    domain = '/'.join(url.split('/')[:3])
    site_name = domain.replace('https://', '').replace('http://', '').replace('www.', '')
    
    universal_referers = [
        f'https://www.google.com/search?q={site_name.replace(".", "+")}',
        f'https://www.google.co.in/search?q={site_name.replace(".", "+")}+news',
        'https://www.bing.com/search?q=' + site_name.replace('.', '+'),
        'https://duckduckgo.com/?q=' + site_name.replace('.', '+'),
        f'{domain}/',
        f'{domain}/latest',
        f'{domain}/news',
        'https://twitter.com/',
        'https://facebook.com/',
        ''  # No referer
    ]
    
    # Advanced session configurations
    session_configs = [
        {
            'timeout': 15,
            'allow_redirects': True,
            'verify': True,
            'stream': False
        },
        {
            'timeout': 20,
            'allow_redirects': True,
            'verify': False,
            'stream': True
        },
        {
            'timeout': 10,
            'allow_redirects': False,
            'verify': True,
            'stream': False
        }
    ]
    
    # Try multiple strategies with enhanced headers
    for attempt in range(len(universal_user_agents)):
        for referer_idx, referer in enumerate(universal_referers):
            for config_idx, config in enumerate(session_configs):
                try:
                    ua = universal_user_agents[attempt]
                    
                    # Enhanced headers that mimic real browser requests
                    headers = {
                        'User-Agent': ua,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'DNT': '1',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'cross-site' if referer else 'none',
                        'Sec-Fetch-User': '?1',
                        'Cache-Control': 'max-age=0',
                    }
                    
                    # Add Chrome-specific headers for Chrome user agents
                    if 'Chrome' in ua:
                        headers.update({
                            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-ch-viewport-width': '1920',
                            'sec-ch-viewport-height': '1080'
                        })
                    
                    if referer:
                        headers['Referer'] = referer
                    
                    print(f"🔄 Attempt {attempt+1}.{referer_idx+1}.{config_idx+1}: {ua.split()[0][:15]}... Ref: {referer[:30]}...")
                    
                    # Create session with realistic settings
                    session = requests.Session()
                    session.headers.update(headers)
                    
                    # Add realistic cookies for better compatibility
                    session.cookies.update({
                        'cookieconsent_status': 'dismiss',
                        '_ga': f'GA1.2.{random.randint(100000000, 999999999)}.{int(time.time())}',
                        '_gid': f'GA1.2.{random.randint(100000000, 999999999)}.{int(time.time())}',
                    })
                    
                    # For certain sites, establish session via homepage first (like NDTV success)
                    if referer_idx < 3 and any(site in url.lower() for site in ['ndtv.com', 'cnn.com', 'bbc.com']):
                        try:
                            print(f"🏠 Establishing session via {domain}...")
                            homepage_response = session.get(domain, timeout=10)
                            if homepage_response.status_code == 200:
                                time.sleep(random.uniform(1, 2))
                        except Exception as e:
                            print(f"⚠️ Homepage visit failed: {e}")
                    
                    # Now request the actual article
                    response = session.get(url, **config)
                    
                    if response.status_code == 200:
                        content = response.text
                        
                        # Universal blocking detection
                        content_lower = content.lower()
                        block_indicators = [
                            'access denied', 'forbidden', 'blocked', 'error 503', 'error 403',
                            'edgesuite', 'akamai', 'cloudflare ray id', 'reference #18.',
                            'your request has been blocked', 'access to this page has been denied',
                            'service unavailable', 'temporarily unavailable', 'bot protection',
                            'suspicious activity', 'verify you are human', 'captcha', 'recaptcha',
                            'checking your browser', 'please wait while we verify', 'security check'
                        ]
                        
                        if any(indicator in content_lower[:3000] for indicator in block_indicators):
                            print(f"❌ Blocked content detected (indicator found), trying next strategy...")
                            continue
                        
                        # Check content quality - adjust thresholds based on site
                        min_length = 8000 if 'ndtv.com' in url else 5000
                        decent_length = 3000 if 'ndtv.com' in url else 2000
                        
                        if len(content) > min_length:
                            print(f"✅ Success with strategy {attempt+1}.{referer_idx+1}.{config_idx+1}! Got {len(content)} characters")
                            return content
                        elif len(content) > decent_length:
                            # Double-check it's not an error page
                            site_indicators = ['article', 'news', 'content', 'story', 'post']
                            if any(indicator in content_lower for indicator in site_indicators):
                                print(f"✅ Success (decent content) with strategy {attempt+1}.{referer_idx+1}.{config_idx+1}! Got {len(content)} characters")
                                return content
                            else:
                                print(f"⚠️ Suspicious content ({len(content)} chars), trying next...")
                        else:
                            print(f"⚠️ Short content ({len(content)} chars), trying next...")
                            
                    elif response.status_code in [403, 503, 451, 429]:
                        print(f"❌ HTTP {response.status_code} (blocked/rate limited), trying next strategy...")
                        continue
                    else:
                        print(f"⚠️ HTTP {response.status_code}, trying next...")
                        
                except Exception as e:
                    print(f"❌ Strategy {attempt+1}.{referer_idx+1}.{config_idx+1} failed: {e}")
                    continue
                
                # Small delay between attempts to avoid rate limiting
                time.sleep(random.uniform(0.5, 1.5))
    
    print("❌ All enhanced fallback strategies failed")
    return None

def process_markdown_to_html(text):
    """Convert markdown text to HTML for proper display"""
    try:
        # Convert markdown to HTML with extensions
        html = markdown.markdown(text, extensions=['nl2br', 'fenced_code', 'tables'])
        return html
    except Exception as e:
        print(f"⚠️ Markdown processing failed: {e}")
        # Enhanced fallback: basic formatting
        text = text.replace('**', '<strong>').replace('**', '</strong>')
        text = text.replace('*', '<em>').replace('*', '</em>')
        
        # Handle headers
        text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        
        # Handle line breaks and paragraphs
        text = text.replace('\n\n', '</p><p>')
        text = f'<p>{text}</p>'
        
        # Clean up empty paragraphs
        text = re.sub(r'<p>\s*</p>', '', text)
        
        return text

def extract_and_summarize(url):
    """Extract article and return title, content, and 1-minute summary - Render optimized"""
    try:
        print(f"🔄 Processing: {url}")

        # Check if we're being rate limited by NDTV specifically
        if 'ndtv.com' in url.lower():
            print("🎯 NDTV detected - checking for rate limiting...")
            # Add a longer delay for NDTV to avoid rate limiting
            time.sleep(random.uniform(2, 5))
        
        # Universal strategy: Try Playwright first, then enhanced fallback for ALL sites
        html_content = None
        
        # For NDTV, use enhanced fallback first since it's proven to work better
        if 'ndtv.com' in url.lower():
            print("🎯 NDTV detected - using enhanced fallback method first...")
            html_content = get_html_fallback(url)
            
            # If fallback fails, try Playwright as backup for NDTV
            if not html_content:
                print("🔄 NDTV fallback failed, trying Playwright as backup...")
                try:
                    html_content = get_html_with_human_behavior(url)
                except Exception as e:
                    print(f"❌ Playwright also failed for NDTV: {e}")
        else:
            # For all other sites: Try Playwright first, then enhanced fallback
            print("🎭 Trying Playwright first...")
            try:
                html_content = get_html_with_human_behavior(url)
                if html_content:
                    print(f"✅ Playwright succeeded: {len(html_content)} characters")
            except Exception as e:
                print(f"❌ Playwright failed: {e}")
                html_content = None
            
            # If Playwright failed or returned nothing, use enhanced fallback
            if not html_content:
                print("🔄 Falling back to enhanced anti-bot method...")
                html_content = get_html_fallback(url)
                if html_content:
                    print(f"✅ Enhanced fallback succeeded: {len(html_content)} characters")

        if not html_content:
            # Special handling for NDTV rate limiting
            if 'ndtv.com' in url.lower():
                return {
                    "error": "NDTV is currently blocking automated access due to rate limiting. This is because:\n"
                            "• Multiple recent requests from the same IP address\n"
                            "• NDTV's enhanced anti-bot protection (Akamai EdgeSuite)\n"
                            "• Temporary IP-based blocking\n\n"
                            "💡 Solutions:\n"
                            "• Wait 10-15 minutes before trying again\n"
                            "• Try accessing from a different network/location\n"
                            "• Use a VPN if available\n"
                            "• Try the article URL directly in a regular browser first\n\n"
                            "The system will work normally once the rate limit expires."
                }
            return {"error": "Failed to access the article. The site might have strong anti-bot protection."}
        
        # Check for access denied, error pages, or blocked content
        html_lower = html_content.lower()
        error_indicators = [
            'access denied', 'forbidden', 'blocked', 'error 403', 'error 503',
            'service unavailable', 'temporarily unavailable', 'edgesuite',
            'cloudflare', 'bot protection', 'captcha', 'verification required',
            'your request has been blocked', 'access to this page has been denied'
        ]
        
        if any(indicator in html_lower[:2000] for indicator in error_indicators):
            print("🚫 Detected blocked/error page, trying enhanced bypass...")
            
            # Try fallback method if Playwright was used
            if html_content and len(html_content) < 5000:  # Small response likely means error page
                print("🔄 Trying requests fallback for bypass...")
                fallback_content = get_html_fallback(url)
                if fallback_content and len(fallback_content) > len(html_content):
                    html_content = fallback_content
                    print(f"✅ Fallback successful: {len(html_content)} characters")
            
            # Still blocked? Return specific error
            html_lower_updated = html_content.lower()
            if any(indicator in html_lower_updated[:2000] for indicator in error_indicators):
                return {
                    "error": "The website is blocking automated access. This could be due to:\n"
                            "• Increased anti-bot protection\n"
                            "• CDN/EdgeSuite restrictions\n"
                            "• Temporary server issues\n\n"
                            "Try again in a few minutes or use a different article URL."
                }

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

        try:
            exec(generated_code, exec_namespace)
            title = exec_namespace.get('title', '')
            content = exec_namespace.get('content', '')
        except Exception as e:
            print(f"⚠️ AI extraction failed: {e}")
            title = ''
            content = ''

        # Enhanced fallback extraction with Wikipedia-specific handling
        if len(str(content)) < 100:
            soup = BeautifulSoup(html_content, 'html.parser')
            print("🔧 Using enhanced fallback extraction...")
            
            # Title extraction with multiple fallbacks
            if not title:
                # Wikipedia specific title
                if 'wikipedia.org' in url.lower():
                    wiki_title = soup.find('h1', class_='firstHeading')
                    title = wiki_title.get_text().strip() if wiki_title else ''
                
                # General title fallbacks
                if not title:
                    title_tag = soup.find('title')
                    h1_tag = soup.find('h1')
                    og_title = soup.find('meta', property='og:title')
                    
                    title = (title_tag and title_tag.get_text().strip()) or \
                           (h1_tag and h1_tag.get_text().strip()) or \
                           (og_title and og_title.get('content', '')) or \
                           "Article"
            
            # Content extraction with site-specific handling
            content_text = ""
            
            # Wikipedia specific extraction
            if 'wikipedia.org' in url.lower():
                print("🌐 Detected Wikipedia, using specialized extraction...")
                
                # Get main content div
                content_div = soup.find('div', id='mw-content-text')
                if content_div:
                    # Get all paragraphs in the main content
                    paragraphs = content_div.find_all('p', recursive=True)
                    content_paragraphs = []
                    
                    for p in paragraphs:
                        text = p.get_text().strip()
                        # Skip empty paragraphs and references
                        if len(text) > 50 and not text.startswith('[') and 'cite' not in text.lower():
                            content_paragraphs.append(text)
                    
                    content_text = ' '.join(content_paragraphs[:10])  # First 10 substantial paragraphs
                    print(f"📝 Wikipedia extraction: {len(content_text)} characters")
            
            # General content extraction fallbacks
            if len(content_text) < 100:
                print("🔧 Using general content extraction...")
                
                # Try article tag first
                article = soup.find('article')
                if article:
                    paragraphs = article.find_all('p')
                    content_text = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 20])
                
                # Try main content areas
                if len(content_text) < 100:
                    content_selectors = [
                        'div[class*="content"]',
                        'div[class*="article"]', 
                        'div[class*="story"]',
                        'div[class*="text"]',
                        'div[class*="body"]',
                        'main',
                        '.post-content',
                        '.entry-content'
                    ]
                    
                    for selector in content_selectors:
                        content_divs = soup.select(selector)
                        if content_divs:
                            for div in content_divs:
                                paragraphs = div.find_all('p')
                                text = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 20])
                                if len(text) > len(content_text):
                                    content_text = text
                            if len(content_text) > 100:
                                break
                
                # Last resort: all paragraphs
                if len(content_text) < 100:
                    paragraphs = soup.find_all('p')
                    content_text = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 20])
            
            content = content_text
            print(f"📝 Final extraction: {len(content)} characters")

        if len(str(content)) < 50:
            return {"error": "Could not extract sufficient content from the article."}

        # Generate 1-minute summary
        summary_prompt = f"""Create a concise 1-minute summary of this article that captures the key points:

        Title: {title}
        Content: {content[:4000]}

        Instructions:
        - Write 2-3 short paragraphs that someone can read in about 1 minute
        - Use **bold** for important terms and concepts
        - Use clear, engaging language
        - Focus on the most important information
        - Make it informative and easy to understand

        IMPORTANT: Write your response directly in markdown format. Do NOT wrap it in code blocks or use ```markdown tags.
        
        Example format:
        **Key Point**: Description of the main issue or event.

        Second paragraph with more details and **important terms** highlighted.

        Final paragraph with conclusions or implications.
        """

        summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
        summary_raw = re.sub(r'<think>.*?</think>', '', summary_response.content, flags=re.DOTALL).strip()
        
        # Clean up any code block wrapping that AI might add
        if '```markdown' in summary_raw:
            summary_raw = summary_raw.split('```markdown')[1].split('```')[0].strip()
        elif summary_raw.startswith('```') and summary_raw.endswith('```'):
            summary_raw = summary_raw[3:-3].strip()
        
        # Process markdown to HTML for proper display
        summary_html = process_markdown_to_html(summary_raw)

        return {
            "title": title,
            "content": content,
            "summary": summary_raw,  # Keep raw for API
            "summary_html": summary_html,  # HTML version for display
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
            'summary_html': result['summary_html'],
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

@app.route('/debug', methods=['POST'])
def debug_extraction():
    """Debug endpoint to test extraction without AI processing"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'})
        
        # Get HTML content
        html_content = None
        try:
            html_content = get_html_with_human_behavior(url)
        except Exception as e:
            print(f"❌ Playwright failed: {e}")
            html_content = get_html_fallback(url)

        if not html_content:
            return jsonify({'error': 'Failed to fetch content'})
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract basic info
        title = soup.find('title')
        title_text = title.get_text().strip() if title else 'No title'
        
        # Get page structure info
        paragraphs = soup.find_all('p')
        p_count = len(paragraphs)
        total_text = ' '.join([p.get_text().strip() for p in paragraphs])
        
        return jsonify({
            'url': url,
            'title': title_text,
            'html_length': len(html_content),
            'paragraph_count': p_count,
            'total_text_length': len(total_text),
            'sample_text': total_text[:500] + '...' if len(total_text) > 500 else total_text,
            'is_wikipedia': 'wikipedia.org' in url.lower()
        })
        
    except Exception as e:
        return jsonify({'error': f'Debug failed: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
