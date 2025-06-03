import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Configurações do e-mail
EMAIL_REMETENTE = #Email utilizado para enviar os emails
SENHA_APP = #Senha criada pelo google

# Lista de destinatários
DESTINATARIOS = [
    #Emails que irão receber a atualização
]

# Função para verificar atualizações no subreddit do GTA Online
def verificar_atualizacao():
    url = 'https://www.reddit.com/r/gtaonline/new.json?limit=5'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        posts = response.json()['data']['children']
        for post in posts:
            titulo = post['data']['title'].lower()
            if 'weekly update' in titulo:
                link = "https://www.reddit.com" + post['data']['permalink']
                return f"📰 Nova atualização semanal do GTA Online!\n\n{post['data']['title']}\n\n🔗 {link}"
    return None

# Função para enviar o e-mail
def enviar_email(destinatarios, assunto, corpo):
    msg = MIMEText(corpo, "plain", "utf-8")
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = ", ".join(destinatarios)
    msg['Subject'] = assunto

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_APP)
        server.sendmail(EMAIL_REMETENTE, destinatarios, msg.as_string())

# Execução principal
print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Verificando atualizações do GTA Online...")

atualizacao = verificar_atualizacao()
if atualizacao:
    enviar_email(
        DESTINATARIOS,
        "🚨 Atualização Semanal do GTA Online Detectada!",
        atualizacao
    )
    print("✅ E-mail enviado com sucesso!")
else:
    print("❌ Nenhuma atualização detectada até o momento.")
