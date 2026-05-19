import React from 'react';

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

export default CartaoPizza;