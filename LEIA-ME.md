# 🎮 Jogo do Galo Acessível – Instruções

## Ficheiros incluídos

| Ficheiro | Descrição |
|---|---|
| `jogo_do_galo_acessivel.html` | Jogo completo (standalone ou com servidor) |
| `server_tts.py` | Servidor Python com voz Microsoft Neural (edge-tts) |

---

## Opção A – Abrir diretamente no Microsoft Edge (sem instalação)

1. Abre o ficheiro `jogo_do_galo_acessivel.html` no **Microsoft Edge**
2. O jogo usa automaticamente a **voz Microsoft Fernanda Neural** disponível no Edge
3. O badge de voz mostrará **"Web"**

> ✅ Funciona imediatamente, sem instalar nada.

---

## Opção B – Com servidor Python (voz neural de máxima qualidade)

### Instalação (uma vez)

```bash
pip install flask edge-tts
```

### Execução

```bash
python server_tts.py
```

- O browser abre automaticamente em `http://localhost:5050`
- O badge de voz mostrará **"Neural"** (edge-tts ativo)
- Voz padrão: **Microsoft Fernanda Neural (pt-PT)**

### Vozes disponíveis (PT-PT)

| Nome | Género | Qualidade |
|---|---|---|
| pt-PT-FernandaNeural | Feminino | ⭐⭐⭐ (padrão) |
| pt-PT-RaquelNeural | Feminino | ⭐⭐⭐ |
| pt-PT-DuarteNeural | Masculino | ⭐⭐⭐ |

---

## Funcionalidades de Acessibilidade

- 🔊 **Síntese de voz** – lê cada jogada, resultado e navegação
- ⌨️ **Teclado completo** – setas + Enter, sem rato
- 📢 **ARIA live regions** – compatível com NVDA, JAWS, Narrator
- 🎵 **Feedback sonoro** – tons distintos para X e O, vitória, erro
- 🔁 **Botão Repetir** – relê o estado atual
- 🤖 **Modo CPU** – adversário automático (Minimax inderrotável)

## Atalhos de Teclado

| Tecla | Ação |
|---|---|
| ↑ ↓ ← → | Navegar no tabuleiro |
| Enter / Espaço | Jogar na casa selecionada |
| R | Nova partida |
| V | Ligar/desligar voz |
| Tab | Navegar nos botões |
