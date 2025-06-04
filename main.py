from dataclasses import dataclass


# Define a class é o dataclass já inicializa os atributos
@dataclass
class Cliente:
    nome: str
    email: str
    idade: int

    def exibir(self):
        print(f"Meu nome é {self.nome}")


gui = Cliente(nome="Luis", email="ldd@gmail.con", idade=33);
print(gui)

gui.exibir()