from datetime import datetime

ano_nascimento = int(input("Informe seu ano de nascimento"))
ano_atual = datetime.now().year

print(f"\nAniversários de {ano_nascimento} até {ano_atual}:\n")

for ano in range(ano_nascimento + 1, ano_atual + 1):
    idade = ano - ano_nascimento
    print(f"ano {ano} - {idade} anos")
    
    if idade == 18:
        print("--> Você atingiu a maioridade!")
 