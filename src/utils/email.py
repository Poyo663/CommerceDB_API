
import os

from dotenv import load_dotenv

load_dotenv()


def enviar_email_exclusao(destinatario: str, token: str) -> None:

    modo = os.getenv("EMAIL_MODE")

    if modo != "development":
        raise RuntimeError(
            "Serviço de envio de e-mail não configurado."
        )

    print("\n" + "=" * 60)
    print("SIMULAÇÃO DE ENVIO DE E-MAIL")
    print("=" * 60)

    print(f"Destinatário: {destinatario}")
    print("Assunto: Confirmação de exclusão de comércio")

    print(f"""
Olá!

Recebemos uma solicitação de exclusão do seu comércio
na plataforma CommerceDB API.

Seu token de confirmação é:

{token}

O token possui validade de 30 minutos.

Caso você não tenha solicitado a exclusão,
ignore esta mensagem.

Atenciosamente,
Equipe CommerceDB API
    """)

    print("=" * 60)
