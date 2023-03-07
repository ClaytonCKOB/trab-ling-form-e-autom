from re import search, sub

class StateMachine:
    def __init__(self):
        self.events = {'login': self.login, 'home': self.home}
        self.current_state = 'q0'
        self.final_states = ['q0']
        self.current_event = 'home'

    def execute(self, palavra):
        print(self.events[self.current_event](palavra))
        return self.events[self.current_event](palavra)

    def home(self, palavra):
        if(search('^senha', palavra)):
            palavra = sub(r"^senha", '', palavra)
            self.current_state = 'q1'
            return 'Senha aceita.'


    def login(self, palavra):
        while(len(palavra) > 0):
            if(search('^operacao', palavra)):
                palavra = sub(r"^operacao", '', palavra)
                if self.current_state == 'q1':
                    self.current_state = 'q3'
                else:
                    return 'Erro ao realizar o login'

            elif(search('^retorno operacao', palavra)):
                palavra = sub(r"^retorno operacao", '', palavra)
                if self.current_state == 'q3':
                    self.current_state = 'q1'
                else:
                    return 'Erro ao realizar o login'
            elif(search('^encerrar', palavra)):
                palavra = sub(r"^encerrar", '', palavra)
                if self.current_state == 'q1':
                    self.current_state = 'q0'
                else:
                    return 'Erro ao realizar o login'
            else:
                return 'Erro ao realizar o login'

        if self.current_state in self.final_states:
            self.current_event = 'home'
            self.current_state = 'q0'
            return 'Login efetuado.'
        else:
            return 'Erro ao realizar o login'

