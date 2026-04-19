"""HTTP сервер для обработки запросов."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import urllib.parse

PACKAGE_DIR = Path(__file__).parent
TEMPLATES_DIR = PACKAGE_DIR / 'templates'


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path.endswith('.html'):
            path = path[:-5]

        if path.startswith('/css/'):
            self.serve_static(path[1:], 'text/css')
            return
        if path.startswith('/js/'):
            self.serve_static(path[1:], 'application/javascript')
            return

        if path == "/" or path == "/index":
            self.serve_template('index.html')
        elif path == "/catalog":
            self.serve_template('catalog.html')
        elif path == "/category":
            self.serve_template('category.html')
        elif path == "/contacts":
            self.serve_template('contacts.html')
        else:
            self.send_404()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        print("\n" + "=" * 50)
        print("ПОЛУЧЕН POST-ЗАПРОС")
        print(f"Путь: {self.path}")
        print(f"Данные: {post_data}")
        print("=" * 50 + "\n")

        self.serve_template('contacts.html')

    def serve_template(self, template_name):
        template_path = TEMPLATES_DIR / template_name
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
        except FileNotFoundError:
            self.send_404()

    def serve_static(self, file_path, content_type):
        full_path = PACKAGE_DIR / 'static' / file_path
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", f"{content_type}; charset=utf-8")
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
        except FileNotFoundError:
            self.send_404()

    def send_404(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("<h1>404 - Страница не найдена</h1>", "utf-8"))


def run_server(host="localhost", port=8080):
    server = HTTPServer((host, port), MyServer)
    print(f"Сервер запущен: http://{host}:{port}")
    print("Нажми Ctrl+C для остановки\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nОстанавливаем сервер...")
    server.server_close()
    print("Сервер остановлен")


if __name__ == "__main__":
    run_server()