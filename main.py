import shutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, \
    QMessageBox, QFileDialog
import os
import json
from parsec import wireguard_connect
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('WireGuard Configuration')

        # Layouts
        main_layout = QVBoxLayout()
        ip_layout = QHBoxLayout()
        mac_layout = QHBoxLayout()
        peer_id_layout = QHBoxLayout()
        profile_layout = QHBoxLayout()
        name_layout = QHBoxLayout()

        # IP
        self.ip_label = QLabel('IP:')
        self.ip_input = QLineEdit(self)
        ip_layout.addWidget(self.ip_label)
        ip_layout.addWidget(self.ip_input)

        # MAC
        self.mac_label = QLabel('MAC Address:')
        self.mac_input = QLineEdit(self)
        mac_layout.addWidget(self.mac_label)
        mac_layout.addWidget(self.mac_input)

        # Peer ID
        self.peer_id_label = QLabel('Peer ID:')
        self.peer_id_input = QLineEdit(self)
        peer_id_layout.addWidget(self.peer_id_label)
        peer_id_layout.addWidget(self.peer_id_input)

        # Profile Path
        self.profile_label = QLabel('WireGuard Profile Path:')
        self.profile_button = QPushButton('Select Profile', self)
        self.profile_button.clicked.connect(self.openFileDialog)
        profile_layout = QHBoxLayout()
        profile_layout.addWidget(self.profile_label)
        profile_layout.addWidget(self.profile_button)

        # Name
        self.name_label = QLabel('Configuration Name:')
        self.name_input = QLineEdit(self)
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)

        # Buttons
        self.save_button = QPushButton('Save Configuration', self)
        self.save_button.clicked.connect(self.save_config)
        self.connect_button = QPushButton('Connect', self)
        self.connect_button.clicked.connect(lambda: wireguard_connect("test", "Mac"))


        # Add layouts to main layout
        main_layout.addLayout(ip_layout)
        main_layout.addLayout(mac_layout)
        main_layout.addLayout(peer_id_layout)
        main_layout.addLayout(profile_layout)
        main_layout.addLayout(name_layout)
        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.connect_button)

        self.setLayout(main_layout)
        self.show()

    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select WireGuard Profile", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            # Copie du fichier sélectionné dans le dossier config/name/vpn
            config_name = self.name_input.text()  # Assurez-vous que name_input est défini et accessible
            target_dir = f'config/{config_name}/vpn'
            os.makedirs(target_dir, exist_ok=True)
            shutil.copy(fileName, target_dir)

    def save_config(self):
        config = {
            'ip': self.ip_input.text(),
            'mac': self.mac_input.text(),
            'peer_id': self.peer_id_input.text(),
            'profile_path': self.profile_input.text()
        }
        config_name = self.name_input.text()
        if config_name:
            os.makedirs(f'config/{config_name}/', exist_ok=True)
            with open(f'config/{config_name}/{config_name}.conf', 'w') as file:
                json.dump(config, file)
            QMessageBox.information(self, 'Success', 'Configuration saved successfully.')
        else:
            QMessageBox.warning(self, 'Error', 'Please enter a configuration name.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
