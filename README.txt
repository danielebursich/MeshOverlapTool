
README - Mesh Overlap Dashboard (Eseguibile)

CONTENUTO:
- mesh_overlap_app.py .......... Codice principale dell'applicazione
- mesh_overlap_app.spec ........ Configurazione per generare l'eseguibile
- lancia_dashboard.bat ......... Avvio rapido per Windows
- requirements.txt ............. Librerie richieste
- Manuale_statistico.pdf ....... Guida dei parametri statistici

ISTRUZIONI:
1. Installa Python 3.9+ e PyInstaller:
   pip install pyinstaller

2. Installa le dipendenze:
   pip install -r requirements.txt

3. Genera il file .exe con:
   pyinstaller mesh_overlap_app.spec

4. Lancia il file eseguibile da:
   dist/mesh_overlap_dashboard/mesh_overlap_dashboard.exe
