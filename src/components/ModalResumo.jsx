import React from 'react';

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

export default ModalResumo;