from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import os
hostName = "localhost"
serverPort = os.environ['PORT']
chrome_options = Options()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(executable_path=os.environ.get(
    "CHROMEDRIVER_PATH"), chrome_options=chrome_options)


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            delay = 3  # seconds
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in query.split("&"))
            searchQuery = query_components["query"]
            browser.get("https://open.spotify.com/search/" + searchQuery)
            myElem = WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'onVWL7MW4PW9FyVajBAc')))
            self.wfile.write(bytes(browser.page_source, "utf-8"))
        except TimeoutException:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            print("Loading took too much time!")
            self.wfile.write(bytes("Failed", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
