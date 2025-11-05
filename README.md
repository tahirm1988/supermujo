 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
index 1606c278459a8a0c1a4cad74a41e1fab41c7f98d..3e8fd0aee9559f9e3b9b17f033408634c4f77d4d 100644
--- a/README.md
+++ b/README.md
@@ -1,2 +1,102 @@
 # supermujo
-igra super mujo, 2d, bosanska tematika 
+Igra Super Mujo je mala 2D platformerska avantura napravljena u Pygame-u.
+
+## Pokretanje (korak po korak)
+
+Ako si početnik i prvi put pokrećeš Python program, slijedi ove korake redom.
+
+### 1. Instaliraj Python
+
+1. Otvori [python.org/downloads](https://www.python.org/downloads/).
+2. Preuzmi najnoviju verziju Pythona 3.11 ili noviju (Windows korisnici neka obavezno označe **Add Python to PATH** tokom instalacije).
+3. Nakon instalacije otvori novi terminal:
+   - **Windows:** Start ➜ upiši "PowerShell" ➜ otvori **Windows PowerShell**.
+   - **macOS:** Spotlight (Cmd+Space) ➜ upiši "Terminal" ➜ otvori **Terminal**.
+   - **Linux:** otvori aplikaciju **Terminal** iz menija.
+4. Provjeri da li je Python instaliran naredbom:
+
+   ```bash
+   python --version
+   ```
+
+   Ako dobiješ grešku, probaj `python3 --version` ili na Windowsu `py --version`.
+
+### 2. Preuzmi kod igre
+
+1. Klikni na zeleni gumb **Code** na GitHubu i izaberi **Download ZIP**.
+2. Otvori preuzeti ZIP i raspakuj ga (npr. na Desktop ili u Documents).
+3. U terminalu se prebaci u raspakovanu mapu. Primjer za Windows (pretpostavljamo da je mapa na Desktopu):
+
+   ```powershell
+   cd $Env:USERPROFILE\Desktop\supermujo-main
+   ```
+
+   Na macOS/Linuxu (ako je folder na Desktopu):
+
+   ```bash
+   cd ~/Desktop/supermujo-main
+   ```
+
+### 3. (Opcionalno) napravi virtualno okruženje
+
+Virtualno okruženje drži pakete odvojeno od ostatka sistema. Ako ti djeluje komplikovano, ovaj korak možeš preskočiti.
+
+```bash
+python -m venv .venv
+```
+
+- **Windows PowerShell:**
+
+  ```powershell
+  .venv\Scripts\Activate.ps1
+  ```
+
+- **macOS/Linux:**
+
+  ```bash
+  source .venv/bin/activate
+  ```
+
+Kad je okruženje aktivno, u promptu će se pojaviti prefiks `(venv)` ili slično.
+
+### 4. Instaliraj Pygame
+
+U aktivnom terminalu (i virtualnom okruženju, ako ga koristiš) instaliraj Pygame:
+
+```bash
+pip install pygame
+```
+
+Ako dobiješ poruku da se `pip` ne prepoznaje, pokušaj s `python -m pip install pygame` ili `py -m pip install pygame` na Windowsu.
+
+### 5. Pokreni igru
+
+Ostani u direktoriju projekta (`supermujo-main` ili kako si ga već nazvao) i pokreni jednu od naredbi:
+
+```bash
+python super_mujo.py
+```
+
+Ako dobiješ grešku da `python` nije prepoznat, probaj `python3 super_mujo.py` (macOS/Linux) ili `py super_mujo.py` (Windows).
+
+Ako želiš, možeš pokrenuti i kao modul:
+
+```bash
+python -m super_mujo
+```
+
+### 6. Česti problemi
+
+- **Prozor se odmah zatvori:** provjeri da li se u terminalu pojavila greška (npr. `pygame` nije instaliran).
+- **`ModuleNotFoundError: pygame`:** ponovo pokreni korak „Instaliraj Pygame“ i provjeri da li se instalacija završila bez grešaka.
+- **`PermissionError` na Windowsu pri aktivaciji `.venv`:** otvori PowerShell kao Administrator i pokreni `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, zatim pokušaj ponovo.
+- **Ne vidiš fajlove u terminalu:** pokreni `dir` (Windows) ili `ls` (macOS/Linux) i provjeri da li se među fajlovima nalazi `super_mujo.py`.
+
+## Kontrole
+
+- Strelice lijevo/desno ili A/D za kretanje.
+- Space ili strelica gore za skok.
+- R nakon pada za ponovno igranje trenutnog nivoa.
+- ESC u završnom ekranu za izlaz, R za novi krug.
+
+Igra prati Muju koji obilazi nivoe inspirisane bosanskim lokacijama, sakuplja specijalitete poput kafe i ćevapa te stiže do zlatnog cilja.
 
EOF
)
