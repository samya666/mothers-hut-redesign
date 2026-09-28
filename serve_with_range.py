import os
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler

class RangeRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def send_head(self):
        if 'Range' not in self.headers:
            return super().send_head()

        path = self.translate_path(self.path)
        if not os.path.exists(path) or os.path.isdir(path):
            return super().send_head()

        file_size = os.path.getsize(path)
        range_header = self.headers['Range']
        match = re.match(r'bytes=(\d+)-(\d*)', range_header)
        if not match:
            return super().send_head()

        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else file_size - 1
        end = min(end, file_size - 1)

        if start >= file_size:
            self.send_error(416, "Requested Range Not Satisfiable")
            return None

        self.send_response(206)
        self.send_header('Content-type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.end_headers()

        f = open(path, 'rb')
        f.seek(start)
        return f

    def copyfile(self, source, outputfile):
        if 'Range' in self.headers and hasattr(source, 'seek'):
            range_header = self.headers['Range']
            match = re.match(r'bytes=(\d+)-(\d*)', range_header)
            if match:
                path = self.translate_path(self.path)
                file_size = os.path.getsize(path)
                start = int(match.group(1))
                end = int(match.group(2)) if match.group(2) else file_size - 1
                end = min(end, file_size - 1)
                length = end - start + 1
                
                buffer_size = 64 * 1024
                while length > 0:
                    chunk = source.read(min(length, buffer_size))
                    if not chunk:
                        break
                    outputfile.write(chunk)
                    length -= len(chunk)
                source.close()
                return

        super().copyfile(source, outputfile)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(('0.0.0.0', 8080), RangeRequestHandler)
    print("Serving HTTP with Range Request support on port 8080...")
    server.serve_forever()
