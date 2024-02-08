from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from configparser import ConfigParser
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField


KV = '''
MDScreen:
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        MDTopAppBar:
            title: "Valor no bilhete único"
    
    BoxLayout:
        orientation: 'vertical'
        spacing: '15dp'
        padding: [0, 0, 0, '400dp']

        MDRectangleFlatButton:
            id: value
            text: "Valor no Passe"
            font_size: '20dp'
            pos_hint: {'center_x':0.5}
            on_release: app.hide()
        
        MDRectangleFlatButton:
            id: total
            text: "Total Gasto"
            font_size: '15dp'
            pos_hint: {'center_x':0.5}
            on_release: app.hide()
    
        MDRectangleFlatButton:
            id: button3
            text: "Somar Valor"
            font_size: '15dp'
            pos_hint: {'center_x':0.5}
            on_release: app.somar()
        
        MDRectangleFlatButton:
            id: button1
            text: "Subtrair R$2.73"
            font_size: '15dp'
            pos_hint: {'center_x':0.5}
            on_release: app.sub_value()

        MDRectangleFlatButton:
            id: button2
            text: "Valor Personalizado"
            font_size: '15dp'
            pos_hint: {'center_x':0.5}
            on_release: app.custom_value()
'''

class main_app(MDApp):
    def __init__(self):
        super().__init__()
        self.kvs = Builder.load_string(KV)
        self.config = ConfigParser()


    def build(self):
        screen = Screen()
        screen.add_widget(self.kvs)
        self.load_config()
        self.total(False)
        return screen
    

    def load_config(self):
        # recupera e mostra o valor do passe
        self.config.read('config.ini')
        
        if 'value' not in self.config.sections():
            self.config.add_section('value')
            self.config.set('value', 'amount', '0')
            #self.kvs.ids.value.text = f"Total: R$0.00"

            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
        else:
            saved_value = self.config.getfloat('value', 'amount')
            self.kvs.ids.value.text = f"Total: R${saved_value:.2f}"


    def sub_value(self):
        # subtrai 2.73 do valor total e mostra o valor no botão 'value' (valor no passe)
        # atualiza e mostra o valor gasto no botão 'total' (gasto total)
        try:
            current_value = self.config.getfloat('value', 'amount')
            new_value = current_value - 2.73
            aux = True

            if new_value < 0:
                new_value = current_value
                aux = False

            if aux:    
                self.total(True)
            
            self.kvs.ids.value.text = f"Total: R${new_value:.2f}"
            self.save_config()
        except:
            pass


    def total(self, bool):
        # recupera a quantidade de usos do passe
        # multiplica por 2.73 e mostra o valor no botão gasto
        self.config.read('config.ini')
        if 'qnt' not in self.config.sections():
            self.config.add_section('qnt')
            self.config.set('qnt', 'amount', '0')
            self.kvs.ids.total.text = f"Gasto: R$0.00"

        if bool == True:
            aux = self.config.getint('qnt', 'amount')
            self.config.set('qnt', 'amount', str(aux+1))
            value_saved = self.config.getint('qnt', 'amount')
            self.kvs.ids.total.text = f"Gasto: R${value_saved * 2.73}"
        else:
            value_saved = self.config.getint('qnt', 'amount')
            self.kvs.ids.total.text = f"Gasto: R${value_saved * 2.73}"

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


    def custom_value(self):
        # chama a caixa de dialogo para valor personalizado
        content = MDTextField(
            hint_text="Digite o valor",
            input_filter="float",
            max_text_length=10,
            on_text_validate=self.on_enter_pressed
        )
        
        self.dialog = MDDialog(
            title="Valor Personalizado",
            type="custom",
            content_cls=content,
            size_hint=(0.8, 0.4),
            buttons=[
                ("Cancelar", lambda *args: self.dialog.dismiss()),
            ],
        )
        self.dialog.open()


    def on_enter_pressed(self, instance):
        # quando 'enter' é presionado, o valor digitado
        # é mostrado no botão 'value' (valor no bilhete)
        if instance.text:
            custom_value = float(instance.text)
            self.kvs.ids.value.text = f"Total: R${custom_value:.2f}"
            self.save_config()
            self.dialog.dismiss()


    def somar(self):
        # chama a caixa de dialogo para somar um valor ao valor atual do passe
        content = MDTextField(
            hint_text="Digite o valor",
            input_filter="float",
            max_text_length=10,
            on_text_validate=self.on_enter_pressed_sum
        )
        
        self.dialog = MDDialog(
            title="Valor Personalizado",
            type="custom",
            content_cls=content,
            size_hint=(0.8, 0.4),
            buttons=[
                ("Cancelar", lambda *args: self.dialog.dismiss()),
            ],
        )
        self.dialog.open()


    def on_enter_pressed_sum(self, instance):
        # recupera o valor atual no passe e soma com o valor indicado pelo usuario
        try:
            saved_value = self.config.getfloat('value','amount')
        except:
            saved_value = 0
        
        if instance.text:
            custom_value = float(instance.text)
            new_value = saved_value + custom_value
            self.kvs.ids.value.text = f"Total: R${new_value:.2f}"
            self.save_config()
            self.dialog.dismiss()


    def hide(self):
        aux = self.kvs.ids.value.text
        aux2 = self.kvs.ids.total.text

        if aux != 'Valor no Passe' and aux2 != 'Total Gasto':
            self.kvs.ids.value.text = 'Valor no Passe'
            self.kvs.ids.total.text = 'Total Gasto'
        else:
            self.load_config()
            self.total(False)


    def save_config(self):
        # salva o valor do passe 
        self.config.read('config.ini')
        if 'value' not in self.config.sections():
            self.config.add_section('value')
        
        value_to_save = self.kvs.ids.value.text.replace("Total: R$", "").strip()
        self.config.set('value', 'amount', str(value_to_save))
        
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


if __name__ == "__main__":
    main_app().run()
