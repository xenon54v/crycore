## Sprint 1 — AES-128 ECB

В Sprint 1 была реализована базовая версия CryptoCore для шифрования и расшифрования файлов с использованием AES-128 в режиме ECB.

## Возможности Sprint 1

- шифрование файлов алгоритмом AES-128;
- расшифрование файлов;
- режим ECB;
- дополнение данных по стандарту PKCS#7;
- работа с текстовыми и бинарными файлами;
- проверка корректности AES-128 ключа;
- обработка ошибок командной строки;
- автоматические тесты;
- проверка совместимости ECB с OpenSSL.

## Build and installation

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

Установить проект:

```powershell
pip install -e .
```

После установки становится доступна команда:

```powershell
cryptocore
```

## Dependencies

Проект использует:

- Python 3.10 или новее;
- `pycryptodome` — реализация AES;
- `pytest` — автоматические тесты;
- OpenSSL — проверка совместимости реализации.

## Использование ECB

Шифрование с явно указанным выходным файлом:

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted.bin --output decrypted.bin
```

Ключ AES-128 должен содержать ровно 16 байт и передаваться в шестнадцатеричном формате.

Пример:

```text
000102030405060708090a0b0c0d0e0f
```

## Выходной файл по умолчанию

Параметр `--output` можно не указывать.

При шифровании результат будет записан в:

```text
encrypted.bin
```

Пример:

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt
```

При расшифровании результат будет записан в:

```text
decrypted.bin
```

Пример:

```powershell
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted.bin
```

## Реализация

Основные файлы Sprint 1:

```text
src/cryptocore/
├── cli.py
├── file_io.py
├── crypto/
│   └── aes.py
└── modes/
    └── ecb.py
```

`aes.py` содержит работу с AES-примитивом из `pycryptodome`.

`ecb.py` реализует:

- PKCS#7 padding;
- PKCS#7 unpadding;
- разбиение данных на блоки по 16 байт;
- последовательное шифрование и расшифрование блоков в режиме ECB.

`file_io.py` отвечает за чтение и запись файлов в бинарном режиме.

`cli.py` реализует интерфейс командной строки, проверку аргументов, ключа и выбор операции шифрования или расшифрования.

## Тестирование Sprint 1

Автоматические тесты находятся в:

```text
tests/test_cli.py
tests/test_ecb.py
tests/test_padding.py
```

Проверяется:

- PKCS#7 padding;
- PKCS#7 unpadding;
- шифрование и расшифрование;
- работа с несколькими блоками;
- данные размером ровно один блок;
- пустые данные;
- бинарные данные;
- неправильная длина ключа;
- некорректный ciphertext;
- повреждённый padding;
- ошибки командной строки;
- выходные файлы по умолчанию;
- полный цикл шифрования и расшифрования файла.

Запуск тестов:

```powershell
pytest -v
```

## Проверка полного цикла

Создать тестовый файл:

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

Проверить совпадение файлов:

```powershell
(Get-FileHash plaintext.txt -Algorithm SHA256).Hash
(Get-FileHash decrypted.txt -Algorithm SHA256).Hash
```

Хэши должны совпадать.

## Проверка ECB через OpenSSL

Для проверки совместимости используется одинаковый AES-128 ключ.

Пример команды OpenSSL:

```powershell
openssl enc -aes-128-ecb -K 000102030405060708090a0b0c0d0e0f -nosalt -in plaintext.txt -out openssl_ecb.bin
```

Результат OpenSSL сравнивается с результатом CryptoCore побайтово.

Автоматическая проверка находится в:

```text
tests/test_openssl_interop.py
```

Она проверяет, что ciphertext, полученный CryptoCore в режиме ECB, совпадает с результатом OpenSSL при одинаковом ключе и исходных данных.


## Sprint 2

Во втором спринте в CryptoCore была добавлена поддержка новых режимов работы AES:

- CBC;
- CFB-128;
- OFB;
- CTR.

Режимы CBC, CFB, OFB и CTR используют 16-байтовый IV.

При шифровании IV генерируется автоматически с помощью `os.urandom(16)` и записывается в начало выходного файла:

```text
<16-byte IV><ciphertext>
```

При расшифровании IV можно получить двумя способами:

1. автоматически из первых 16 байт входного файла;
2. явно передать через параметр `--iv`.

## Использование CBC

Шифрование:

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted.bin
```

Расшифрование с IV из файла:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted.bin --output decrypted.txt
```

Расшифрование с явно указанным IV:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input ciphertext.bin --output decrypted.txt
```

## Использование CFB

Шифрование:

```powershell
cryptocore --algorithm aes --mode cfb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode cfb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted.bin --output decrypted.txt
```

## Использование OFB

Шифрование:

```powershell
cryptocore --algorithm aes --mode ofb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode ofb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted.bin --output decrypted.txt
```

## Использование CTR

Шифрование:

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode ctr --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted.bin --output decrypted.txt
```

## Особенности режимов

ECB и CBC используют дополнение PKCS#7.

CFB, OFB и CTR работают как потоковые режимы и не используют padding. Поэтому размер зашифрованных данных в этих режимах совпадает с размером исходных данных.

## Структура проекта после Sprint 2

```text
src/
└── cryptocore/
    ├── cli.py
    ├── file_io.py
    ├── iv.py
    ├── crypto/
    │   └── aes.py
    └── modes/
        ├── ecb.py
        ├── cbc.py
        ├── cfb.py
        ├── ofb.py
        └── ctr.py

tests/
├── test_cli.py
├── test_ecb.py
├── test_cbc.py
├── test_cfb.py
├── test_ofb.py
├── test_ctr.py
├── test_iv.py
└── test_padding.py
```

## Тестирование Sprint 2

Для запуска всех тестов используется команда:

```powershell
pytest -v
```

Во втором спринте дополнительно проверяются:

- генерация IV;
- проверка длины IV;
- режим CBC;
- режим CFB-128;
- режим OFB;
- режим CTR;
- работа с частичными блоками;
- отсутствие padding в потоковых режимах;
- автоматическое чтение IV из начала файла;
- работа с явно переданным параметром `--iv`;
- полный цикл шифрования и расшифрования файлов.

## Совместимость с OpenSSL

В Sprint 2 необходимо проверить совместимость CryptoCore с OpenSSL в двух направлениях:

```text
CryptoCore -> OpenSSL
OpenSSL -> CryptoCore
```

Для проверки должен использоваться одинаковый AES-128 ключ и одинаковый IV.

Пример расшифрования файла через OpenSSL:

```powershell
openssl enc -aes-128-cbc -d -K 000102030405060708090a0b0c0d0e0f -iv AABBCCDDEEFF00112233445566778899 -in ciphertext.bin -out decrypted.txt
```

Пример шифрования через OpenSSL:

```powershell
openssl enc -aes-128-cbc -K 000102030405060708090a0b0c0d0e0f -iv AABBCCDDEEFF00112233445566778899 -in plaintext.txt -out ciphertext.bin
```

## OpenSSL interoperability tests

Для проверки совместимости CryptoCore с OpenSSL используется один и тот же AES-128 ключ и одинаковый IV.

Ключ:

```text
000102030405060708090a0b0c0d0e0f
```

Пример IV:

```text
AABBCCDDEEFF00112233445566778899
```

### CryptoCore -> OpenSSL

Сначала файл шифруется через CryptoCore:

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plain.txt --output crypto_cbc.bin
```

Первые 16 байт файла содержат IV. Его нужно отделить от ciphertext.

Пример для PowerShell:

```powershell
$bytes = [System.IO.File]::ReadAllBytes("crypto_cbc.bin")

$iv = $bytes[0..15]
$ciphertext = $bytes[16..($bytes.Length - 1)]

[System.IO.File]::WriteAllBytes("cbc_cipher_only.bin", $ciphertext)

$ivHex = ($iv | ForEach-Object { $_.ToString("x2") }) -join ""
```

После этого ciphertext можно расшифровать через OpenSSL:

```powershell
openssl enc -aes-128-cbc -d -K 000102030405060708090a0b0c0d0e0f -iv $ivHex -in cbc_cipher_only.bin -out openssl_decrypted.txt
```

Аналогично можно проверить остальные режимы:

```powershell
openssl enc -aes-128-cfb -d -K 000102030405060708090a0b0c0d0e0f -iv $ivHex -in cfb_cipher_only.bin -out openssl_cfb_decrypted.txt
```

```powershell
openssl enc -aes-128-ofb -d -K 000102030405060708090a0b0c0d0e0f -iv $ivHex -in ofb_cipher_only.bin -out openssl_ofb_decrypted.txt
```

```powershell
openssl enc -aes-128-ctr -d -K 000102030405060708090a0b0c0d0e0f -iv $ivHex -in ctr_cipher_only.bin -out openssl_ctr_decrypted.txt
```

### OpenSSL -> CryptoCore

Сначала файл шифруется через OpenSSL.

CBC:

```powershell
openssl enc -aes-128-cbc -K 000102030405060708090a0b0c0d0e0f -iv AABBCCDDEEFF00112233445566778899 -in plain.txt -out openssl_cbc.bin
```

После этого файл расшифровывается через CryptoCore:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cbc.bin --output decrypted_cbc.txt
```

CFB:

```powershell
openssl enc -aes-128-cfb -K 000102030405060708090a0b0c0d0e0f -iv AABBCCDDEEFF00112233445566778899 -in plain.txt -out openssl_cfb.bin
```

```powershell
cryptocore --algorithm aes --mode cfb --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cfb.bin --output decrypted_cfb.txt
```

OFB:

```powershell
openssl enc -aes-128-ofb -K 000102030405060708090a0b0c0d0e0f -iv AABBCCDDEEFF00112233445566778899 -in plain.txt -out openssl_ofb.bin
```

```powershell
cryptocore --algorithm aes --mode ofb --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_ofb.bin --output decrypted_ofb.txt
```

CTR:

```powershell
openssl enc -aes-128-ctr -K 000102030405060708090a0b0c0d0e0f -iv AABBCCDDEEFF00112233445566778899 -in plain.txt -out openssl_ctr.bin
```

```powershell
cryptocore --algorithm aes --mode ctr --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_ctr.bin --output decrypted_ctr.txt
```

### Автоматическая проверка

Для автоматической проверки совместимости используется файл:

```text
tests/test_openssl_interop.py
```

Запуск:

```powershell
pytest tests/test_openssl_interop.py -v
```

Тесты проверяют оба направления для всех режимов CBC, CFB, OFB и CTR:

```text
CryptoCore -> OpenSSL
OpenSSL -> CryptoCore
```

## Build and installation

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

Установить проект:

```powershell
pip install -e .
```

После установки становится доступна команда:

```powershell
cryptocore
```

## Dependencies

Проект использует:

- Python 3.10 или новее;
- `pycryptodome` — реализация AES;
- `pytest` — автоматические тесты;
- OpenSSL — проверка совместимости реализации с внешним инструментом.


## Sprint 3 — secure random key generation

В Sprint 3 в CryptoCore был добавлен отдельный модуль CSPRNG для генерации криптографически стойких случайных данных.

Для генерации используется функция:

```python
generate_random_bytes(num_bytes: int) -> bytes
```

Она реализована в файле:

```text
src/cryptocore/csprng.py
```

В качестве источника случайности используется `os.urandom()`, который получает криптографически стойкие случайные данные от операционной системы.

Обычный модуль `random` для генерации ключей и IV не используется.

## Автоматическая генерация ключа

При шифровании параметр `--key` теперь можно не указывать.

В этом случае CryptoCore автоматически создаёт случайный 16-байтовый ключ AES-128 и выводит его в терминал.

Пример:

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --input plaintext.txt --output ciphertext.bin
```

Пример вывода:

```text
[INFO] Generated random key: 1a2b3c4d5e6f7890fedcba9876543210
```

Сгенерированный ключ необходимо сохранить самостоятельно, так как он не записывается в зашифрованный файл.

Для расшифрования параметр `--key` остаётся обязательным:

```powershell
cryptocore --algorithm aes --mode ctr --decrypt --key 1a2b3c4d5e6f7890fedcba9876543210 --input ciphertext.bin --output decrypted.txt
```

Если при расшифровании ключ не указан, программа завершает работу с ошибкой.

## Пользовательский ключ

При передаче собственного ключа поведение программы остаётся таким же, как в предыдущих спринтах:

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output ciphertext.bin
```

Если переданный пользователем ключ имеет очевидно слабый шаблон, программа выводит предупреждение в `stderr`.

Например:

```text
[WARNING] The provided key appears to be weak
```

## Генерация IV

Для режимов:

- CBC;
- CFB;
- OFB;
- CTR;

IV также создаётся через общий CSPRNG-модуль:

```python
generate_random_bytes(16)
```

Длина IV составляет 16 байт.

Формат зашифрованного файла остаётся таким же, как в Sprint 2:

```text
<16-byte IV><ciphertext>
```

## Тестирование CSPRNG

Автоматические тесты находятся в:

```text
tests/test_csprng.py
```

Проверяется:

- корректная длина случайных данных;
- обработка неправильного размера;
- отсутствие совпадений среди 1000 сгенерированных AES-128 ключей;
- базовое распределение единичных и нулевых битов;
- автоматическая генерация ключа при шифровании;
- успешное расшифрование с автоматически созданным ключом.

Все тесты проекта можно запустить командой:

```powershell
pytest -v
```

## NIST Statistical Test Suite

Для дополнительной статистической проверки CSPRNG используется NIST Statistical Test Suite 2.1.2.

Тестовые данные создаются скриптом:

```text
scripts/generate_nist_data.py
```

Запуск:

```powershell
python scripts/generate_nist_data.py
```

Скрипт создаёт файл:

```text
nist_test_data.bin
```

размером 10 000 000 байт.

Для запуска NIST STS использовалась команда:

```bash
./assess 1000000
```

Параметры проверки:

```text
Длина последовательности: 1 000 000 бит
Количество последовательностей: 80
Формат: Binary
Количество тестов: 15
```

Были использованы стандартные параметры NIST STS.

Итоговый отчёт сохранён в:

```text
docs/nist/finalAnalysisReport.txt
```

Подробная процедура тестирования и результаты описаны в:

```text
TESTING.md
```

По итогам проверки критических статистических отклонений обнаружено не было.