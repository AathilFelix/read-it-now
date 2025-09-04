from hackclub_ai import get_hackclub_ai
from langchain_core.messages import HumanMessage
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import re
import random
from tqdm import tqdm

def mimic_human_browsing(page, url):
    """Mimic actual human browsing behavior with progress tracking"""
    print("🤖 Mimicking human behavior...")
    
    # Progress bar for human simulation
    steps = [
        "Visiting homepage",
        "Mouse movements", 
        "Initial page load",
        "Reading simulation",
        "Scrolling patterns",
        "Final content load"
    ]
    
    progress = tqdm(steps, desc="Human simulation", ncols=70)
    
    # 1. Start by visiting the homepage first (like a real user)
    base_url = "/".join(url.split("/")[:3])
    progress.set_description("📱 Visiting homepage")
    progress.update(1)
    
    try:
        page.goto(base_url, wait_until='domcontentloaded', timeout=20000)
        time.sleep(random.uniform(1, 2))
        
        # Human-like mouse movements and scrolling on homepage
        progress.set_description("🖱️ Mouse movements")
        progress.update(1)
        
        page.mouse.move(random.randint(100, 800), random.randint(100, 600))
        page.evaluate("window.scrollTo(0, 200)")
        time.sleep(random.uniform(0.5, 1))
        
        # Now navigate to the actual article
        progress.set_description("Loading article...")
        progress.update(1)
        page.goto(url, wait_until='domcontentloaded', timeout=20000)
        
    except Exception as e:
        progress.set_description("Direct navigation...")
        page.goto(url, wait_until='domcontentloaded', timeout=20000)
    
    # 2. Wait like a human reading the page (reduced)
    progress.set_description("📖 Reading simulation")
    progress.update(1)
    time.sleep(random.uniform(1.5, 3))  # Reduced from 3-6
    
    # 3. Human-like scrolling pattern (faster)
    progress.set_description("📜 Scrolling")
    progress.update(1)
    
    scroll_positions = [0, 300, 600, 400, 800]
    for pos in scroll_positions:
        page.evaluate(f"window.scrollTo(0, {pos})")
        time.sleep(random.uniform(0.3, 0.8))
        
        page.mouse.move(
            random.randint(100, 1200), 
            random.randint(100, 700)
        )
        time.sleep(random.uniform(0.1, 0.3)) 
    
    progress.set_description("✅ Content ready")
    progress.update(1)
    time.sleep(random.uniform(1, 2))
    
    progress.close()

def get_html_with_human_behavior(url):
    """Get HTML by perfectly mimicking human behavior - headless for server"""
    print(f"👤 Starting stealth human-like session...")
    
    with sync_playwright() as p:
        # Launch browser in headless mode for server compatibility
        browser = p.chromium.launch(
            headless=True,  # Server compatible
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                # '--disable-web-security',
                # '--ignore-certificate-errors',
                # '--disable-extensions',
                # '--disable-plugins',
                # '--disable-default-apps',
                # '--disable-background-timer-throttling',
                # '--disable-renderer-backgrounding',
                # '--disable-backgrounding-occluded-windows'
            ]
        )
        
        # Create a realistic browser context
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1440, 'height': 900},
            locale='en-US',
            timezone_id='America/New_York',
            geolocation={'latitude': 40.7128, 'longitude': -74.0060},
            permissions=['geolocation']
        )
        
        # Add scripts to hide automation
        # context.add_init_script("""
        #     // Remove webdriver property
        #     delete navigator.__proto__.webdriver;
            
        #     // Mock plugins
        #     Object.defineProperty(navigator, 'plugins', {
        #         get: () => [
        #             {0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"}},
        #         ],
        #     });
            
        #     // Mock languages
        #     Object.defineProperty(navigator, 'languages', {
        #         get: () => ['en-US', 'en'],
        #     });
            
        #     // Add chrome object
        #     window.chrome = {
        #         runtime: {},
        #         loadTimes: function() {},
        #         csi: function() {},
        #         app: {}
        #     };
            
        #     // Mock permissions
        #     const originalQuery = window.navigator.permissions.query;
        #     window.navigator.permissions.query = (parameters) => (
        #         parameters.name === 'notifications' ?
        #             Promise.resolve({ state: Notification.permission }) :
        #             originalQuery(parameters)
        #     );
        # """)
        
        # Set human-like headers
        context.set_extra_http_headers({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.google.com/'
        })
        
        page = context.new_page()
        
        try:
            # Mimic complete human browsing session
            mimic_human_browsing(page, url)
            
            # Check if we successfully loaded the page
            title = page.title()
            print(f"📄 Page title: {title}")
            
            if any(block_word in title.lower() for block_word in ['access denied', 'forbidden', 'blocked', 'error']):
                print(f"❌ Still getting blocked: {title}")
                
                # Try one more human trick - quick interactions
                print("🖱️ Trying human interactions...")
                try:
                    page.click('body')
                    time.sleep(0.5)  # Reduced
                    page.keyboard.press('Tab')
                    time.sleep(0.3)  # Reduced
                    page.keyboard.press('Enter')
                    time.sleep(1)    # Reduced
                except:
                    pass
                
                title = page.title()
                if any(block_word in title.lower() for block_word in ['access denied', 'forbidden', 'blocked']):
                    print(f"❌ Still blocked after human simulation")
                    return None
            
            html = page.content()
            print(f"✅ Human browsing successful! Got {len(html)} characters")
            
            return html
            
        except Exception as e:
            print(f"❌ Human browsing failed: {e}")
            return None
        finally:
            browser.close()

def scrape_with_ai(url):
    '''
    Enhanced scraper that perfectly mimics human browsing - server optimized
    '''
    print(f"🔄 Starting stealth scraping session...")
    print(f"🎯 Target: {url}")
    print("=" * 60)

    html_content = get_html_with_human_behavior(url)
    
    if not html_content:
        print("❌ Human simulation failed")
        print("💡 The site might have detected automation despite human simulation")
        return
    
    print("🤖 Processing with AI...")
    llm = get_hackclub_ai()
    
    prompt = f"""Extract content from this news article: {url}

The HTML contains a news article. Extract:
1. Article title (look for h1, h2, or meta og:title or anything useful)
2. Main article content (look for div with story/content classes or paragraph tags)

The HTML is provided as 'html_content' variable.
BeautifulSoup is available as 'BeautifulSoup'.

Set variables 'title' and 'content' as strings.

Only output raw Python code, no explanations."""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        generated_code = response.content.strip()
        
        # Clean response
        generated_code = re.sub(r'<think>.*?</think>', '', generated_code, flags=re.DOTALL)
        if '```python' in generated_code:
            generated_code = generated_code.split('```python')[1].split('```')[0]
        elif '```' in generated_code:
            generated_code = generated_code.split('```')[1].split('```')[0]
        generated_code = generated_code.strip()
        
        # print("🤖 AI Generated extraction code:")
        # print("-" * 40)
        # print(generated_code)
        # print("-" * 40)
        
        # Execute extraction with progress
        print("⚙️ Extracting content...")
        
        exec_namespace = {
            'BeautifulSoup': BeautifulSoup,
            'html_content': html_content,
            'soup': BeautifulSoup(html_content, 'html.parser'),
            'url': url
        }
        
        exec(generated_code, exec_namespace)
        
        title = exec_namespace.get('title', '')
        content = exec_namespace.get('content', '')
        
        print(f"\n📰 Extracted Title: {title}")
        print(f"📝 Content Length: {len(str(content))} characters")
        
        if len(str(content)) < 100:
            print("🔧 Trying manual fallback extraction...")
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Manual title extraction
            title = title or (soup.find('title') and soup.find('title').get_text().strip()) or "No title"
            
            # Manual content extraction
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 10])
            
            print(f"📝 Fallback content length: {len(content)} characters")
        
        if len(str(content)) < 50:
            print("❌ Insufficient content extracted")
            return
        
        # Generate summary with progress
        print("🧠 Generating AI summary...")
        summary_prompt = f"""Summarize this news article in 2-3 paragraphs so that it should be read in 1 minute:

Title: {title}
Content: {content[:4000]}"""

        summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
        
        print(f"\n📄 AI Summary:")
        summary_response_cleaned = re.sub(r'<think>.*?</think>', '', summary_response.content, flags=re.DOTALL)
        print("=" * 60)
        print(summary_response_cleaned)
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()