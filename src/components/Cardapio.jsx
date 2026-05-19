import React from 'react';
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

export default Cardapio;