import itertools

groups = {"x": {"x1", "x2", "g"}, "y": {"y1", "y2"}}
ports = {"x": 100, "y": 120}
input_elements = {"x1", "x", "-p120"}

input_groups = set(itertools.chain.from_iterable([groups.get(e, {e}) for e in input_elements if not e.startswith("-p")]))
input_port = ["".join(e[2:]) for e in input_elements if e.startswith("-p")]
selected_group = [key for key, value in groups.items() if value >= input_groups]
if selected_group:
    selected_port = ports.get(selected_group[0], 0) if not input_port else input_port[0]
    print(sorted(list(input_groups)), "->", selected_port)
else:
    print("nothing")