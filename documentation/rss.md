<!--Headings -->
# RSS Dokumentacja

## Wstęp
### Opis działania
#### Aplikacja pozwala użytkownikowi zapisywać URL stron wybranych przez niego jak i ich zapisywanie oraz ich przeglądanie 
## Instalacja
### Wymagania systemowe:
* Wersja Pythona: Python 3.7.7
* Windows, Linux
    * Na komputerze w Start wpisać cmd, zostanie otwarty terminal w którym trzeba wpisać poniższe polecenie.

    ```
    pip install -r requairements.txt
    ```
    * W celu otwarcia aplikacji należy wpisać poniższe polecenie w teminalu:
    ```
    py main.py
    ```

## Metody Działania
* logowanie i rejestracja

    * logowanie
        * Użytkowanik podaje login i hasło 
        * Jeśli podane dane są błędne zostaje wyświetlony komunikat Failed to login, bad credentials i jeśli użytkownik nie ma konta zostaje wyświetlone Don't have an account? Register

    * rejestracja
        * Zostaje wyświetlone okno rejestracji
        * Urzytkownik podaje login i hasło którego bedzie używał 
        * Jeśli takowy już istnieje zostaje wyświetlony komunikat i zmianie loginu na inny
        * Jeśli użytkownik jest już zajerestrowany zostaje wyświetony komunikat o zalogowaniu się
           
  
## Główny widok
* Po zalogowaniu zostaje wyświetlone okno z poniższymi opcjami: 
     
    * Dodawanie URL(addURL)
        * Po wejściu w to okienko zostaje wyświetlone okno dodania URL w którym wklejamy adres i  klikając OK zatwierdzamy lub wychodzimy klikając przycisk cacel 
        * Użytkownik podaje Url którego chce dodać jeśli podany adres jest błędny zostaje wyświetlony komunikat it\'s not a url
      
    * Ususwanie URL(removeURL)
        * Zostaje otwarte okno usuwania URL w którym użytkownuk ma możliwość kliknięciem wybrać URL 
        * Użytkowanik wybiera URL którego chce usunąc i go usuwa
      
    * Dodawanie gruo(AddGroup)          
        * Zostaje otwarte okno dodania grupy
        * Użytkownik podaje nazwe grupy której chce dodać 
        * Zostaje ona wyświetlona w oknach grup w pierwszej kolumnie w oknie głównym
        
    * Usuwanie grupy
        * Zostaje otworzona lista grup
        * Użytkownik ma możliwość wyboru jednej lubwielu grup które chce usunąć
                          
    * Wylogownanie i wyjście
        * Klikając w okno App dostajemy możliwość wyjścia z aplikacji i wylogowania 

