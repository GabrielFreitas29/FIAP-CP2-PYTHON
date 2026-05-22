# 🎸 Fiap Hero – Pink Floyd

Projeto desenvolvido em Python utilizando a biblioteca Pygame, inspirado em jogos de ritmo como Guitar Hero.  
O jogador deve acertar as notas no tempo correto utilizando as teclas do teclado enquanto a música toca ao fundo.

---

## 📌 Sobre o Projeto

O **Fiap Hero – Pink Floyd** é um jogo musical em 2D onde as notas descem pelas colunas e o jogador precisa pressionar as teclas correspondentes no momento exato para ganhar pontos e manter o combo.

A música utilizada no projeto é:

🎵 *Another Brick in the Wall – Pink Floyd*

O projeto foi desenvolvido com foco em:
- Programação orientada a objetos
- Manipulação de áudio
- Renderização gráfica em tempo real
- Controle de eventos do teclado
- Lógica de timing e pontuação

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
└── README.md
```

---

# ⚙️ Requisitos para Rodar o Projeto

Antes de executar o jogo, é necessário ter instalado:

- Python 3.10 ou superior
- Biblioteca Pygame

---

# 📥 Instalação

## 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-repositorio/fiap-hero.git
```

---

## 2️⃣ Entrar na pasta do projeto

```bash
cd fiap-hero
```

---

## 3️⃣ Instalar o Pygame

```bash
pip install pygame
```

---

# ▶️ Como Executar

Execute o arquivo principal:

```bash
python main.py
```

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

# 🧠 Funcionalidades

✅ Sistema de notas sincronizadas com a música  
✅ Sistema de combo  
✅ Sistema de pontuação  
✅ Barra de vida  
✅ Feedback visual:
- PERFECT
- ÓTIMO
- OK
- MISS

✅ Tela de pausa  
✅ Tela de vitória  
✅ Tela de game over  
✅ Efeitos sonoros  
✅ Interface gráfica estilizada  

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

# 🧱 Estrutura do Código

O projeto foi dividido em classes principais:

## `Nota`
Responsável pelas notas que descem pela tela.

## `TextoFeedback`
Responsável pelos textos animados de feedback.

## `Jogo`
Controla:
- lógica do jogo
- pontuação
- vida
- combos
- pausa
- spawn das notas
- vitória e derrota

---

# 🎵 Sistema Musical

O mapa de notas foi criado manualmente utilizando:
- BPM da música
- Compassos
- Batidas

```python
BPM = 99
BEAT = 60000 / BPM
COMPASSO = BEAT * 4
```

As notas são sincronizadas usando milissegundos.

---

# 📸 Interface

O jogo possui:
- menu inicial
- HUD em tempo real
- barra de progresso da música
- barra de vida
- efeitos de brilho nas colunas
- feedback visual animado

---

# 🚀 Melhorias Futuras

- Adicionar novas músicas
- Sistema de ranking
- Seleção de dificuldade
- Sistema de recordes
- Mais efeitos visuais
- Menu de configurações
- Suporte para controles

---

# 👨‍💻 Integrantes

| RM | Nome |
|----|------|
| 570881 | Gabriel Freitas da Silva Carvalho |
| 572892 | Erick Martins Picolo |
| 572171 | Guilherme Marcon Dantas |
| 569782 | Luiz Felipe Cardoso de Oliveira |

---

# 📚 Disciplina

Projeto acadêmico desenvolvido para fins educacionais utilizando Python e Pygame.

---

# 🎸 “Pink Floyd aprovaria.”

```
