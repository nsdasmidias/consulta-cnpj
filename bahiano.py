import requests

# Cores
VERDE = "\033[92m"
BRANCO = "\033[97m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
CINZA = "\033[90m"
RESET = "\033[0m"

def exibir_banner():
    print(r"""
   /\_/\  
  | (o)(o) |
     ^    
    ||||| 
    '|||' 
""")
    print("=======================================================")
    print(f"             {VERDE}CONSULTA DE CNPJ (BAHIANO07z){RESET}")
    print("=======================================================")
    print("  [+] Criador : (BAHIANO07z)")
    print("  [+] Versão  : Multi-Consultas")
    print("=======================================================\n")

# --- FUNÇÃO CNPJ ---
def consultar_cnpj_completo(cnpj_raw):
    cnpj = "".join(filter(str.isdigit, cnpj_raw))
    if len(cnpj) != 14:
        print(f"\n{VERMELHO}[!] CNPJ inválido. Deve conter 14 dígitos.{RESET}")
        input(f"\n{CINZA}Pressione Enter para voltar ao menu...{RESET}")
        return

    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    print(f"\nBusca realizada para o CNPJ: {cnpj}...")

    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            razao = dados.get("razao_social", "N/A")
            estab = dados.get("estabelecimento", {})
            fantasia = estab.get("nome_fantasia", "N/A")
            situacao = estab.get("situacao_cadastral", "N/A")
            data_sit = estab.get("data_situacao_cadastral", "N/A")
            data_abertura = estab.get("data_inicio_atividade", "N/A")
            
            porte_nome = dados.get("porte", {}).get("descricao", "N/A")
            tipo = "MATRIZ" if estab.get("tipo") == "Matriz" else "FILIAL"
            natureza = dados.get("natureza_juridica", {}).get("descricao", "N/A")
            capital = dados.get("capital_social", "N/A")
            email = estab.get("email", "N/A")

            print("=" * 55)
            print("             INFORMAÇÕES DA EMPRESA (CNPJ)")
            print("=" * 55)
            print(f"• Razão Social : {razao}")
            print(f"• Nome Fantasia: {fantasia}")
            print(f"• CNPJ         : {cnpj_raw}")
            print(f"• Situação     : {situacao} (Desde: {data_sit})")
            print(f"• Data Abertura: {data_abertura}")
            print(f"• Tipo / Porte : {tipo} / {porte_nome}")
            print(f"• Natureza     : {natureza}")
            print(f"• Capital Social: R$ {capital}")
            print("\n--- CONTATO ---")
            print(f"• E-mail       : {email}")
            print("=" * 55)
        else:
            print(f"\n{VERMELHO}[!] Erro ao buscar CNPJ (Status: {resposta.status_code}){RESET}")
    except Exception as e:
        print(f"\n{VERMELHO}[!] Falha na conexão: {e}{RESET}")

    input(f"\n{CINZA}Pressione Enter para voltar ao menu...{RESET}")

# --- FUNÇÃO CONSULTAR REGISTRO ---
def consultar_ekyc_completo(dado_input):
    API_KEY = "YIe857PGnVvfbIm6F4tGGKectJIrHfDnZc5rsA1ieEFKvSj9KFuGPYrahInY".strip()
    dado = dado_input.strip().replace(" ", "")

    if not dado.startswith("+"):
        dado = f"+{dado}"

    url = f"https://business.didit.me/api/v1/sessions/{dado}"

    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "service_type": "ws",
        "identifier": dado
    }

    print(f"\nConsultando registro para: {dado}...")

    try:
        resposta = requests.post(url, json=payload, headers=headers, timeout=10)
        dados = resposta.json()

        print("=" * 55)
        print("             RESULTADO CONSULTA DE REGISTRO")
        print("=" * 55)
        print(f"• Telefone / Dado : {dado}")

        if dados.get("success"):
            data_info = dados.get("data", {})
            registrado = data_info.get("registered")

            if registrado is True:
                print(f"• Status WhatsApp : REGISTRADO (Possui WhatsApp)")
            elif registrado is False:
                print(f"• Status WhatsApp : NÃO REGISTRADO (Sem WhatsApp)")
            else:
                print(f"• Status WhatsApp : Desconhecido")
        else:
            print(f"• Erro na Busca   : {dados.get('message', 'Erro desconhecido')}")

        print("=" * 55)

    except Exception as e:
        print(f"\n{VERMELHO}[!] Falha na conexão: {e}{RESET}")

    input(f"\n{CINZA}Pressione Enter para voltar ao menu...{RESET}")


# --- MENU PRINCIPAL ---
if __name__ == "__main__":
    while True:
        exibir_banner()
        print(f"{VERDE}[1]{RESET} {BRANCO}Consultar CNPJ{RESET}")
        print(f"{VERDE}[2]{RESET} {BRANCO}Consultar Registro{RESET}")
        print(f"{VERDE}[0]{RESET} {BRANCO}Sair{RESET}")
        
        opcao = input(f"\n{VERDE}Opção > {RESET}").strip()

        if opcao == "1":
            # chama sua função de CNPJ
            pass 
        elif opcao == "2":
            dado = input("\nDigite o Telefone com DDI e DDD (Ex: 5571999999999): ")
            consultar_ekyc_completo(dado)
        elif opcao == "0":
            print(f"\n{VERDE}Saindo...{RESET}\n")
            break


# --- 3. NOVA FUNÇÃO: CONSULTA CEP (AWESOMEAPI) ---
def consultar_cep(cep):
    API_KEY_AWESOME = "bdf772a3a46869..."  # Cole sua chave completa aqui
    cep = cep.strip().replace("-", "").replace(".", "")
    url = f"https://cep.awesomeapi.com.br/json/{cep}"
    headers = {
        "Authorization": f"Bearer {API_KEY_AWESOME}"
    }

    print(f"\nConsultando CEP: {cep}...")

    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        dados = resposta.json()

        print("=" * 55)
        print("             RESULTADO CONSULTA DE CEP")
        print("=" * 55)

        if resposta.status_code == 200:
            print(f"• Logradouro : {dados.get('address', 'N/A')}")
            print(f"• Bairro     : {dados.get('district', 'N/A')}")
            print(f"• Cidade     : {dados.get('city', 'N/A')}")
            print(f"• Estado     : {dados.get('state', 'N/A')}")
            print(f"• DDD        : {dados.get('ddd', 'N/A')}")
        else:
            print(f"• Erro       : {dados.get('message', 'CEP não encontrado')}")

        print("=" * 55)

    except Exception as e:
        print(f"\n{VERMELHO}[!] Falha na conexão: {e}{RESET}")

    input(f"\n{CINZA}Pressione Enter para voltar ao menu...{RESET}")

    telefone = telefone.strip().replace(" ", "").replace("-", "").replace("+", "")

    # Coloque aqui as SUAS credenciais REAIS do painel da Z-API:
    instance_id = "https://api.z-api.io/instances/{instanceId}/token/{token}/profile-picture"
    token = "https://api.z-api.io/instances/{instanceId}/token/{token}/profile-picture"
    client_token = "SEU_CLIENT_TOKEN_REAL"

    url = f"https://api.z-api.io/instances/{instance_id}/token/{token}/profile-picture?phone={telefone}"

    headers = {
        "client-token": client_token,
        "content-type": "application/json"
    }

    print(f"\nConsultando foto via Z-API para: +{telefone}...")

    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        dados = resposta.json()

        print("=" * 55)
        print("             RESULTADO FOTO PERFIL (Z-API)")
        print("=" * 55)

        if resposta.status_code == 200:
            link_foto = dados.get("link")
            if link_foto:
                print(f"• Telefone   : +{telefone}")
                print(f"• Link da Foto: {link_foto}")
            else:
                print(f"• Telefone   : +{telefone}")
                print(f"• Status     : Não possui foto visível")
        else:
            print(f"• Erro       : {dados.get('message', 'Erro na requisição')}")

        print("=" * 55)

    except Exception as e:
        print(f"\n[!] Falha na conexão: {e}")

    input("\nPressione Enter para voltar ao menu...")

def consultar_didit_ekyc(dado):
    api_key = "PEMEhOgPZiwYRKcpM1pSCh7_k6ELQ1Ht9HgFgTfuYAM"
    url = f"https://business.didit.me/api/v1/verify/{dado}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    print(f"\n{VERDE}Consultando via Didit API...{RESET}")
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            dados = res.json()
            print("=" * 45)
            print(f" Resultado: {dados}")
            print("=" * 45)
        else:
            print(f"\n{VERMELHO}Erro na consulta Didit. Status: {res.status_code}{RESET}")
    except Exception as e:
        print(f"\n{VERMELHO}Erro de conexão: {e}{RESET}")
    input(f"\n{CINZA}Pressione Enter para voltar ao menu...{RESET}")

def consultar_ip(ip):
    url = f"http://ip-api.com/json/{ip}?lang=pt-BR"
    print(f"\n{VERDE}Consultando IP via ip-api...{RESET}")
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            dados = res.json()
            if dados.get("status") == "success":
                print("=" * 45)
                print(f" IP         : {dados.get('query')}")
                print(f" País       : {dados.get('country')}")
                print(f" Estado     : {dados.get('regionName')}")
                print(f" Cidade     : {dados.get('city')}")
                print(f" Provedor   : {dados.get('isp')}")
                print(f" Org        : {dados.get('org')}")
                print("=" * 45)
            else:
                print(f"\n{VERMELHO}IP inválido ou não encontrado.{RESET}")
        else:
            print(f"\n{VERMELHO}Erro na consulta. Status: {res.status_code}{RESET}")
    except Exception as e:
        print(f"\n{VERMELHO}Erro de conexão: {e}{RESET}")
    input(f"\n{CINZA}Pressione Enter para voltar ao menu...{RESET}")

        else:
            print(f"\n{VERMELHO}Erro na consulta. St>")
    except Exception as e:
        print(f"\n{VERMELHO}Erro de conexão: {e}{RES>")
    input(f"\n{CINZA}Pressione Enter para voltar ao >")



# --- MENU PRINCIPAL ---
if __name__ == "__main__":
    while True:
        exibir_banner()
        print(f"{VERDE}[1]{RESET} {BRANCO}Consultar CNPJ{RESET}")
        print(f"{VERDE}[2]{RESET} {BRANCO}Consultar Registro{RESET}")
        print(f"{VERDE}[3]{RESET} {BRANCO}Consultar CEP{RESET}")
        print(f"{VERDE}[4]{RESET} {BRANCO}Consultar IP{RESET}")
        print(f"{VERDE}[0]{RESET} {BRANCO}Sair{RESET}")
        opcao = input(f"\n{VERDE}Opção > {RESET}").strip()

        if opcao == "1":
            cnpj = input("\nDigite o CNPJ: ")
            # Se a sua função de CNPJ tiver outro nome, chame ela aqui:
            consultar_cnpj(cnpj) 
        elif opcao == "2":
            dado = input("\nDigite o Telefone com DDI e DDD (Ex: 5571999999999): ")
            consultar_ekyc_completo(dado)
        elif opcao == "3":
            cep = input("\nDigite o CEP (Apenas números): ")
            consultar_cep(cep)
        elif opcao == "4":
            ip = input("\nDigite o IP ou Domínio: ")
            consultar_ip(ip)
        elif opcao == "5":
            cpf = input("\nDigite o CPF (apenas números): ")
            data_nasc = input("Digite a Data de Nascimento (AAAA-MM-DD): ")
            consultar_cpf_io(cpf, data_nasc)
        elif opcao == "0":
            print(f"\n{VERDE}Saindo...{RESET}\n")
            break


