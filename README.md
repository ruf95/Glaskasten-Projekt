# Glaskasten-Projekt

🌟 Glaskasten – Die Python Arcade Machine

Willkommen im Glaskasten-Projekt – einer Mischung aus Retro-Charme, Hardware-Bastelei und modernem Python-Engineering.
Unser Ziel: eine eigene Arcade-Maschine entwickeln, komplett mit selbstgebautem Controller, individuellen Spielen und einem Launcher, der alles zusammenhält.
Das Ganze wird später als physische Installation in einem Glaskasten an unserer Uni stehen.

🧩 Inhalt

[Über das Projekt](#über-das-projekt)

[Features](#features)

[Technischer Überblick](#technischer-überblick)

[Lizenz](#lizenz)


🎮 Über das Projekt

Der Glaskasten ist ein Arcade-Automat auf Python-Basis.
In ihm laufen kleine, selbst entwickelte Spiele, die über einen grafischen Launcher ausgewählt werden.
Die Bedienung erfolgt über einen selbst entwickelten Hardware-Controller, gesteuert über ein Arduino-Board.

Unser Fokus:

Verständlich strukturierter Code

Einfache Erweiterbarkeit (neue Spiele sollen super easy eingebunden werden)

Saubere Trennung zwischen Launcher, Spielen und Hardware

Eine reale, installierte Arcade-Machine für Events & Projekte an der Uni

✨ Features

🕹 Eigener Arcade-Launcher in Python & pygame

📦 Modulare Spielstruktur — jedes Spiel ist ein eigenes Mini-Projekt

🎨 Animierte Cover-Navigation wie bei echten Spielsystemen

🔌 Arduino-Controller für echte Arcade-Button-Inputs

🖥 Installation in einem Uni-Glaskasten als Dauer-Exponat

🔧 Einfache Erweiterbarkeit über Game-Templates

⚙️ Technischer Überblick
🎛 Launcher

Grafikengine über pygame

Blättern durch Cover mit animierten Übergängen

Hintergrundbilder, Fade-Ins, Slide-Animationen

Laden von Spielen als Subprozess oder Modul

🕹 Spiele

Jedes Spiel ist ein eigenes Python-Modul

Gemeinsame Schnittstelle: start(), quit(), Assets, Configs

Spiele können problemlos hinzugefügt oder entfernt werden

🔌 Controller

Eingabe über Arduino-Serial

Mappings im Python-Frontend

Optionaler Fallback auf Tastatur-Steuerung



📄 Lizenz

MIT
