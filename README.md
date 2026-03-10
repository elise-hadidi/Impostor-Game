#  Impostor-Game

Live Demo: https://xfkrji7pjxlzbw6urrwaxz.streamlit.app/
A spy-themed party game built with Python and Streamlit  playable on one shared screen or phone. No accounts, no setup, just pass the device.

---

##  How to Play

One player is secretly the **Impostor**. Everyone else is an **Agent** who gets the same secret word. The impostor gets a related **hint word** instead  close enough to bluff, different enough to trip them up.

Players take turns describing the word without saying it. After discussion, the group tries to identify the impostor.

**Example:**
- Agents get: `Volcano`
- Impostor gets the hint: `Mountain`

---

##  Screenshots

### Enter players
<img width="499" height="679" alt="Screenshot 2026-03-09 at 4 50 48 PM" src="https://github.com/user-attachments/assets/fe1d2aba-3715-4ccb-af5f-5e2eca2a4703" />


### Game setup  generate a random word
<img width="497" height="678" alt="Screenshot 2026-03-09 at 4 51 02 PM" src="https://github.com/user-attachments/assets/4e55bd58-25ee-45c7-b9a3-e2c3e05a7d05" />


### Each player sees their role privately
<img width="499" height="683" alt="Screenshot 2026-03-09 at 4 51 14 PM" src="https://github.com/user-attachments/assets/0f7a373a-559d-435c-b2d0-352f332c7343" />
<img width="500" height="681" alt="Screenshot 2026-03-09 at 4 51 26 PM" src="https://github.com/user-attachments/assets/dca2c1c9-397c-4742-b0b7-38c9dbff27e9" />


### App picks who goes first
<img width="498" height="678" alt="Screenshot 2026-03-09 at 4 51 55 PM" src="https://github.com/user-attachments/assets/de3bc2bd-2a77-4d01-92a0-e96574f24c9d" />


### Impostor revealed
<img width="498" height="682" alt="Screenshot 2026-03-09 at 4 52 03 PM" src="https://github.com/user-attachments/assets/ca8abe8d-9a1c-44c2-a5e9-9362be379468" />


---

##  Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/elise-hadidi/impostor.git
cd impostor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

##  Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web app framework & session state |

No external libraries  just pure Python and Streamlit.

---

##  Game Flow

1. Enter players  
2. App generates a random secret word
3. A player's name shown, everyone else looks away
4. That player taps the screen to see AGENT (+ word) or IMPOSTOR (+ hint word)
5. App randomly picks who starts
6. Group discusses, then hits Reveal Impostor
7. App reveals impostor name, secret word, and impostor's hint revealed
     
---

##  Project Structure

```
Impostor-Game/
├── impostor-app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
└── README.md
```
