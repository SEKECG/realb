import uvicorn
from threading import Thread
from IPython.display import display, IFrame
import socket

PORT_RANGE = (8000, 9000)

def load_ipython_extension(ipython):
    ipython.register_magic_function(fh, 'line')

def find_available_port(host):
    for port in range(PORT_RANGE[0], PORT_RANGE[1]):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((host, port)) != 0:
                return port
    raise RuntimeError("No available ports found")

class JupyterReloader:
    def __init__(self):
        self.server = None

    def load(self, app, page='/', width='100%', height='600px', port=None, host='127.0.0.1'):
        if port is None:
            port = find_available_port(host)
        self.server = Server(uvicorn.Config(app, host=host, port=port))
        self.server.run_in_thread()
        display(IFrame(src=f"http://{host}:{port}{page}", width=width, height=height))
        return self.server

class Server:
    def __init__(self, config):
        self.config = config
        self.should_exit = False
        self.thread = None

    def run(self):
        uvicorn.Server(self.config).run()

    def run_in_thread(self):
        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()
        self._wait_for_startup()

    def _wait_for_startup(self):
        timeout = 5
        while timeout > 0:
            if self.config.is_ready:
                return
            timeout -= 1
            time.sleep(1)
        raise RuntimeError("Server failed to start within timeout period")

    def close(self):
        self.should_exit = True
        if self.thread:
            self.thread.join(timeout=5)

    def install_signal_handlers(self):
        pass

class TupleNoPrint(tuple):
    def __repr__(self):
        return ""

    def __str__(self):
        return ""

def fh(line):
    args = line.split()
    app = args[0]
    page = args[1] if len(args) > 1 else '/'
    width = args[2] if len(args) > 2 else '100%'
    height = args[3] if len(args) > 3 else '600px'
    port = int(args[4]) if len(args) > 4 else None
    host = args[5] if len(args) > 5 else '127.0.0.1'
    reloader = JupyterReloader()
    reloader.load(app, page, width, height, port, host)