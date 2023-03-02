from re import search, sub

class StateMachine:
    def init(self):
        pass
    
    def login(self, palavra):
        current_state = 'q0'
        final_states = ['q0']

        while(len(palavra) > 0):

            if(search('^senha', palavra)):
                palavra = sub(r"^senha", '', palavra)
                current_state = 'q1'
            elif(search('^operacao', palavra)):
                palavra = sub(r"^operacao", '', palavra)
                if current_state == 'q1':
                    current_state = 'q3'
                else:
                    return print('Erro ao realizar o login')
            elif(search('^retorno operacao', palavra)):
                palavra = sub(r"^retorno operacao", '', palavra)
                if current_state == 'q3':
                    current_state = 'q1'
                else:
                    return print('Erro ao realizar o login')
            elif(search('^encerrar', palavra)):
                palavra = sub(r"^encerrar", '', palavra)
                if current_state == 'q1':
                    current_state = 'q0'
                else:
                    return print('Erro ao realizar o login')
            else:
                return print('Erro ao realizar o login')


        if current_state in final_states:
            return print('Login efetuado.')
        else:
            return print('Erro ao realizar o login')


StateMachine = StateMachine()

# exemplo funcional
StateMachine.login('senhaoperacaoretorno operacaoencerrar')

# exemplo com erro
StateMachine.login('operacaosenhaoperacaoretorno operacaoencerrar')
