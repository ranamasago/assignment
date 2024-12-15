import flet as ft
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text
class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE
class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE
class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 500
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ActionButton(text="10^x", button_clicked=self.button_clicked),
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="x²", button_clicked=self.button_clicked),
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="x³", button_clicked=self.button_clicked),
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="x!", button_clicked=self.button_clicked),
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="1/x", button_clicked=self.button_clicked),
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )
    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value += data
        elif data in ("+", "-", "*", "/"):
            self.operand1 = float(self.result.value)
            self.operator = data
            self.new_operand = True
        elif data == "=":
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()
        elif data == "%":
            self.result.value = str(float(self.result.value) / 100)
            self.reset()
        elif data == "+/-":
            if float(self.result.value) > 0:
                self.result.value = "-" + self.result.value
            elif float(self.result.value) < 0:
                self.result.value = self.result.value[1:]
        elif data == "10^x":
            self.result.value = str(10 ** float(self.result.value))
            self.new_operand = True
        elif data == "x²":
            self.result.value = str(float(self.result.value) ** 2)
            self.new_operand = True
        elif data == "x³":
            self.result.value = str(float(self.result.value) ** 3)
            self.new_operand = True
        elif data == "x!":
            self.result.value = str(self.factorial(int(self.result.value)))
            self.new_operand = True
        elif data == "1/x":
            if float(self.result.value) == 0:
                self.result.value = "Error"
            else:
                self.result.value = str(1 / float(self.result.value))
            self.new_operand = True
        self.update()
    def factorial(self, n):
        if n == 0 or n == 1:
            return 1
        else:
            result = 1
            for i in range(2, n + 1):
                result *= i
            return result
    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return str(operand1 + operand2)
        elif operator == "-":
            return str(operand1 - operand2)
        elif operator == "*":
            return str(operand1 * operand2)
        elif operator == "/":
            if operand2 == 0:
                return "Error"
            return str(operand1 / operand2)
    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True
def main(page: ft.Page):
    page.title = "Calculator App"
    calc = CalculatorApp()
    page.add(calc)
ft.app(target=main)

import flet as ft
def main(page: ft.Page):
    page.title = "Calc App"
    result = ft.Text(value="0")
    page.add(
        result,
        ft.ElevatedButton(text="AC"),
        ft.ElevatedButton(text="+/-"),
        ft.ElevatedButton(text="%"),
        ft.ElevatedButton(text="/"),
        ft.ElevatedButton(text="7"),
        ft.ElevatedButton(text="8"),
        ft.ElevatedButton(text="9"),
        ft.ElevatedButton(text="*"),
        ft.ElevatedButton(text="4"),
        ft.ElevatedButton(text="5"),
        ft.ElevatedButton(text="6"),
        ft.ElevatedButton(text="-"),
        ft.ElevatedButton(text="1"),
        ft.ElevatedButton(text="2"),
        ft.ElevatedButton(text="3"),
        ft.ElevatedButton(text="+"),
        ft.ElevatedButton(text="0"),
        ft.ElevatedButton(text="."),
        ft.ElevatedButton(text="="),
        ft.ElevatedButton(text="10^x"),
        ft.ElevatedButton(text="x²"),
        ft.ElevatedButton(text="x³"),
        ft.ElevatedButton(text="x!"),
        ft.ElevatedButton(text="1/x"),
    )
ft.app(target=main)

import flet as ft
def main(page: ft.Page):
    page.title = "Calc App"
    result = ft.Text(value="0")
    page.add(
        ft.Row(controls=[result]),
        ft.Row(
            controls=[
                ft.ElevatedButton(text="10^x"),
                ft.ElevatedButton(text="AC"),
                ft.ElevatedButton(text="+/-"),
                ft.ElevatedButton(text="%"),
                ft.ElevatedButton(text="/"),
            ]
        ),
        ft.Row(
            controls=[
                ft.ElevatedButton(text="x²"),
                ft.ElevatedButton(text="7"),
                ft.ElevatedButton(text="8"),
                ft.ElevatedButton(text="9"),
                ft.ElevatedButton(text="*"),
            ]
        ),
        ft.Row(
            controls=[
                ft.ElevatedButton(text="x³"),
                ft.ElevatedButton(text="4"),
                ft.ElevatedButton(text="5"),
                ft.ElevatedButton(text="6"),
                ft.ElevatedButton(text="-"),
            ]
        ),
        ft.Row(
            controls=[
                ft.ElevatedButton(text="x!"),
                ft.ElevatedButton(text="1"),
                ft.ElevatedButton(text="2"),
                ft.ElevatedButton(text="3"),
                ft.ElevatedButton(text="+"),
            ]
        ),
        ft.Row(
            controls=[
                ft.ElevatedButton(text="1/x"),
                ft.ElevatedButton(text="0"),
                ft.ElevatedButton(text="."),
                ft.ElevatedButton(text="="),
            ]
        ),
    )
ft.app(target=main)

import flet as ft
def main(page: ft.Page):
    page.title = "Calc App"
    result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
    class CalcButton(ft.ElevatedButton):
        def __init__(self, text, expand=1):
            super().__init__()
            self.text = text
            self.expand = expand
    class DigitButton(CalcButton):
        def __init__(self, text, expand=1):
            CalcButton.__init__(self, text, expand)
            self.bgcolor = ft.colors.WHITE24
            self.color = ft.colors.WHITE
    class ActionButton(CalcButton):
        def __init__(self, text):
            CalcButton.__init__(self, text)
            self.bgcolor = ft.colors.ORANGE
            self.color = ft.colors.WHITE
    class ExtraActionButton(CalcButton):
        def __init__(self, text):
            CalcButton.__init__(self, text)
            self.bgcolor = ft.colors.BLUE_GREY_100
            self.color = ft.colors.BLACK
    page.add(
        ft.Container(
            width=500,
            bgcolor=ft.colors.BLACK,
            border_radius=ft.border_radius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[result], alignment="end"),
                    ft.Row(
                        controls=[
                            ExtraActionButton(text="10^x"),
                            ExtraActionButton(text="AC"),
                            ExtraActionButton(text="+/-"),
                            ExtraActionButton(text="%"),
                            ActionButton(text="/"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ActionButton(text="x²"),
                            DigitButton(text="7"),
                            DigitButton(text="8"),
                            DigitButton(text="9"),
                            ActionButton(text="*"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ActionButton(text="x³"),
                            DigitButton(text="4"),
                            DigitButton(text="5"),
                            DigitButton(text="6"),
                            ActionButton(text="-"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ActionButton(text="x!"),
                            DigitButton(text="1"),
                            DigitButton(text="2"),
                            DigitButton(text="3"),
                            ActionButton(text="+"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="1/x"),
                            DigitButton(text="0", expand=2),
                            DigitButton(text="."),
                            ActionButton(text="="),
                        ]
                    ),
                ]
            ),
        )
    )
ft.app(target=main)

import flet as ft
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
class DigitButton(CalcButton):
    def __init__(self, text, expand=1):
        CalcButton.__init__(self, text, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE
class ActionButton(CalcButton):
    def __init__(self, text):
        CalcButton.__init__(self, text)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE
class ExtraActionButton(CalcButton):
    def __init__(self, text):
        CalcButton.__init__(self, text)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK
class CalculatorApp(ft.Container):
    # application's root control (i.e. "view") containing all other controls
    def __init__(self):
        super().__init__()
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 500
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ActionButton(text="10^x"),
                        ExtraActionButton(text="AC"),
                        ExtraActionButton(text="+/-"),
                        ExtraActionButton(text="%"),
                        ActionButton(text="/"),
                    ]
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="x²"),
                        DigitButton(text="7"),
                        DigitButton(text="8"),
                        DigitButton(text="9"),
                        ActionButton(text="*"),
                    ]
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="x³"),
                        DigitButton(text="4"),
                        DigitButton(text="5"),
                        DigitButton(text="6"),
                        ActionButton(text="-"),
                    ]
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="x!"),
                        DigitButton(text="1"),
                        DigitButton(text="2"),
                        DigitButton(text="3"),
                        ActionButton(text="+"),
                    ]
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="1/x"),
                        DigitButton(text="0", expand=2),
                        DigitButton(text="."),
                        ActionButton(text="="),
                    ]
                ),
            ]
        )
def main(page: ft.Page):
    page.title = "Calc App"
    # create application instance
    calc = CalculatorApp()
    # add application's root control to the page
    page.add(calc)
ft.app(target=main)

import flet as ft
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text
class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE
class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE
class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK
class CalculatorApp(ft.Container):
    # application's root control (i.e. "view") containing all other controls
    def __init__(self):
        super().__init__()
        self.reset()
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )
    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data
        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True
        elif data in ("="):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()
        elif data in ("%"):
            self.result.value = float(self.result.value) / 100
            self.reset()
        elif data in ("+/-"):
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)
            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )
        self.update()
    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num
    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "*":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)
    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True
def main(page: ft.Page):
    page.title = "Calc App"
    # create application instance
    calc = CalculatorApp()
    # add application's root control to the page
    page.add(calc)
ft.app(target=main)






