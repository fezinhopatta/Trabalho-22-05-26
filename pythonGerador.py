import redis
import io
from docx import Document
from docx.shared import Inches
from PIL import Image, ImageDraw, ImageFont

def format_output(res):
    """Formata as respostas do Redis para imitar a saída padrão do redis-cli"""
    if res is True:
        return "(integer) 1"
    elif res is False:
        return "(integer) 0"
    elif res is None:
        return "(nil)"
    elif isinstance(res, list):
        if not res:
            return "(empty array)"
        return "\n".join([f"{i+1}) \"{item}\"" for i, item in enumerate(res)])
    elif isinstance(res, int):
        return f"(integer) {res}"
    elif isinstance(res, bytes):
        return f"\"{res.decode('utf-8')}\""
    elif isinstance(res, str):
        if res == 'OK':
            return res
        return f"\"{res}\""
    else:
        return str(res)

def create_terminal_image(text):
    """Fabrica uma imagem PNG em memória imitando um terminal escuro"""
    try:
        # Tenta usar a fonte padrão com um tamanho legível (Pillow >= 9.2.0)
        font = ImageFont.load_default(size=16)
        char_width, line_height = 10, 22
    except TypeError:
        # Fallback para versões antigas do Pillow
        font = ImageFont.load_default()
        char_width, line_height = 8, 15

    # Calcula o tamanho ideal da imagem baseado no tamanho do texto
    linhas = text.split('\n')
    max_caracteres = max([len(linha) for linha in linhas] + [1])
    
    largura = (max_caracteres * char_width) + 40
    altura = (len(linhas) * line_height) + 40

    # Cria a imagem (Fundo quase preto #0c0c0c)
    img = Image.new('RGB', (largura, altura), color=(12, 12, 12))
    d = ImageDraw.Draw(img)

    # Escreve o texto simulando terminal (Cinza claro #cccccc)
    d.multiline_text((20, 20), text, font=font, fill=(204, 204, 204), spacing=4)

    # Salva a imagem na memória (BytesIO) para não precisar criar arquivos temporários no disco
    img_stream = io.BytesIO()
    img.save(img_stream, format='PNG')
    img_stream.seek(0)
    
    return img_stream

def main():
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print("Conectado ao Redis com sucesso! Gerando documento...")
    except redis.ConnectionError:
        print("Erro: Não foi possível conectar ao Redis na porta 6379.")
        return

    r.flushdb()

    exercicios = {
        1: [["SET", "usuario", "Carlos"], ["GET", "usuario"], ["SET", "usuario", "Carlos Silva"], ["GET", "usuario"]],
        2: [["MSET", "produto", "Notebook", "preco", "3500", "estoque", "15"], ["MGET", "produto", "preco", "estoque"]],
        3: [["SETNX", "admin", "true"], ["SETNX", "admin", "false"]],
        4: [["SET", "nome", "Maria"], ["APPEND", "nome", " Oliveira"], ["STRLEN", "nome"], ["GETRANGE", "nome", "0", "4"]],
        5: [["SET", "cidade", "Campinas"], ["SETRANGE", "cidade", "0", "São "], ["GET", "cidade"]],
        6: [["SET", "pontos", "10"], ["INCR", "pontos"], ["INCRBY", "pontos", "5"], ["DECRBY", "pontos", "3"], ["GET", "pontos"]],
        7: [["SET", "saldo", "100.50"], ["INCRBYFLOAT", "saldo", "25.75"], ["GET", "saldo"]],
        8: [["SET", "token", "xyz123", "EX", "60"], ["TTL", "token"], ["PERSIST", "token"], ["TTL", "token"]],
        9: [["SET", "sessao", "ativa"], ["PEXPIRE", "sessao", "5000"], ["PTTL", "sessao"]],
        10: [["SET", "curso", "Redis"], ["RENAME", "curso", "disciplina"], ["COPY", "disciplina", "backup_disciplina"], ["TYPE", "disciplina"], ["EXISTS", "disciplina"], ["DEL", "disciplina"]],
        11: [["SET", "minha_chave", "teste"], ["MOVE", "minha_chave", "1"], ["SELECT", "1"], ["GET", "minha_chave"], ["SELECT", "0"]],
        12: [["MSET", "k1", "1", "k2", "2", "k3", "3", "k4", "4", "k5", "5"], ["KEYS", "*"]],
        13: [["RPUSH", "tarefas", "Estudar Redis", "Fazer Exercícios", "Dormir"], ["LRANGE", "tarefas", "0", "-1"]],
        14: [["LLEN", "tarefas"], ["LINDEX", "tarefas", "0"], ["LINDEX", "tarefas", "-1"]],
        15: [["LSET", "tarefas", "1", "Fazer Exercícios Práticos"], ["LRANGE", "tarefas", "0", "-1"]],
        16: [["LINSERT", "tarefas", "BEFORE", "Dormir", "Tomar Café"], ["LRANGE", "tarefas", "0", "-1"]],
        17: [["LPOP", "tarefas"], ["RPOP", "tarefas"], ["LRANGE", "tarefas", "0", "-1"]],
        18: [["RPUSH", "fila_atividade_pendente", "Tarefa 1", "Tarefa 2"], ["LMOVE", "fila_atividade_pendente", "fila_atividade_processando", "LEFT", "RIGHT"]],
        19: [["RPUSH", "logs", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "L10"], ["LTRIM", "logs", "-5", "-1"], ["LRANGE", "logs", "0", "-1"]],
        20: [["RPUSH", "tarefas_repetidas", "Dormir", "Dormir", "Dormir"], ["LREM", "tarefas_repetidas", "1", "Dormir"], ["LREM", "tarefas_repetidas", "0", "Dormir"]],
        21: [["LPOS", "tarefas", "Tomar Café"], ["LPOS", "tarefas", "Dormir", "COUNT", "0"]],
        22: [["LREM", "tarefas", "0", "Estudar Redis"], ["DEL", "tarefas"]],
        23: [["RPUSH", "lista_temp", "item1", "item2"], ["EXPIRE", "lista_temp", "10"], ["TTL", "lista_temp"], ["EXISTS", "lista_temp"]],
        24: [
            ["SET", "ip:192.168.1.50:tentativas", "1", "EX", "10", "NX"],
            ["INCR", "ip:192.168.1.50:tentativas"],
            ["INCR", "ip:192.168.1.50:tentativas"],
            ["GET", "ip:192.168.1.50:tentativas"],
            ["INCRBY", "ip:192.168.1.50:tentativas", "3"],
            ["SET", "ip:192.168.1.50:bloqueado", "true", "EX", "3600"],
            ["EXISTS", "ip:192.168.1.50:bloqueado"]
        ]
    }

    # Inicializa o documento Word
    doc = Document()
    doc.add_heading('Resolução: Exercícios Práticos - Redis CLI', 0)

    for ex_num, cmds in exercicios.items():
        doc.add_heading(f'Exercício {ex_num}', level=1)
        
        output_lines = []
        for cmd in cmds:
            cmd_str = " ".join(cmd)
            output_lines.append(f"127.0.0.1:6379> {cmd_str}")
            
            try:
                res = r.execute_command(*cmd)
                res_str = format_output(res)
                output_lines.append(res_str)
            except Exception as e:
                output_lines.append(f"(error) {str(e)}")

        # Junta tudo no formato de texto multilinhas
        texto_terminal = "\n".join(output_lines)
        
        # Cria a imagem falsa do terminal
        img_stream = create_terminal_image(texto_terminal)
        
        # Insere no Word
        doc.add_picture(img_stream, width=Inches(5.0))
        
        print(f"Exercício {ex_num} processado com sucesso.")

    # Salva o arquivo final
    nome_arquivo = "Lista_Exercicios_Redis.docx"
    doc.save(nome_arquivo)
    print(f"\nDocumento '{nome_arquivo}' gerado com sucesso!")

if __name__ == "__main__":
    main()