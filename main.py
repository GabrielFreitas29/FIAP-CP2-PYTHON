import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(PASTA_BASE)

LARGURA, ALTURA = 1920, 1080
width, height = LARGURA, ALTURA

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fiap Hero – Pink Floyd")
relogio = pygame.time.Clock()
FPS = 60

fundo_menu = pygame.image.load("assets/images/background-initial.png").convert()
fundo_menu = pygame.transform.smoothscale(fundo_menu, (width, height))

fundo_jogo = pygame.image.load("assets/images/black.png").convert()
fundo_jogo = pygame.transform.smoothscale(fundo_jogo, (width, height))


CAMINHO_MUSICA = "assets/audio/another_brick.mp3"
musica_ok = os.path.exists(CAMINHO_MUSICA)
if musica_ok:
    pygame.mixer.music.load(CAMINHO_MUSICA)
    pygame.mixer.music.set_volume(0.8)

CAMINHO_ERRO = "assets/audio/error.mp3"
som_erro = None
if os.path.exists(CAMINHO_ERRO):
    som_erro = pygame.mixer.Sound(CAMINHO_ERRO)
    som_erro.set_volume(0.6)

fonte_titulo = pygame.font.SysFont("Arial", 80, bold=True)
fonte_sub    = pygame.font.SysFont("Arial", 42, bold=True)
fonte_texto  = pygame.font.SysFont("Arial", 30)
fonte_hud    = pygame.font.SysFont("Arial", 36, bold=True)

BRANCO      = (255, 255, 255);  PRETO     = (0,   0,   0);   CINZA  = (60,  60,  60)
VERMELHO    = (220,  50,  50);  VERDE     = (50, 210,  80);   AZUL   = (50, 120, 230)
AMARELO     = (240, 220,  40);  ROXO      = (190,  60, 230);  LARANJA= (255, 150,   0)
VERMELHO_ESC= (100,   0,   0)

NUM_COLUNAS   = 4
TECLAS_COLUNA = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
LABELS_COLUNA = ["D", "F", "J", "K"]
CORES_COLUNA  = [VERMELHO, AZUL, AMARELO, ROXO]

LARGURA_COLUNA  = 150
ESPACO_COLUNA   = 30
INICIO_COLUNAS  = (LARGURA - (NUM_COLUNAS * LARGURA_COLUNA + (NUM_COLUNAS - 1) * ESPACO_COLUNA)) // 2

LARGURA_NOTA  = LARGURA_COLUNA - 16
ALTURA_NOTA   = 28
VELOCIDADE_NOTA = 4

ZONA_ACERTO_Y = ALTURA - 170
TOLERANCIA    = 55

TEMPO_VIAGEM = int((ZONA_ACERTO_Y + ALTURA_NOTA) / (VELOCIDADE_NOTA * FPS) * 1000)

VIDA_MAXIMA   = 100
VIDA_MISS     = 4
VIDA_ERRADA   = 1

def posicao_x_coluna(i):
    return INICIO_COLUNAS + i * (LARGURA_COLUNA + ESPACO_COLUNA)

BPM      = 99
BEAT     = 60000 / BPM
COMPASSO = BEAT * 4

def _ms(compasso, batida=0.0):
    return int(compasso * COMPASSO + batida * BEAT)

MAPA_NOTAS = []

def _nota(comp, batida, coluna):
    MAPA_NOTAS.append((_ms(comp, batida), coluna))

for b in range(6):
    _nota(b, 0.0, 0); _nota(b, 1.0, 1)
    _nota(b, 2.0, 0); _nota(b, 3.0, 1)

for b in range(6, 18):
    _nota(b, 0.0, 0); _nota(b, 1.0, 1)
    _nota(b, 2.0, 0); _nota(b, 3.0, 1)
    if b % 2 == 0:
        _nota(b, 0.0, 3); _nota(b, 2.0, 2)
    else:
        _nota(b, 1.0, 3); _nota(b, 3.0, 2)

for b in range(18, 30):
    _nota(b, 0.0, 0); _nota(b, 1.0, 1)
    _nota(b, 2.0, 0); _nota(b, 3.0, 1)
    p = b % 4
    if p == 0:
        _nota(b, 0.0, 3); _nota(b, 2.0, 2); _nota(b, 3.0, 3)
    elif p == 1:
        _nota(b, 1.0, 3); _nota(b, 3.0, 2)
    elif p == 2:
        _nota(b, 0.5, 3); _nota(b, 2.0, 3); _nota(b, 3.5, 2)
    else:
        _nota(b, 0.0, 2); _nota(b, 1.5, 3); _nota(b, 3.0, 3)

for b in range(30, 42):
    _nota(b, 0.0, 0); _nota(b, 0.5, 3)
    _nota(b, 1.0, 1); _nota(b, 1.5, 2)
    _nota(b, 2.0, 0); _nota(b, 2.5, 3)
    _nota(b, 3.0, 1); _nota(b, 3.5, 2)

_pares = [(2,3),(3,2),(1,2),(3,2),(0,3),(2,3),(1,3),(2,1)]
for b in range(42, 54):
    grupo = _pares[(b % 4) * 2:(b % 4) * 2 + 4] if (b % 4) * 2 + 4 <= len(_pares) else _pares[:4]
    for i, (c1, c2) in enumerate(grupo):
        _nota(b, i * 1.0,       c1)
        _nota(b, i * 1.0 + 0.5, c2)

for b in range(54, 63):
    _nota(b, 0.0, 0); _nota(b, 1.0, 1)
    _nota(b, 2.0, 0); _nota(b, 3.0, 1)
    if b % 2 == 0:
        _nota(b, 2.0, 3)

MAPA_NOTAS.sort()
DURACAO_MUSICA = _ms(63)


class Nota:
    def __init__(self, coluna):
        self.coluna  = coluna
        self.x       = posicao_x_coluna(coluna) + 8
        self.y       = -ALTURA_NOTA
        self.cor     = CORES_COLUNA[coluna]
        self.acertou = False
        self.perdeu  = False

    def atualizar(self):
        self.y += VELOCIDADE_NOTA

    def desenhar(self, superficie):
        if self.acertou or self.perdeu:
            return
        pygame.draw.rect(superficie, self.cor,
                         (self.x, self.y, LARGURA_NOTA, ALTURA_NOTA), border_radius=7)
        pygame.draw.rect(superficie, BRANCO,
                         (self.x + 4, self.y + 3, LARGURA_NOTA - 8, 5), border_radius=3)
        pygame.draw.rect(superficie, BRANCO,
                         (self.x, self.y, LARGURA_NOTA, ALTURA_NOTA), 2, border_radius=7)

    def pode_ser_acertada(self):
        return abs(self.y - ZONA_ACERTO_Y) < TOLERANCIA

    def saiu_da_tela(self):
        return self.y > ZONA_ACERTO_Y + TOLERANCIA + ALTURA_NOTA


class TextoFeedback:
    def __init__(self, texto, cor, cx, y):
        self.texto = texto
        self.cor   = cor
        self.cx    = cx
        self.y     = float(y)
        self.vida  = 45

    def atualizar(self):
        self.vida -= 1
        self.y    -= 1.6

    def desenhar(self, superficie):
        surf = fonte_sub.render(self.texto, True, self.cor)
        surf.set_alpha(max(0, int(255 * self.vida / 45)))
        superficie.blit(surf, (self.cx - surf.get_width() // 2, int(self.y)))

    def morreu(self):
        return self.vida <= 0


class Jogo:
    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.notas          = []
        self.feedbacks      = []
        self.pontuacao      = 0
        self.combo          = 0
        self.melhor_combo   = 0
        self.vida           = VIDA_MAXIMA
        self.fim_de_jogo    = False
        self.vitoria        = False
        self.pausado        = False
        self.tecla_pressionada = [False] * NUM_COLUNAS
        self.indice_mapa    = 0
        self._inicio        = 0
        self._tempo_pausado = 0
        self._pausado_em    = 0

    def iniciar(self):
        self._inicio        = pygame.time.get_ticks()
        self._tempo_pausado = 0
        if musica_ok:
            pygame.mixer.music.play()

    def tempo_musica(self):
        if self.pausado:
            return self._pausado_em - self._inicio - self._tempo_pausado
        return pygame.time.get_ticks() - self._inicio - self._tempo_pausado

    def pausar(self):
        self._pausado_em = pygame.time.get_ticks()
        self.pausado = True
        if musica_ok:
            pygame.mixer.music.pause()

    def despausar(self):
        self._tempo_pausado += pygame.time.get_ticks() - self._pausado_em
        self.pausado = False
        if musica_ok:
            pygame.mixer.music.unpause()

    def tecla_pressionou(self, tecla):
        for i, t in enumerate(TECLAS_COLUNA):
            if tecla == t:
                self.tecla_pressionada[i] = True
                self._tentar_acertar(i)
                return

    def tecla_soltou(self, tecla):
        for i, t in enumerate(TECLAS_COLUNA):
            if tecla == t:
                self.tecla_pressionada[i] = False

    def _tocar_erro(self):
        if som_erro:
            som_erro.play()

    def _tentar_acertar(self, coluna):
        melhor = None
        for nota in self.notas:
            if nota.coluna == coluna and not nota.acertou and not nota.perdeu:
                if nota.pode_ser_acertada():
                    if melhor is None or nota.y > melhor.y:
                        melhor = nota

        cx = posicao_x_coluna(coluna) + LARGURA_COLUNA // 2

        if melhor:
            melhor.acertou = True
            distancia = abs(melhor.y - ZONA_ACERTO_Y)
            if distancia < 12:
                pts, txt, cor = 300, "PERFEITO!", AMARELO
            elif distancia < 30:
                pts, txt, cor = 150, "ÓTIMO!",    VERDE
            else:
                pts, txt, cor =  50, "OK",         BRANCO
            self.combo       += 1
            self.melhor_combo = max(self.melhor_combo, self.combo)
            multiplicador     = 1 + self.combo // 10
            self.pontuacao   += pts * multiplicador
            self.feedbacks.append(TextoFeedback(txt, cor, cx, ZONA_ACERTO_Y - 70))
        else:
            self.combo = 0
            self.vida  = max(0, self.vida - VIDA_ERRADA)
            self._tocar_erro()
            self.feedbacks.append(TextoFeedback("MISS", VERMELHO, cx, ZONA_ACERTO_Y - 70))

    def atualizar(self):
        if self.fim_de_jogo or self.vitoria or self.pausado:
            return

        agora = self.tempo_musica()

        while self.indice_mapa < len(MAPA_NOTAS):
            tempo_nota, coluna = MAPA_NOTAS[self.indice_mapa]
            if agora >= tempo_nota - TEMPO_VIAGEM:
                self.notas.append(Nota(coluna))
                self.indice_mapa += 1
            else:
                break

        if self.indice_mapa >= len(MAPA_NOTAS) and not self.notas:
            if agora >= DURACAO_MUSICA:
                self.vitoria = True
                if musica_ok:
                    pygame.mixer.music.stop()
                return

        for nota in self.notas:
            nota.atualizar()
            if not nota.acertou and not nota.perdeu and nota.saiu_da_tela():
                nota.perdeu  = True
                self.combo   = 0
                self.vida    = max(0, self.vida - VIDA_MISS)
                self._tocar_erro()
                cx = posicao_x_coluna(nota.coluna) + LARGURA_COLUNA // 2
                self.feedbacks.append(TextoFeedback("MISS", VERMELHO, cx, ZONA_ACERTO_Y - 70))

        self.notas     = [n for n in self.notas if n.y < ALTURA + 60]
        self.feedbacks = [fb for fb in self.feedbacks if not fb.morreu()]
        for fb in self.feedbacks:
            fb.atualizar()

        if self.vida <= 0:
            self.vida       = 0
            self.fim_de_jogo = True
            if musica_ok:
                pygame.mixer.music.stop()

    def desenhar(self, superficie):
        superficie.blit(fundo_jogo, (0, 0))
        self._desenhar_colunas(superficie)
        for nota in self.notas:
            nota.desenhar(superficie)
        for fb in self.feedbacks:
            fb.desenhar(superficie)
        self._desenhar_hud(superficie)
        if self.pausado:
            self._desenhar_pause(superficie)
        if self.fim_de_jogo:
            self._desenhar_fim_de_jogo(superficie)
        if self.vitoria:
            self._desenhar_vitoria(superficie)

    def _desenhar_colunas(self, superficie):
        for i in range(NUM_COLUNAS):
            x = posicao_x_coluna(i)
            pygame.draw.rect(superficie, (18, 18, 18), (x, 0, LARGURA_COLUNA, ALTURA))
            pygame.draw.rect(superficie, (45, 45, 45), (x, 0, LARGURA_COLUNA, ALTURA), 1)
            if self.tecla_pressionada[i]:
                brilho = pygame.Surface((LARGURA_COLUNA, ALTURA), pygame.SRCALPHA)
                brilho.fill((*CORES_COLUNA[i], 30))
                superficie.blit(brilho, (x, 0))
            cor_zona = BRANCO if self.tecla_pressionada[i] else CORES_COLUNA[i]
            pygame.draw.rect(superficie, cor_zona,
                             (x, ZONA_ACERTO_Y, LARGURA_COLUNA, 18), border_radius=6)
            pygame.draw.ellipse(superficie, (30, 30, 30),
                                (x + 10, ZONA_ACERTO_Y + 22, LARGURA_COLUNA - 20, 38))
            pygame.draw.ellipse(superficie, CORES_COLUNA[i],
                                (x + 10, ZONA_ACERTO_Y + 22, LARGURA_COLUNA - 20, 38), 3)
            label = fonte_sub.render(LABELS_COLUNA[i], True, CORES_COLUNA[i])
            superficie.blit(label, (x + LARGURA_COLUNA // 2 - label.get_width() // 2,
                                    ZONA_ACERTO_Y + 30))

    def _desenhar_hud(self, superficie):
        agora = self.tempo_musica()

        pts = fonte_hud.render(f"Pontuação: {self.pontuacao:,}", True, BRANCO)
        superficie.blit(pts, (40, 30))

        if self.combo >= 2:
            cor_combo = LARANJA if self.combo < 20 else AMARELO
            cb = fonte_hud.render(f"Combo  x{self.combo}", True, cor_combo)
            superficie.blit(cb, (40, 78))

        bw, bh = 320, 28
        bx = LARGURA - bw - 40
        by = 30
        pygame.draw.rect(superficie, VERMELHO_ESC, (bx, by, bw, bh), border_radius=8)
        hw = int(bw * self.vida / VIDA_MAXIMA)
        cor_vida = VERDE if self.vida > VIDA_MAXIMA * 0.5 else AMARELO if self.vida > VIDA_MAXIMA * 0.25 else VERMELHO
        pygame.draw.rect(superficie, cor_vida, (bx, by, hw, bh), border_radius=8)
        pygame.draw.rect(superficie, BRANCO, (bx, by, bw, bh), 2, border_radius=8)
        label_vida = fonte_texto.render("VIDA", True, BRANCO)
        superficie.blit(label_vida, (bx - 55, by + 4))

        progresso  = min(1.0, agora / DURACAO_MUSICA)
        pw, ph = 500, 10
        px = LARGURA // 2 - pw // 2
        py = ALTURA - 50
        pygame.draw.rect(superficie, CINZA,  (px, py, pw, ph), border_radius=5)
        pygame.draw.rect(superficie, ROXO,   (px, py, int(pw * progresso), ph), border_radius=5)
        pygame.draw.rect(superficie, BRANCO, (px, py, pw, ph), 1, border_radius=5)

        nome_musica = fonte_texto.render(
            "   ", True, CINZA)
        superficie.blit(nome_musica, (LARGURA // 2 - nome_musica.get_width() // 2, ALTURA - 80))

        segundos  = max(0, agora // 1000)
        tempo_lbl = fonte_texto.render(f"{segundos//60}:{segundos%60:02d}", True, CINZA)
        superficie.blit(tempo_lbl, (px + pw + 12, py - 5))

        dica = fonte_texto.render("P – Pausar   |   ESC – Menu", True, CINZA)
        superficie.blit(dica, (LARGURA // 5 - dica.get_width() // 2, ALTURA - 45))

    def _desenhar_pause(self, superficie):
        ov = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 175))
        superficie.blit(ov, (0, 0))
        t = fonte_titulo.render("PAUSADO", True, BRANCO)
        h = fonte_texto.render("Pressione P para continuar", True, CINZA)
        cx = LARGURA // 2
        superficie.blit(t, (cx - t.get_width() // 2, ALTURA // 2 - 60))
        superficie.blit(h, (cx - h.get_width() // 2, ALTURA // 2 + 30))

    def _desenhar_fim_de_jogo(self, superficie):
        ov = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 185))
        superficie.blit(ov, (0, 0))
        go   = fonte_titulo.render("GAME  OVER", True, VERMELHO)
        pts  = fonte_sub.render(f"Pontuação: {self.pontuacao:,}", True, BRANCO)
        cb   = fonte_sub.render(f"Melhor Combo: x{self.melhor_combo}", True, AMARELO)
        dica = fonte_texto.render("R - Reiniciar   |   ESC - Menu", True, CINZA)
        cx   = LARGURA // 2
        superficie.blit(go,   (cx - go.get_width() // 2,   ALTURA // 2 - 140))
        superficie.blit(pts,  (cx - pts.get_width() // 2,  ALTURA // 2 -  40))
        superficie.blit(cb,   (cx - cb.get_width() // 2,   ALTURA // 2 +  20))
        superficie.blit(dica, (cx - dica.get_width() // 2, ALTURA // 2 + 100))

    def _desenhar_vitoria(self, superficie):
        ov = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 185))
        superficie.blit(ov, (0, 0))
        v    = fonte_titulo.render("VOCÊ PASSOU!", True, AMARELO)
        pts  = fonte_sub.render(f"Pontuação Final: {self.pontuacao:,}", True, BRANCO)
        cb   = fonte_sub.render(f"Melhor Combo: x{self.melhor_combo}", True, VERDE)
        msg  = fonte_texto.render("Música completada – Pink Floyd aprovaria.", True, CINZA)
        dica = fonte_texto.render("R - Jogar novamente   |   ESC - Menu", True, CINZA)
        cx   = LARGURA // 2
        superficie.blit(v,    (cx - v.get_width() // 2,    ALTURA // 2 - 140))
        superficie.blit(pts,  (cx - pts.get_width() // 2,  ALTURA // 2 -  45))
        superficie.blit(cb,   (cx - cb.get_width() // 2,   ALTURA // 2 +  20))
        superficie.blit(msg,  (cx - msg.get_width() // 2,  ALTURA // 2 +  80))
        superficie.blit(dica, (cx - dica.get_width() // 2, ALTURA // 2 + 130))


def desenhar_menu(superficie):
    superficie.blit(fundo_menu, (0, 0))
    ov = pygame.Surface((LARGURA, 360), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 185))
    superficie.blit(ov, (0, ALTURA - 360))

    cx = LARGURA // 2
    itens = [
        (fonte_sub,    "Pressione ENTER para jogar",                  AMARELO, ALTURA - 235),
        (fonte_texto,  "Teclas:   D   F   J   K",                     BRANCO,  ALTURA - 170),
        (fonte_texto,  "- Another Brick in the Wall - Pink Floyd",    CINZA,   ALTURA - 125),
        (fonte_texto,  "Acerte as notas na hora certa para pontuar!", CINZA,   ALTURA - 88),
    ]
    for fonte, texto, cor, y in itens:
        s = fonte.render(texto, True, cor)
        superficie.blit(s, (cx - s.get_width() // 2, y))

    if not musica_ok:
        aviso = fonte_texto.render(
            "Coloque 'another_brick.mp3' em assets/audio/ para ativar a música",
            True, LARANJA)
        superficie.blit(aviso, (cx - aviso.get_width() // 2, ALTURA - 50))


estado_jogo = "menu"
jogo = Jogo()
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:

            if estado_jogo == "menu":
                if evento.key == pygame.K_RETURN:
                    jogo.reiniciar()
                    jogo.iniciar()
                    estado_jogo = "jogo"

            elif estado_jogo == "jogo":
                if evento.key == pygame.K_ESCAPE:
                    if musica_ok:
                        pygame.mixer.music.stop()
                    estado_jogo = "menu"

                elif evento.key == pygame.K_p:
                    if not jogo.fim_de_jogo and not jogo.vitoria:
                        if jogo.pausado:
                            jogo.despausar()
                        else:
                            jogo.pausar()

                elif evento.key == pygame.K_r:
                    if jogo.fim_de_jogo or jogo.vitoria:
                        jogo.reiniciar()
                        jogo.iniciar()

                else:
                    jogo.tecla_pressionou(evento.key)

        if evento.type == pygame.KEYUP:
            if estado_jogo == "jogo":
                jogo.tecla_soltou(evento.key)

    if estado_jogo == "jogo":
        jogo.atualizar()

    if estado_jogo == "menu":
        desenhar_menu(tela)
    elif estado_jogo == "jogo":
        jogo.desenhar(tela)

    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
sys.exit()
