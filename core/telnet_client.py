import telnetlib
import time

class TelnetClient:
    def __init__(self, host: str, port: int, password: str, timeout=5):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout

    def send(self, command: str) -> str:
        tn = telnetlib.Telnet(self.host, self.port, self.timeout)
        tn.read_until(b"password: ")
        tn.write(self.password.encode() + b"\n")
        time.sleep(0.2)

        tn.write(command.encode() + b"\n")
        time.sleep(0.3)

        output = tn.read_very_eager().decode("utf-8", errors="ignore")
        tn.close()
        return output
