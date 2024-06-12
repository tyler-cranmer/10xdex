



def print_functions(abi: str):
    print("Functions in ABI:")
    for entry in abi:
        if entry.get("type") == "function":
            name = entry.get("name")
            inputs = [
                (input["name"], input["type"]) for input in entry.get("inputs", [])
            ]
            outputs = [
                (output["name"], output["type"]) for output in entry.get("outputs", [])
            ]
            print(f"\nFunction Name: {name}")
            print("Inputs:")
            for inp in inputs:
                print(f"  {inp[0]} ({inp[1]})")
            print("Outputs:")
            for out in outputs:
                print(f"  {out[0]} ({out[1]})")