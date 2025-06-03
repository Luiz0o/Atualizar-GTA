import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import socket

# Configurações do e-mail
EMAIL_REMETENTE = #Email utilizado para enviar os emails
SENHA_APP = #Senha criada pelo google

# Lista de destinatários
DESTINATARIOS = [
    #Emails que irão receber a atualização
]

# Corpo da mensagem de teste
atualizacao = """🧪 Este é um **teste** do sistema automático de notificações do GTA Online.

Se você recebeu este e-mail, está tudo funcionando corretamente!

Em breve você será notificado sempre que o GTA Online tiver uma nova atualização semanal. 😉
"""

# Função para enviar o e-mail
def enviar_email(destinatarios, assunto, corpo):
    msg = MIMEText(corpo, "plain", "utf-8")
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = ", ".join(destinatarios)
    msg['Subject'] = assunto

    # Força IPv4 (resolve smtp.gmail.com para endereço IPv4)
    smtp_host = socket.gethostbyname('smtp.gmail.com')

    with smtplib.SMTP(smtp_host, 587) as server:
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_APP)
        server.sendmail(EMAIL_REMETENTE, destinatarios, msg.as_string())

# Execução principal
print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Enviando e-mail de teste...")
enviar_email(
    DESTINATARIOS,
    "🧪 Teste do sistema de alertas do GTA Online",
    atualizacao
)
print("✅ E-mail de teste enviado com sucesso!")
