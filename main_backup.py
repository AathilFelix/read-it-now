from hackclub_ai import get_hackclub_ai
from langchain_core.messages import HumanMessage
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import re
import random

def mimic_human_browsing(page, url):
    """Mimic actual human browsing behavior with progress tracking"""
    print("🤖 Mimicking human behavior...")
    
    # 1. Start by visiting the homepage first (like a real user)
    base_url = "/".join(url.split("/")[:3])
    
    try:
        page.goto(base_url, wait_until='domcontentloaded', timeout=20000)
        time.sleep(random.uniform(1, 2))
        
        page.mouse.move(random.randint(100, 800), random.randint(100, 600))
        page.evaluate("window.scrollTo(0, 200)")
        time.sleep(random.uniform(0.5, 1))
        
        # Now navigate to the actual article
        page.goto(url, wait_until='domcontentloaded', timeout=20000)
        
    except Exception as e:
        page.goto(url, wait_until='domcontentloaded', timeout=20000)
    
    # 2. Wait like a human reading the page (reduced)
    time.sleep(random.uniform(1.5, 3))  # Reduced from 3-6
    
    # 3. Human-like scrolling pattern (faster)
    scroll_positions = [0, 300, 600, 400, 800]
    for pos in scroll_positions:
        page.evaluate(f"window.scrollTo(0, {pos})")
        time.sleep(random.uniform(0.3, 0.8))
        
        page.mouse.move(
            random.randint(100, 1200), 
            random.randint(100, 700)
        )
        time.sleep(random.uniform(0.1, 0.3)) 
    
    time.sleep(random.uniform(1, 2))


def get_html_with_human_behavior(url):
    """Get HTML by perfectly mimicking human behavior - Ultra stealth mode for NDTV"""
    print(f"👤 Starting ultra-stealth human-like session for NDTV...")
    
    # Randomize browser characteristics for each request
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'
    ]
    
    viewports = [
        {'width': 1920, 'height': 1080},
        {'width': 1366, 'height': 768},
        {'width': 1440, 'height': 900},
        {'width': 1536, 'height': 864},
        {'width': 1280, 'height': 720}
    ]
    
    timezones = ['America/New_York', 'America/Los_Angeles', 'Europe/London', 'Asia/Kolkata']
    
    # Randomize for this session
    chosen_ua = random.choice(user_agents)
    chosen_viewport = random.choice(viewports)
    chosen_timezone = random.choice(timezones)
    
    try:
        with sync_playwright() as p:
            # Enhanced launch arguments to avoid detection
            browser = p.chromium.launch(
                headless=True,  # Required for Render
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-setuid-sandbox',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--single-process',
                    '--disable-gpu',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--ignore-certificate-errors',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--disable-default-apps',
                    '--disable-background-timer-throttling',
                    '--disable-renderer-backgrounding',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-ipc-flooding-protection',
                    '--disable-hang-monitor',
                    '--disable-prompt-on-repost',
                    '--no-default-browser-check',
                    '--disable-sync',
                    '--disable-component-update',
                    '--disable-background-networking',
                    f'--user-agent={chosen_ua}'
                ]
            )
            
            # Create ultra-realistic browser context 
            context = browser.new_context(
                user_agent=chosen_ua,
                viewport=chosen_viewport,
                locale='en-US',
                timezone_id=chosen_timezone,
                extra_http_headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'DNT': '1',
                    'Connection': 'keep-alive'
                }
            )
            
            # Ultra-comprehensive scripts to hide ALL automation traces
            context.add_init_script("""
                // Complete webdriver removal
                delete navigator.__proto__.webdriver;
                delete navigator.webdriver;
                delete window.navigator.webdriver;
                
                // Override webdriver property completely
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                    configurable: true
                });
                
                // Remove automation traces from window
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                
                // Mock realistic Chrome environment
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {
                            0: {type: "application/x-google-chrome-pdf", suffixes: "pdf"},
                            description: "Portable Document Format",
                            filename: "internal-pdf-viewer",
                            length: 1,
                            name: "Chrome PDF Plugin"
                        },
                        {
                            0: {type: "application/x-nacl", suffixes: ""},
                            description: "Native Client Executable",
                            filename: "internal-nacl-plugin", 
                            length: 1,
                            name: "Native Client"
                        }
                    ],
                });
                
                // Realistic language settings
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en', 'hi'],
                });
                
                // Enhanced Chrome object with realistic properties
                window.chrome = {
                    runtime: {
                        onConnect: undefined,
                        onMessage: undefined,
                        getManifest: undefined,
                        connect: undefined
                    },
                    loadTimes: function() {
                        return {
                            commitLoadTime: Date.now() - Math.random() * 1000,
                            connectionInfo: 'h2',
                            finishDocumentLoadTime: Date.now() - Math.random() * 500,
                            finishLoadTime: Date.now() - Math.random() * 300,
                            firstPaintAfterLoadTime: 0,
                            firstPaintTime: Date.now() - Math.random() * 800,
                            navigationType: 'Navigation',
                            npnNegotiatedProtocol: 'h2',
                            requestTime: Date.now() - Math.random() * 1200,
                            startLoadTime: Date.now() - Math.random() * 1000,
                            wasAlternateProtocolAvailable: false,
                            wasFetchedViaSpdy: true,
                            wasNpnNegotiated: true
                        };
                    },
                    csi: function() {
                        return {
                            onloadT: Date.now(),
                            startE: Date.now() - Math.random() * 2000,
                            tran: 15
                        };
                    }
                };
                
                // Mock realistic hardware concurrency
                Object.defineProperty(navigator, 'hardwareConcurrency', {
                    get: () => 4 + Math.floor(Math.random() * 4)
                });
                
                // Mock realistic device memory
                Object.defineProperty(navigator, 'deviceMemory', {
                    get: () => Math.pow(2, Math.floor(Math.random() * 3) + 2)
                });
                
                // Override permission queries
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
                
                // Add realistic screen properties
                Object.defineProperty(screen, 'availWidth', {
                    get: () => screen.width
                });
                Object.defineProperty(screen, 'availHeight', {
                    get: () => screen.height - 40
                });
                
                // Mock WebGL vendor/renderer to avoid detection
                const getParameter = WebGLRenderingContext.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === 37445) {
                        return 'Google Inc. (NVIDIA)';
                    }
                    if (parameter === 37446) {
                        return 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.5671)';
                    }
                    return getParameter(parameter);
                };
                
                // Override toString to hide traces
                window.navigator.webdriver = undefined;
                Object.defineProperty(navigator, 'webdriver', {
                    value: undefined,
                    writable: false
                });
            """)
            
            page = context.new_page()
            
            # Add more stealth: block tracking and analytics
            page.route("**/*", lambda route: (
                route.abort() if any(tracker in route.request.url for tracker in [
                    'google-analytics', 'googletagmanager', 'facebook.com/tr',
                    'doubleclick', 'googlesyndication', 'amazon-adsystem',
                    'scorecardresearch', 'quantserve', 'outbrain', 'taboola'
                ]) else route.continue_()
            ))
            
            # NDTV-specific ultra-human browsing pattern
            if 'ndtv.com' in url.lower():
                print("🎯 Applying NDTV-specific ultra-stealth pattern...")
                
                # First, visit Google and search for NDTV (simulate organic traffic)
                page.goto('https://www.google.com', wait_until='domcontentloaded')
                time.sleep(random.uniform(2, 4))
                
                # Simulate typing in search box
                try:
                    search_box = page.locator('input[name="q"]')
                    if search_box.count() > 0:
                        search_box.fill('NDTV news site')
                        time.sleep(random.uniform(1, 2))
                        page.keyboard.press('Enter')
                        time.sleep(random.uniform(2, 3))
                    
                    # Click on NDTV main site link (simulate organic entry)
                    try:
                        ndtv_link = page.locator('a[href*="ndtv.com"]').first
                        if ndtv_link.count() > 0:
                            ndtv_link.click()
                            time.sleep(random.uniform(3, 5))
                    except:
                        # Fallback: direct navigation
                        page.goto('https://www.ndtv.com', wait_until='domcontentloaded')
                        time.sleep(random.uniform(3, 5))
                except Exception as e:
                    print(f"⚠️ Google search failed: {e}")
                    page.goto('https://www.ndtv.com', wait_until='domcontentloaded')
                    time.sleep(random.uniform(3, 5))
                
                # Browse around NDTV homepage like a real user
                page.mouse.move(random.randint(200, 800), random.randint(100, 400))
                page.evaluate("window.scrollTo(0, 300)")
                time.sleep(random.uniform(2, 3))
                
                page.mouse.move(random.randint(300, 900), random.randint(200, 600))
                page.evaluate("window.scrollTo(0, 600)")
                time.sleep(random.uniform(1, 2))
                
                # Now navigate to the actual article
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
            else:
                # Standard human behavior for other sites
                mimic_human_browsing(page, url)
            
            # Extended wait for content to load (NDTV might have delayed loading)
            time.sleep(random.uniform(3, 6))
            
            # Additional human-like interactions
            page.mouse.move(random.randint(100, 1000), random.randint(100, 600))
            page.evaluate("window.scrollTo(0, 400)")
            time.sleep(random.uniform(1, 2))
            
            page.mouse.move(random.randint(200, 800), random.randint(300, 700))
            page.evaluate("window.scrollTo(0, 800)")
            time.sleep(random.uniform(1, 2))
            
            # Get final HTML content
            html_content = page.content()
            
            # Check if we got blocked
            title = page.title()
            print(f"📄 Page title: {title}")
            
            if any(block_word in title.lower() for block_word in ['access denied', 'forbidden', 'blocked', 'error', 'unavailable']):
                print(f"❌ Still blocked with title: {title}")
                return None
            
            print(f"✅ Success! Got {len(html_content)} characters")
            return html_content
            
    except Exception as e:
        print(f"❌ Playwright failed: {e}")
        return None
