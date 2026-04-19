import telnetlib
import asyncio

class TelnetClient:
    def __init__(self, host: str, port: int, password: str, timeout=5):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout

    def _send_blocking(self, command: str) -> str:
        tn = telnetlib.Telnet(self.host, self.port, self.timeout)

        tn.read_until(b"password: ")
        tn.write(self.password.encode() + b"\n")

        tn.write(command.encode() + b"\n")
        tn.write(b"\n")

        output = tn.read_very_eager().decode("utf-8", errors="ignore")
        tn.close()
        return output

    async def send(self, command: str) -> str:
        return await asyncio.to_thread(self._send_blocking, command)
