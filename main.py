def main():
    print("Hello from autogen-content-generation-cautious-fortnight!")
    smth = 42
    wong = smth + 1
    statement = """{smth} plus one is {wong}."""
    print(statement)
    print(statement.format(smth=smth, wong=wong))

if __name__ == "__main__":
    main()
