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
            'pagamento': self.pagamento,
            'investimento': self.investimento
        }

    def execute(self, palavra):
        return self.events[self.current_event](palavra)

    def home(self, palavra):
        old_state = self.current_state

        if(search('^encerrar', palavra)):
            self.current_event = 'home'
            self.analyzeEvent(old_state, ['q1'], 'q0', 'Logout realizado.')

        elif(search('^pix', palavra)):
            self.current_event = 'pix'
            self.analyzeEvent(old_state, ['q1'], 'q34', 'Pix iniciado.')

        elif(search('^depositar poupanca')):
            self.current_event = 'depositar-poupanca'
            self.analyzeEvent(old_state, ['q1'], 'q1', 'Depósito iniciado.')

        elif(search('^sacar poupanca')):
            self.current_event = 'saque-poupanca'
            self.analyzeEvent(old_state, ['q1'], 'q57', 'Saque iniciado.')
        
        elif(search('^fazer emprestimo')):
            self.current_event = 'fazer-emprestimo'
            self.analyzeEvent(old_state, ['q1'], 'q18', 'Empréstimo iniciado.')
        
        elif(search('^pagar parcela')):
            self.current_event = 'pagar-parcela'
            self.analyzeEvent(old_state, ['q1'], 'q30', 'Empréstimo iniciado.')
        
        elif(search('^transferencia')):
            self.current_event = 'transferencia'
            self.analyzeEvent(old_state, ['q1'], 'q51', 'Transferência iniciada.')
        
        elif(search('^pagamento')):
            self.current_event = 'pagamento'
            self.analyzeEvent(old_state, ['q1'], 'q23', 'Pagamento iniciado.')

        elif(search('^investimento')):
            self.current_event = 'investimento'
            self.analyzeEvent(old_state, ['q1'], 'q2', 'Pagamento iniciado.')


    def login(self, palavra):
        if(search('^senha', palavra)):
            self.current_event = 'home'
            self.analyzeEvent('q0', ['q0'], 'q11', 'Logout realizado.')
        else:
            self.current_event = 'home'
            return self.errorMessage('q0')

    def pix(self, palavra):
        old_state = self.current_state
        
        if(search('^voltar', palavra)):
            return self.analyzeEvent(old_state, ['q34', 'q35', 'q36', 'q37', 'q47', 'q39', 'q40'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            return self.analyzeEvent(old_state, ['q42','q48', 'q47', 'q36', 'q39', 'q40', 'q37'], 'q11', 'Pix cancelado.')
        
        elif(search('^chave', palavra)):
            if(self.current_state == 'q47'):
                return self.analyzeEvent(old_state, ['q47'], 'q48', 'Chave inserida.')
            elif(self.current_state == 'q39'):
                return self.analyzeEvent(old_state, ['q39'], 'q40', 'Chave inserida.')
            elif(self.current_state == 'q35'):
                return self.analyzeEvent(old_state, ['q35'], 'q43', 'Chave inserida.')
            else:
                return self.errorMessage('?')

        elif(search('^valor', palavra)):
            return self.analyzeEvent(old_state, ['q36'], 'q44', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            transitions = {'q42': 'q46', 'q48': 'q49', 'q40': 'q51', 'q37': 'q45'}
            
            if(self.current_state in transitions.keys()):
                return self.analyzeEvent(old_state, [self.current_state], transitions[self.current_state], 'Senha inserida.')
            else:
                return self.errorMessage('?')
         
        elif(search('^\[invalido\]', palavra)):
            transitions = {'q46':'q42', 'q49': 'q48', 'q50': 'q39', 'q51': 'q40', 'q43': 'q35', 'q44': 'q36', 'q45':'q37'}
            
            if(self.current_state in transitions.keys()):
                return self.analyzeEvent(old_state, [self.current_state], transitions[self.current_state], 'Senha inserida.')
            else:
                return self.errorMessage('?')

        elif(search('^\[valido\]', palavra)):
            transitions = {'q46':'q34', 'q49': 'q34', 'q50':'q40', 'q51':'q34', 'q43':'q36', 'q44':'q37', 'q45': 'q34'}
            
            if(self.current_state in transitions.keys()):
                return self.analyzeEvent(old_state, [self.current_state], transitions[self.current_state], 'Senha inserida.')
            else:
                return self.errorMessage('?')

        elif(search('^\[lendo\]', palavra)):
            return self.analyzeEvent(old_state, ['q34'], 'q34', 'Lendo...')

        elif(search('^\[leitura\]', palavra)):
            return self.analyzeEvent(old_state, ['q34'], 'q35', 'Lendo...')

        elif(search('^excluir', palavra)):
            return self.analyzeEvent(old_state, ['q40'], 'q39', 'Chave excluída.')
        
        elif(search('^cadastrar', palavra)):
            return self.analyzeEvent(old_state, ['q40'], 'q41', 'Chave cadastrada.')

        elif(search('^qr code', palavra)):
            return self.analyzeEvent(old_state, ['q33'], 'q34', 'Qr code inserido.')
        
        elif(search('^pagar', palavra)):
            return self.analyzeEvent(old_state, ['q33'], 'q45', 'Pagamento iniciado.')
        else:
            self.current_event = 'login'
            return self.errorMessage('q0')

    def sacarPoupanca(self, palavra):
        old_state = self.current_state
        
        if(search('^voltar', palavra)):
            return self.analyzeEvent(old_state, ['q57', 'q58'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q57', 'q58'], 'q1', 'Saque cancelado.')
        
        elif(search('^valor', palavra)):
            return self.analyzeEvent(old_state, ['q57'], 'q58', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q58'], 'q59', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            return self.analyzeEvent(old_state, ['q59'], 'q58', 'Senha incorreta.')

        elif(search('^\[valido\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q51'], 'q1', 'Saque realizado.')

        else:
            self.current_event = 'login'
            return self.errorMessage('q0')

    def depositarPoupanca(self, palavra):
        old_state = self.current_state
        
        if(search('^voltar', palavra)):
            self.analyzeEvent(old_state, ['q15', 'q16'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q15','q16'], 'q11', 'Deposito cancelado.')
        
        elif(search('^valor', palavra)):
            return self.analyzeEvent(old_state, ['q15'], 'q16', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q16'], 'q17', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            return self.analyzeEvent(old_state, ['q17'], 'q16', 'Senha incorreta.')

        elif(search('^\[valido\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q17'], 'q1', 'Depósito realizado.')

        else:
            self.current_event = 'home'
            return self.errorMessage('q0')

    def fazerEmprestimo(self, palavra):
        old_state = self.current_state
        
        if(search('^voltar', palavra)):
            self.analyzeEvent(old_state, ['q18', 'q19', 'q20', 'q21'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q18', 'q19', 'q21'], 'q1', 'Empréstimo cancelado.')

        elif(search('^valor', palavra)):
            return self.analyzeEvent(old_state, ['q18'], 'q19', 'Valor inserido.')
        
        elif(search('^prazo', palavra)):
            return self.analyzeEvent(old_state, ['q19'], 'q20', 'Prazo inserido.')
        
        elif(search('^parcelas', palavra)):
            return self.analyzeEvent(old_state, ['q20'], 'q21', 'Parcelas inseridas.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q21'], 'q22', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            return self.analyzeEvent(old_state, ['q22'], 'q21', 'Senha incorreta.')

        elif(search('^\[valido\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q22'], 'q1', 'Empréstimo realizado.')  
        
        else:
            self.current_event = 'login'
            return self.errorMessage('q0')

    def pagarParcela(self, palavra):
        old_state = self.current_state
        
        if(search('^voltar', palavra)):
            self.analyzeEvent(old_state, ['q31', 'q30'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q30','q31'], 'q1', 'Pagamento cancelado.')
        
        elif(search('^id emprestimo', palavra)):
            return self.analyzeEvent(old_state, ['q30'], 'q31', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q31'], 'q32', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            return self.analyzeEvent(old_state, ['q32'], 'q31', 'Senha incorreta.')

        elif(search('^\[valido\]', palavra)):
            self.current_event = 'home'
            return self.analyzeEvent(old_state, ['q32'], 'q1', 'Pagamento realizado.')

        else:
            self.current_event = 'login'
            return self.errorMessage('q0')

    def transferencia(self, palavra):
        old_state = self.current_state
        
        if(search('^voltar', palavra)):
            self.analyzeEvent(old_state, ['q51', 'q55'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q51','q53', 'q55'], 'q11', 'Transferência cancelada.')
        
        elif(search('^conta', palavra)):
            return self.analyzeEvent(old_state, ['q51'], 'q52', 'Conta inserida.')
        
        elif(search('^valor', palavra)):
            return self.analyzeEvent(old_state, ['q53'], 'q54', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q55'], 'q56', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            transitions = {'q52': 'q51', 'q54': 'q53', 'q56': 'q55'}
            
            if(self.current_state in transitions.keys()):
                return self.analyzeEvent(old_state, [self.current_state], transitions[self.current_state], 'Senha inserida.')
            else:
                return self.errorMessage('?')

        elif(search('^\[valido\]', palavra)):
            transitions = {'q52':'q53', 'q54':'q55', 'q56': 'q1'}
            
            if(self.current_state in transitions.keys()):
                return self.analyzeEvent(old_state, [self.current_state], transitions[self.current_state], 'Senha inserida.')
            else:
                return self.errorMessage('?')
        else:
            self.current_event = 'login'
            return self.errorMessage('q0')
    
    def pagamento(self, palavra):
        old_state = self.current_state
        
        if(search('^voltar', palavra)):
            self.analyzeEvent(old_state, ['q23', 'q28', 'q24', 'q26'], self.come_back_state, 'Retorno da operação.')

        elif(search('^cancela', palavra)):
            self.analyzeEvent(old_state, ['q24','q26'], 'q1', 'Transferência cancelada.')
        
        elif(search('^\[leitura\]', palavra)):
            self.analyzeEvent(old_state, ['q23'], 'q23', 'Realizando leitura.')
        
        elif(search('^codigo de barras', palavra)):
            return self.analyzeEvent(old_state, ['q28'], 'q29', 'Lendo código de barras.')
        
        elif(search('^data de pagamento', palavra)):
            return self.analyzeEvent(old_state, ['q24'], 'q25', 'Data de pagamento inserida.')

        elif(search('^manual', palavra)):
            return self.analyzeEvent(old_state, ['q23'], 'q28', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q26'], 'q27', 'Senha inserida.')

        elif(search('^\[invalido\]', palavra)):
            transitions = {'q29': 'q28', 'q25': 'q24', 'q27': 'q26'}
            
            if(self.current_state in transitions.keys()):
                return self.analyzeEvent(old_state, [self.current_state], transitions[self.current_state], 'Senha inserida.')
            else:
                return self.errorMessage('?')
                
        elif(search('^\[valido\]', palavra)):
            transitions = {'q23': 'q24', 'q29': 'q24', 'q25':'q26'}
            
            if(self.current_state in transitions.keys()):
                return self.analyzeEvent(old_state, [self.current_state], transitions[self.current_state], 'Senha inserida.')
            else:
                return self.errorMessage('?')
        else:
            self.current_event = 'login'
            return self.errorMessage('q0')
    
    def investimento(self, palavra):
        old_state = self.current_state
        
        if(search('^voltar', palavra)):
            self.analyzeEvent(old_state, ['q10', 'q13', 'q11', 'q3', 'q8', 'q4'], self.come_back_state, 'Retorno da operação.')

        elif(search('^fixa', palavra)):
            self.analyzeEvent(old_state, ['q2'], 'q10', 'Transferência cancelada.')
        
        elif(search('^varivel', palavra)):
            return self.analyzeEvent(old_state, ['q2'], 'q3', 'Senha inserida.')
        
        elif(search('^tesouro direto', palavra)):
            return self.analyzeEvent(old_state, ['q10'], 'q13', 'Lendo código de barras.')
        
        elif(search('^fiis', palavra)):
            return self.analyzeEvent(old_state, ['q3'], 'q8', 'Senha inserida.')

        elif(search('^acoes', palavra)):
            return self.analyzeEvent(old_state, ['q3'], 'q4', 'Senha inserida.')

        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q6'], 'q7', 'Senha inserida.')

        elif(search('^codigo', palavra)):
            transitions = {'q13': 'q14', 'q11': 'q12', 'q4':'q5', 'q8':'q9'}
            
            if(self.current_state in transitions.keys()):
                return self.analyzeEvent(old_state, [self.current_state], transitions[self.current_state], 'Senha inserida.')
            else:
                return self.errorMessage('?')

        elif(search('^variavel', palavra)):
            return self.analyzeEvent(old_state, ['q2'], 'q3', 'Valor inserido.')
        
        elif(search('^senha', palavra)):
            return self.analyzeEvent(old_state, ['q6'], 'q7', 'Senha inserida.')

        elif(search('^cdb', palavra)):
            return self.analyzeEvent(old_state, ['q10'], 'q11', 'Senha inserida.')


        elif(search('^\[invalido\]', palavra)):
            transitions = {'q14':'q13', 'q12': 'q11', 'q9':'q8', 'q5':'q4', 'q7': 'q6'}
            
            if(self.current_state in transitions.keys()):
                return self.analyzeEvent(old_state, [self.current_state], transitions[self.current_state], 'Senha inserida.')
            else:
                return self.errorMessage('?')
                
        elif(search('^\[valido\]', palavra)):
            transitions = {'q5':'q6', 'q9': 'q6', 'q12':'q6', 'q14':'q6'}
            
            if(self.current_state in transitions.keys()):
                return self.analyzeEvent(old_state, [self.current_state], transitions[self.current_state], 'Senha inserida.')
            else:
                return self.errorMessage('?')
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
        self.current_event = 'login'
        return {'text': 'Erro: movimento não permitido', 'old_state':old_state, 'dest_state':cur_state, 'cur_state': 'q0','error': 1}