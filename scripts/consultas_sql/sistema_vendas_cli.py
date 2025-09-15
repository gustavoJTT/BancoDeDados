import os
import sys
from typing import Optional
import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'postgres',
    'database': 'sistema_vendas'
}

class SistemaVendasCLI:
    def __init__(self):
        self.conexao = None
        print("Sistema de Vendas - CLI Inicializado")
        print("=" * 50)

    def conectar_banco(self):
        try:
            self.conexao = psycopg2.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database']
            )

            print("Conectando ao banco PostgreSQL...")
            #self.conexao = psycopg2.connect(**pg_config)
            self.conexao.autocommit = True
            print("Conexão estabelecida com sucesso!")
            return True
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            return False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return False
        return True

    def desconectar_banco(self):
        if self.conexao:
            self.conexao.close()
            print("Conexão com o banco de dados encerrada.")

    def executar_query(self, sql: str) -> tuple[list[str], list[tuple]]:
        """Executa uma consulta SQL e retorna colunas e linhas"""
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute(sql)
                if cursor.description:
                    colunas = [desc[0] for desc in cursor.description]
                    linhas = cursor.fetchall()
                    return colunas, linhas
                return [], []
        except psycopg2.Error as e:
            print(f"Erro ao executar consulta: {e}")
            return [], []
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return [], []

    def exibir_resultado(self, colunas: list[str], linhas: list[tuple], descricao: str = "") -> None:
        """Exibe os resultados de uma consulta formatados"""
        if descricao:
            print(f"\n{descricao}")
            print("=" * len(descricao))

        if not linhas:
            print("Consulta realizada com sucesso, mas sem retorno")
            return

        # Calcular larguras das colunas
        larguras = [len(col) for col in colunas]
        for linha in linhas:
            for i, valor in enumerate(linha):
                larguras[i] = max(larguras[i], len(str(valor or 'NULL')))

        # Exibir cabeçalho
        cabecalho = " | ".join(col.ljust(larguras[i]) for i, col in enumerate(colunas))
        print(cabecalho)
        print("-" * len(cabecalho))

        # Exibir dados
        for linha in linhas:
            valores = [str(valor or 'NULL').ljust(larguras[i]) for i, valor in enumerate(linha)]
            print(" | ".join(valores))

        print(f"\nTotal: {len(linhas)} registro(s)")

    def executar_consulta(self, sql: str, descricao: str) -> None:
        """Executa uma consulta SQL e exibe os resultados formatados"""
        colunas, linhas = self.executar_query(sql)
        self.exibir_resultado(colunas, linhas, descricao)

    # ========================================
    # FUNCOES COM CONSULTAS SQL
    # ========================================

    def consulta_01_usuarios_ativos(self):
        """1. Listagem de Usuários Ativos"""
        sql = """
        SELECT id_usuario, nome, email, telefone
        FROM usuario
        WHERE ativo = TRUE
        ORDER BY nome;
        """
        self.executar_consulta(sql, "1. Listagem de Usuários Ativos")

    def consulta_02_produtos_categoria(self):
        """2. Catálogo de Produtos por Categoria"""
        sql = """
        SELECT categoria, nome, preco, quantidade_estoque
        FROM produto
        WHERE ativo = TRUE
        ORDER BY categoria, nome;
        """
        self.executar_consulta(sql, "2. Catálogo de Produtos por Categoria")

    def consulta_03_pedidos_status(self):
        """3. Contagem de Pedidos por Status"""
        sql = """
        SELECT status_pedido, COUNT(*) as quantidade_pedidos
        FROM pedido
        GROUP BY status_pedido
        ORDER BY quantidade_pedidos DESC;
        """
        self.executar_consulta(sql, "3. Contagem de Pedidos por Status")

    def consulta_04_estoque_baixo(self):
        """4. Alerta de Estoque Baixo"""
        sql = """
        SELECT nome, categoria, quantidade_estoque, preco
        FROM produto
        WHERE quantidade_estoque < 20 AND ativo = TRUE
        ORDER BY quantidade_estoque ASC;
        """
        self.executar_consulta(sql, "4. Alerta de Estoque Baixo (menos de 20 unidades)")

    def consulta_05_pedidos_recentes(self):
        """5. Histórico de Pedidos Recentes"""
        sql = """
        SELECT p.id_pedido, u.nome as cliente, p.data_pedido, p.status_pedido, p.valor_total
        FROM pedido p
        JOIN usuario u ON p.id_usuario = u.id_usuario
        WHERE p.data_pedido >= CURRENT_DATE - INTERVAL '30 days'
        ORDER BY p.data_pedido DESC;
        """
        self.executar_consulta(sql, "5. Histórico de Pedidos Recentes (últimos 30 dias)")

    def consulta_06_produtos_caros_categoria(self):
        """6. Produtos Mais Caros por Categoria"""
        sql = """
        SELECT categoria, nome, preco
        FROM produto p1
        WHERE preco = (
            SELECT MAX(preco)
            FROM produto p2
            WHERE p2.categoria = p1.categoria AND p2.ativo = TRUE
        ) AND ativo = TRUE
        ORDER BY categoria;
        """
        self.executar_consulta(sql, "6. Produtos Mais Caros por Categoria")

    def consulta_07_contatos_incompletos(self):
        """7. Clientes com Dados Incompletos"""
        sql = """
        SELECT id_usuario, nome, email, telefone, endereco
        FROM usuario
        WHERE (telefone IS NULL OR telefone = '')
           OR (endereco IS NULL OR endereco = '')
        AND ativo = TRUE
        ORDER BY nome;
        """
        self.executar_consulta(sql, "7. Clientes com Dados Incompletos")

    def consulta_08_pedidos_enviados(self):
        """8. Pedidos Pendentes de Entrega"""
        sql = """
        SELECT p.id_pedido, u.nome as cliente, p.data_pedido, p.status_pedido,
               p.valor_total, p.endereco_entrega
        FROM pedido p
        JOIN usuario u ON p.id_usuario = u.id_usuario
        WHERE p.status_pedido IN ('pendente', 'confirmado', 'processando', 'enviado')
        ORDER BY p.data_pedido;
        """
        self.executar_consulta(sql, "8. Pedidos Pendentes de Entrega")

    def consulta_09_detalhamento_pedido(self):
        """9. Detalhamento Completo de Pedidos"""
        sql = """
        SELECT p.id_pedido, u.nome as cliente, u.email, p.data_pedido, p.status_pedido,
               pr.nome as produto, ip.quantidade, ip.preco_unitario, ip.subtotal
        FROM pedido p
        JOIN usuario u ON p.id_usuario = u.id_usuario
        JOIN itens_pedido ip ON p.id_pedido = ip.id_pedido
        JOIN produto pr ON ip.id_produto = pr.id_produto
        ORDER BY p.id_pedido, pr.nome;
        """
        self.executar_consulta(sql, "9. Detalhamento Completo de Pedidos")

    def consulta_10_ranking_produtos(self):
        """10. Ranking dos Produtos Mais Vendidos"""
        sql = """
        SELECT pr.nome, pr.categoria, SUM(ip.quantidade) as total_vendido,
               SUM(ip.subtotal) as receita_total
        FROM produto pr
        JOIN itens_pedido ip ON pr.id_produto = ip.id_produto
        GROUP BY pr.id_produto, pr.nome, pr.categoria
        ORDER BY total_vendido DESC, receita_total DESC;
        """
        self.executar_consulta(sql, "10. Ranking dos Produtos Mais Vendidos")

    def consulta_11_clientes_sem_compras(self):
        """11. Análise de Clientes Sem Compras"""
        sql = """
        SELECT u.id_usuario, u.nome, u.email, u.telefone, u.data_cadastro
        FROM usuario u
        LEFT JOIN pedido p ON u.id_usuario = p.id_usuario
        WHERE p.id_usuario IS NULL AND u.ativo = TRUE
        ORDER BY u.data_cadastro DESC;
        """
        self.executar_consulta(sql, "11. Análise de Clientes Sem Compras")

    def consulta_12_estatisticas_cliente(self):
        """12. Estatísticas de Compras por Cliente"""
        sql = """
        SELECT u.nome, u.email,
               COUNT(p.id_pedido) as total_pedidos,
               COALESCE(SUM(p.valor_total), 0) as total_gasto,
               COALESCE(AVG(p.valor_total), 0) as ticket_medio
        FROM usuario u
        LEFT JOIN pedido p ON u.id_usuario = p.id_usuario
        WHERE u.ativo = TRUE
        GROUP BY u.id_usuario, u.nome, u.email
        ORDER BY total_gasto DESC;
        """
        self.executar_consulta(sql, "12. Estatísticas de Compras por Cliente")

    def consulta_13_relatorio_mensal(self):
        """13. Relatório Mensal de Vendas"""
        sql = """
        SELECT EXTRACT(YEAR FROM data_pedido) as ano,
               EXTRACT(MONTH FROM data_pedido) as mes,
               COUNT(*) as total_pedidos,
               SUM(valor_total) as receita_total,
               AVG(valor_total) as ticket_medio
        FROM pedido
        WHERE status_pedido NOT IN ('cancelado')
        GROUP BY EXTRACT(YEAR FROM data_pedido), EXTRACT(MONTH FROM data_pedido)
        ORDER BY ano DESC, mes DESC;
        """
        self.executar_consulta(sql, "13. Relatório Mensal de Vendas")

    def consulta_14_produtos_nao_vendidos(self):
        """14. Produtos que Nunca Foram Vendidos"""
        sql = """
        SELECT pr.id_produto, pr.nome, pr.categoria, pr.preco, pr.quantidade_estoque
        FROM produto pr
        LEFT JOIN itens_pedido ip ON pr.id_produto = ip.id_produto
        WHERE ip.id_produto IS NULL AND pr.ativo = TRUE
        ORDER BY pr.categoria, pr.nome;
        """
        self.executar_consulta(sql, "14. Produtos que Nunca Foram Vendidos")

    def consulta_15_ticket_medio_categoria(self):
        """15. Análise de Ticket Médio por Categoria"""
        sql = """
        SELECT pr.categoria,
               COUNT(DISTINCT p.id_pedido) as total_pedidos,
               SUM(ip.subtotal) as receita_total,
               AVG(ip.subtotal) as ticket_medio_item,
               SUM(ip.quantidade) as total_itens_vendidos
        FROM produto pr
        JOIN itens_pedido ip ON pr.id_produto = ip.id_produto
        JOIN pedido p ON ip.id_pedido = p.id_pedido
        WHERE p.status_pedido NOT IN ('cancelado')
        GROUP BY pr.categoria
        ORDER BY receita_total DESC;
        """
        self.executar_consulta(sql, "15. Análise de Ticket Médio por Categoria")

    # ========================================
    # MENUS
    # ========================================
    def menu_exercicios(self):
        """MENU"""
        while True:
            print("=" * 40)
            print("1. Listagem de Usuários Ativos")
            print("2. Catálogo de Produtos por Categoria")
            print("3. Contagem de Pedidos por Status")
            print("4. Alerta de Estoque Baixo")
            print("5. Histórico de Pedidos Recentes")
            print("6. Produtos Mais Caros por Categoria")
            print("7. Clientes com Dados Incompletos")
            print("8. Pedidos Pendentes de Entrega")
            print("9. Detalhamento Completo de Pedidos")
            print("10. Ranking dos Produtos Mais Vendidos")
            print("11. Análise de Clientes Sem Compras")
            print("12. Estatísticas de Compras por Cliente")
            print("13. Relatório Mensal de Vendas")
            print("14. Produtos que Nunca Foram Vendidos")
            print("15. Análise de Ticket Médio por Categoria")
            print("0. Voltar ao Menu Principal")
            print("=" * 40)

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.consulta_01_usuarios_ativos()
            elif opcao == "2":
                self.consulta_02_produtos_categoria()
            elif opcao == "3":
                self.consulta_03_pedidos_status()
            elif opcao == "4":
                self.consulta_04_estoque_baixo()
            elif opcao == "5":
                self.consulta_05_pedidos_recentes()
            elif opcao == "6":
                self.consulta_06_produtos_caros_categoria()
            elif opcao == "7":
                self.consulta_07_contatos_incompletos()
            elif opcao == "8":
                self.consulta_08_pedidos_enviados()
            elif opcao == "9":
                self.consulta_09_detalhamento_pedido()
            elif opcao == "10":
                self.consulta_10_ranking_produtos()
            elif opcao == "11":
                self.consulta_11_clientes_sem_compras()
            elif opcao == "12":
                self.consulta_12_estatisticas_cliente()
            elif opcao == "13":
                self.consulta_13_relatorio_mensal()
            elif opcao == "14":
                self.consulta_14_produtos_nao_vendidos()
            elif opcao == "15":
                self.consulta_15_ticket_medio_categoria()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")

            input("\nPressione ENTER para continuar...")

def main():
    cli = SistemaVendasCLI()
    if cli.conectar_banco():
        try:
            cli.menu_exercicios()
        finally:
            cli.desconectar_banco()
    else:
        print("Falha ao conectar ao banco de dados.")
        sys.exit(1)

if __name__ == "__main__":
    main()
