class EnrollmentState:
    def __init__(self):
        self.has_begin_enroll = False
        self.capture_count = 0
        self.has_finalize = False

    def on_update_state(self, begin_enroll: bool = None, capture_count: int = None, finalize: bool = None):
        """
        Atualiza o estado do processo de cadastro.
        :param begin_enroll: Define se o processo de cadastro começou.
        :param capture_count: Atualiza a contagem de capturas.
        :param finalize: Define se o processo foi finalizado.
        
        """
        if begin_enroll is not None:
            self.has_begin_enroll = begin_enroll
        if capture_count is not None:
            self.capture_count = capture_count
        if finalize is not None:
            self.has_finalize = finalize

    def __repr__(self):
        return (f"EnrollmentState(has_begin_enroll={self.has_begin_enroll}, "
                f"capture_count={self.capture_count}, has_finalize={self.has_finalize})")

    def on_update_state(self):
        print("Updating enrollment state...")
