import pathlib

from statemachine import StateMachine as ST1
from state_machine_2 import StateMachine as ST2

st1 = ST1()
st2 = ST2("Final.jff")


def compare_automata(events):
    st1.reset()
    st2.reset()

    for i, l in enumerate(events, start=1):
        l = l.strip() # Remove '\n'

        # Run the same event on both automata
        r1 = st1.execute(l)
        r2 = st2.process(l)

        # Compare output
        if (
            r1["old_state"] != r2["old_state"]
            or r1["dest_state"] != r2["dest_state"]
            or r1["error"] != r2["error"]
        ):
            print(
                f"    Diferença encontrada no teste {file.name}, linha {i}, evento {l}"
            )
            print("    Saída Autômato: ", r1)
            print("    Saída Referência: ", r2)
            return False
    
    # Compare final state
    if st1.current_state != st2.states[st2.current_state]:
        print(
            f"Automatos terminaram em estados diferentes: {st1.current_state} e {st2.states[st2.current_state]}"
        )
        return False
    return True

# Run all tests
tests = pathlib.Path(__file__).parent / "tests"
for file in tests.iterdir():
    with file.open() as events:
        if compare_automata(events):
            output = "OK"
        else:
            output = "ERRO"
    print(f"Teste '{file.name}': {output}")
