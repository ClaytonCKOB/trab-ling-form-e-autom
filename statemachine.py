from re import search, sub

class StateMachine:
    def __init__(self):
        self.current_state = 'q0'
        self.final_states = ['q0']
        self.current_event = 'login'
        self.come_back_state = 'q0'
        self.events = {
            'login': self.login, 
            'home': self.home,
            'depositar-poupanca': self.depositarPoupanca,
            'sacar-poupanca': self.sacarPoupanca,
            'fazer-emprestimo': self.fazerEmprestimo,
            'pagar-parcela': self.pagarParcela,
            'transferencia': self.transferencia,
            'pagamento': self.pagamento
        }

    def execute(self, palavra):
        return self.events[self.current_event](palavra)

    def home(self, palavra):
        old_state = self.current_state

        if(search('^encerrar', palavra)):
            self.current_event = 'home'
            self.analyzeEvent(old_state, ['q11'], 'q0', 'Logout realizado.')

        elif(search('^pix', palavra)):
            self.current_event = 'pix'
            self.analyzeEvent(old_state, ['q11'], 'q1', 'Pix iniciado.')

        elif(search('^depositar poupanca')):
            self.current_event = 'depositar-poupanca'
            self.analyzeEvent(old_state, ['q11'], 'q1', 'Depósito iniciado.')

        elif(search('^saque poupanca')):
            self.current_event = 'saque-poupanca'
            self.analyzeEvent(old_state, ['q11'], 'q1', 'Saque iniciado.')
        
        elif(search('^fazer emprestimo')):
            self.current_event = 'fazer-poupanca'
            self.analyzeEvent(old_state, ['q11'], 'q1', 'Empréstimo iniciado.')
        
        elif(search('^pagar parcela')):
            self.current_event = 'pagar-parcela'
            self.analyzeEvent(old_state, ['q11'], 'q1', 'Empréstimo iniciado.')
        
        elif(search('^transferencia')):
            self.current_event = 'transferencia'
            self.analyzeEvent(old_state, ['q11'], 'q1', 'Transferência iniciada.')
        
        elif(search('^pagamento')):
            self.current_event = 'pagamento'
            self.analyzeEvent(old_state, ['q11'], 'q1', 'Pagamento iniciado.')

    
    def login(self, palavra):
        if(search('^senha', palavra)):
            self.current_event = 'home'
            self.analyzeEvent('q0', ['q0'], 'q11', 'Logout realizado.')
        else:
            self.current_event = 'home'
            return self.errorMessage('q0')

    def pix(self, palavra):
        old_state = self.current_state
        
        if(search('^volta', palavra)):
            self.analyzeEvent(old_state, ['q1', 'q2'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q1','q2'], 'q11', 'Pix cancelado.')
        
        elif(search('^chave', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Chave inserida.')
        
        elif(search('^valor', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q2'], 'q3', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            return self.analyzeEvent(old_state, ['q3'], 'q2', 'Senha incorreta.')

        elif(search('^\[valido\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q3'], 'q11', 'Transferência realizada.')
        
        elif(search('^\[lendo\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q3'], 'q11', 'Lendo...')

        elif(search('^\[leitura\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q3'], 'q11', 'Leitura realizado')

        elif(search('^excluir', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Chave excluída.')
        
        elif(search('^cadastrar', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Chave cadastrada.')

        elif(search('^qr code', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Qr code inserido.')
        
        elif(search('^pagar', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Pagamento iniciado.')

        else:
            self.current_event = 'login'
            return self.errorMessage('q0')

    def sacarPoupanca(self, palavra):
        old_state = self.current_state
        
        if(search('^volta', palavra)):
            self.analyzeEvent(old_state, ['q1', 'q2'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q1', 'q2'], 'q11', 'Saque cancelado.')
        
        elif(search('^valor', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q2'], 'q3', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            return self.analyzeEvent(old_state, ['q3'], 'q2', 'Senha incorreta.')

        elif(search('^\[valido\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q3'], 'q11', 'Saque realizado.')

        else:
            self.current_event = 'login'
            return self.errorMessage('q0')

    def depositarPoupanca(self, palavra):
        old_state = self.current_state
        
        if(search('^volta', palavra)):
            self.analyzeEvent(old_state, ['q1', 'q2'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q1','q2'], 'q11', 'Deposito cancelado.')
        
        elif(search('^valor', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q2'], 'q3', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            return self.analyzeEvent(old_state, ['q3'], 'q2', 'Senha incorreta.')

        elif(search('^\[valido\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q3'], 'q11', 'Depósito realizado.')

        else:
            self.current_event = 'home'
            return self.errorMessage('q0')

    def fazerEmprestimo(self, palavra):
        old_state = self.current_state
        
        if(search('^volta', palavra)):
            self.analyzeEvent(old_state, ['q1', 'q2'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q1', 'q2', 'q3', 'q4'], 'q11', 'Empréstimo cancelado.')

        elif(search('^valor', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Valor inserido.')
        
        elif(search('^prazo', palavra)):
            return self.analyzeEvent(old_state, ['q2'], 'q3', 'Prazo inserido.')
        
        elif(search('^parcelas', palavra)):
            return self.analyzeEvent(old_state, ['q2'], 'q3', 'Parcelas inseridas.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q2'], 'q3', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            return self.analyzeEvent(old_state, ['q3'], 'q2', 'Senha incorreta.')

        elif(search('^\[valido\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q3'], 'q11', 'Empréstimo realizado.')  
        
        else:
            self.current_event = 'login'
            return self.errorMessage('q0')

    def pagarParcela(self, palavra):
        old_state = self.current_state
        
        if(search('^volta', palavra)):
            self.analyzeEvent(old_state, ['q1', 'q2'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q1','q2'], 'q11', 'Pagamento cancelado.')
        
        elif(search('^id emprestimo', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q2'], 'q3', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            return self.analyzeEvent(old_state, ['q3'], 'q2', 'Senha incorreta.')

        elif(search('^\[valido\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q3'], 'q11', 'Pagamento realizado.')

        else:
            self.current_event = 'login'
            return self.errorMessage('q0')

    def transferencia(self, palavra):
        old_state = self.current_state
        
        if(search('^volta', palavra)):
            self.analyzeEvent(old_state, ['q1', 'q2'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q1','q2'], 'q11', 'Transferência cancelada.')
        
        elif(search('^conta', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Conta inserida.')
        
        elif(search('^valor', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q2'], 'q3', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            return self.analyzeEvent(old_state, ['q3'], 'q2', 'Senha incorreta.')

        elif(search('^\[valido\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q3'], 'q11', 'Transferência realizada.')

        else:
            self.current_event = 'login'
            return self.errorMessage('q0')
    
    def pagamento(self, palavra):
        old_state = self.current_state
        
        if(search('^volta', palavra)):
            self.analyzeEvent(old_state, ['q1', 'q2'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q1','q2'], 'q11', 'Transferência cancelada.')
        
        elif(search('^leitura', palavra)):
            self.analyzeEvent(old_state, ['q1'], 'q1', 'Realizando leitura.')
        
        elif(search('^codigo de barras', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Lendo código de barras.')
        
        elif(search('^data de pagamento', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Data de pagamento inserida.')
        
        elif(search('^pagamento', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Pagamento realizado.')

        elif(search('^valor', palavra)):
            return self.analyzeEvent(old_state, ['q1'], 'q2', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q2'], 'q3', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            return self.analyzeEvent(old_state, ['q3'], 'q2', 'Senha incorreta.')

        elif(search('^\[valido\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q3'], 'q11', 'Transferência realizada.')

        else:
            self.current_event = 'login'
            return self.errorMessage('q0')

    def analyzeEvent(self, old_state, required, goal, text):
        self.come_back_state = old_state
        if self.current_state in required:
            self.current_state = goal
            return {'text': text, 'old_state': old_state, 'dest_state': self.current_state, 'cur_state': self.current_state, 'error': 0}
        else:
            return  self.errorMessage(goal)

    def errorMessage(self, cur_state):
        old_state = self.current_state
        self.current_state = 'q0'
        return {'text': 'Erro: movimento não permitido', 'old_state':old_state, 'dest_state':cur_state, 'cur_state': 'q0','error': 1}