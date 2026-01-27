
class Hash:
    # should f_a, f_b in int or float? -> Probably int

    @staticmethod
    def encode(f_a:float, f_b:float, delta_t_frames) -> int:
        """
        takes in f_a, f_b, t_f and returns encoded hash value 

        f_a, f_b: frequency bin indices (int)
        delta_t_frames: integer difference in frames (anchor->target)
        """
        f_a = int(f_a) & ((1 << 11) - 1)
        f_b = int(f_b) & ((1 << 11) - 1)
        dt  = int(delta_t_frames) & ((1 << 10) - 1)

        hash_val = (f_a << (11 + 10)) | (f_b << 10) | dt
        return hash_val & 0xFFFFFFFF

    @staticmethod
    def decode(hash_val) -> tuple[int, int, int]:
        dt  = hash_val & ((1 << 10) - 1)
        f_b = (hash_val >> 10) & ((1 << 11) - 1)
        f_a = (hash_val >> (10 + 11)) & ((1 << 11) - 1)
        return f_a, f_b, dt