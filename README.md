# 🎸 Fiap Hero – Pink Floyd

Projeto desenvolvido em Python utilizando a biblioteca Pygame, inspirado em jogos de ritmo como Guitar Hero.  
O jogador deve acertar as notas no tempo correto utilizando as teclas do teclado enquanto a música toca ao fundo.

---

## 📌 Sobre o Projeto

O **Fiap Hero – Pink Floyd** é um jogo musical em 2D onde as notas descem pelas colunas e o jogador precisa pressionar as teclas correspondentes no momento exato para ganhar pontos e manter o combo.

A música utilizada no projeto é:

🎵 *Another Brick in the Wall – Pink Floyd*

---

# 🖥️ Tecnologias Utilizadas

- Python 3
- Pygame

---

# 📂 Estrutura do Projeto

```bash
FIAP-HERO/
│
├── assets/
│   ├── audio/
│   │   ├── another_brick.mp3
│   │   └── error.mp3
│   │
│   └── images/
│       ├── background-initial.png
│       └── black.png
│
├── main.py
```

---

# ⚙️ Requisitos para Rodar o Projeto

Antes de executar o jogo, é necessário ter instalado:

- Python 3.11
- Biblioteca Pygame

---

# 📥 Instalação

## 1️⃣ Clonar o repositório

---

# 🎮 Controles do Jogo

| Tecla | Função |
|------|------|
| D | Nota Vermelha |
| F | Nota Azul |
| J | Nota Amarela |
| K | Nota Roxa |
| ENTER | Iniciar jogo |
| P | Pausar |
| R | Reiniciar |
| ESC | Voltar ao menu |  

---

# 🏆 Sistema de Pontuação

| Resultado | Pontos |
|----------|--------|
| PERFEITO | 300 |
| ÓTIMO | 150 |
| OK | 50 |
| MISS | 0 |

O jogo também possui multiplicador de combo:

```python
multiplicador = 1 + combo // 10
```

Quanto maior o combo, maior a pontuação.

---

# 👨‍💻 Integrantes

| RM | Nome |
|----|------|
| 570881 | Gabriel Freitas da Silva Carvalho |
| 572892 | Erick Martins Picolo |
| 572171 | Guilherme Marcon Dantas |
| 569782 | Luiz Felipe Cardoso de Oliveira |

---

# 🎸 “Pink Floyd daria nota máxima.”

```
