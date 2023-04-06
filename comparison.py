import pathlib

from statemachine import StateMachine as ST1
from state_machine_2 import StateMachine as ST2

st1 = ST1()
st2 = ST2("Final.jff")

used_transitions = set()


def compare_automata(events):
    st1.reset()
    st2.reset()

    errors = []
    for i, l in enumerate(events, start=1):
        l = l.strip()  # Remove '\n'

        used_transitions.add((st2.current_state, l))

        # Run the same event on both automata
        r1 = st1.execute(l)
        r2 = st2.process(l)

        # Compare output
        if (
            r1["old_state"] != r2["old_state"]
            or r1["dest_state"] != r2["dest_state"]
            or r1["error"] != r2["error"]
        ):
            errors.append(
                f"    Diferença encontrada: linha {i}, evento {l}\n"
                f"    Saída Autômato: {r1}\n"
                f"    Saída Referência: {r2}"
            )
            return errors

    # Compare final state
    if st1.current_state != st2.states[st2.current_state]:
        errors.append(
            f"Automatos terminaram em estados diferentes: {st1.current_state} e {st2.states[st2.current_state]}"
        )
        return errors
    return errors


# Run all tests
tests = pathlib.Path(__file__).parent / "tests"
for file in tests.iterdir():
    with file.open() as events:
        if errors := compare_automata(events):
            output = "ERRO"
        else:
            output = "OK"
    print(f"Teste '{file.name}': {output}")

    for error in errors:
        print(error)

print()

untested = st2.transitions.keys() - used_transitions
if untested:
    print(f"Transições não testadas: {len(untested)}")
    for transition in sorted(untested):
        state, event = transition
        print(f"- {st2.states[state]}, {event}")
else:
    print("Todas as transições foram testadas")
