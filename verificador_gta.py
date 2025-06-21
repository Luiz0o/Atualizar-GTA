import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time

# Configurações do e-mail
EMAIL_REMETENTE = #Email utilizado para enviar os emails
SENHA_APP = #Senha criada pelo google

# Lista de destinatários
DESTINATARIOS = [
    #Emails que irão receber a atualização
]

# Função para verificar atualizações do usuário específico
def verificar_atualizacao():
    # URL para pegar os posts submetidos pelo usuário PapaXan em formato JSON
    url_posts_recentes = 'https://www.reddit.com/user/PapaXan/submitted.json?limit=10' # Reduzi para 10 para focar mais nos recentes e evitar posts muito antigos
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response_recentes = requests.get(url_posts_recentes, headers=headers)
        response_recentes.raise_for_status() # Lança uma exceção para códigos de status HTTP de erro (4xx ou 5xx)
        
        posts = response_recentes.json()['data']['children']
        for post in posts:
            titulo = post['data']['title'].lower()
            
            # Adicionei 'weekly' aqui, caso o PapaXan use isso com frequência
            if any(palavra in titulo for palavra in ["new", "update", "patch", "dlc", "content", "weekly"]):
                titulo_original = post['data']['title']
                link = "https://www.reddit.com" + post['data']['permalink']
                
                # --- NOVO: Buscar o conteúdo completo da postagem ---
                url_post_completo = link + ".json" # Adiciona .json ao link do post para pegar os detalhes
                
                # É bom adicionar um pequeno atraso entre requisições para não sobrecarregar o Reddit
                time.sleep(1) 
                
                response_completo = requests.get(url_post_completo, headers=headers)
                response_completo.raise_for_status()
                
                post_data_completa = response_completo.json()
                
                # O corpo do texto geralmente está em post_data_completa[0]['data']['children'][0]['data']['selftext']
                # Pode variar se for um cross-post ou outro tipo de conteúdo.
                corpo_post = post_data_completa[0]['data']['children'][0]['data'].get('selftext', 'Conteúdo principal não disponível ou postagem de link/imagem.')
                
                # Se o post tiver conteúdo (não for só um link), adicionamos ao e-mail
                mensagem_corpo = f"📢 Nova postagem sobre atualizações do GTA Online (via PapaXan)!\n\n" \
                                 f"📌 Título: {titulo_original}\n" \
                                 f"🔗 Link: {link}\n\n" \
                                 f"--- Conteúdo da Postagem ---\n{corpo_post}\n" \
                                 f"---------------------------"
                                 
                return mensagem_corpo

    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Erro ao acessar o Reddit: {e}")
    except KeyError as e:
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Erro ao parsear a resposta do Reddit. Formato inesperado ou chave ausente: {e}")
        
    return None

# Função para enviar o e-mail (permanece a mesma)
def enviar_email(destinatarios, assunto, corpo):
    msg = MIMEText(corpo, "plain", "utf-8")
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = ", ".join(destinatarios)
    msg['Subject'] = assunto

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_REMETENTE, SENHA_APP)
            server.sendmail(EMAIL_REMETENTE, destinatarios, msg.as_string())
    except smtplib.SMTPException as e:
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Erro ao enviar o e-mail: {e}")

# Execução principal
print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Verificando atualizações do GTA Online (via PapaXan)...")

atualizacao = verificar_atualizacao()
if atualizacao:
    enviar_email(
        DESTINATARIOS,
        "🚨 Atualização Semanal do GTA Online Detectada (PapaXan)!",
        atualizacao
    )
    print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ✅ E-mail enviado com sucesso!")
else:
    print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ❌ Nenhuma atualização detectada até o momento.")
