import React, { useState, useEffect } from 'react';
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

export default App;