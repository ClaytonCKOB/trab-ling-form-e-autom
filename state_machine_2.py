from xml.etree import ElementTree


class StateMachine:
    def __init__(self, jflap_file):
        self.initial_state = None
        self.final_states = set()
        self.states = {}  # Key: State ID, Value: State name

        # Implements the transition function:
        # Key: (State ID, Event), Value: Next State ID
        self.transitions = {}

        self.current_state = None

        self.load_file(jflap_file)

    def reset(self):
        self.current_state = self.initial_state

    def load_file(self, file):
        tree = ElementTree.parse(file)
        automaton = tree.find("automaton")

        # Loading the States
        for state in automaton.findall("state"):
            state_id = state.get("id")
            state_name = state.get("name")

            self.states[state_id] = state_name
            if state.find("initial") is not None:
                self.initial_state = state_id
            if state.find("final") is not None:
                self.final_states.add(state_id)

        # Loading the transition function
        for transition in automaton.findall("transition"):
            from_state = transition.find("from").text
            to_state = transition.find("to").text
            read = transition.find("read").text

            self.transitions[from_state, read] = to_state

        self.current_state = self.initial_state

    def process(self, event):
        old_state = self.current_state

        try:
            next_state = self.transitions[old_state, event]
            self.current_state = next_state

            return {
                "old_state": self.states[old_state],
                "dest_state": self.states[self.current_state],
                "cur_state": self.states[self.current_state],
                "error": 0,
            }
        except KeyError:
            self.current_state = self.initial_state
            return {
                "old_state": self.states[old_state],
                "dest_state": self.states[self.initial_state],
                "cur_state": self.states[self.initial_state],
                "error": 1,
            }

    def accept(self):
        return self.current_state in self.final_states


if __name__ == "__main__":
    s = StateMachine("Final.jff")
    with open("tests/depositar_poupanca.txt") as f:
        for l in f:
            l = l.strip()
            s.process(l)

    print(f"Interação terminou no estado {s.current_state}")
    if s.accept():
        print("Aceitação")
    else:
        print("Rejeição")
