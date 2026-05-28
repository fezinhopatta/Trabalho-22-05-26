import redis
import io
from docx import Document
from docx.shared import Inches
from PIL import Image, ImageDraw, ImageFont

def format_output(res, base_indent=""):
    """Formata as respostas reais do Redis para imitar perfeitamente o redis-cli, incluindo listas aninhadas"""
    if res is True:
        return "(integer) 1"
    if res is False:
        return "(integer) 0"
    if res is None:
        return "(nil)"
    if isinstance(res, int):
        return f"(integer) {res}"
    if isinstance(res, bytes):
        # Decodifica bytes para string
        return f'"{res.decode("utf-8")}"'
    if isinstance(res, str):
        # O Redis só não coloca aspas quando a resposta é um OK genérico
        return res if res == 'OK' else f'"{res}"'
    if isinstance(res, list):
        if not res:
            return "(empty array)"
        
        lines = []
        for i, item in enumerate(res):
            prefix = f"{i+1}) "
            if isinstance(item, list):
                # Resolve as indentações de listas dentro de listas (como no comando SCAN)
                sub_lines = format_output(item).split('\n')
                lines.append(f"{base_indent}{prefix}{sub_lines[0]}")
                
                # Calcula o espaço para manter o alinhamento das sub-listas
                padding = " " * len(prefix)
                for sub in sub_lines[1:]:
                    lines.append(f"{base_indent}{padding}{sub}")
            else:
                lines.append(f"{base_indent}{prefix}{format_output(item)}")
        return "\n".join(lines)
    
    return str(res)

def format_cmd_string(cmd_list):
    """Garante que strings com espaço recebam aspas (ex: "Estudar Redis") para a visualização correta"""
    formatted_parts = []
    for part in cmd_list:
        if ' ' in part:
            formatted_parts.append(f'"{part}"')
        else:
            formatted_parts.append(part)
    return " ".join(formatted_parts)

def create_terminal_image(text):
    """Fabrica a imagem PNG em memória imitando o terminal Ubuntu/Redis-cli"""
    try:
        font = ImageFont.load_default(size=16)
        char_width, line_height = 10, 22
    except TypeError:
        font = ImageFont.load_default()
        char_width, line_height = 8, 15

    linhas = text.split('\n')
    max_caracteres = max([len(linha) for linha in linhas] + [1])
    
    largura = (max_caracteres * char_width) + 40
    altura = (len(linhas) * line_height) + 40

    img = Image.new('RGB', (largura, altura), color=(12, 12, 12))
    d = ImageDraw.Draw(img)

    d.multiline_text((20, 20), text, font=font, fill=(204, 204, 204), spacing=4)

    img_stream = io.BytesIO()
    img.save(img_stream, format='PNG')
    img_stream.seek(0)
    
    return img_stream

def main():
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print("Conectado ao Redis com sucesso! Executando comandos REAIS e gerando documento...")
    except redis.ConnectionError:
        print("Erro: Não foi possível conectar ao Redis na porta 6379.")
        return

    exercicios = {
        1: {
            "run": [["SET", "usuario", "Carlos"], ["GET", "usuario"], ["SET", "usuario", "Carlos Silva"], ["GET", "usuario"]]
        },
        2: {
            "run": [["MSET", "produto", "Notebook", "preco", "3500", "estoque", "15"], ["MGET", "produto", "preco", "estoque"]]
        },
        3: {
            "run": [["SETNX", "admin", "true"], ["SETNX", "admin", "false"]]
        },
        4: {
            "run": [["SET", "nome", "Maria"], ["APPEND", "nome", " Oliveira"], ["STRLEN", "nome"], ["GETRANGE", "nome", "0", "4"]]
        },
        5: {
            "run": [["SET", "cidade", "Campinas"], ["SETRANGE", "cidade", "0", "São "], ["GET", "cidade"]]
        },
        6: {
            "run": [["SET", "pontos", "10"], ["INCR", "pontos"], ["INCRBY", "pontos", "5"], ["DECRBY", "pontos", "3"], ["GET", "pontos"]]
        },
        7: {
            "run": [["SET", "saldo", "100.50"], ["INCRBYFLOAT", "saldo", "25.75"], ["GET", "saldo"]]
        },
        8: {
            "run": [["SET", "token", "xyz123", "EX", "60"], ["TTL", "token"], ["PERSIST", "token"], ["TTL", "token"]]
        },
        9: {
            "run": [["SET", "sessao", "ativa"], ["PEXPIRE", "sessao", "5000"], ["PTTL", "sessao"]]
        },
        10: {
            "run": [["SET", "curso", "Redis"], ["RENAME", "curso", "disciplina"], ["COPY", "disciplina", "backup_disciplina"], ["TYPE", "disciplina"], ["EXISTS", "disciplina"], ["DEL", "disciplina"]]
        },
        11: {
            "run": [["SET", "minha_chave", "teste"], ["MOVE", "minha_chave", "1"], ["SELECT", "1"], ["GET", "minha_chave"], ["SELECT", "0"]]
        },
        12: {
            "run": [["MSET", "k1", "1", "k2", "2", "k3", "3", "k4", "4", "k5", "5"], ["KEYS", "*"], ["SCAN", "0"]]
        },
        13: {
            "run": [["RPUSH", "tarefas", "Estudar Redis", "Fazer Exercicios", "Dormir"], ["LRANGE", "tarefas", "0", "-1"]]
        },
        14: {
            "setup": [["RPUSH", "tarefas", "Estudar Redis", "Fazer Exercicios", "Dormir"]], 
            "run": [["LLEN", "tarefas"], ["LINDEX", "tarefas", "0"], ["LINDEX", "tarefas", "-1"]]
        },
        15: {
            "setup": [["RPUSH", "tarefas", "Estudar Redis", "Fazer Exercicios", "Dormir"]], 
            "run": [["LSET", "tarefas", "1", "Fazer Exercicios Praticos"], ["LRANGE", "tarefas", "0", "-1"]]
        },
        16: {
            "setup": [["RPUSH", "tarefas", "Estudar Redis", "Fazer Exercicios Praticos", "Dormir"]], 
            "run": [["LINSERT", "tarefas", "BEFORE", "Dormir", "Tomar Cafe"], ["LRANGE", "tarefas", "0", "-1"]]
        },
        17: {
            "setup": [["RPUSH", "tarefas", "Estudar Redis", "Fazer Exercicios Praticos", "Tomar Cafe", "Dormir"]], 
            "run": [["LPOP", "tarefas"], ["RPOP", "tarefas"], ["LRANGE", "tarefas", "0", "-1"]]
        },
        18: {
            "run": [["RPUSH", "fila_atividade_pendente", "Tarefa 1", "Tarefa 2"], ["LMOVE", "fila_atividade_pendente", "fila_atividade_processando", "LEFT", "RIGHT"]]
        },
        19: {
            "run": [["RPUSH", "logs", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "L10"], ["LTRIM", "logs", "-5", "-1"], ["LRANGE", "logs", "0", "-1"]]
        },
        20: {
            "setup": [["RPUSH", "tarefas", "Estudar Redis", "Fazer Exercicios"]], 
            "run": [["RPUSH", "tarefas", "Dormir", "Dormir", "Dormir"], ["LREM", "tarefas", "1", "Dormir"], ["LREM", "tarefas", "0", "Dormir"], ["LRANGE", "tarefas", "0", "-1"]]
        },
        21: {
            "setup": [["RPUSH", "tarefas", "Estudar Redis", "Fazer Exercicios", "Dormir", "Tomar Cafe", "Dormir"]], 
            "run": [["LPOS", "tarefas", "Estudar Redis"], ["LPOS", "tarefas", "Dormir", "COUNT", "0"]]
        },
        22: {
            "setup": [["RPUSH", "tarefas", "Estudar Redis", "Fazer Exercicios", "Estudar Redis", "Dormir"]], 
            "run": [["LREM", "tarefas", "0", "Estudar Redis"], ["DEL", "tarefas"]]
        },
        23: {
            "run": [["RPUSH", "lista_temp", "item1", "item2"], ["EXPIRE", "lista_temp", "10"], ["TTL", "lista_temp"], ["EXISTS", "lista_temp"]]
        },
        24: {
            "run": [
                ["SET", "ip:192.168.1.50:tentativas", "1", "EX", "10", "NX"],
                ["INCR", "ip:192.168.1.50:tentativas"],
                ["INCR", "ip:192.168.1.50:tentativas"],
                ["GET", "ip:192.168.1.50:tentativas"],
                ["INCRBY", "ip:192.168.1.50:tentativas", "3"],
                ["SET", "ip:192.168.1.50:bloqueado", "true", "EX", "3600"],
                ["EXISTS", "ip:192.168.1.50:bloqueado"]
            ]
        }
    }

    doc = Document()
    doc.add_heading('Resolução: Exercícios Práticos - Redis CLI', 0)

    for ex_num, block in exercicios.items():
        doc.add_heading(f'Exercício {ex_num}', level=1)
        
        # GARANTIA ABSOLUTA DE ISOLAMENTO: Limpa completamente a engine do Redis
        # antes de rodar cada exercício, garantindo que nenhum lixo vaze.
        r.flushall() 
        
        # Roda a preparação invisível (se houver)
        for cmd in block.get("setup", []):
            try:
                r.execute_command(*cmd)
            except Exception:
                pass

        output_lines = []
        for cmd in block.get("run", []):
            # Transforma as palavras do comando em string colocando aspas nas que tem espaço
            cmd_str = format_cmd_string(cmd)
            output_lines.append(f"127.0.0.1:6379> {cmd_str}")
            
            try:
                # EXECUÇÃO REAL do comando no banco de dados
                res = r.execute_command(*cmd)
                # Formata baseando-se no tipo do dado retornado pela engine
                res_str = format_output(res)
                output_lines.append(res_str)
            except Exception as e:
                output_lines.append(f"(error) ERR {str(e)}")

        texto_terminal = "\n".join(output_lines)
        img_stream = create_terminal_image(texto_terminal)
        
        doc.add_picture(img_stream, width=Inches(5.5))
        print(f"Exercício {ex_num} executado e processado com sucesso.")

    nome_arquivo = "Lista_Exercicios_Redis.docx"
    doc.save(nome_arquivo)
    print(f"\nDocumento '{nome_arquivo}' gerado com sucesso com outputs REAIS!")

if __name__ == "__main__":
    main()