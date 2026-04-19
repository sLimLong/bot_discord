import telnetlib
import asyncio

class TelnetClient:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

    def _send_blocking(self, command: str):
        tn = telnetlib.Telnet(self.host, self.port, timeout=5)
        tn.read_until(b"password: ")
        tn.write(self.password.encode("utf-8") + b"\n")
        tn.read_until(b"> ")
        tn.write(command.encode("utf-8") + b"\n")
        output = tn.read_until(b"> ", timeout=5).decode("utf-8")
        tn.close()
        return output

    async def send(self, command: str):
        return await asyncio.to_thread(self._send_blocking, command)
