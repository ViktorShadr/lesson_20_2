from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def _get_index(self):
        return """
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Blog</title>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="container mt-4">
          <h1>Lorem Blog</h1>
          <ul class="list-group">
            <a href="/?page=news1" class="list-group-item list-group-item-action">New one</a>
            <a href="/?page=news2" class="list-group-item list-group-item-action">New two</a>
            <a href="/?page=news3" class="list-group-item list-group-item-action">New three</a>
          </ul>
        </body>
        </html>
        """

    def _get_article_content(self, page_address):
        articles = {
            'news1': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque...',
            'news2': 'Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit...',
            'news3': 'Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore...'
        }
        return articles.get(page_address, 'Article not found!')

    def _get_blog_article(self, page_address):
        return f"""
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Blog</title>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="container mt-4">
          <div class="card">
            <div class="card-header">
              <a class="btn btn-primary" href="/">Back</a>
            </div>
            <div class="card-body">
              <p>{self._get_article_content(page_address)}</p>
            </div>
          </div>
        </body>
        </html>
        """

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        page = query.get('page', [None])[0]
        html = self._get_blog_article(page) if page else self._get_index()

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started: http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
