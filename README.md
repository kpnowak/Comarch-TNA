# Projekt Raport Obecności

Ten projekt zawiera skrypty Pythona, które pobierają dane o obecności z API Comarch TNA i zapisują je albo do pliku tekstowego, albo do bazy danych Microsoft SQL Server. Dostępne są cztery skrypty:

- **to_txt_all.py**  
  Pobiera dane o obecności dla **wszystkich użytkowników** (tych, którzy mają zarejestrowane wejście, wyjście lub oba) w zadanym okresie i zapisuje dane do pliku TXT.

- **to_txt_only_active.py**  
  Pobiera dane o obecności dla **tylko aktywnych użytkowników** w zadanym okresie i zapisuje dane do pliku TXT.

- **to_SQL_all.py**  
  Pobiera dane o obecności dla **wszystkich użytkowników** w zadanym okresie i zapisuje dane do tabeli w bazie danych Microsoft SQL Server.

- **to_SQL_only_active.py**  
  Pobiera dane o obecności dla **tylko aktywnych użytkowników** w zadanym okresie i zapisuje dane do tabeli w bazie danych Microsoft SQL Server.

---

## Wymagania wstępne

### 1. Python 3.12  
Pobierz i zainstaluj Pythona 3.12 z [Microsoft Store](https://apps.microsoft.com/detail/9ncvdn91xzqp?hl=pl-pl&gl=PL).

### 2. Sterownik ODBC dla SQL Server (tylko dla skryptów SQL)  
Jeśli planujesz uruchamiać **to_SQL_all.py** lub **to_SQL_only_active.py**, pobierz i zainstaluj sterownik ODBC dla SQL Server z [tej strony](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows).

> **Uwaga:** Jeśli uruchamiasz tylko skrypty zapisujące do plików TXT (**to_txt_all.py** lub **to_txt_only_active.py**), nie musisz instalować sterownika ODBC.

---

## Konfiguracja

1. **Pobierz lub sklonuj pliki projektu** do katalogu na swoim komputerze.

2. **Otwórz Wiersz Poleceń** i przejdź do katalogu projektu. Przykład, jeśli skrypty znajdują się w `C:\Projects\AttendanceReport`, wpisz:

   ```bash
   cd C:\Projects\AttendanceReport

3. **Zainstaluj wymagane biblioteki Pythona** przy użyciu pliku requirements.txt. W Wierszu Poleceń wpisz:

   ```bash
   pip install -r requirements.txt

---

# Uruchamianie Skryptów

Podczas uruchamiania każdego ze skryptów zostaniesz poproszony o podanie:

- `IDENTYFIKATOR_KLUCZA`: Identyfikator Twojego klucza API.
- `KLUCZ`: Twój tajny klucz.
- `FROM_DATE`: Data początkowa (format: RRRR-MM-DD).
- `TILL_DATE`: Data końcowa (format: RRRR-MM-DD).

---

## Uruchamianie skryptów zapisujących do pliku TXT

### `to_txt_all.py`

Skrypt zapisuje dane o obecności dla **wszystkich użytkowników** (niezależnie od statusu aktywności), którzy mają zarejestrowane wejście, wyjście lub oba w danym okresie, do pliku TXT.

```bash
python to_txt_all.py
```

### `to_txt_only_active.py`

Skrypt zapisuje dane o obecności dla **tylko aktywnych użytkowników** (gdzie status to "ACTIVE"), którzy mają zarejestrowane wejście, wyjście lub oba w danym okresie, do pliku TXT.

```bash
python to_txt_only_active.py
```

---

## Uruchamianie skryptów zapisujących do SQL

### `to_SQL_all.py`

Skrypt zapisuje dane o obecności dla **wszystkich użytkowników** (niezależnie od statusu aktywności), którzy mają zarejestrowane wejście, wyjście lub oba w danym okresie, do tabeli w **Microsoft SQL Server**.

```bash
python to_SQL_all.py.py
```

### `to_SQL_only_active.py`

Skrypt zapisuje dane o obecności dla **tylko aktywnych użytkowników** (gdzie status to "ACTIVE"), którzy mają zarejestrowane wejście, wyjście lub oba w danym okresie, do tabeli w **Microsoft SQL Server**.

```bash
python to_SQL_only_active.py
```


Podczas uruchamiania dowolnego ze skryptów SQL zostaniesz także poproszony o podanie swojego **connection stringa** do bazy danych SQL Server.
Upewnij się, że masz zainstalowany sterownik ODBC zgodnie z powyższymi wskazówkami.