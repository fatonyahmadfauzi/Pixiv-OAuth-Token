# Dziennik zmian

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔜 Coming Soon

- **Mobile Web Support** — The web app currently only supports desktop browsers. Upcoming update will bring full responsive mobile support, allowing users to generate Pixiv OAuth tokens directly from mobile devices without needing the desktop app.


---

## [1.0.5] - 2026-04-03

### ✨ Dodano

- **Uruchamianie obsługujące Internet GUI**
Przed uruchomieniem głównego okna GUI inteligentny ekran powitalny `NetLoadingScreen` przeprowadza teraz przed lotem kontrolę połączenia internetowego. Jeśli nie zostanie znalezione żadne połączenie, bezpiecznie ponawia próbę w tle, aż do nawiązania połączenia. Co więcej, aktywny monitor czasu działania wyświetli alert przechodzący z powrotem do ekranu ładowania, jeśli połączenie zostanie zerwane w trakcie użytkowania.
- **Native GUI Mody dokumentacji**
Zastąpiono przekierowania przeglądarki zewnętrznej w celu uzyskania krytycznej dokumentacji. **Dziennik zmian**, **Warunki korzystania** i **Polityka prywatności** są teraz wyświetlane w natywnych, dynamicznych i przejrzystych oknach dialogowych `tkinter` (pobierane asynchronicznie bezpośrednio z repozytorium GitHub).
- **Kompleksowe lokalizacje terminali**
Interaktywny interfejs GitHub CLI (nawigacja po problemach) i wszystkie układy prawne/wsparcia oparte na terminalu są teraz autentycznie zlokalizowane we wszystkich 11 obsługiwanych językach.

### ✨ Zmieniono

- **Przeprojektowana CLI Estetyka**
Usunięto starsze ozdobne obramowania pudełek, aby uzyskać znacznie czystszy, zmodernizowany wyświetlacz terminala wyrównany do lewej strony.
- **Automatyczne cyfrowe podpisywanie kodów**
Znacząco zmodernizowano potok `sign_auto.bat`. Skrypt teraz dynamicznie automatycznie wykrywa `signtool.exe` głęboko w Windows SDK, bez wysiłku stosując certyfikat z podpisem własnym do wszystkich wygenerowanych kompilacji jednocześnie (w tym do konfiguracji instalatora i aliasów pobierania `_latest`), aby ukryć podstawowe flagi „Nieznany wydawca” SmartScreen.

### 🐞 Naprawiono

- **Błąd właściwości instalatora**
Naprawiono anomalię polegającą na tym, że instalator `Setup.exe` wyświetlał `0.0.0.0` we właściwościach systemu Windows. Konstruktor poprawnie wstawia teraz ścisłe nagłówki PE `VersionInfoVersion` podczas kompilacji, aby odzwierciedlić dokładnie pasujący numer wersji (e.g., 1.0.5.0) natychmiast po renderowaniu.

---

## [1.0.4] - 2026-03-29

### 🐞 Naprawiono

- **Portable CLI/GUI — Przywracanie wersji po aktualizacji**: `VERSION_FILE` i `CONFIG_FILE` zostały rozwiązane przy użyciu `Path(__file__)`, które w trybie zamrożonym (PyInstaller onefile) wskazuje na tymczasowy katalog `_MEIPASS` — katalog, który jest niszczony po zamknięciu aplikacji. Oba pliki są teraz rozpoznawane przy użyciu `_app_dir()` / `app_dir()`, co poprawnie zwraca folder zawierający rzeczywisty `.exe`, zapewniając zachowanie tożsamości wersji po ponownym uruchomieniu.
- **CLI — Aktualizacja nadpisała temp `.py` zamiast exe**: Podczas działania jako zamrożony plik wykonywalny `_self_update()` nadpisywał wyodrębniony `.py` w katalogu tymczasowym zamiast zastępować rzeczywisty `.exe`. Funkcja wykrywa teraz `is_frozen` i bezpośrednio pobiera nowy plik wykonywalny, zastępując go skryptem aktualizującym `.bat` (ten sam mechanizm co GUI).

### ✨ Dodano

- **Automatyczna aktualizacja uwzględniająca architekturę (CLI + GUI)**: Zarówno przenośne, jak i konfiguracyjne przepływy aktualizacji wykrywają teraz architekturę działającego pliku wykonywalnego (`x64`, `x86`, `ARM64` lub rodzajowy) na podstawie jego nazwy pliku i pobierają dokładnie pasujący wariant z folderu `downloads/`, zapobiegając przypadkowym niezgodnościom architektury podczas aktualizacji.
- **CLI Przebieg aktualizacji instalatora instalacyjnego**: CLI odzwierciedla teraz zachowanie GUI w przypadku instalacji instalacyjnych — podczas uruchamiania z `Program Files` pobiera najnowszy instalator instalacyjny `.exe` i uruchamia go w trybie cichym (`/VERYSILENT /NORESTART`) zamiast podejmować próbę lokalnej zamiany plików binarnych.

---

## [1.0.3] - 2026-03-26

### ✨ Zmieniono

— Zastąpiono domyślną etykietę kompilacji lokalnej z `REL-LOCAL` na `BUILD-UNKNOWN` w narzędziach środowiska wykonawczego/wersji i wygenerowanych manifestach.
- GUI zawiera teraz akcję w górnym menu **Dziennik zmian** i menu rozwijane **Wersja** z wyraźnym wpisem sprawdzającym wersję.
- Dodano automatyczne sprawdzanie wersji przy uruchamianiu w GUI z wyskakującymi akcjami aktualizacji (**Aktualizacja** / **Później**), a także obsługę przepływu aktualizacji w przypadku zamrożonych dystrybucji instalacyjnych/przenośnych.
- Zaktualizowano generowanie kodu kompilacji do stylu uniksowego `REL-U<unix_ms>` w przypadku zmian wersji (`patch/minor/major`).

## [1.0.2] - 2026-03-23

### ✨ Dodano

- **Konsola debugowania (GUI)**
Dedykowany przycisk `⚙ Debug` w prawym górnym rogu nagłówka GUI otwiera ciemną konsolę terminala, która rejestruje każde zdarzenie aplikacji w czasie rzeczywistym. Przechwycone zdarzenia obejmują: uruchomienie aplikacji, zmiany języka, wszystkie kliknięcia przycisków (Otwórz logowanie, Token wymiany, Odśwież token, Kopiuj token dostępu/odświeżenia, Samouczek), Stany żądań HTTP (wysłanie/powodzenie/niepowodzenie), kroki przepływu PKCE, operacje w schowku, zapisy konfiguracji i ostrzeżenia. Wszystkie komunikaty debugowania są w pełni zlokalizowane we wszystkich 11 obsługiwanych językach. Konsola obsługuje transmisję strumieniową na żywo nowych wiadomości po otwarciu, wstępne wypełnianie dzienników historycznych od początku sesji, a także przyciski **Kopiuj wszystko** i **Wyczyść**.

## [1.0.1] - 2026-03-22

### ✨ Dodano

- **Inteligentne czyszczenie plików README dla wydań**
Automatycznie usuwa sekcje języka lokalizacji z pliku `` podczas kompilacji dystrybuowalnego `.zip`, zastępując łącza wewnętrzne bezwzględnymi łączami GitHub.
- **Ujednolicona obsługa dwóch instalatorów**
Skrypt kreatora InnoSetup generuje teraz ujednolicony instalator, który zachęca użytkowników końcowych do opcjonalnej instalacji samodzielnego CLI lub graficznego GUI.

### 🐞 Naprawiono

- **Rozdzielczość ścieżki kompilacji instalatora**
Naprawiono krytyczny problem z niedopasowaniem ścieżki w `make_installer_iss_dual.py`, gdzie `iscc` nie udało się zlokalizować `app\pixiv_oauth.ico`, generując pliki kompilacji bezpośrednio w skonfigurowanym katalogu `scripts\`.

## [1.0.0] - 2026-03-21

### ✨ Dodano

- Początkowe samodzielne dystrybucje wykonywalne (`.exe`) skompilowane dla trybów GUI i CLI.
- Wstępnie zoptymalizowana integracja bezserwerowa zsynchronizowana z Vercel z automatycznym wykrywaniem języka.
- Dodano przepustkę ekstremalnego zaciemniania JavaScript dla internetowych punktów końcowych.
