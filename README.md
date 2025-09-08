# Precificador de Imóveis IA

Sistema web para precificação de imóveis em Jacareí utilizando inteligência artificial 

## Tutorial rápido: rodando o projeto pelo terminal do VS Code

Copie e cole os comandos abaixo, um por um, no terminal do VS Code:

```sh
git clone https://github.com/Alvasync/ProjetoIntegrador1.git
cd ProjetoIntegrador1
python -m venv venv
venv\Scripts\activate   # (Windows)
# ou
source venv/bin/activate  # (Linux/Mac)
pip install -r requirements.txt
python app.py
```

Acesse no navegador:
```
http://localhost:5000
```

---

## Funcionalidades

- Precificação automática de imóveis (casas, terrenos, apartamentos, comercial)
- Sistema de login e cadastro
- Visualização de diferentes tipos de imóveis
- Tema claro/escuro
- Interface responsiva e moderna

## Tecnologias Utilizadas

- Python/Flask
- SQLite
- HTML5/CSS3
- JavaScript
- Flask-SQLAlchemy
- Flask-Bcrypt

## Estrutura do Projeto

```
precificador_imoveis_ia/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   └── index.html
├── app.py
├── README.md
└── requirements.txt
```

## Contribuindo

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/NomeDaFeature`)
3. Commit suas mudanças (`git commit -m 'Descrição da feature'`)
4. Push para a Branch (`git push origin feature/NomeDaFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 