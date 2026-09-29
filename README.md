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