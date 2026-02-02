import click
import csv
import os
from rich.console import Console
from datetime import datetime
from rich.table import Table 

@click.group()
def main():
    pass

@main.command('add', help="Adicionar uma nova despesa.")
@click.option('--data', prompt="Digite a data (DD/MM/YYYY)", type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--descricao', prompt="Digite a descrição")
@click.option('--valor', prompt="Digite o valor", type=click.FloatRange(min=0))
def add(data, descricao, valor):
    data = data.strftime("%d/%m/%Y")

    click.echo("Escolha a categoria")
    click.echo("1. Alimentação")
    click.echo("2. Transporte")
    click.echo("3. Moradia")
    click.echo("4. Saúde")
    click.echo("5. Outros")

    escolha_da_categoria = click.prompt("Digite o número correspondente", type=click.IntRange(1, 5))

    if escolha_da_categoria == 1:
        categoria = "Alimentação"
    elif escolha_da_categoria == 2:
        categoria = "Transporte"
    elif escolha_da_categoria == 3:
        categoria = "Moradia"
    elif escolha_da_categoria == 4:
        categoria = "Saúde"
    else:
        categoria = "Outros"

    if os.path.exists("despesas.csv"):
        with open("despesas.csv", "r", newline="") as arquivo:
            dados = csv.reader(arquivo) 
            next (dados, None)

            id = 1

            for linha in dados:
                if linha:
                    id = int(linha[0])

            id += 1
    else:
        id = 1

    if os.path.exists("despesas.csv"):
        with open("despesas.csv", "a", newline="") as arquivo:
            dados = csv.writer(arquivo, lineterminator="\n")

            dados.writerow([f"{id}", f"{data}",f"{descricao}", f"{valor:.2f}", f"{categoria}"])
            
            click.echo(f"Despesa com ID {id} adicionada com sucesso!")
    else:
        with open("despesas.csv", "w", newline="") as arquivo:
            dados = csv.writer(arquivo, lineterminator="\n")

            dados.writerow(["ID", "Data", "Descrição", "Valor", "Categoria"])
            dados.writerow([f"{id}", f"{data}",f"{descricao}", f"{valor:.2f}", f"{categoria}"])
            
            click.echo(f"Despesa com ID {id} adicionada com sucesso!")

@main.command('edit', help='Editar uma despesa existente.')
@click.argument('id', type=click.IntRange(min=0))
def edit(id):
    if not os.path.exists("despesas.csv"):
        click.echo("Nenhuma despesa encontrada com o ID fornecido.")
        return

    with open("despesas.csv", "r") as arquivo:
        id_encontrado = False

        dados = csv.reader(arquivo)

        next(dados, None)

        for linha in dados:
            if int(linha[0]) == id:
                id_encontrado = True
                data_atual = linha[1]
                descricao_atual = linha[2]
                valor_atual = linha[3]
                categoria_atual = linha[4]
                break

        if not id_encontrado:
            click.echo("Nenhuma despesa encontrada com o ID fornecido.")
            return
        
    click.echo(f"Editando despesa com ID: {id}")

    data_editada = click.prompt(f"Data atual: {data_atual}. Digite a nova data (DD/MM/YYYY) ou pressione Enter para manter:", type=click.DateTime(formats=["%d/%m/%Y"]), default=None, show_default=False)
    descricao_editada = click.prompt(f"Descrição atual: {descricao_atual}. Digite a nova descrição ou pressione Enter para manter:", default="")
    valor_editado = click.prompt(f"Valor atual: {valor_atual}. Digite o novo valor ou pressione Enter para manter:", type=click.FloatRange(min=0), default=None, show_default=False)
    click.echo(f"Categoria atual: {categoria_atual}. Escolha uma nova categoria ou pressione Enter para manter:")

    if data_editada is not None:
        data_editada = data_editada.strftime("%d/%m/%Y")

    click.echo("Escolha a categoria")
    click.echo("1. Alimentação")
    click.echo("2. Transporte")
    click.echo("3. Moradia")
    click.echo("4. Saúde")
    click.echo("5. Outros")

    escolha_da_categoria_editada = click.prompt(f"Digite o número correspondente:", type=click.IntRange(1, 5), default=None, show_default=False)

    if escolha_da_categoria_editada == 1:
        categoria_editada = "Alimentação"
    elif escolha_da_categoria_editada == 2:
        categoria_editada = "Transporte"
    elif escolha_da_categoria_editada == 3:
        categoria_editada = "Moradia"
    elif escolha_da_categoria_editada == 4:
        categoria_editada = "Saúde"
    else:
        categoria_editada = "Outros"

    with open("despesas.csv", "r", newline="") as arquivo:
        with open("temporario.csv", "w", newline="") as arquivo_temporario:
            leitura = csv.reader(arquivo)
            escrita = csv.writer(arquivo_temporario)

            cabecalho = next(leitura, None)

            if cabecalho:
                escrita.writerow(cabecalho)

            for linha in leitura:
                if int(linha[0]) == id:

                    lista = []

                    lista.append(id)

                    if data_editada is None:
                        lista.append(linha[1])
                    else:
                        lista.append(data_editada)

                    if descricao_editada == "":
                        lista.append(linha[2])
                    else:
                        lista.append(descricao_editada)

                    if valor_editado is None:
                        lista.append(f"{float(linha[3]):.2f}")
                    else:
                        lista.append(f"{valor_editado:.2f}")

                    if escolha_da_categoria_editada is None:
                        lista.append(linha[4])
                    else:
                        lista.append(categoria_editada)

                    escrita.writerow(lista)

                else:
                    escrita.writerow(linha)

    os.remove("despesas.csv")
    os.rename("temporario.csv", "despesas.csv")

    click.echo("Despesa editada com sucesso!")

@main.command('delete', help='Deletar uma despesa existente.')
@click.argument('id', type=click.IntRange(min=1))
def delete(id):
    if not os.path.exists("despesas.csv"):
        click.echo("Nenhuma despesa encontrada com o ID fornecido.")
        return

    with open("despesas.csv", "r") as arquivo:
        id_encontrado = False

        dados = csv.reader(arquivo)

        next(dados, None)

        for linha in dados:
            if int(linha[0]) == id:
                id_encontrado = True
                break

        if id_encontrado == False:
            click.echo("Nenhuma despesa encontrada com o ID fornecido.")
            return

    with open("despesas.csv", "r", newline="") as arquivo:
        with open("temporario.csv", "w", newline="") as arquivo_temporario:
            leitura = csv.reader(arquivo)
            escrita = csv.writer(arquivo_temporario)

            cabecalho = next(leitura, None)

            if cabecalho:
                escrita.writerow(cabecalho)

            id_novo = 1

            for linha in leitura:
                if int(linha[0]) == id:
                    continue
                else:
                    escrita.writerow([id_novo, linha[1], linha[2], linha[3], linha[4]])
                    id_novo += 1

        os.remove("despesas.csv")
        os.rename("temporario.csv", "despesas.csv")

        click.echo(f"Despesa com ID {id} removida com sucesso!")

@main.command('list', help='Listar todas as despesas registradas.')
@click.option("--category", type=click.Choice(["Alimentação", "Transporte", "Moradia", "Saúde", "Outros"], case_sensitive=False), help="Filtra as despesas por categoria")
@click.option("--month-year", type=click.DateTime(formats=["%m/%Y"]), help="Filtra as despesas de um mês/ano específico (formato MM/YYYY).")
def list(category, month_year):

    if month_year:
        month_year = month_year.strftime("%m/%Y")

    tabela = Table(title="Lista de Despesas")

    tabela.add_column("ID", justify="center", style="red")
    tabela.add_column("Data", justify="center", style="cyan")
    tabela.add_column("Descrição", justify="center", style="magenta")
    tabela.add_column("Valor (R$)", justify="center", style="green")
    tabela.add_column("Categoria", justify="center", style="orange")

    valor_total = 0.0

    with open("despesas.csv", "r", newline="") as arquivo:
        dados = csv.reader(arquivo)

        next(dados, None)
        
        for linha in dados:

            if category:
                if linha[4] != category:
                    continue

            elif month_year:
                if linha[1][-7:] != month_year:
                    continue

            valor_total += float(linha[3])
            tabela.add_row(linha[0], linha[1], linha[2], f"{float(linha[3]):.2f}", linha[4])

    tabela.add_row("","", "", "", "", end_section=True)
    tabela.add_row("Total", "", "", f"{valor_total:.2f}", "")

    console = Console()
    console.print(tabela)

@main.command('resume', help='Exibir o resumo financeiro mensal.')
@click.argument("data")
def resume(data):
    try:
        datetime.strptime(data, "%m/%Y")
    except ValueError:
        click.echo("Formato inválido! Use o formato MM/YYYY.")
        return

    with open("despesas.csv", "r", newline="") as arquivo:
        dados = csv.reader(arquivo)

        next(dados, None)

        valor_total = 0
        valor_alimentacao = 0
        valor_transporte = 0
        valor_moradia = 0
        valor_saude = 0
        valor_outros = 0

        for linha in dados:
            if linha[1][-7:] == data:
                if linha[4] == "Alimentação":
                    valor_total += float(linha[3]) 
                    valor_alimentacao += float(linha[3]) 
                elif linha[4] == "Transporte":
                    valor_total += float(linha[3])
                    valor_transporte += float(linha[3]) 
                elif linha[4] == "Moradia":
                    valor_total += float(linha[3])
                    valor_moradia += float(linha[3]) 
                elif linha[4] == "Saúde":
                    valor_total +=float(linha[3])
                    valor_saude += float(linha[3]) 
                else:
                    valor_total += float(linha[3])
                    valor_outros += float(linha[3]) 
            else:
                continue

        if valor_total == 0:
            click.echo("Nenhuma despesa encontrada para este mês.")
            return

        percentual_alimentacao = (valor_alimentacao / valor_total) * 100
        percentual_transporte = (valor_transporte / valor_total) * 100
        percentual_moradia = (valor_moradia / valor_total) * 100
        percentual_saude = (valor_saude / valor_total) * 100
        percentual_outros = (valor_outros / valor_total) * 100

        tabela = Table(title=f"Resumo Financeiro: {data}")

        tabela.add_column("Categoria", justify="center", style="orange")
        tabela.add_column("Valor (R$)", justify="center", style="green")
        tabela.add_column("Percentual (%)", justify="center", style="cyan")

        if valor_alimentacao > 0:
            tabela.add_row("Alimentação", f"{valor_alimentacao:.2f}", f"{percentual_alimentacao:.1f}%")
        if valor_transporte > 0:
            tabela.add_row("Transporte", f"{valor_transporte:.2f}", f"{percentual_transporte:.1f}%")
        if valor_moradia > 0:
            tabela.add_row("Moradia", f"{valor_moradia:.2f}", f"{percentual_moradia:.1f}%")
        if valor_saude > 0:
            tabela.add_row("Saúde", f"{valor_saude:.2f}", f"{percentual_saude:.1f}%")
        if valor_outros > 0:
            tabela.add_row("Outros", f"{valor_outros:.2f}", f"{percentual_outros:.1f}%")

        tabela.add_row("", "", "", end_section=True)
        tabela.add_row("Total Geral", f"{valor_total:.2f}", "100.0%")

        console = Console()
        console.print(tabela)

if __name__ == '__main__':
    main()