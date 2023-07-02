class s_t:
    def __init__(self, s: int):
        self.d = int(s // (24*60*60))
        self.h = int((s - self.d * (24*60*60)) // (60*60))
        self.m = int((s - self.d * (24*60*60) - self.h * (60*60)) // (60))
        self.s = int((s - self.d * (24*60*60) - self.h * (60*60) - self.m * 60))

        _t = []
        if self.d > 0:
            _t.append(f"{self.d} днів")
        if self.h > 0:
            _t.append(f"{self.h} год")
        if self.m > 0:
            _t.append(f"{self.m} хв")
        if self.s > 0:
            _t.append(f"{self.s} сек")

        self._t = " ".join(_t)

    def __str__(self):
        return self._t

    def __repr__(self):
        return self._t