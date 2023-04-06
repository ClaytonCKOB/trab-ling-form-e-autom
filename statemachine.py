from re import search, sub


class StateMachine:
    def __init__(self):
        """
        Sets the state machine's default properties
        """
        self.current_state = "q0"
        self.final_states = ["q0"]
        self.current_event = "login"
        self.come_back_state = "q0"
        self.events = {
            "login": self.login,
            "home": self.home,
            "depositar-poupanca": self.depositarPoupanca,
            "sacar-poupanca": self.sacarPoupanca,
            "fazer-emprestimo": self.fazerEmprestimo,
            "pagar-parcela": self.pagarParcela,
            "transferencia": self.transferencia,
            "pagamento": self.pagamento,
            "investimento": self.investimento,
            "pix": self.pix,
        }

    def analyzeEvent(self, old_state, required, goal, text):
        """
        Analyzes if the transition exists from the current state.
        Returns message with information about its success.
        """
        self.come_back_state = old_state
        if self.current_state in required:
            self.current_state = goal
            if goal == "q1":
                self.current_event = "home"
            return {
                "text": text,
                "old_state": old_state,
                "dest_state": self.current_state,
                "cur_state": self.current_state,
                "error": 0,
            }
        else:
            return self.errorMessage(goal)

    def errorMessage(self, cur_state):
        """
        Resets state and event and returns an error message
        """
        old_state = self.current_state
        self.reset()
        return {
            "text": "Erro: movimento não permitido",
            "old_state": old_state,
            "dest_state": cur_state,
            "cur_state": "q0",
            "error": 1,
        }

    def reset(self):
        """
        Resets state machine to the first state and event
        """
        self.current_state = "q0"
        self.current_event = "login"

    def execute(self, palavra):
        """
        Redirects the input word to the function responsible for the current event
        """
        return self.events[self.current_event](palavra)

    def home(self, palavra):
        """
        Performs the transition of states, if possible, and returns a message about its success.
        Additionally, in case of error, resets to the login event.
        """
        old_state = self.current_state

        if search("^encerrar$", palavra):
            self.current_event = "login"
            return self.analyzeEvent(old_state, ["q1"], "q0", "Logout realizado.")

        elif search("^pix$", palavra):
            self.current_event = "pix"
            return self.analyzeEvent(old_state, ["q1"], "q33", "Pix iniciado.")

        elif search("^depositar poupanca$", palavra):
            self.current_event = "depositar-poupanca"
            return self.analyzeEvent(old_state, ["q1"], "q15", "Depósito iniciado.")

        elif search("^sacar poupanca$", palavra):
            self.current_event = "sacar-poupanca"
            return self.analyzeEvent(old_state, ["q1"], "q57", "Saque iniciado.")

        elif search("^fazer emprestimo$", palavra):
            self.current_event = "fazer-emprestimo"
            return self.analyzeEvent(old_state, ["q1"], "q18", "Empréstimo iniciado.")

        elif search("^pagar parcela$", palavra):
            self.current_event = "pagar-parcela"
            return self.analyzeEvent(old_state, ["q1"], "q30", "Empréstimo iniciado.")

        elif search("^transferencia$", palavra):
            self.current_event = "transferencia"
            return self.analyzeEvent(
                old_state, ["q1"], "q51", "Transferência iniciada."
            )

        elif search("^pagamento$", palavra):
            self.current_event = "pagamento"
            return self.analyzeEvent(old_state, ["q1"], "q23", "Pagamento iniciado.")

        elif search("^investimento$", palavra):
            self.current_event = "investimento"
            return self.analyzeEvent(old_state, ["q1"], "q2", "Investimento iniciado.")

        else:
            return self.errorMessage("q0")

    def login(self, palavra):
        """
        Performs the transition of states, if possible, and returns a message about its success.
        """
        if search("^senha$", palavra):
            self.current_event = "home"
            return self.analyzeEvent("q0", ["q0"], "q1", "Login realizado.")
        else:
            self.current_event = "home"
            return self.errorMessage("q0")

    def pix(self, palavra):
        """
        Performs the transition of states, if possible, and returns a message about its success.
        Additionally, in case of error, resets to the login event.
        """
        old_state = self.current_state

        if search("^voltar$", palavra):
            transitions = {
                "q47": "q45",
                "q49": "q47",
                "q33": "q1",
                "q42": "q41",
                "q41": "q40",
                "q39": "q40",
                "q34": "q33",
                "q45": "q33",
                "q40": "q33",
            }
            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Chave inserida.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^cancela$", palavra):
            return self.analyzeEvent(
                old_state,
                ["q38", "q41", "q42", "q48", "q47", "q35", "q39", "q40", "q37", "q49"],
                "q33",
                "Pix cancelado.",
            )

        elif search("^chave$", palavra):
            transitions = {"q41": "q44", "q39": "q38", "q45": "q46"}
            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Chave inserida.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^valor$", palavra):
            transitions = {"q36": "q44", "q47": "q48"}
            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Valor inserido.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^senha$", palavra):
            transitions = {"q35": "q36", "q42": "q43", "q38": "q37", "q49": "q50"}
            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Senha inserida.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^\[invalido\]$", palavra):
            # transitions = {'q46':'q42', 'q49': 'q48', 'q50': 'q39', 'q51': 'q40', 'q43': 'q35', 'q44': 'q36', 'q45':'q37'}
            transitions = {
                "q36": "q35",
                "q44": "q41",
                "q43": "q42",
                "q38": "q37",
                "q37": "q38",
                "q46": "q45",
                "q48": "q47",
                "q50": "q49",
            }
            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Operação inválida.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^\[valido\]$", palavra):
            transitions = {
                "q36": "q33",
                "q34": "q35",
                "q44": "q42",
                "q43": "q33",
                "q37": "q33",
                "q46": "q47",
                "q48": "q49",
                "q50": "q33",
            }
            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Operação válida.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^\[leitura\]$", palavra):
            return self.analyzeEvent(old_state, ["q34"], "q34", "Lendo...")

        elif search("^excluir$", palavra):
            return self.analyzeEvent(old_state, ["q40"], "q39", "Exclusão de chave.")

        elif search("^chaves$", palavra):
            transitions = {"q33": "q40"}
            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Configuração de chaves.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^cadastrar$", palavra):
            return self.analyzeEvent(old_state, ["q40"], "q41", "Cadastro iniciado.")

        elif search("^qr code$", palavra):
            return self.analyzeEvent(old_state, ["q33"], "q34", "Qr code inserido.")

        elif search("^pagar$", palavra):
            return self.analyzeEvent(old_state, ["q33"], "q45", "Pagamento iniciado.")
        else:
            self.current_event = "login"
            return self.errorMessage("q0")

    def sacarPoupanca(self, palavra):
        """
        Performs the transition of states, if possible, and returns a message about its success.
        Additionally, in case of error, resets to the login event.
        """
        old_state = self.current_state

        if search("^voltar$", palavra):
            return self.analyzeEvent(
                old_state, ["q57", "q58"], self.come_back_state, "Retorno da operação."
            )

        elif search("^cancela$", palavra):
            return self.analyzeEvent(
                old_state, ["q57", "q58"], "q1", "Saque cancelado."
            )

        elif search("^valor$", palavra):
            return self.analyzeEvent(old_state, ["q57"], "q58", "Valor inserido.")

        elif search("^senha$", palavra):
            return self.analyzeEvent(old_state, ["q58"], "q59", "Senha inserida.")

        elif search("^\[invalido\]$", palavra):
            return self.analyzeEvent(old_state, ["q59"], "q58", "Senha incorreta.")

        elif search("^\[valido\]$", palavra):
            self.current_event = "home"
            return self.analyzeEvent(old_state, ["q59"], "q1", "Saque realizado.")

        else:
            self.current_event = "login"
            return self.errorMessage("q0")

    def depositarPoupanca(self, palavra):
        """
        Performs the transition of states, if possible, and returns a message about its success.
        Additionally, in case of error, resets to the login event.
        """
        old_state = self.current_state

        if search("^voltar$", palavra):
            return self.analyzeEvent(
                old_state, ["q15", "q16"], self.come_back_state, "Retorno da operação."
            )

        elif search("^cancela$", palavra):
            return self.analyzeEvent(
                old_state, ["q15", "q16"], "q1", "Deposito cancelado."
            )

        elif search("^valor$", palavra):
            return self.analyzeEvent(old_state, ["q15"], "q16", "Valor inserido.")

        elif search("^senha$", palavra):
            return self.analyzeEvent(old_state, ["q16"], "q17", "Senha inserida.")

        elif search("^\[invalido\]$", palavra):
            return self.analyzeEvent(old_state, ["q17"], "q16", "Senha incorreta.")

        elif search("^\[valido\]$", palavra):
            self.current_event = "home"
            return self.analyzeEvent(old_state, ["q17"], "q1", "Depósito realizado.")

        else:
            self.current_event = "home"
            return self.errorMessage("q0")

    def fazerEmprestimo(self, palavra):
        """
        Performs the transition of states, if possible, and returns a message about its success.
        Additionally, in case of error, resets to the login event.
        """
        old_state = self.current_state

        if search("^voltar$", palavra):
            return self.analyzeEvent(
                old_state,
                ["q18", "q19", "q20", "q21"],
                self.come_back_state,
                "Retorno da operação.",
            )

        elif search("^cancela$", palavra):
            return self.analyzeEvent(
                old_state, ["q18", "q19", "q20", "q21"], "q1", "Empréstimo cancelado."
            )

        elif search("^valor$", palavra):
            return self.analyzeEvent(old_state, ["q18"], "q19", "Valor inserido.")

        elif search("^prazo$", palavra):
            return self.analyzeEvent(old_state, ["q19"], "q20", "Prazo inserido.")

        elif search("^parcelas$", palavra):
            return self.analyzeEvent(old_state, ["q20"], "q21", "Parcelas inseridas.")

        elif search("^senha$", palavra):
            return self.analyzeEvent(old_state, ["q21"], "q22", "Senha inserida.")

        elif search("^\[invalido\]$", palavra):
            return self.analyzeEvent(old_state, ["q22"], "q21", "Senha incorreta.")

        elif search("^\[valido\]$", palavra):
            self.current_event = "home"
            return self.analyzeEvent(old_state, ["q22"], "q1", "Empréstimo realizado.")

        else:
            self.current_event = "login"
            return self.errorMessage("q0")

    def pagarParcela(self, palavra):
        """
        Performs the transition of states, if possible, and returns a message about its success.
        Additionally, in case of error, resets to the login event.
        """
        old_state = self.current_state

        if search("^voltar$", palavra):
            transitions = {"q31": "q30", "q30": "q1"}
            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Retorno da operação.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^cancela$", palavra):
            return self.analyzeEvent(
                old_state, ["q30", "q31"], "q1", "Pagamento cancelado."
            )

        elif search("^id emprestimo$", palavra):
            return self.analyzeEvent(
                old_state, ["q30"], "q31", "Empréstimo selecionado."
            )

        elif search("^senha$", palavra):
            return self.analyzeEvent(old_state, ["q31"], "q32", "Senha inserida.")

        elif search("^\[invalido\]$", palavra):
            return self.analyzeEvent(old_state, ["q32"], "q31", "Senha incorreta.")

        elif search("^\[valido\]$", palavra):
            self.current_event = "home"
            return self.analyzeEvent(old_state, ["q32"], "q1", "Pagamento realizado.")

        else:
            self.current_event = "login"
            return self.errorMessage("q0")

    def transferencia(self, palavra):
        """
        Performs the transition of states, if possible, and returns a message about its success.
        Additionally, in case of error, resets to the login event.
        """
        old_state = self.current_state

        if search("^voltar$", palavra):
            transitions = {"q53": "q51", "q55": "q53", "q51": "q1"}

            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Retorno da Operação",
                )
            else:
                return self.errorMessage("q0")

        elif search("^cancela$", palavra):
            return self.analyzeEvent(
                old_state, ["q51", "q53", "q55"], "q1", "Transferência cancelada."
            )

        elif search("^conta$", palavra):
            return self.analyzeEvent(old_state, ["q51"], "q52", "Conta inserida.")

        elif search("^valor$", palavra):
            return self.analyzeEvent(old_state, ["q53"], "q54", "Valor inserido.")

        elif search("^senha$", palavra):
            return self.analyzeEvent(old_state, ["q55"], "q56", "Senha inserida.")

        elif search("^\[invalido\]$", palavra):
            transitions = {"q52": "q51", "q54": "q53", "q56": "q55"}

            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Operação inválida.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^\[valido\]$", palavra):
            transitions = {"q52": "q53", "q54": "q55", "q56": "q1"}

            if self.current_state in transitions.keys():
                if self.current_state == "q56":
                    return self.analyzeEvent(
                        old_state,
                        [self.current_state],
                        transitions[self.current_state],
                        "Transferência finalizada.",
                    )
                else:
                    return self.analyzeEvent(
                        old_state,
                        [self.current_state],
                        transitions[self.current_state],
                        "Operação válida.",
                    )
            else:
                return self.errorMessage("q0")
        else:
            self.current_event = "login"
            return self.errorMessage("q0")

    def pagamento(self, palavra):
        """
        Performs the transition of states, if possible, and returns a message about its success.
        Additionally, in case of error, resets to the login event.
        """
        old_state = self.current_state

        if search("^voltar$", palavra):
            transitions = {"q23": "q1", "q28": "q23", "q24": "q28", "q26": "q24"}
            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Retorno da operação.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^cancela$", palavra):
            return self.analyzeEvent(
                old_state, ["q24", "q26"], "q1", "Transferência cancelada."
            )

        elif search("^\[leitura\]$", palavra):
            return self.analyzeEvent(old_state, ["q23"], "q23", "Realizando leitura.")

        elif search("^codigo de barras$", palavra):
            return self.analyzeEvent(
                old_state, ["q28"], "q29", "Lendo código de barras."
            )

        elif search("^data de pagamento$", palavra):
            return self.analyzeEvent(
                old_state, ["q24"], "q25", "Data de pagamento inserida."
            )

        elif search("^manual$", palavra):
            return self.analyzeEvent(old_state, ["q23"], "q28", "Valor inserido.")

        elif search("^senha$", palavra):
            return self.analyzeEvent(old_state, ["q26"], "q27", "Senha inserida.")

        elif search("^\[invalido\]$", palavra):
            transitions = {"q29": "q28", "q25": "q24", "q27": "q26"}

            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Operação inválida.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^\[valido\]$", palavra):
            transitions = {"q23": "q24", "q29": "q24", "q25": "q26", "q27": "q1"}

            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Operação válida.",
                )
            else:
                return self.errorMessage("q0")
        else:
            self.current_event = "login"
            return self.errorMessage("q0")

    def investimento(self, palavra):
        """
        Performs the transition of states, if possible, and returns a message about its success.
        Additionally, in case of error, resets to the login event.
        """
        old_state = self.current_state

        if search("^voltar$", palavra):
            return self.analyzeEvent(
                old_state,
                ["q10", "q13", "q11", "q3", "q8", "q4", "q2"],
                self.come_back_state,
                "Retorno da operação.",
            )

        elif search("^fixa$", palavra):
            return self.analyzeEvent(
                old_state, ["q2"], "q10", "Transferência cancelada."
            )

        elif search("^variavel$", palavra):
            return self.analyzeEvent(
                old_state, ["q2"], "q3", "Investimento em renda variável iniciado."
            )

        elif search("^tesouro direto$", palavra):
            return self.analyzeEvent(
                old_state, ["q10"], "q13", "Investimento em tesouro direto iniciado."
            )

        elif search("^fiis$", palavra):
            return self.analyzeEvent(
                old_state, ["q3"], "q8", "Investimento em FIIS selecionado."
            )

        elif search("^acoes$", palavra):
            return self.analyzeEvent(
                old_state, ["q3"], "q4", "Investimento em açoes selecionado."
            )

        elif search("^senha$", palavra):
            return self.analyzeEvent(old_state, ["q6"], "q7", "Senha inserida.")

        elif search("^codigo$", palavra):
            transitions = {"q13": "q14", "q11": "q12", "q4": "q5", "q8": "q9"}

            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Código inserido.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^cdb$", palavra):
            return self.analyzeEvent(
                old_state, ["q10"], "q11", "Investimento em CDB selecionado."
            )

        elif search("^\[invalido\]$", palavra):
            transitions = {
                "q14": "q13",
                "q12": "q11",
                "q9": "q8",
                "q5": "q4",
                "q7": "q6",
            }

            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Operação inválida.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^\[valido\]$", palavra):
            transitions = {"q5": "q6", "q9": "q6", "q12": "q6", "q14": "q6", "q7": "q1"}

            if self.current_state in transitions.keys():
                return self.analyzeEvent(
                    old_state,
                    [self.current_state],
                    transitions[self.current_state],
                    "Operação válida.",
                )
            else:
                return self.errorMessage("q0")

        elif search("^cancela$", palavra):
            return self.analyzeEvent(
                old_state, ["q2", "q6"], "q1", "Investimento cancelado."
            )

        else:
            self.current_event = "login"
            return self.errorMessage("q0")
