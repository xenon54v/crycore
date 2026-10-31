import struct


class SHA256:
    _INITIAL_HASH = [
        0x6A09E667,
        0xBB67AE85,
        0x3C6EF372,
        0xA54FF53A,
        0x510E527F,
        0x9B05688C,
        0x1F83D9AB,
        0x5BE0CD19,
    ]

    _K = [
        0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
        0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
        0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
        0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
        0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
        0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
        0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
        0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
        0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
        0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
        0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3,
        0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
        0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5,
        0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
        0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
        0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
    ]

    def __init__(self) -> None:
        self._h = self._INITIAL_HASH.copy()
        self._buffer = bytearray()
        self._message_length = 0

    @staticmethod
    def _right_rotate(value: int, bits: int) -> int:
        return (
            (value >> bits) |
            (value << (32 - bits))
        ) & 0xFFFFFFFF

    @classmethod
    def _ch(cls, x: int, y: int, z: int) -> int:
        return (x & y) ^ (~x & z)

    @classmethod
    def _maj(cls, x: int, y: int, z: int) -> int:
        return (x & y) ^ (x & z) ^ (y & z)

    @classmethod
    def _big_sigma0(cls, x: int) -> int:
        return (
            cls._right_rotate(x, 2) ^
            cls._right_rotate(x, 13) ^
            cls._right_rotate(x, 22)
        )

    @classmethod
    def _big_sigma1(cls, x: int) -> int:
        return (
            cls._right_rotate(x, 6) ^
            cls._right_rotate(x, 11) ^
            cls._right_rotate(x, 25)
        )

    @classmethod
    def _small_sigma0(cls, x: int) -> int:
        return (
            cls._right_rotate(x, 7) ^
            cls._right_rotate(x, 18) ^
            (x >> 3)
        )

    @classmethod
    def _small_sigma1(cls, x: int) -> int:
        return (
            cls._right_rotate(x, 17) ^
            cls._right_rotate(x, 19) ^
            (x >> 10)
        )

    def _process_block(self, block: bytes) -> None:
        words = list(struct.unpack(">16I", block))

        for index in range(16, 64):
            value = (
                self._small_sigma1(words[index - 2])
                + words[index - 7]
                + self._small_sigma0(words[index - 15])
                + words[index - 16]
            ) & 0xFFFFFFFF

            words.append(value)

        a, b, c, d, e, f, g, h = self._h

        for index in range(64):
            temp1 = (
                h
                + self._big_sigma1(e)
                + self._ch(e, f, g)
                + self._K[index]
                + words[index]
            ) & 0xFFFFFFFF

            temp2 = (
                self._big_sigma0(a)
                + self._maj(a, b, c)
            ) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        self._h[0] = (self._h[0] + a) & 0xFFFFFFFF
        self._h[1] = (self._h[1] + b) & 0xFFFFFFFF
        self._h[2] = (self._h[2] + c) & 0xFFFFFFFF
        self._h[3] = (self._h[3] + d) & 0xFFFFFFFF
        self._h[4] = (self._h[4] + e) & 0xFFFFFFFF
        self._h[5] = (self._h[5] + f) & 0xFFFFFFFF
        self._h[6] = (self._h[6] + g) & 0xFFFFFFFF
        self._h[7] = (self._h[7] + h) & 0xFFFFFFFF

    def update(self, data: bytes) -> None:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("SHA256.update() requires bytes")

        self._message_length += len(data)
        self._buffer.extend(data)

        while len(self._buffer) >= 64:
            block = bytes(self._buffer[:64])
            del self._buffer[:64]

            self._process_block(block)

    def _finalize(self) -> bytes:
        copied = SHA256()
        copied._h = self._h.copy()
        copied._buffer = self._buffer.copy()
        copied._message_length = self._message_length

        bit_length = copied._message_length * 8

        copied._buffer.append(0x80)

        while len(copied._buffer) % 64 != 56:
            copied._buffer.append(0x00)

        copied._buffer.extend(
            bit_length.to_bytes(8, byteorder="big")
        )

        while copied._buffer:
            block = bytes(copied._buffer[:64])
            del copied._buffer[:64]

            copied._process_block(block)

        return b"".join(
            value.to_bytes(4, byteorder="big")
            for value in copied._h
        )

    def digest(self) -> bytes:
        return self._finalize()

    def hexdigest(self) -> str:
        return self.digest().hex()

    @classmethod
    def hash(cls, data: bytes) -> str:
        sha = cls()
        sha.update(data)
        return sha.hexdigest()