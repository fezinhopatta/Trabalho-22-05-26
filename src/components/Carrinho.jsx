import React from 'react';

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

export default Carrinho;