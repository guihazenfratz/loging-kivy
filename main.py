from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") > 0 and self.email.text.count(".") > 0:
            if self.password.text != "":
                resposta = db.add_user(self.email.text, self.password.text, self.namee.text)
                if resposta != -1:
                    db.save()
                    self.reset()
                    sm.current = "login"
                else:
                    invalidForm("Erro", "Este e-mail já está cadastrado em nosso banco de dados.")
            else:
                invalidForm("Erro", "Senha inválida.")
        else:
            invalidForm("Erro", "Preencha um nome e um e-mail válidos.")

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            dados_usuario = db.get_user(self.email.text)
            sm.get_screen("main").n.text = "Account Name: " + dados_usuario[1]
            sm.get_screen("main").email.text = "Email: " + self.email.text
            sm.get_screen("main").created.text = "Created: " + dados_usuario[2]
            self.reset()
            sm.current = "main"
        else:
            invalidForm("Erro de Login", "E-mail ou senha incorretos.")

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    email = ObjectProperty(None)
    created = ObjectProperty(None)

    def logOut(self):
        sm.current = "login"


class WindowManager(ScreenManager):
    pass


def invalidForm(titulo, mensagem):
    pop = Popup(
        title=titulo,
        content=Label(text=mensagem),
        size_hint=(None, None),
        size=(400, 200)
    )
    pop.open()


kv = Builder.load_file("mk.kv")

db = DataBase("user.txt")

sm = WindowManager()
sm.add_widget(LoginWindow(name="login"))
sm.add_widget(CreateAccountWindow(name="create"))
sm.add_widget(MainWindow(name="main"))


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()