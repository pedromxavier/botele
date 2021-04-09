from botele import Botele
from botele.filter import UnknownCommand

from cstream import stderr
from minerva_ufrj import Minerva
import lorem


class pedromxavierbot(Botele):
    @Botele.command("lorem", "Lorem Ipsum")
    def lorem(self, info: dict):
        info["bot"].send_message(chat_id=info["chat_id"], text=lorem.paragraph())

    @Botele.command("minerva", "Renova os livros da biblioteca")
    def minerva(self, info: dict):
        params = {
            "chat_id": info["chat_id"],
            "message_id": info["message_id"],
        }
        info["bot"].delete_message(**params)

        text: str
        if len(info["args"]) != 2:
            text = "Este comando precisa de usuário e senha."
        else:
            user, pswd = info["args"]
            m = Minerva(user, pswd)
            if m.renew():
                text = f"[{user}] renovado com sucesso."
            else:
                text = f"[{user}] falha ao renovar."

        params = {"chat_id": info["chat_id"], "text": text}
        info["bot"].send_message(**params)

    @Botele.message(UnknownCommand(None))
    def unknown(self, info: dict):
        cmd = info["text"]
        info["bot"].send_message(
            chat_id=info["chat_id"],
            text=f"Comando desconhecido: `{cmd}`",
            parse_mode=self.MARKDOWN,
        )

    @Botele.error
    def error(self, info: dict):
        stderr[0] << info["error"]
