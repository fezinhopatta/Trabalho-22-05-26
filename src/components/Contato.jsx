import React, { useState } from 'react';

function Contato() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [mensagem, setMensagem] = useState('');

  const [erroNome, setErroNome] = useState('');
  const [erroEmail, setErroEmail] = useState('');
  const [erroMensagem, setErroMensagem] = useState('');

  const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

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

export default Contato;