from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
from env import StartupEnv
from metrics import calculate_metrics
from agent import choose_action

env = StartupEnv()

class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/start':
            state = env.reset()
            money, product, team = state
            health, status = calculate_metrics(money, product, team)

            data = {
                "money": money,
                "product": product,
                "team": team,
                "health": health,
                "status": status
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        elif self.path.startswith('/action/'):
            action = self.path.split('/')[-1]
            state, reward, done = env.step(action)
            money, product, team = state
            health, status = calculate_metrics(money, product, team)

            data = {
                "money": money,
                "product": product,
                "team": team,
                "reward": reward,
                "health": health,
                "status": status,
                "done": done
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        elif self.path == '/ai':
            action = choose_action()
            state, reward, done = env.step(action)
            money, product, team = state
            health, status = calculate_metrics(money, product, team)

            data = {
                "ai_action": action,
                "money": money,
                "product": product,
                "team": team,
                "reward": reward,
                "health": health,
                "status": status,
                "done": done
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <h1>AI Startup Simulator</h1>
            <p>Open these links:</p>
            <ul>
            <li>/start</li>
            <li>/action/hire</li>
            <li>/action/develop</li>
            <li>/action/marketing</li>
            <li>/action/save</li>
            <li>/action/loan</li>
            <li>/ai</li>
            </ul>
            </html>
            """)

server = HTTPServer(('0.0.0.0', 8000), MyServer)
print("Server running at http://127.0.0.1:8000")
server.serve_forever()

