import typer

app = typer.Typer()

@app.command()
def hello(name: str = "", formal:bool=False):
    try:
        if name != str:
            raise ValueError("Name must be a string")
        if formal:
            if name == "":
                print(f"Salutations and warmest regards!")
            else:
                print(f"Salutations and warmest regards, Mx. {name}!")
        else:
            if name == "":
                print(f"Welcome aboard!")
            else:
                print(f"Welcome aboard, {name}!")
    except ValueError as e:
        print(f"Error: {e}")

@app.command()
def square(number: int):
    square = number * 2
    print(f"The square of {number} is {square}!")

@app.command()
def addition(x: int, y: int):
    try:
        result = x + y
        print(f"{x} + {y} = {result}")
    except Exception as error:
        print(f"There was a mistake!: {error}")

@app.command()
def subtraction(x: int, y: int):
    try:
        result = x - y
        print(f"{x} - {y} = {result}")
    except Exception as error:
            print(f"There was a mistake!: {error}")

if __name__ == "__main__":
    app()