from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDRectangleFlatButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.lang import Builder

from datetime import datetime

import pyrebase
import certifi
import ssl

# Window.size=(720,1480) # HD+
# Window.size = (1080, 2220)  # FHD+
# Window.top = -200
# Window.size=(2960,1440) # WQHD+

ssl._create_default_https_context = ssl._create_unverified_context

# ~~~~~~~~~~~~~~ DataBase ~~~~~~~~~~~~~~~~~~~
firebaseConfig = {"apiKey": "AIzaSyAIKiLY261OEhtdxlTCrL1PEaTVB8vMbYI",
                  "authDomain": "dbdemo-a62f0.firebaseapp.com",
                  "databaseURL": "https://dbdemo-a62f0-default-rtdb.firebaseio.com",
                  "projectId": "dbdemo-a62f0",
                  "storageBucket": "dbdemo-a62f0.appspot.com",
                  "messagingSenderId": "667257549819",
                  "appId": "1:667257549819:web:30c76d2f62215474c7915e",
                  "measurementId": "G-B6LVL19SNH"}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class CustomDropDown(DropDown):
    pass


class RegisterScreen(Screen):
    pass


class ContentDrawer(BoxLayout):
    pass


class InputScreen(Screen):
    pass


class LoginScreen(Screen):
    def show_dialog(self):
        self.dialog = MDDialog(title="Apakah anda sudah memiliki akun VeryMon ?",
                               text='Pilih "Daftar" jika belum memiliki akun VeryMon',
                               size_hint=(0.95, 1),
                               buttons=[
                                   MDRaisedButton(text='Daftar', on_release=self.registerscreen),
                                   MDRaisedButton(text='Tutup', on_release=self.close_dialog)
                               ])
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def registerscreen(self, obj):
        self.dialog.dismiss()
        self.manager.transition.direction = 'left'
        self.manager.current = 'registerscreen'


class Hapus(MDRaisedButton):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_release')
            return True  # consumed on_touch_down & stop propagation / bubbling
        return super(Hapus, self).on_touch_down(touch)


class Edit(MDIconButton):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_release')
            return True
        return super(Edit, self).on_touch_down(touch)


class EditScreen(Screen):
    temp_ids = ''

    def on_pre_enter(self, *args):
        # get database
        dbs = db.child(MainMenuScreen.temp_email).child("data").child(self.temp_ids).get()

        # tgl
        tgl = self.ids.tgl
        tgl.text = dbs.val()["tgl"]

        # nama keuangan
        nama = self.ids.nama
        nama.text = dbs.val()["nama"]

        # jenis keuangan
        jenis = self.ids.jenis
        jenis.text = dbs.val()["jenis"]

        # Keluar / Masuk
        print(dbs.val()['io'])
        for i in range(2):
            if dbs.val()["io"] == 'Masuk':
                self.ids.chk_msk.active = True
            else:
                self.ids.chk_klr.active = True

        # jumlah uang
        jumlah = self.ids.jumlah
        jumlah.text = dbs.val()["jumlah"]

        # keterangan data
        keterangan = self.ids.keterangan
        keterangan.text = dbs.val()["keterangan"]

    def show_dialog(self):
        self.dialog = MDDialog(title="Yakin ingin keluar dan tidak merubah data ?",
                               size_hint=(.95, 1),
                               buttons=[MDRaisedButton(text='Ya', on_release=self.dlg_cnl),
                                        MDRaisedButton(text='Tidak', on_release=self.dlg_cls)])
        self.dialog.open()

    def dlg_cnl(self, obj):
        self.dialog.dismiss()
        self.manager.transition.direction = 'right'
        self.manager.current = 'mainmenuscreen'

    def dlg_cls(self, obj):
        self.dialog.dismiss()


class MainMenuScreen(Screen):
    temp_email = ''
    temp_delete = None

    def on_enter(self, *args):
        dbs = db.child(self.temp_email).child("data").get()
        grid = self.ids['grid_banner']
        grid.clear_widgets()
        loading = self.ids['loading']
        try:
            for self.i in dbs.each():
                # ~~~~~~~ Banner ~~~~~~~~
                card = MDCard(size_hint=(.9, .5))
                layout = FloatLayout(pos_hint={'center_x': .5, 'center_y': .5})
                card.add_widget(layout)

                # ~~~~~~~ ID Data ~~~~~~~~
                ids = self.i.val()['ids']
                dataid = MDRaisedButton(text=f'{ids}',
                                        pos_hint={'center_x': .28, 'top': 1})
                layout.add_widget(dataid)

                # ~~~~~~~ Nama Data ~~~~~~~~
                nama = self.i.val()['nama']
                datanama = MDLabel(text=nama,
                                   font_style='H6',
                                   halign='left',
                                   pos_hint={'center_x': .55, 'center_y': .8})
                layout.add_widget(datanama)

                # ~~~~~~~ Keterangan Data ~~~~~~~~
                keterangan = self.i.val()['keterangan']
                dataket = MDLabel(text=keterangan,
                                  font_style='Body1',
                                  halign='left',
                                  size_hint=(.8, .3),
                                  pos_hint={'center_x': .47, 'center_y': .5})
                bgket = MDRectangleFlatButton(size_hint=(.9, .45),
                                              pos_hint={'center_x': .5, 'top': .7},
                                              disabled=True)
                layout.add_widget(bgket)
                layout.add_widget(dataket)

                # ~~~~~~~ Keluar atau Masuk ~~~~~~~~
                io = self.i.val()['io']
                dataio = MDLabel(text=io,
                                 font_style='Button',
                                 halign='right',
                                 pos_hint={'center_x': .45, 'top': .65})
                layout.add_widget(dataio)

                # ~~~~~~~ Jenis Data ~~~~~~~~
                jenis = self.i.val()['jenis']
                datajenis = MDLabel(text=jenis,
                                    font_style='Button',
                                    halign='left',
                                    pos_hint={'center_x': .55, 'top': .65})
                layout.add_widget(datajenis)

                # ~~~~~~~ tgl Data ~~~~~~~~
                tgl = self.i.val()['tgl']
                datatgl = MDLabel(text=tgl,
                                  font_style='Button',
                                  halign='right',
                                  pos_hint={'center_x': .45, 'center_y': .8})
                layout.add_widget(datatgl)

                # ~~~~~~~ Jumlah Uang ~~~~~~~~
                jumlah = self.i.val()['jumlah']
                matauang = self.i.val()['mata_uang']
                datajumlah = MDLabel(text=matauang + ' ' + jumlah + '',
                                     font_style='Button',
                                     halign='right',
                                     pos_hint={'center_x': .45, 'top': .55})
                layout.add_widget(datajumlah)

                # ~~~~~~~ Button Delete ~~~~~~~~
                hapus = Hapus(id=f'{ids}',
                              text='Hapus',
                              on_release=self.delete)

                clear = MDRaisedButton(text='Tutup')

                delete_dialog = MDDialog(title='Apakah Anda Yakin ?',
                                         size_hint=(0.95, 1),
                                         buttons=[hapus, clear])

                hapus.bind(on_release=delete_dialog.dismiss)

                delete = MDIconButton(icon='trash-can',
                                      pos_hint={'center_x': .9, 'top': 1},
                                      on_release=delete_dialog.open)

                clear.bind(on_release=delete_dialog.dismiss)

                layout.add_widget(delete)

                # ~~~~~~~ Button Delete ~~~~~~~~
                # edit_menu = print('Teredit')
                edit = Edit(id=f'{ids}',
                            icon='pencil',
                            pos_hint={'center_x': .8, 'top': 1},
                            on_release=self.edited)

                layout.add_widget(edit)

                grid.add_widget(card)

            loading.active = False
        except:
            Snackbar(text="Data Kosong").show()
            loading.active = False

    def delete(self, instance):
        db.child(self.temp_email).child("data").child(instance.id).remove()
        self.on_enter()

    def edited(self, instance):
        EditScreen.temp_ids = instance.id
        print(instance.id)
        self.manager.transition.direction = 'left'
        self.manager.current = 'editscreen'


sm = ScreenManager()
sm.add_widget(LoginScreen(name='loginscreen'))
sm.add_widget(RegisterScreen(name='registerscreen'))
sm.add_widget(MainMenuScreen(name='mainmenuscreen'))
sm.add_widget(InputScreen(name='inputscreen'))
sm.add_widget(EditScreen(name='editscreen'))


class VeryMonApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('main.kv')

        self.dropdown = CustomDropDown()
        mainbutton = self.screen.ids['registerscreen'].ids['drop_pertanyaan']
        mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        self.dialog = MDDialog(title="Email / Password Salah!",
                               text='Pilih "Daftar" jika belum atau "Lupa Password" jika sudah tapi lupa password',
                               size_hint=(0.95, 1),
                               buttons=[MDRaisedButton(text='Tutup', on_release=self.dialog_tutup)])

    def login(self, email_field, password_field):
        try:
            auth.sign_in_with_email_and_password(email_field, password_field)
            self.temp_email = email_field
            self.temp_email = self.temp_email.replace('.', '_')
            MainMenuScreen.temp_email = self.temp_email
            self.root.current = 'mainmenuscreen'
            self.root.transition.direction = 'left'
        except:
            self.dialog.open()

    def dialog_tutup(self, obj):
        self.dialog.dismiss()

    def daftar(self, nama, email, no_hp, password_field_daftar, password_field_daftar_ulangpassword, drop_pertanyaan,
               isi_jawaban):
        if nama == '':
            Snackbar(text="Mohon Isi Nama Anda").show()
        elif email == '':
            Snackbar(text="Mohon Isi Email Anda").show()
        elif no_hp == '':
            Snackbar(text="Mohon Isi No Hp Anda").show()
        elif password_field_daftar == '':
            Snackbar(text="Mohon Isi Password Anda").show()
        elif password_field_daftar_ulangpassword == '':
            Snackbar(text="Mohon Ulangi Password Anda").show()
        elif len(password_field_daftar) <= 6:
            Snackbar(text="Password Terlalu pendek").show()
        elif password_field_daftar != password_field_daftar_ulangpassword:
            Snackbar(text="Password Tidak sama mohon cek kembali password anda").show()
        elif drop_pertanyaan == 'Pertanyaan Keamanan Anda':
            Snackbar(text="Mohon Pilih Pertanyaan Keamanan Anda").show()
        elif isi_jawaban == '':
            Snackbar(text="Mohon isi jawaban anda").show()
        else:
            data = {'nama': "%s" % nama,
                    'email': "%s" % email,
                    'no_hp': "%s" % no_hp,
                    'password_field_daftar': "%s" % password_field_daftar,
                    'drop_pertanyaan': "%s" % drop_pertanyaan,
                    'isi_jawaban': "%s" % isi_jawaban}
            try:
                auth.create_user_with_email_and_password(email, password_field_daftar)
                email = email.replace('.', '_')
                db.child(email).set(data)
                Snackbar(text="Berhasil Mendaftar, Silahkan Masuk kembali").show()
                self.keluar()
            except:
                Snackbar(text="Form Pendaftaran tidak valid, mohon lengkapi kolom dan coba lagi").show()

        print(nama, email, no_hp, password_field_daftar, password_field_daftar_ulangpassword, drop_pertanyaan,
              isi_jawaban)

    def keluar(self):
        self.root.transition.direction = 'right'
        self.root.current = 'loginscreen'

    def inputscreen(self):
        self.root.transition.direction = 'left'
        self.root.current = 'inputscreen'

    def mainmenuscreen(self):
        self.root.transition.direction = 'right'
        self.root.current = 'mainmenuscreen'

    def simpan(self, nama, jenis, chk_msk, chk_klr, jumlah, mata_uang, keterangan):
        if nama == '':
            Snackbar(text="Nama data tidak boleh kosong").show()
        elif jenis == '':
            Snackbar(text="Jenis data tidak boleh kosong").show()
        elif jumlah == '':
            Snackbar(text="Jumalh tidak boleh kosong").show()
        elif len(keterangan) >= 200:
            Snackbar(text="Keterangan terlalu panjang").show()
        else:
            ids = datetime.now()
            id_data = str(ids)
            id_data = id_data.replace(":", "")
            id_data = id_data.replace(".", "")
            id_data = id_data.replace("-", "")
            id_data = id_data.replace(" ", "")

            i = datetime.now()
            tgl = f'{i.day}-{i.month}-{i.year}'

            io = ''
            if chk_msk:
                io = 'Masuk'
            elif chk_klr:
                io = 'Keluar'

            data = {'nama': "%s" % nama,
                    'jenis': "%s" % jenis,
                    'jumlah': "%s" % jumlah,
                    'io': "%s" % io,
                    'mata_uang': "%s" % mata_uang,
                    'keterangan': "%s" % keterangan,
                    'tgl': "%s" % tgl,
                    'ids': "%s" % id_data}

            try:
                db.child(self.temp_email).child("data").child(id_data).set(data)
                Snackbar(text="Data Berhasil Disimpan").show()
            except:
                Snackbar(text="Data Invalid").show()

            self.root.transition.direction = 'right'
            self.root.current = 'mainmenuscreen'

    def edit(self, nama, jenis, mata_uang, chk_msk, chk_klr, jumlah, keterangan, tgl):
        if nama == '':
            Snackbar(text="Nama data tidak boleh kosong").show()
        elif jenis == '':
            Snackbar(text="Jenis data tidak boleh kosong").show()
        elif jumlah == '':
            Snackbar(text="Jumalh tidak boleh kosong").show()
        elif len(keterangan) >= 200:
            Snackbar(text="Keterangan terlalu panjang").show()
        else:

            io = ''
            if chk_msk:
                io = 'Masuk'
            elif chk_klr:
                io = 'Keluar'

            data = {'ids': "%s" % EditScreen.temp_ids,
                    'tgl': "%s" % tgl,
                    'mata_uang': "%s" % mata_uang,
                    'nama': "%s" % nama,
                    'jenis': "%s" % jenis,
                    'jumlah': "%s" % jumlah,
                    'io': "%s" % io,
                    'keterangan': "%s" % keterangan}
            print(data)

            try:
                id_data = EditScreen.temp_ids
                db.child(self.temp_email).child("data").child(id_data).set(data)
                Snackbar(text="Data Berhasil Disimpan").show()

            except:
                Snackbar(text="Data Invalid").show()

            self.root.transition.direction = 'right'
            self.root.current = 'mainmenuscreen'

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        return self.screen


main = VeryMonApp()
main.run()
