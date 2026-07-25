import requests
import re

def consultar_cnpj_completo(cnpj_raw):
    # Limpa caracteres especiais do CNPJ
    cnpj = re.sub(r'\D', '', cnpj_raw)
    
    if len(cnpj) != 14:
        print("\n[!] Erro: O CNPJ deve ter exatamente 14 dígitos.\n")
        return

    url = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
    headers = {"Accept": "application/json"}

    print(f"\nBusca realizada para o CNPJ: {cnpj}...\n")

    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        
        if resposta.status_code == 429:
            print("[!] Limite do plano gratuito atingido (máx. 3 consultas/minuto).")
            return

        if resposta.status_code == 200:
            dados = resposta.json()
            
            if dados.get("status") == "ERROR":
                print(f"[!] Erro: {dados.get('message', 'CNPJ não encontrado.')}\n")
                return

            # --- EXIBIÇÃO COMPLETA DOS DADOS PÚBLICOS ---
            print("=" * 55)
            print("             INFORMAÇÕES DA EMPRESA (CNPJ)             ")
            print("=" * 55)
            
            # Dados Principais
            print(f"• Razão Social    : {dados.get('nome', 'N/A')}")
            print(f"• Nome Fantasia   : {dados.get('fantasia', 'N/A')}")
            print(f"• CNPJ            : {dados.get('cnpj', 'N/A')}")
            print(f"• Situação        : {dados.get('situacao', 'N/A')} (Desde: {dados.get('data_situacao', 'N/A')})")
            print(f"• Data de Abertura: {dados.get('abertura', 'N/A')}")
            print(f"• Tipo / Porte    : {dados.get('tipo', 'N/A')} / {dados.get('porte', 'N/A')}")
            print(f"• Natureza Juríd. : {dados.get('natureza_juridica', 'N/A')}")
            print(f"• Capital Social  : R$ {dados.get('capital_social', '0,00')}")
            
            # Contato
            print("\n--- CONTATO ---")
            print(f"• E-mail          : {dados.get('email', 'N/A')}")
            print(f"• Telefone        : {dados.get('telefone', 'N/A')}")

            # Endereço
            print("\n--- ENDEREÇO ---")
            print(f"• CEP             : {dados.get('cep', 'N/A')}")
            print(f"• Logradouro      : {dados.get('logradouro', 'N/A')}, Nº {dados.get('numero', 'N/A')}")
            print(f"• Complemento     : {dados.get('complemento', 'N/A')}")
            print(f"• Bairro          : {dados.get('bairro', 'N/A')}")
            print(f"• Município / UF  : {dados.get('municipio', 'N/A')} - {dados.get('uf', 'N/A')}")

            # Atividade Principal
            print("\n--- ATIVIDADE PRINCIPAL ---")
            for ativ in dados.get('atividade_principal', []):
                print(f"• [{ativ.get('code')}] {ativ.get('text')}")

            # Atividades Secundárias
            secundarias = dados.get('atividades_secundarias', [])
            if secundarias:
                print("\n--- ATIVIDADES SECUNDÁRIAS ---")
                for ativ in secundarias[:3]: # Exibe as 3 primeiras
                    print(f"• [{ativ.get('code')}] {ativ.get('text')}")

            # Quadro de Sócios e Administradores (QSA)
            socios = dados.get('qsa', [])
            if socios:
                print("\n--- QUADRO DE SÓCIOS (QSA) ---")
                for soc in socios:
                    print(f"• Nome: {soc.get('nome')} | Qualificação: {soc.get('qual')}")

            print("=" * 55 + "\n")

        else:
            print(f"[!] Erro no servidor: Código {resposta.status_code}\n")

    except Exception as e:
        print(f"[!] Falha na conexão: {e}\n")

if __name__ == "__main__":
    entrada = input("Digite o CNPJ que deseja consultar: ").strip()
    if entrada:
        consultar_cnpj_completo(entrada)

import os
import re
import requests

# 1. Definição de Cores ANSI
VERDE = "\033[92m"
BRANCO = "\033[1;37m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
CINZA = "\033[90m"
RESET = "\033[0m"

def limpar_tela():
    # Limpa o terminal no Linux/Termux/Windows
    os.system("cls" if os.name == "nt" else "clear")

def exibir_banner():
    limpar_tela()
    
    # Arte ASCII em Verde
    banner = f"""{VERDE}
      .---.
     /     \\
    | () () |
     \\  ^  /
      |||||
      '|||'
    {RESET}"""
    
    print(banner)
    print(f"{BRANCO}==============================================")
    print(f"{VERDE}            CONSULTA DE CNPJ (BAHIANO77z)      ")
    print(f"{BRANCO}==============================================")
    print(f"{CINZA}  [+] Criador : {BRANCO} (BAHIANO77z)")
    print(f"{CINZA}  [+] Versão  : {BRANCO}Em breve Outros tipos de consultas")
    print(f"{BRANCO}=============================================={RESET}\n")

def consultar_cnpj():
    exibir_banner()
    entrada = input(f"{BRANCO}Digite o CNPJ para consultar: {RESET}").strip()
    
    # Limpa pontuações do CNPJ
    cnpj = re.sub(r'\D', '', entrada)
    
    if len(cnpj) != 14:
        print(f"\n{VERMELHO}[!] Erro: O CNPJ deve conter 14 dígitos.{RESET}\n")
        input(f"{CINZA}Pressione Enter para voltar...{RESET}")
        return

    url = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
    headers = {"Accept": "application/json"}

    print(f"\n{AMARELO}[*] Consulta feita com Sucesso.{RESET}\n")

    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        
        if resposta.status_code == 429:
            print(f"{AMARELO}[!] Limite atingido (máx. 3 consultas/min no plano grátis).{RESET}\n")
            input(f"{CINZA}Pressione Enter para voltar...{RESET}")
            return

        if resposta.status_code == 200:
            dados = resposta.json()
            
            if dados.get("status") == "ERROR":
                print(f"{VERMELHO}[!] Erro: {dados.get('message', 'CNPJ não encontrado.')}{RESET}\n")
                input(f"{CINZA}Pressione Enter para voltar...{RESET}")
                return

            # Exibição dos Dados Formatados
            print(f"{BRANCO}==============================================")
            print(f"{VERDE}             DADOS DA EMPRESA                 ")
            print(f"{BRANCO}==============================================")
            print(f"{VERDE}• Razão Social  :{RESET} {dados.get('nome', 'N/A')}")
            print(f"{VERDE}• Nome Fantasia :{RESET} {dados.get('fantasia', 'N/A')}")
            print(f"{VERDE}• CNPJ          :{RESET} {dados.get('cnpj', 'N/A')}")
            print(f"{VERDE}• Situação      :{RESET} {dados.get('situacao', 'N/A')}")
            print(f"{VERDE}• Abertura      :{RESET} {dados.get('abertura', 'N/A')}")
            print(f"{VERDE}• Porte         :{RESET} {dados.get('porte', 'N/A')}")
            print(f"{VERDE}• Capital Social:{RESET} R$ {dados.get('capital_social', '0,00')}")
            
            print(f"\n{VERDE}--- CONTATO & ENDEREÇO ---{RESET}")
            print(f"{VERDE}• E-mail        :{RESET} {dados.get('email', 'N/A')}")
            print(f"{VERDE}• Telefone      :{RESET} {dados.get('telefone', 'N/A')}")
            print(f"{VERDE}• CEP           :{RESET} {dados.get('cep', 'N/A')}")
            print(f"{VERDE}• Endereço     :{RESET} {dados.get('logradouro', 'N/A')}, Nº {dados.get('numero', 'N/A')}")
            print(f"{VERDE}• Cidade/UF     :{RESET} {dados.get('municipio', 'N/A')} - {dados.get('uf', 'N/A')}")
            print(f"{BRANCO}=============================================={RESET}\n")

        else:
            print(f"{VERMELHO}[!] Erro no servidor: Código {resposta.status_code}{RESET}\n")

    except Exception as e:
        print(f"{VERMELHO}[!] Falha na conexão: {e}{RESET}\n")

    input(f"{CINZA}Pressione Enter para voltar ao menu...{RESET}")

# Loop Principal do Menu
if __name__ == "__main__":
    while True:
        exibir_banner()
        print(f"{VERDE}[1]{RESET} {BRANCO}Consultar CNPJ{RESET}")
        print(f"{VERDE}[0]{RESET} {BRANCO}Sair{RESET}\n")
        
        opcao = input(f"{VERDE}Opção > {RESET}").strip()
        
        if opcao == "1":
            consultar_cnpj()
        elif opcao == "0":
            print(f"\n{AMARELO}Saindo...{RESET}\n")
            break
        else:
            print(f"\n{VERMELHO}Opção inválida!{RESET}")
            input(f"{CINZA}Pressione Enter para tentar novamente...{RESET}")

