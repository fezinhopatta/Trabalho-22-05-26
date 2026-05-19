import os
import shutil
import subprocess

print("🚀 Iniciando a reestruturação automática do projeto React + Vite...")

# 1. LIMPEZA SEGURA (Apaga apenas arquivos do front-end que podem estar errados, mantendo o .git intacto)
arquivos_para_deletar = ['src', 'node_modules', 'package.json', 'package-lock.json', 'vite.config.js', 'index.html']

for item in arquivos_para_deletar:
    if os.path.exists(item):
        try:
            if os.path.isdir(item):
                shutil.rmtree(item)
                print(f"🗑️  Diretório removido: {item}")
            else:
                os.remove(item)
                print(f"🗑️  Arquivo removido: {item}")
        except Exception as e:
            print(f"⚠️  Não foi possível remover {item}: {e}")

# 2. CRIAÇÃO DAS PASTAS E DIRETÓRIOS ESTRUTURAIS
os.makedirs('src/components', exist_ok=True)
print("📁 Estrutura de pastas 'src/components' criada com sucesso.")

# 3. MAPEAMENTO DE CONTEÚDO DOS ARQUIVOS DO PROJETO
arquivos_projeto = {}

# --- CONFIGURAÇÕES DO SISTEMA (RAIZ) ---
arquivos_projeto['package.json'] = """{
  "name": "pizzaria-fatec",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.3.0",
    "vite": "^5.2.11"
  }
}"""

arquivos_projeto['vite.config.js'] = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})"""

arquivos_projeto['index.html'] = """<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Pizzaria Fatec - Escolha seu Sabor</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>"""

# --- ENTRADAS DO REACT ---
arquivos_projeto['src/main.jsx'] = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css' 

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)"""

arquivos_projeto['src/index.css'] = "/* CSS global reset basico */"

arquivos_projeto['src/App.css'] = """body { font-family: sans-serif; line-height: 1.6; margin: 0; color: #333; }
header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 5%; background: #eee; }
nav ul { list-style: none; display: flex; gap: 20px; padding: 0; }
nav a { text-decoration: none; color: #d32f2f; font-weight: bold; }
.conteudo-principal { padding: 2rem 5%; max-width: 1200px; margin: auto; }
.titulo-pagina { text-align: center; color: #222; }
.grade-de-pizzas { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 2rem; }
.cartao-pizza { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; text-align: center; transition: transform 0.2s; }
.cartao-pizza:hover { transform: translateY(-5px); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
.cartao-pizza img { max-width: 100%; border-radius: 4px; }
.sabor-preco { font-weight: bold; color: #2e7d32; font-size: 1.2rem; }
.botao-pedir, .botao-finalizar, .botao-enviar { display: inline-block; background: #d32f2f; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; cursor: pointer; border: none; font-weight: bold; }
.botao-finalizar { background: #2e7d32; margin-top: 1rem; width: 100%; max-width: 200px; }
.botao-finalizar:hover { background: #1b5e20; }
.carrinho-secao { margin-top: 3rem; padding: 2rem; background: #f9f9f9; border: 1px solid #ddd; border-radius: 8px; }
.carrinho-lista { list-style: none; padding: 0; }
.carrinho-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #eee; }
.botao-remover { background: #ff5252; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 0.9rem; }
.botao-remover:hover { background: #d32f2f; }
.carrinho-total-container { display: flex; flex-direction: column; align-items: flex-end; margin-top: 1rem; }
.carrinho-total { font-size: 1.5rem; font-weight: bold; color: #2e7d32; }
.modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal { background: white; padding: 2.5rem; border-radius: 8px; width: 90%; max-width: 500px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); }
.modal h2 { margin-top: 0; color: #222; border-bottom: 2px solid #eee; padding-bottom: 10px; }
.resumo-lista { list-style: none; padding: 0; margin: 1.5rem 0; }
.resumo-item { padding: 8px 0; border-bottom: 1px dashed #ddd; display: flex; justify-content: space-between; }
.resumo-metricas { background: #f5f5f5; padding: 1rem; border-radius: 5px; margin-bottom: 1.5rem; }
.resumo-metricas p { margin: 5px 0; font-size: 1.1rem; }
.modal-botoes { display: flex; gap: 15px; justify-content: flex-end; }
.botao-confirmar { background: #2e7d32; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }
.botao-confirmar:hover { background: #1b5e20; }
.botao-fechar { background: #757575; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }
.botao-fechar:hover { background: #616161; }
.contato-secao { margin-top: 4rem; padding: 2rem; background: #fff; border: 1px solid #ddd; border-radius: 8px; max-width: 600px; margin-left: auto; margin-right: auto; }
.grupo-formulario { margin-bottom: 1.5rem; }
.grupo-formulario label { display: block; margin-bottom: 0.5rem; font-weight: bold; color: #444; }
.grupo-formulario input, .grupo-formulario textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 1rem; }
.grupo-formulario textarea { resize: vertical; height: 120px; }
.msg-erro { color: #d32f2f; font-size: 0.85rem; margin-top: 5px; display: block; font-weight: bold; }
.botao-enviar { background: #d32f2f; width: 100%; font-size: 1.1rem; }
.botao-enviar:hover { background: #b71c1c; }
footer { text-align: center; padding: 2rem; background: #222; color: white; margin-top: 3rem; }"""

arquivos_projeto['src/App.jsx'] = """import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Cardapio from './components/Cardapio';
import Carrinho from './components/Carrinho';
import Contato from './components/Contato';
import ModalResumo from './components/ModalResumo';
import './App.css';

function App() {
  const [carrinho, setCarrinho] = useState(() => {
    const salvo = localStorage.getItem('carrinho_pizzaria');
    return salvo ? JSON.parse(salvo) : [];
  });

  const [modalAberto, setModalAberto] = useState(false);

  useEffect(() => {
    localStorage.setItem('carrinho_pizzaria', JSON.stringify(carrinho));
  }, [carrinho]);

  const adicionarAoCarrinho = (nome, preco) => {
    const novoItem = {
      id: Date.now().toString(),
      nome: nome,
      preco: preco
    };
    setCarrinho([...carrinho, novoItem]);
  };

  const removerDoCarrinho = (id) => {
    setCarrinho(carrinho.filter(item => item.id !== id));
  };

  const confirmarPedido = () => {
    alert('Pedido confirmado com sucesso! Sua pizza já está sendo preparada.');
    setCarrinho([]);
    localStorage.removeItem('carrinho_pizzaria');
    setModalAberto(false);
  };

  return (
    <div className="App">
      <Header />
      <main className="conteudo-principal">
        <Cardapio onAdicionar={adicionarAoCarrinho} />
        <Carrinho 
          carrinho={carrinho} 
          onRemover={removerDoCarrinho} 
          onFinalizar={() => setModalAberto(true)} 
        />
        <Contato />
      </main>
      <footer className="rodape-principal">
        <p>&copy; 2026 <strong>Pizzaria Fatec Pompéia</strong>. Todos os direitos reservados.</p>
      </footer>
      {modalAberto && (
        <ModalResumo 
          carrinho={carrinho} 
          onFechar={() => setModalAberto(false)} 
          onConfirmar={confirmarPedido} 
        />
      )}
    </div>
  );
}

export default App;"""

# --- COMPONENTES FILHOS ---
arquivos_projeto['src/components/Header.jsx'] = """import React from 'react';

function Header() {
  return (
    <header className="cabecalho-principal">
      <div className="logo">
        <img src="https://placehold.co/150x50?text=Logo+Pizzaria" alt="Logotipo da Pizzaria Fatec" width="150" height="50" />
      </div>
      <nav className="menu">
        <ul>
          <li><a href="#inicio">Início</a></li>
          <li><a href="#cardapio">Cardápio</a></li>
          <li><a href="#carrinho">Carrinho</a></li>
          <li><a href="#contato">Contato</a></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;"""

arquivos_projeto['src/components/CartaoPizza.jsx'] = """import React from 'react';

function CartaoPizza({ imagem, nome, ingredientes, preco, onAdicionar }) {
  return (
    <article className="cartao-pizza">
      <img src={imagem} alt={`Pizza de ${nome}`} width="250" height="250" />
      <h2 className="sabor-nome">{nome}</h2>
      <p className="sabor-ingredientes">{ingredientes}</p>
      <p className="sabor-preco">R$ {preco.toFixed(2).replace('.', ',')}</p>
      <button className="botao-pedir" onClick={() => onAdicionar(nome, preco)}>
        Pedir Agora
      </button>
    </article>
  );
}

export default CartaoPizza;"""

arquivos_projeto['src/components/Cardapio.jsx'] = """import React from 'react';
import CartaoPizza from './CartaoPizza';

function Cardapio({ onAdicionar }) {
  const pizzas = [
    { id: 1, nome: "Calabresa Clássica", ingredientes: "Massa fina, molho de tomate artesanal, calabresa premium e cebola fatiada.", preco: 45.00, imagem: "https://placehold.co/250x250?text=Pizza+Calabresa" },
    { id: 2, nome: "Margherita Especial", ingredientes: "Mussarela fresca, fatias de tomate, manjericão orgânico e um fio de azeite extra virgem.", preco: 50.00, imagem: "https://placehold.co/250x250?text=Pizza+Margherita" },
    { id: 3, nome: "Frango com Catupiry", ingredientes: "Frango desfiado e temperado coberto com o legítimo e cremoso Catupiry.", preco: 55.00, imagem: "https://placehold.co/250x250?text=Pizza+Frango" }
  ];

  return (
    <section>
      <h1 id="cardapio" className="titulo-pagina">Nosso Cardápio Delicioso</h1>
      <div className="grade-de-pizzas">
        {pizzas.map(pizza => (
          <CartaoPizza key={pizza.id} {...pizza} onAdicionar={onAdicionar} />
        ))}
      </div>
    </section>
  );
}

export default Cardapio;"""

arquivos_projeto['src/components/Carrinho.jsx'] = """import React from 'react';

function Carrinho({ carrinho, onRemover, onFinalizar }) {
  const total = carrinho.reduce((soma, item) => soma + item.preco, 0);

  return (
    <section id="carrinho" className="carrinho-secao">
      <h2>Seu Carrinho</h2>
      <ul className="carrinho-lista">
        {carrinho.length === 0 ? (
          <li style={{ color: '#666' }}>Seu carrinho está vazio.</li>
        ) : (
          carrinho.map(item => (
            <li key={item.id} className="carrinho-item">
              <span><strong>{item.nome}</strong> - R$ {item.preco.toFixed(2).replace('.', ',')}</span>
              <button className="botao-remover" onClick={() => onRemover(item.id)}>Remover</button>
            </li>
          ))
        )}
      </ul>
      <div className="carrinho-total-container">
        <div className="carrinho-total">
          Total: R$ <span>{total.toFixed(2).replace('.', ',')}</span>
        </div>
        {carrinho.length > 0 && (
          <button className="botao-finalizar" onClick={onFinalizar}>Finalizar Pedido</button>
        )}
      </div>
    </section>
  );
}

export default Carrinho;"""

arquivos_projeto['src/components/ModalResumo.jsx'] = """import React from 'react';

function ModalResumo({ carrinho, onFechar, onConfirmar }) {
  const total = carrinho.reduce((soma, item) => soma + item.preco, 0);

  return (
    <div className="modal-overlay" style={{ display: 'flex' }}>
      <div className="modal">
        <h2>Resumo do Pedido</h2>
        <ul className="resumo-lista">
          {carrinho.map(item => (
            <li key={item.id} className="resumo-item">
              <span>{item.nome}</span> 
              <span>R$ {item.preco.toFixed(2).replace('.', ',')}</span>
            </li>
          ))}
        </ul>
        <div className="resumo-metricas">
          <p>Quantidade Total: <strong>{carrinho.length}</strong> itens</p>
          <p>Soma Final: <strong style={{ color: '#2e7d32' }}>R$ {total.toFixed(2).replace('.', ',')}</strong></p>
        </div>
        <div className="modal-botoes">
          <button className="botao-fechar" onClick={onFechar}>Fechar Modal</button>
          <button className="botao-confirmar" onClick={onConfirmar}>Confirmar</button>
        </div>
      </div>
    </div>
  );
}

export default ModalResumo;"""

arquivos_projeto['src/components/Contato.jsx'] = """import React, { useState } from 'react';

function Contato() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [mensagem, setMensagem] = useState('');

  const [erroNome, setErroNome] = useState('');
  const [erroEmail, setErroEmail] = useState('');
  const [erroMensagem, setErroMensagem] = useState('');

  const regexEmail = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;

  const handleSubmit = (evento) => {
    evento.preventDefault();
    let valido = true;

    if (nome.trim() === "") {
      setErroNome("O campo Nome é obrigatório.");
      valido = false;
    } else {
      setErroNome("");
    }

    if (email.trim() === "") {
      setErroEmail("O campo E-mail é obrigatório.");
      valido = false;
    } else if (!regexEmail.test(email.trim())) {
      setErroEmail("Por favor, insira um e-mail válido.");
      valido = false;
    } else {
      setErroEmail("");
    }

    if (mensagem.trim() === "") {
      setErroMensagem("O campo Mensagem é obrigatório.");
      valido = false;
    } else if (mensagem.trim().length < 10) {
      setErroMensagem("A mensagem deve conter no mínimo 10 caracteres.");
      valido = false;
    } else {
      setErroMensagem("");
    }

    if (valido) {
      alert("Mensagem enviada com sucesso! Entraremos em contato em breve.");
      setNome('');
      setEmail('');
      setMensagem('');
    }
  };

  return (
    <section id="contato" className="contato-secao">
      <h2>Fale Conosco</h2>
      <form onSubmit={handleSubmit} noValidate>
        <div className="grupo-formulario">
          <label htmlFor="nome">Nome Completo *</label>
          <input 
            type="text" 
            id="nome" 
            value={nome}
            onChange={(e) => { setNome(e.target.value); setErroNome(''); }}
            placeholder="Digite seu nome" 
          />
          <span className="msg-erro">{erroNome}</span>
        </div>

        <div className="grupo-formulario">
          <label htmlFor="email">E-mail *</label>
          <input 
            type="email" 
            id="email" 
            value={email}
            onChange={(e) => { setEmail(e.target.value); setErroEmail(''); }}
            placeholder="exemplo@email.com" 
          />
          <span className="msg-erro">{erroEmail}</span>
        </div>

        <div className="grupo-formulario">
          <label htmlFor="mensagem">Mensagem *</label>
          <textarea 
            id="mensagem" 
            value={mensagem}
            onChange={(e) => { setMensagem(e.target.value); setErroMensagem(''); }}
            placeholder="Deixe sua mensagem (mínimo de 10 caracteres)"
          ></textarea>
          <span className="msg-erro">{erroMensagem}</span>
        </div>

        <button type="submit" className="botao-enviar">Enviar Mensagem</button>
      </form>
    </section>
  );
}

export default Contato;"""

# 4. ESCRITA DOS ARQUIVOS EM DISCO
for caminho, conteudo in arquivos_projeto.items():
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo.strip())
    print(f"📝 Arquivo gerado: {caminho}")

print("\n📦 Instalandos pacotes e dependências com o npm. Aguarde...")

# 5. EXECUÇÃO DO NPM INSTALL VIA SUBPROCESS
try:
    subprocess.run(['npm', 'install'], check=True)
    print("\n✅ PROJETO RECONSTRUÍDO COM SUCESSO E SEM ERROS!")
    print("👉 Agora basta rodar no terminal: npm run dev")
except subprocess.CalledProcessError as err:
    print(f"\n❌ Erro durante a execução do npm install: {err}")