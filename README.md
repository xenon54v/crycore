# CryptoCore

CryptoCore — учебная консольная программа для шифрования и расшифрования файлов с использованием AES-128 в режиме ECB.

## Возможности

- шифрование файлов алгоритмом AES-128;
- расшифрование файлов;
- режим ECB;
- дополнение данных по стандарту PKCS#7;
- работа с текстовыми и бинарными файлами;
- проверка корректности ключа;
- обработка ошибок командной строки.

## Требования

- Python 3.10 или новее;
- pycryptodome;
- pytest для запуска тестов.

## Установка

Создать виртуальное окружение:

```powershell
python -m venv .venv
```

Активировать его:

```powershell
.venv\Scripts\Activate.ps1
```

Установить зависимости:

```powershell
pip install -r requirements.txt
```

Установить проект в режиме разработки:

```powershell
pip install -e .
```

После установки становится доступна команда:

```powershell
cryptocore
```

## Использование

### Шифрование

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted.bin
```

### Расшифрование

```powershell
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted.bin --output decrypted.txt
```

Ключ AES-128 должен содержать ровно 16 байт и передаваться в шестнадцатеричном формате.

Пример корректного ключа:

```text
000102030405060708090a0b0c0d0e0f
```

## Структура проекта

```text
src/
└── cryptocore/
    ├── cli.py
    ├── file_io.py
    ├── crypto/
    │   └── aes.py
    └── modes/
        └── ecb.py

tests/
├── test_cli.py
├── test_ecb.py
└── test_padding.py
```

`aes.py` содержит работу с AES-примитивом.

`ecb.py` реализует обработку блоков в режиме ECB и дополнение PKCS#7.

`file_io.py` отвечает за чтение и запись бинарных файлов.

`cli.py` реализует интерфейс командной строки.

## Тестирование

Для запуска всех тестов:

```powershell
pytest -v
```

На текущем этапе Sprint 1 реализовано 25 автоматических тестов.

Проверяется:

- PKCS#7 padding;
- PKCS#7 unpadding;
- шифрование и расшифрование;
- работа с несколькими блоками;
- пустые данные;
- бинарные данные;
- неправильный ключ;
- повреждённые зашифрованные данные;
- ошибки командной строки;
- полный цикл шифрования и расшифрования файла.

## Проверка полного цикла

Создать файл:

```powershell
"Hello CryptoCore!" | Set-Content -Encoding UTF8 plaintext.txt
```

Зашифровать:

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted.bin
```

Расшифровать:

```powershell
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted.bin --output decrypted.txt
```

Для проверки совпадения файлов можно сравнить их SHA-256:

```powershell
(Get-FileHash plaintext.txt -Algorithm SHA256).Hash
(Get-FileHash decrypted.txt -Algorithm SHA256).Hash
```

Хэши исходного и расшифрованного файлов должны совпадать.