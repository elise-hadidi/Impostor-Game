import streamlit as st
import random

# ── WORD BANK (secret word, impostor hint) ────────────────────────────────────
WORD_PAIRS = [
    ("Sushi", "Rice"),
    ("Volcano", "Mountain"),
    ("Ballet", "Dance"),
    ("Submarine", "Boat"),
    ("Cactus", "Plant"),
    ("Hammock", "Bed"),
    ("Glacier", "Ice"),
    ("Barbecue", "Grill"),
    ("Telescope", "Binoculars"),
    ("Quicksand", "Sand"),
    ("Chandelier", "Lamp"),
    ("Avalanche", "Snow"),
    ("Trampoline", "Mattress"),
    ("Escalator", "Stairs"),
    ("Flamingo", "Bird"),
    ("Sauna", "Shower"),
    ("Igloo", "House"),
    ("Lasso", "Rope"),
    ("Parachute", "Umbrella"),
    ("Surfboard", "Skateboard"),
    ("Campfire", "Fireplace"),
    ("Compass", "Map"),
    ("Treadmill", "Track"),
    ("Fondue", "Soup"),
    ("Kayak", "Canoe"),
    ("Bonsai", "Tree"),
    ("Sundial", "Clock"),
    ("Zipline", "Slide"),
    ("Pinata", "Balloon"),
    ("Lighthouse", "Tower"),
    ("Quicksand", "Beach"),
    ("Hammock", "Swing"),
    ("Treehouse", "Cabin"),
    ("Stapler", "Tape"),
    ("Escalator", "Elevator"),
]

st.set_page_config(page_title="IMPOSTOR", layout="centered")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Share+Tech+Mono&family=Outfit:wght@300;400;600&display=swap');

:root {
    --bg: #080a0e;
    --surface: #0f1318;
    --card: #141820;
    --border: #1e2530;
    --red: #e8334a;
    --red-glow: rgba(232,51,74,0.35);
    --green: #00e5a0;
    --green-glow: rgba(0,229,160,0.25);
    --amber: #f5a623;
    --text: #d0d8e8;
    --muted: #4a5568;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
}
.stApp { background: var(--bg) !important; }
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.07) 2px, rgba(0,0,0,0.07) 4px);
    pointer-events: none; z-index: 999;
}
#MainMenu, footer, header { visibility: hidden; }

.stTextInput input, .stNumberInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
    color: var(--text) !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stTextInput input:focus {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 2px rgba(232,51,74,0.15) !important;
}
div.stButton > button {
    width: 100%;
    background: var(--red) !important;
    color: white !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.4rem !important;
    letter-spacing: 0.12em !important;
    padding: 0.7rem !important;
    box-shadow: 0 0 20px var(--red-glow) !important;
}
div.stButton > button:hover {
    box-shadow: 0 0 35px var(--red-glow) !important;
    transform: translateY(-1px) !important;
}
.stAlert { border-radius: 3px !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "screen": "players",
        "players": [],
        "word": "",
        "impostor_hint": "",
        "num_impostors": 1,
        "impostor_indices": [],
        "current_idx": 0,
        "show_word": False,
        "first_player": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def go(screen):
    st.session_state.screen = screen
    st.session_state.show_word = False
    st.rerun()

def logo():
    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 0.5rem;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:clamp(3rem,10vw,6rem);
                    letter-spacing:0.15em;color:#e8334a;
                    text-shadow:0 0 40px rgba(232,51,74,0.35),0 0 80px rgba(232,51,74,0.15);
                    line-height:1;">IMPOSTOR</div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;
                    color:#4a5568;letter-spacing:0.3em;">// classified party game //</div>
    </div>
    <hr style="border:none;border-top:1px solid #1e2530;margin:1.5rem 0;">
    """, unsafe_allow_html=True)

def mono(text, color="#4a5568", size="0.7rem"):
    st.markdown(f"""<div style="font-family:'Share Tech Mono',monospace;font-size:{size};
                color:{color};letter-spacing:0.2em;text-transform:uppercase;
                margin-bottom:0.5rem;">{text}</div>""", unsafe_allow_html=True)

def big_title(text, color="#d0d8e8"):
    st.markdown(f"""<div style="font-family:'Bebas Neue',sans-serif;font-size:clamp(2rem,8vw,4rem);
                letter-spacing:0.12em;color:{color};text-align:center;margin-bottom:0.5rem;">
                {text}</div>""", unsafe_allow_html=True)

def divider():
    st.markdown("<hr style='border:none;border-top:1px solid #1e2530;margin:1.2rem 0;'>", unsafe_allow_html=True)

def show_error(text):
    st.markdown(f"<div style='color:#e8334a;font-family:Share Tech Mono,monospace;font-size:0.8rem;margin-top:0.3rem;'>{text}</div>", unsafe_allow_html=True)

# ── SCREEN 1: ENTER PLAYERS ───────────────────────────────────────────────────
if st.session_state.screen == "players":
    logo()
    big_title("WHO'S PLAYING?")
    divider()

    mono("// type a name and press enter //")
    new_player = st.text_input("Player name", placeholder="e.g. Sarah",
                               label_visibility="collapsed", key="player_input")
    if new_player and new_player.strip() and new_player.strip() not in st.session_state.players:
        st.session_state.players.append(new_player.strip())
        st.rerun()

    if st.session_state.players:
        mono(f"// {len(st.session_state.players)} players //", color="#d0d8e8", size="0.75rem")
        cols_per_row = 4
        players = st.session_state.players
        for row_start in range(0, len(players), cols_per_row):
            row = players[row_start:row_start + cols_per_row]
            cols = st.columns(len(row))
            for i, p in enumerate(row):
                with cols[i]:
                    st.markdown(f"""<div style="background:#0f1318;border:1px solid #1e2530;
                                border-radius:3px;padding:0.4rem 0.6rem;
                                font-family:'Share Tech Mono',monospace;font-size:0.78rem;
                                text-align:center;margin-bottom:0.2rem;">{p}</div>""",
                                unsafe_allow_html=True)
                    if st.button("✕", key=f"rm_{p}_{row_start+i}"):
                        st.session_state.players.remove(p)
                        st.rerun()

    divider()
    if st.button("NEXT →", key="to_setup"):
        if len(st.session_state.players) < 3:
            show_error("⚠ Add at least 3 players to continue")
        else:
            go("setup")

# ── SCREEN 2: SETUP ───────────────────────────────────────────────────────────
elif st.session_state.screen == "setup":
    logo()
    big_title("GAME SETUP")
    divider()

    mono("// secret word //")
    if st.session_state.word:
        st.markdown("""<div style="background:#0f1318;border:1px solid #00e5a0;border-radius:3px;
                    padding:1rem 1.5rem;text-align:center;margin-bottom:0.8rem;
                    box-shadow:0 0 15px rgba(0,229,160,0.08);">
            <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#4a5568;
                        letter-spacing:0.2em;margin-bottom:0.4rem;">WORD READY</div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;letter-spacing:0.1em;
                        color:#00e5a0;">✓ ready to play</div>
        </div>""", unsafe_allow_html=True)
    if st.button("🎲  GENERATE RANDOM WORD", key="gen_word"):
        pair = random.choice(WORD_PAIRS)
        st.session_state.word = pair[0]
        st.session_state.impostor_hint = pair[1]
        st.rerun()

    divider()

    mono("// number of impostors //")
    st.session_state.num_impostors = st.number_input("Number of impostors",
        min_value=1, max_value=max(1, len(st.session_state.players) // 2),
        value=st.session_state.num_impostors, label_visibility="collapsed", key="num_imp")

    divider()

    if st.button("START →", key="start_game"):
        if not st.session_state.word.strip():
            show_error("⚠ Generate a secret word first")
        else:
            n = int(st.session_state.num_impostors)
            st.session_state.impostor_indices = random.sample(range(len(st.session_state.players)), n)
            st.session_state.current_idx = 0
            st.session_state.first_player = None
            go("cover")

    if st.button("← BACK", key="back_setup"):
        go("players")

# ── SCREEN 3: COVER ───────────────────────────────────────────────────────────
elif st.session_state.screen == "cover":
    name = st.session_state.players[st.session_state.current_idx]
    total = len(st.session_state.players)
    current_num = st.session_state.current_idx + 1

    st.markdown(f"""
    <div style="text-align:center;padding:3rem 1rem 1rem;">
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.68rem;
                    color:#4a5568;letter-spacing:0.3em;margin-bottom:0.8rem;">
            // PLAYER {current_num} OF {total} //</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:clamp(3.5rem,14vw,7rem);
                    letter-spacing:0.15em;color:#d0d8e8;line-height:1;">
            {name.upper()}</div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.72rem;
                    color:#4a5568;letter-spacing:0.2em;margin-top:1.2rem;line-height:1.8;">
            // it's your turn //<br>everyone else — look away 👀</div>
    </div>
    <hr style="border:none;border-top:1px solid #1e2530;margin:2rem 0 1rem;">
    """, unsafe_allow_html=True)

    if st.button("I'M READY →", key="ready"):
        go("reveal")

# ── SCREEN 4: REVEAL ──────────────────────────────────────────────────────────
elif st.session_state.screen == "reveal":
    idx = st.session_state.current_idx
    name = st.session_state.players[idx]
    is_impostor = idx in st.session_state.impostor_indices

    if is_impostor:
        st.markdown(f"""
        <div style="background:#141820;border:2px solid #e8334a;border-radius:4px;
                    padding:2.5rem 2rem;text-align:center;margin:1.5rem 0;
                    box-shadow:0 0 40px rgba(232,51,74,0.2);">
            <div style="font-family:'Share Tech Mono',monospace;font-size:0.68rem;
                        color:#4a5568;letter-spacing:0.3em;margin-bottom:1.2rem;">
                // {name.upper()} //</div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:4rem;
                        letter-spacing:0.1em;color:#e8334a;
                        text-shadow:0 0 30px rgba(232,51,74,0.6);">IMPOSTOR</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;
                        color:#4a5568;margin-top:1rem;letter-spacing:0.1em;">
                blend in — don't get caught</div>
        </div>""", unsafe_allow_html=True)

        if not st.session_state.show_word:
            if st.button("👁  REVEAL MY HINT", key="reveal_btn"):
                st.session_state.show_word = True
                st.rerun()
        else:
            hint = st.session_state.impostor_hint
            st.markdown(f"""<div style="background:#0f1318;border:1px solid #e8334a;border-radius:3px;
                        padding:1.2rem 1.5rem;text-align:center;">
                <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#4a5568;
                            letter-spacing:0.2em;margin-bottom:0.5rem;">YOUR HINT WORD</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;letter-spacing:0.1em;
                            color:#e8334a;text-shadow:0 0 20px rgba(232,51,74,0.4);">{hint}</div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#4a5568;
                            margin-top:0.5rem;">use this to bluff — the real word is different</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:#141820;border:1px solid #1e2530;border-radius:4px;
                    padding:2.5rem 2rem;text-align:center;margin:1.5rem 0;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:0.68rem;
                        color:#4a5568;letter-spacing:0.3em;margin-bottom:1.2rem;">
                // {name.upper()} //</div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:4rem;
                        letter-spacing:0.1em;color:#00e5a0;
                        text-shadow:0 0 30px rgba(0,229,160,0.4);">AGENT</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;
                        color:#4a5568;margin-top:1rem;letter-spacing:0.1em;">
                remember the word — find the impostor</div>
        </div>""", unsafe_allow_html=True)

        if not st.session_state.show_word:
            if st.button("👁  REVEAL THE WORD", key="reveal_btn"):
                st.session_state.show_word = True
                st.rerun()
        else:
            w = st.session_state.word
            st.markdown(f"""<div style="background:#0f1318;border:1px solid #00e5a0;border-radius:3px;
                        padding:1.2rem 1.5rem;text-align:center;font-family:'Share Tech Mono',monospace;
                        color:#d0d8e8;font-size:1.6rem;letter-spacing:0.06em;
                        box-shadow:0 0 20px rgba(0,229,160,0.1);">{w}</div>""",
                        unsafe_allow_html=True)

    divider()
    remaining = len(st.session_state.players) - st.session_state.current_idx - 1
    next_label = f"DONE — NEXT PLAYER ({remaining} left) →" if remaining > 0 else "DONE — START GAME →"
    if st.button(next_label, key="next_player"):
        st.session_state.current_idx += 1
        if st.session_state.current_idx >= len(st.session_state.players):
            st.session_state.first_player = random.choice(st.session_state.players)
            go("go_first")
        else:
            go("cover")

# ── SCREEN 5: WHO GOES FIRST ──────────────────────────────────────────────────
elif st.session_state.screen == "go_first":
    first = st.session_state.first_player
    st.markdown(f"""
    <div style="text-align:center;padding:3rem 1rem 1rem;">
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;
                    color:#4a5568;letter-spacing:0.3em;margin-bottom:1.5rem;">
            // everyone has their assignment //</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:clamp(1.5rem,6vw,2.5rem);
                    letter-spacing:0.12em;color:#4a5568;margin-bottom:0.5rem;">GOES FIRST</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:clamp(3.5rem,14vw,7rem);
                    letter-spacing:0.15em;color:#f5a623;line-height:1;
                    text-shadow:0 0 40px rgba(245,166,35,0.4);">
            {first.upper()}</div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.72rem;
                    color:#4a5568;letter-spacing:0.2em;margin-top:1.5rem;line-height:1.8;">
            // discuss, then find the impostor //</div>
    </div>
    <hr style="border:none;border-top:1px solid #1e2530;margin:2rem 0 1rem;">
    """, unsafe_allow_html=True)

    if st.button("REVEAL IMPOSTOR →", key="to_result"):
        go("result")

# ── SCREEN 6: RESULT ──────────────────────────────────────────────────────────
elif st.session_state.screen == "result":
    impostor_names = [st.session_state.players[i] for i in st.session_state.impostor_indices]
    w = st.session_state.word
    h = st.session_state.impostor_hint

    logo()

    st.markdown(f"""
    <div style="background:#141820;border:1px solid #e8334a;border-radius:4px;
                padding:2rem;text-align:center;margin-bottom:1.5rem;
                box-shadow:0 0 30px rgba(232,51,74,0.15);">
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.68rem;color:#4a5568;
                    letter-spacing:0.2em;margin-bottom:0.8rem;">// the impostor was //</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:2.8rem;letter-spacing:0.1em;
                    color:#e8334a;text-shadow:0 0 30px rgba(232,51,74,0.5);">
            {" & ".join(impostor_names).upper()}</div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.75rem;color:#4a5568;
                    margin-top:0.8rem;line-height:2;">
            The word was: <span style="color:#00e5a0;">{w}</span>
            &nbsp;·&nbsp;
            Impostor's hint: <span style="color:#e8334a;">{h}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Play again — keep players, go to setup for new word
    if st.button("PLAY AGAIN →", key="play_again"):
        st.session_state.word = ""
        st.session_state.impostor_hint = ""
        st.session_state.current_idx = 0
        st.session_state.first_player = None
        go("setup")

    # New game — keep players, go back to player screen
    if st.button("NEW GAME", key="new_game_result"):
        players = st.session_state.players[:]
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.session_state.players = players
        st.rerun()