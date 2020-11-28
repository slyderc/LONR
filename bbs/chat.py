import asyncio

from blessed import Terminal


class Chat:
    def __init__(self):
        self._users = {}
        self.term = Terminal()

    def names(self):
        return list(username for username in self._users.keys())

    async def send(self, message):
        for recipient, client in self._users.items():
            await client.recv(message)

    async def connect(self, user, reader, writer):
        if not user.can_chat and not user.is_admin:
            return 'You are banned from chat.'
        await self.system_message(f"{user.username} has joined chat")
        self._users[user.username] = client = ChatClient(self, user, reader, writer, self.term)
        await client.chat()
        self._users.pop(user.username)
        await self.system_message(f"{user.username} has left the room")
        return "Leaving chat."

    async def system_message(self, message):
        await self.send(f"{self.term.bright_yellow}*** {message}{self.term.normal}")


class ChatClient:
    def __init__(self, server, user, reader, writer, term):
        self.server = server
        self.user = user
        self.reader = reader
        self.writer = writer
        self.term = term

    async def chat(self):
        prompt = 'chat> '
        self.writer.write(prompt)
        while True:
            line = await self.reader.readline()
            if line is self.reader.BREAK:
                break
            line = line.rstrip()
            if line.startswith('/exit'):
                self.writer.write('\r\n')
                break
            elif line.startswith('/me '):
                _, _, remainder = line.partition(' ')
                line = f"{self.term.bright_green}* {self.user.username} {remainder}{self.term.normal}"
            elif line.startswith('/admin '):
                if self.user.is_admin:
                    _, _, remainder = line.partition(' ')
                    await self.server.system_message(remainder)
                else:
                    await self.print_error("You do not have permission for that command")
                line = ''
            elif line.startswith('/who'):
                names = self.server.names()
                await self.print_info("Users currently in chat:")
                for name in names:
                    await self.print_info(f"  {name}")
                line = ''
            elif line.strip():
                line = f"<{self.user.username}> {line}"
            if line.strip():
                await self.send(line)
            self.writer.write('\r\x1b[2K' + prompt)

    async def print_error(self, message):
        await self.print(f"{self.term.bright_red}!!! {message}{self.term.normal}")

    async def print_info(self, message):
        await self.print(f"{self.term.bright_blue}** {message}{self.term.normal}")

    async def send(self, message):
        await self.server.send(message)

    async def print(self, message):
        self.writer.write(f'\x1b7\n\x1b[1A\x1b[1L{message}\x1b8')

    async def recv(self, message):
        await self.print(message)


_chat = Chat()


def get_chat():
    return _chat
