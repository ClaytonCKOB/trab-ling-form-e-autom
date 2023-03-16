from re import search, sub

class StateMachine:
    def __init__(self):
        self.events = {'login': self.login, 'home': self.home}
        self.current_state = 'q0'
        self.final_states = ['q0']
        self.current_event = 'home'

    def execute(self, palavra):
        return self.events[self.current_event](palavra)

    def home(self, palavra):
        if(search('^senha', palavra)):
            old_state = self.current_state
            self.current_event = 'login'
            palavra = sub(r"^senha", '', palavra)            
            if self.current_state == 'q0':
                self.current_state = 'q1'
                return  {'text':'Senha aceita.', 'old_state': old_state, 'dest_state': self.current_state, 'cur_state': self.current_state, 'error': 0}
            else:
                return self.errorMessage('q1')

    def login(self, palavra):
        while(len(palavra) > 0):
            old_state = self.current_state
            if(search('^operacao', palavra)):
                palavra = sub(r"^operacao", '', palavra)
                if self.current_state == 'q1':
                    self.current_state = 'q3'
                    return {'text':'Operação realizada.', 'old_state': old_state, 'dest_state': self.current_state, 'cur_state': self.current_state, 'error': 0}
                else:
                    return  self.errorMessage('q3')

            elif(search('^retorno operacao', palavra)):
                palavra = sub(r"^retorno operacao", '', palavra)
                if self.current_state == 'q3':
                    self.current_state = 'q1'
                    return {'text':'Retorno da operação.', 'old_state': old_state, 'dest_state': self.current_state, 'cur_state': self.current_state, 'error': 0}
                else:
                    return self.errorMessage('q1')
            elif(search('^encerrar', palavra)):
                palavra = sub(r"^encerrar", '', palavra)
                if self.current_state == 'q1':
                    self.current_state = 'q0'
                    return {'text':'Operação encerrada', 'old_state': old_state, 'dest_state': self.current_state, 'cur_state': self.current_state, 'error': 0}
                else:
                    return self.errorMessage('q0')
            else:
                self.current_event = 'home'
                return self.errorMessage('q0')

        if self.current_state in self.final_states:
            self.current_event = 'home'
            self.current_state = 'q0'
            return {'text':'Login efetuado.', 'old_state': old_state, 'dest_state': self.current_state, 'cur_state': self.current_state, 'error': 0}
        else:
            return self.errorMessage('q0')

    def errorMessage(self, cur_state):
        old_state = self.current_state
        self.current_state = 'q0'
        return {'text': 'Erro: movimento não permitido', 'old_state':old_state, 'dest_state':cur_state, 'cur_state': 'q0','error': 1}