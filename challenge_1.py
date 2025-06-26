# Entrada do usuário
email = input("Digite seu e-mail: ").strip()

# Regras
caractere = "@"
dominios_validos = ["gmail.com", "outlook.com"]

# Validações
if (
    caractere in email
    and email.count(caractere) == 1
    and not email.startswith(caractere)
    and not email.endswith(caractere)
    and " " not in email
):

    nome_usuario, dominio = email.split(caractere)
    print(nome_usuario)
    print(dominio)

    if dominio in dominios_validos:
        print("E-mail válido")
    else:
        print("E-mail inválido: domínio não permitido")
else:
    print("E-mail inválido: formato incorreto")