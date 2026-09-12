import json
import urllib.parse
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

class TikTokAPIHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # URL পার্স করা
        parsed_url = urllib.parse.urlparse(self.path)
        
        # শুধুমাত্র /get_user রাউট এলাউ করা
        if parsed_url.path == '/get_user':
            query_params = urllib.parse.parse_qs(parsed_url.query)
            username = query_params.get('username', [None])[0]
            
            # username না থাকলে Error JSON
            if not username:
                self.send_json_response({
                    "status": "error",
                    "message": "Username parameter is required. Example: /get_user?username=xrror4044",
                    "API_OWNER": "DIPTO",
                    "CHANNEL": "https://t.me/Xrror_404"
                }, status_code=400)
                return
            
            # Cloudflare Worker API-তে রিকোয়েস্ট পাঠানো
            target_url = f"https://tiktokinfov10.itfreeforever.workers.dev/?username={urllib.parse.quote(username)}"
            
            headers = {
                "Host": "tiktokinfov10.itfreeforever.workers.dev",
                "sec-ch-ua-platform": '"Android"',
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 SCRGlitx/1.0",
                "Accept": "*/*",
                "sec-ch-ua": '"Not=A?Brand";v="99", "Android WebView";v="151", "Chromium";v="151"',
                "sec-ch-ua-mobile": "?1",
                "Origin": "https://fintok.neocities.org",
                "X-Requested-With": "com.aistudio.scrglitx.vkmzp",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://fintok.neocities.org/",
                "Accept-Language": "en-US,en;q=0.9",
                "Priority": "u=1, i"
            }
            
            req = urllib.request.Request(target_url, headers=headers, method='GET')
            
            try:
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_body = response.read().decode('utf-8')
                    status_code = response.getcode()
                    self.process_and_send(res_body, status_code)
                        
            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8')
                self.process_and_send(error_body, e.code)
            except Exception as e:
                self.send_json_response({
                    "status": "error", 
                    "message": str(e),
                    "API_OWNER": "DIPTO",
                    "CHANNEL": "https://t.me/Xrror_404"
                }, status_code=500)
        else:
            self.send_json_response({
                "status": "error", 
                "message": "Not Found. Use /get_user?username=your_name",
                "API_OWNER": "DIPTO",
                "CHANNEL": "https://t.me/Xrror_404"
            }, status_code=404)

    def process_and_send(self, res_body, status_code):
        """JSON ডেটা মডিফাই করে কাস্টম ক্রেডিট যুক্ত করার ফাংশন"""
        try:
            json_data = json.loads(res_body)
            
            if isinstance(json_data, dict):
                # পুরাতন dev ক্রেডিট রিমুভ করা
                json_data.pop("dev", None)
                
                # আপনার নিজস্ব কাস্টম ক্রেডিট যোগ করা
                json_data["API_OWNER"] = "DIPTO"
                json_data["CHANNEL"] = "https://t.me/Xrror_404"
                
            self.send_json_response(json_data, status_code=status_code)
        except Exception:
            # যদি রেসপন্স JSON না হয়
            self.send_json_response({
                "status": "raw_response", 
                "data": res_body,
                "API_OWNER": "DIPTO",
                "CHANNEL": "https://t.me/Xrror_404"
            }, status_code=status_code)

    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=4, ensure_ascii=False).encode('utf-8'))

# সার্ভার চালনা
def run_server():
    server_address = ('0.0.0.0', 5000)
    httpd = HTTPServer(server_address, TikTokAPIHandler)
    print("\n==================================================")
    print(" Server Running Successfully!")
    print(" Open Link: http://127.0.0.1:5000/get_user?username=xrror4044")
    print("==================================================\n")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()