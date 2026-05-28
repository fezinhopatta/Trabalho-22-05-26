import redis
from docx import Document
from docx.shared import Pt, RGBColor
import time

# Conexão com o Redis local (Padrão no Debian)
# decode_responses=True converte os bytes em strings automaticamente
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def format_redis_output(result):
    """Formata a saída do redis-py para se assemelhar ao output do redis-cli"""
    if result is True or result == "OK": 
        return "OK"
    if result is False: 
        return "(integer) 0"
    if result is None: 
        return "(nil)"
    if isinstance(result, int): 
        return f"(integer) {result}"
    if isinstance(result, float): 
        return f'"{result}"'
    if isinstance(result, str): 
        return f'"{result}"'
    if isinstance(result, (list, tuple)):
        if not result: return "(empty array)"
        lines = []
        for i, item in enumerate(result):
            if isinstance(item, (list, tuple)):
                # Tratamento para arrays aninhados (ex: retorno do SCAN)
                sub_lines = [f"    {j+1}) \"{str(x)}\"" for j, x in enumerate(item)]
                lines.append(f"{i+1}) \n" + "\n".join(sub_lines))
            else:
                lines.append(f"{i+1}) \"{str(item)}\"")
        return "\n".join(lines)
    return str(result)

def main():
    # Limpa os bancos de dados para garantir que os testes rodem de forma limpa
    r.flushall()

    doc = Document()
    doc.add_heading('Lista de Exercícios Práticos - Resultados Redis CLI', 0)

    # Definição dos 24 exercícios
    exercicios = [
        (1, "Cadastro de Usuário", [
            ["SET", "usuario", "Carlos"],
            ["GET", "usuario"],
            ["SET", "usuario", "Carlos Silva"],
            ["GET", "usuario"]
        ]),
        (2, "Cadastro de Produto", [
            ["MSET", "produto", "Notebook", "preco", "3500", "estoque", "15"],
            ["MGET", "produto", "preco", "estoque"]
        ]),
        (3, "Controle de Login", [
            ["SETNX", "admin", "token_123"],
            ["SETNX", "admin", "token_456"]
        ]),
        (4, "Nome Completo", [
            ["SET", "nome", "Maria"],
            ["APPEND", "nome", " Oliveira"],
            ["STRLEN", "nome"],
            ["GETRANGE", "nome", "0", "4"]
        ]),
        (5, "Alteração Parcial", [
            ["SET", "cidade", "Campinas"],
            ["SETRANGE", "cidade", "0", "São "],
            ["GET", "cidade"]
        ]),
        (6, "Sistema de Pontuação", [
            ["SET", "pontos", "10"],
            ["INCR", "pontos"],
            ["INCRBY", "pontos", "5"],
            ["DECRBY", "pontos", "3"],
            ["GET", "pontos"]
        ]),
        (7, "Carteira Digital", [
            ["SET", "saldo", "100.50"],
            ["INCRBYFLOAT", "saldo", "25.75"],
            ["GET", "saldo"]
        ]),
        (8, "Token Temporário", [
            ["SETEX", "token", "60", "xyz987"],
            ["TTL", "token"],
            ["PERSIST", "token"],
            ["TTL", "token"]
        ]),
        (9, "Expiração em Milissegundos", [
            ["SET", "sessao", "abc123"],
            ["PEXPIRE", "sessao", "5000"],
            ["PTTL", "sessao"]
        ]),
        (10, "Gerenciamento de Chaves", [
            ["SET", "curso", "Redis"],
            ["RENAME", "curso", "disciplina"],
            ["COPY", "disciplina", "backup_disciplina"],
            ["TYPE", "disciplina"],
            ["EXISTS", "disciplina"],
            ["DEL", "disciplina"]
        ]),
        (11, "Banco Redis", [
            ["SET", "chave_teste", "Estou no DB 0"],
            ["MOVE", "chave_teste", "1"],
            ["SELECT", "1"],
            ["GET", "chave_teste"],
            ["SELECT", "0"] # Volta para o banco padrão
        ]),
        (12, "Listagem de Chaves", [
            ["MSET", "k1", "v1", "k2", "v2", "k3", "v3", "k4", "v4", "k5", "v5"],
            ["KEYS", "*"],
            ["SCAN", "0"]
        ]),
        (13, "Lista de Tarefas", [
            ["RPUSH", "tarefas", "Estudar Redis", "Fazer Exercícios", "Dormir"],
            ["LRANGE", "tarefas", "0", "-1"]
        ]),
        (14, "Controle de Fila", [
            ["LLEN", "tarefas"],
            ["LINDEX", "tarefas", "0"],
            ["LINDEX", "tarefas", "-1"]
        ]),
        (15, "Alteração de Item", [
            ["LSET", "tarefas", "1", "Fazer Exercícios Práticos"],
            ["LRANGE", "tarefas", "0", "-1"]
        ]),
        (16, "Inserção Estratégica", [
            ["LINSERT", "tarefas", "BEFORE", "Dormir", "Tomar Café"],
            ["LRANGE", "tarefas", "0", "-1"]
        ]),
        (17, "Remoção de Elementos", [
            ["LPOP", "tarefas"],
            ["RPOP", "tarefas"],
            ["LRANGE", "tarefas", "0", "-1"]
        ]),
        (18, "Movendo Itens Entre Filas", [
            ["RPUSH", "fila_atividade_pendente", "Job_A", "Job_B"],
            ["LMOVE", "fila_atividade_pendente", "fila_atividade_processando", "LEFT", "RIGHT"],
            ["LRANGE", "fila_atividade_processando", "0", "-1"]
        ]),
        (19, "Histórico Limitado", [
            ["RPUSH", "logs", "log1", "log2", "log3", "log4", "log5", "log6", "log7", "log8", "log9", "log10"],
            ["LTRIM", "logs", "-5", "-1"],
            ["LRANGE", "logs", "0", "-1"]
        ]),
        (20, "Remoção por Valor", [
            ["RPUSH", "tarefas", "Dormir", "Dormir", "Dormir"],
            ["LREM", "tarefas", "1", "Dormir"],
            ["LREM", "tarefas", "0", "Dormir"],
            ["LRANGE", "tarefas", "0", "-1"]
        ]),
        (21, "Localização de Elementos", [
            ["RPUSH", "tarefas", "Estudar Redis"],
            ["LPOS", "tarefas", "Estudar Redis"],
            ["RPUSH", "tarefas", "ItemRepetido", "ItemRepetido"],
            ["LPOS", "tarefas", "ItemRepetido", "COUNT", "0"]
        ]),
        (22, "Remoção Múltipla", [
            ["RPUSH", "tarefas_multi", "A", "B", "C", "D"],
            ["LPOP", "tarefas_multi", "3"],
            ["LRANGE", "tarefas_multi", "0", "-1"]
        ]),
        (23, "Expiração em Listas", [
            ["RPUSH", "lista_temporaria", "Item1"],
            ["EXPIRE", "lista_temporaria", "2"],
            ["TTL", "lista_temporaria"]
        ]),
        (24, "Desafio - Fila de Atualização do Debian", [
            # Fluxo simulando uma fila de tarefas de um sysadmin Debian
            ["RPUSH", "debian:fila_apt", "apt update", "apt upgrade -y", "apt autoremove -y"],
            ["LRANGE", "debian:fila_apt", "0", "-1"],
            ["LPOP", "debian:fila_apt"], # Processando a primeira task
            ["SET", "debian:status_servico", "Atualizando pacotes...", "EX", "300"],
            ["GET", "debian:status_servico"]
        ])
    ]

    for num, titulo, comandos in exercicios:
        doc.add_heading(f'Exercício {num} - {titulo}', level=1)
        
        # Criação do bloco de simulação de terminal
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(12)
        
        for cmd in comandos:
            cmd_str = " ".join(cmd)
            # Executa o comando no Redis enviando os argumentos brutos
            try:
                # O python desempacota a lista com o *cmd
                resultado = r.execute_command(*cmd) 
                saida_formatada = format_redis_output(resultado)
                texto = f"127.0.0.1:6379> {cmd_str}\n{saida_formatada}\n"
            except Exception as e:
                texto = f"127.0.0.1:6379> {cmd_str}\n(error) {str(e)}\n"
            
            # Adicionando o texto no parágrafo com fonte monoespaçada
            run = p.add_run(texto)
            run.font.name = 'Courier New'
            run.font.size = Pt(10)
            
    # Salva o arquivo final
    doc.save('Resultados_Redis.docx')
    print("Arquivo 'Resultados_Redis.docx' gerado com sucesso!")

if __name__ == "__main__":
    try:
        r.ping()
        main()
    except redis.exceptions.ConnectionError:
        print("Erro: Não foi possível conectar ao Redis. Verifique se o serviço está rodando no Debian (sudo systemctl status redis-server).")