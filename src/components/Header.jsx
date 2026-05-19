import React from 'react';

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

export default Header;