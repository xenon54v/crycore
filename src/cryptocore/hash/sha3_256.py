class SHA3_256:
    RATE = 136
    OUTPUT_SIZE = 32
    MASK_64 = 0xFFFFFFFFFFFFFFFF

    _ROUND_CONSTANTS = [
        0x0000000000000001,
        0x0000000000008082,
        0x800000000000808A,
        0x8000000080008000,
        0x000000000000808B,
        0x0000000080000001,
        0x8000000080008081,
        0x8000000000008009,
        0x000000000000008A,
        0x0000000000000088,
        0x0000000080008009,
        0x000000008000000A,
        0x000000008000808B,
        0x800000000000008B,
        0x8000000000008089,
        0x8000000000008003,
        0x8000000000008002,
        0x8000000000000080,
        0x000000000000800A,
        0x800000008000000A,
        0x8000000080008081,
        0x8000000000008080,
        0x0000000080000001,
        0x8000000080008008,
    ]

    _ROTATION_OFFSETS = [
        [0, 36, 3, 41, 18],
        [1, 44, 10, 45, 2],
        [62, 6, 43, 15, 61],
        [28, 55, 25, 21, 56],
        [27, 20, 39, 8, 14],
    ]

    def __init__(self) -> None:
        self._state = [0] * 25
        self._buffer = bytearray()

    @classmethod
    def _rotate_left(cls, value: int, shift: int) -> int:
        shift %= 64

        if shift == 0:
            return value & cls.MASK_64

        return (
            (value << shift)
            | (value >> (64 - shift))
        ) & cls.MASK_64

    @classmethod
    def _keccak_f(cls, state: list[int]) -> None:
        for round_constant in cls._ROUND_CONSTANTS:
            # Theta
            c = [
                state[x]
                ^ state[x + 5]
                ^ state[x + 10]
                ^ state[x + 15]
                ^ state[x + 20]
                for x in range(5)
            ]

            d = [
                c[(x - 1) % 5]
                ^ cls._rotate_left(c[(x + 1) % 5], 1)
                for x in range(5)
            ]

            for x in range(5):
                for y in range(5):
                    state[x + 5 * y] ^= d[x]

            # Rho + Pi
            b = [0] * 25

            for x in range(5):
                for y in range(5):
                    new_x = y
                    new_y = (2 * x + 3 * y) % 5

                    b[new_x + 5 * new_y] = cls._rotate_left(
                        state[x + 5 * y],
                        cls._ROTATION_OFFSETS[x][y],
                    )

            # Chi
            for x in range(5):
                for y in range(5):
                    state[x + 5 * y] = (
                        b[x + 5 * y]
                        ^ (
                            (~b[(x + 1) % 5 + 5 * y])
                            & b[(x + 2) % 5 + 5 * y]
                        )
                    ) & cls.MASK_64

            # Iota
            state[0] ^= round_constant

    def _absorb_block(self, block: bytes) -> None:
        for index in range(self.RATE // 8):
            start = index * 8
            lane = int.from_bytes(
                block[start:start + 8],
                byteorder="little",
            )

            self._state[index] ^= lane

        self._keccak_f(self._state)

    def update(self, data: bytes) -> None:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("SHA3_256.update() requires bytes")

        self._buffer.extend(data)

        while len(self._buffer) >= self.RATE:
            block = bytes(self._buffer[:self.RATE])
            del self._buffer[:self.RATE]

            self._absorb_block(block)

    def _finalize(self) -> bytes:
        copied = SHA3_256()
        copied._state = self._state.copy()
        copied._buffer = self._buffer.copy()

        padding_length = self.RATE - len(copied._buffer)

        padding = bytearray(padding_length)
        padding[0] = 0x06
        padding[-1] |= 0x80

        copied._buffer.extend(padding)

        while copied._buffer:
            block = bytes(copied._buffer[:self.RATE])
            del copied._buffer[:self.RATE]

            copied._absorb_block(block)

        output = bytearray()

        while len(output) < self.OUTPUT_SIZE:
            for index in range(self.RATE // 8):
                output.extend(
                    copied._state[index].to_bytes(
                        8,
                        byteorder="little",
                    )
                )

                if len(output) >= self.OUTPUT_SIZE:
                    break

            if len(output) < self.OUTPUT_SIZE:
                self._keccak_f(copied._state)

        return bytes(output[:self.OUTPUT_SIZE])

    def digest(self) -> bytes:
        return self._finalize()

    def hexdigest(self) -> str:
        return self.digest().hex()

    @classmethod
    def hash(cls, data: bytes) -> str:
        sha3 = cls()
        sha3.update(data)
        return sha3.hexdigest()