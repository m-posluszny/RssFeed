<!--Headings -->

# RSS Dokumentacja

## Wstęp

### Opis działania

#### Aplikacja pozwala użytkownikowi zapisywać URL stron wybranych przez niego jak i ich zapisywanie oraz ich przeglądanie

## Instalacja

### Wymagania systemowe:

- Wersja Pythona: Python 3.7.7
- Windows, Linux

  - Na komputerze w Start wpisać cmd, zostanie otwarty terminal w którym trzeba wpisać poniższe polecenie.

  ```
  pip install -r requirements.txt
  ```

  - W celu otwarcia aplikacji należy wpisać poniższe polecenie w teminalu:

  ```
  py rssfeed.py
  ```

## Metody Działania

- logowanie i rejestracja

  - logowanie

    - Użytkowanik podaje login i hasło
    - Jeśli podane dane są błędne zostaje wyświetlony komunikat Failed to login, bad credentials i jeśli użytkownik nie ma konta zostaje wyświetlone Don't have an account? Register

  - rejestracja
    - Zostaje wyświetlone okno rejestracji
    - Urzytkownik podaje login i hasło którego bedzie używał
    - Jeśli takowy już istnieje zostaje wyświetlony komunikat i zmianie loginu na inny
    - Jeśli użytkownik jest już zajerestrowany zostaje wyświetony komunikat o zalogowaniu się

## Główny widok

- Po zalogowaniu zostaje wyświetlony widok z listą grup, wszystkimi urlami, podglądem artykułu oraz pasek akcji z poniższymi opcjami:

  - Dodawanie URL(add_url)
    - Po wejściu w to okienko zostaje wyświetlone okno dodania URL w którym wklejamy adres i klikając OK zatwierdzamy lub wychodzimy klikając przycisk cancel
    - Użytkownik podaje Url którego chce dodać jeśli podany adres jest błędny zostaje wyświetlony komunikat it\'s not a url
  - Ususwanie URL(remove_url)
    - Zostaje otwarte okno usuwania URL w którym użytkownuk ma możliwość kliknięciem wybrać URL
    - Użytkowanik wybiera URL którego chce usunąć i go usuwa
  - Dodawanie grup(add_group)
    - Zostaje otwarte okno dodania grupy
    - Użytkownik podaje nazwe grupy której chce dodać
    - Zostaje ona wyświetlona w oknach grup w pierwszej kolumnie w oknie głównym
  - Usuwanie grupy(remove_group)

    - Zostaje otworzona lista grup
    - Użytkownik ma możliwość wyboru jednej lub wielu grup które chce usunąć

  - Dodawanie URL do grupy(add_url_to_group)

    - Po wejściu w to okienko zostaje wyświetlone okno dodania URL do grupy w którym wklejamy wybieramy grupy i interesujące nas adresy URL,klikając OK zatwierdzamy lub wychodzimy klikając przycisk cancel

  - Wyświetlenie najpopularniejszych adresów(show_popular_urls)
    - Po kliknięciu przycisku "Show Popular URLs" w górnym pasku, do grup użytkownika zostaje dodana grupa, w której pobrane zostanie
      5 najpopularniejszych adresów URL spośród użytkowników w bazie danych.
  - Wylogownanie i wyjście
    - Klikając w okno App dostajemy możliwość wyjścia z aplikacji i wylogowania

- W Głównym widoku znajdują się od lewej strony:
  - Lista wszystkich grup użytkownika, po których rozwinięciu ukazuje się lista adresów URL w danej grupie. Po kliknięciu prawym przyciskiem myszy na grupę bądź URL pojawia się opcja odświeżenia zawartości, pobierająca najświeższe artykuły.
  - Lista artykułów z aktywne(wybranej) grupy bądź adresu
  - Podgląd artykułu zawierający od góry, tytuł, treść, przycisk otwierający w przeglądarce okno z pełnym artykułem
