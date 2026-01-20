#!/usr/bin/env python3
"""
Sinistra Keys v4.1 - Dual Center Mapping + Splash Screen
by kidD Icarus / kidDicarus Inc.

Physical Center + Target Center for proper RTL keyboard reversal.
Your physical middle key plays your target note, everything mirrors around that.

Cross-platform: Mac (IAC Driver) + Windows (loopMIDI)
"""

import sys
import time
import rtmidi
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QFrame, QGroupBox,
    QSpinBox, QGridLayout, QSplashScreen
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QPoint
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QPainter, QBrush, QPen, QLinearGradient, QRadialGradient, QPolygon

# ============== BRANDING COLORS ==============
COLORS = {
    'bg_dark': '#0a0a0a',
    'bg_panel': '#151515',
    'bg_card': '#1a1a1a',
    'crimson': '#8B0000',
    'crimson_light': '#B22222',
    'crimson_bright': '#DC143C',
    'gold': '#DAA520',
    'gold_light': '#FFD700',
    'gold_bright': '#FFF700',
    'text': '#E0E0E0',
    'text_dim': '#808080',
    'border': '#2a2a2a',
    'green': '#228B22',
    'green_light': '#32CD32'
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text']};
}}
QGroupBox {{
    background-color: {COLORS['bg_panel']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 10px;
    font-weight: bold;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
    color: {COLORS['gold']};
}}
QLabel {{
    color: {COLORS['text']};
}}
QComboBox {{
    background-color: {COLORS['bg_panel']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 5px 10px;
    color: {COLORS['text']};
    min-width: 100px;
}}
QComboBox:hover {{
    border-color: {COLORS['crimson']};
}}
QComboBox::drop-down {{
    border: none;
    padding-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_panel']};
    color: {COLORS['text']};
    selection-background-color: {COLORS['crimson']};
}}
QPushButton {{
    background-color: {COLORS['bg_panel']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 6px 12px;
    color: {COLORS['text']};
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: {COLORS['crimson']};
    border-color: {COLORS['crimson_light']};
}}
QPushButton:pressed {{
    background-color: {COLORS['crimson_light']};
}}
QPushButton#startBtn {{
    background-color: {COLORS['crimson']};
    border-color: {COLORS['crimson_light']};
    font-size: 14px;
    padding: 12px 24px;
}}
QPushButton#startBtn:hover {{
    background-color: {COLORS['crimson_light']};
}}
QSpinBox {{
    background-color: {COLORS['bg_panel']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 4px 8px;
    color: {COLORS['text']};
    min-width: 50px;
}}
QFrame#keyboardCard {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 8px;
}}
"""


# ============== SPLASH SCREEN ==============
def create_splash_pixmap():
    """Create a branded splash screen pixmap"""
    width, height = 500, 350
    pixmap = QPixmap(width, height)
    pixmap.fill(QColor('#050505'))
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Background with radial gradient
    bg_gradient = QRadialGradient(width/2, height/2, max(width, height)/2)
    bg_gradient.setColorAt(0, QColor('#1a1a1a'))
    bg_gradient.setColorAt(0.7, QColor('#0f0f0f'))
    bg_gradient.setColorAt(1, QColor('#050505'))
    painter.setBrush(QBrush(bg_gradient))
    painter.setPen(QPen(QColor(COLORS['crimson_light']), 3))
    painter.drawRoundedRect(2, 2, width-4, height-4, 15, 15)
    
    # Crimson glow line at top
    glow_gradient = QLinearGradient(0, 0, width, 0)
    glow_gradient.setColorAt(0, QColor('#050505'))
    glow_gradient.setColorAt(0.3, QColor(COLORS['crimson_bright']))
    glow_gradient.setColorAt(0.5, QColor(COLORS['crimson_light']))
    glow_gradient.setColorAt(0.7, QColor(COLORS['crimson_bright']))
    glow_gradient.setColorAt(1, QColor('#050505'))
    painter.setPen(QPen(QBrush(glow_gradient), 4))
    painter.drawLine(20, 10, width-20, 10)
    
    # k.I. Logo
    painter.setFont(QFont('Arial Black', 72, QFont.Weight.Bold))
    painter.setPen(QColor(COLORS['gold_light']))
    painter.drawText(0, 40, width, 120, Qt.AlignmentFlag.AlignCenter, "k.I.")
    
    # SINISTRA KEYS text
    painter.setFont(QFont('Arial', 28, QFont.Weight.Bold))
    painter.setPen(QColor(COLORS['crimson_light']))
    painter.drawText(0, 140, width, 50, Qt.AlignmentFlag.AlignCenter, "SINISTRA KEYS")
    
    # Subtitle
    painter.setFont(QFont('Arial', 12))
    painter.setPen(QColor(COLORS['text_dim']))
    painter.drawText(0, 185, width, 30, Qt.AlignmentFlag.AlignCenter, "RTL/LTR MIDI Keyboard Engine")
    
    # Piano keys illustration
    keys_y = 220
    keys_x = 100
    key_width = 35
    key_height = 70
    black_key_width = 22
    black_key_height = 45
    
    # White keys
    painter.setBrush(QColor('#F0F0F0'))
    painter.setPen(QPen(QColor('#888888'), 1))
    for i in range(8):
        x = keys_x + i * (key_width + 5)
        painter.drawRoundedRect(x, keys_y, key_width, key_height, 3, 3)
    
    # Black keys
    painter.setBrush(QColor('#1a1a1a'))
    painter.setPen(QPen(QColor('#333333'), 1))
    black_positions = [0, 1, 3, 4, 5]
    for i in black_positions:
        x = keys_x + i * (key_width + 5) + key_width - black_key_width//2 + 2
        painter.drawRoundedRect(x, keys_y, black_key_width, black_key_height, 2, 2)
    
    # RTL Arrow
    painter.setBrush(QColor(COLORS['crimson']))
    painter.setPen(Qt.PenStyle.NoPen)
    arrow_y = keys_y + 25
    arrow_points = [
        QPoint(keys_x + 30, arrow_y + 10),
        QPoint(keys_x + 60, arrow_y - 10),
        QPoint(keys_x + 60, arrow_y),
        QPoint(keys_x + 280, arrow_y),
        QPoint(keys_x + 280, arrow_y + 20),
        QPoint(keys_x + 60, arrow_y + 20),
        QPoint(keys_x + 60, arrow_y + 30),
    ]
    painter.setOpacity(0.7)
    painter.drawPolygon(QPolygon(arrow_points))
    painter.setOpacity(1.0)
    
    # Loading text
    painter.setFont(QFont('Arial', 11))
    painter.setPen(QColor(COLORS['gold']))
    painter.drawText(0, height - 50, width, 30, Qt.AlignmentFlag.AlignCenter, "Initializing MIDI Engine...")
    
    # Footer
    painter.setFont(QFont('Arial', 9))
    painter.setPen(QColor(COLORS['text_dim']))
    painter.drawText(0, height - 30, width, 20, Qt.AlignmentFlag.AlignCenter, 
                     "kidD Icarus • kidDicarus Inc. • Notatio Sinistra")
    
    painter.end()
    return pixmap


# ============== NOTE HELPERS ==============
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def midi_to_name(note):
    if note < 0 or note > 127:
        return '???'
    octave = (note // 12) - 1
    name = NOTE_NAMES[note % 12]
    return f"{name}{octave}"

def name_to_midi(name):
    name = name.strip().upper()
    name = name.replace('DB', 'C#').replace('EB', 'D#').replace('GB', 'F#')
    name = name.replace('AB', 'G#').replace('BB', 'A#')
    
    for i, n in enumerate(NOTE_NAMES):
        if name.startswith(n):
            rest = name[len(n):]
            if rest.lstrip('-').isdigit():
                octave = int(rest)
                return i + 12 * (octave + 1)
    return 60


# ============== KEYBOARD INPUT HANDLER ==============
class KeyboardInput:
    def __init__(self, index, on_note_callback):
        self.index = index
        self.midi_in = None
        self.midi_out = None
        self.on_note_callback = on_note_callback
        self.active = False
        
        self.rtl_mode = True
        self.physical_center = 52
        self.target_center = 60
        self.low = 36
        self.high = 96
        self.channel_filter = 0
        
    def transform_note(self, note):
        if not self.rtl_mode:
            return note
        transformed = self.physical_center + self.target_center - note
        while transformed < self.low:
            transformed += 12
        while transformed > self.high:
            transformed -= 12
        return max(0, min(127, transformed))
    
    def midi_callback(self, event, data=None):
        message, delta_time = event
        if len(message) < 3:
            if self.midi_out:
                self.midi_out.send_message(message)
            return
        
        status = message[0]
        channel = status & 0x0F
        msg_type = status & 0xF0
        
        if self.channel_filter > 0 and channel != (self.channel_filter - 1):
            if self.midi_out:
                self.midi_out.send_message(message)
            return
        
        if msg_type in (0x90, 0x80):
            in_note = message[1]
            velocity = message[2]
            out_note = self.transform_note(in_note)
            out_message = [status, out_note, velocity]
            
            if self.midi_out:
                self.midi_out.send_message(out_message)
            
            event_type = 'ON' if msg_type == 0x90 and velocity > 0 else 'OFF'
            self.on_note_callback(self.index, in_note, out_note, event_type)
        else:
            if self.midi_out:
                self.midi_out.send_message(message)
    
    def start(self, in_port_index, out_port_index):
        try:
            self.midi_in = rtmidi.MidiIn()
            self.midi_out = rtmidi.MidiOut()
            self.midi_in.open_port(in_port_index)
            self.midi_out.open_port(out_port_index)
            self.midi_in.set_callback(self.midi_callback)
            self.active = True
            return True, "Connected"
        except Exception as e:
            self.stop()
            return False, str(e)
    
    def stop(self):
        self.active = False
        if self.midi_in:
            self.midi_in.close_port()
            self.midi_in = None
        if self.midi_out:
            self.midi_out.close_port()
            self.midi_out = None


# ============== SIGNALS ==============
class MIDISignals(QObject):
    note_processed = pyqtSignal(int, int, int, str)


# ============== KEYBOARD CARD WIDGET ==============
class KeyboardCard(QFrame):
    def __init__(self, index, input_ports, output_ports, parent=None):
        super().__init__(parent)
        self.index = index
        self.setObjectName("keyboardCard")
        self.init_ui(input_ports, output_ports)
        
    def init_ui(self, input_ports, output_ports):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 10)
        
        header = QHBoxLayout()
        self.title_label = QLabel(f"KB {self.index + 1}")
        self.title_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.title_label.setStyleSheet(f"color: {COLORS['gold']};")
        header.addWidget(self.title_label)
        header.addStretch()
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 14px;")
        header.addWidget(self.status_indicator)
        layout.addLayout(header)
        
        in_layout = QHBoxLayout()
        in_layout.addWidget(QLabel("In:"))
        self.in_port_combo = QComboBox()
        self.in_port_combo.addItem("-- None --")
        for port in input_ports:
            self.in_port_combo.addItem(port)
        in_layout.addWidget(self.in_port_combo, 1)
        layout.addLayout(in_layout)
        
        out_layout = QHBoxLayout()
        out_layout.addWidget(QLabel("Out:"))
        self.out_port_combo = QComboBox()
        self.out_port_combo.addItem("-- None --")
        for port in output_ports:
            self.out_port_combo.addItem(port)
        out_layout.addWidget(self.out_port_combo, 1)
        layout.addLayout(out_layout)
        
        mode_layout = QHBoxLayout()
        self.rtl_btn = QPushButton("◀ RTL")
        self.rtl_btn.setCheckable(True)
        self.rtl_btn.setChecked(True)
        self.rtl_btn.clicked.connect(lambda: self.set_mode(True))
        mode_layout.addWidget(self.rtl_btn)
        self.ltr_btn = QPushButton("LTR ▶")
        self.ltr_btn.setCheckable(True)
        self.ltr_btn.clicked.connect(lambda: self.set_mode(False))
        mode_layout.addWidget(self.ltr_btn)
        layout.addLayout(mode_layout)
        
        phys_layout = QHBoxLayout()
        phys_layout.addWidget(QLabel("Phys:"))
        self.physical_combo = QComboBox()
        self.physical_combo.addItems(['C2', 'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'C5'])
        self.physical_combo.setCurrentText('E3')
        phys_layout.addWidget(self.physical_combo, 1)
        layout.addLayout(phys_layout)
        
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Target:"))
        self.target_combo = QComboBox()
        self.target_combo.addItems(['C2', 'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'C5'])
        self.target_combo.setCurrentText('C4')
        target_layout.addWidget(self.target_combo, 1)
        layout.addLayout(target_layout)
        
        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("L:"))
        self.low_spin = QSpinBox()
        self.low_spin.setRange(0, 127)
        self.low_spin.setValue(36)
        range_layout.addWidget(self.low_spin)
        range_layout.addWidget(QLabel("H:"))
        self.high_spin = QSpinBox()
        self.high_spin.setRange(0, 127)
        self.high_spin.setValue(96)
        range_layout.addWidget(self.high_spin)
        layout.addLayout(range_layout)
        
        self.note_label = QLabel("—")
        self.note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.note_label.setFont(QFont("Courier", 12, QFont.Weight.Bold))
        self.note_label.setStyleSheet(f"color: {COLORS['gold']}; padding: 6px; background-color: {COLORS['bg_panel']}; border-radius: 4px;")
        layout.addWidget(self.note_label)
        
        self.update_mode_buttons()
        
    def set_mode(self, rtl):
        self.rtl_btn.setChecked(rtl)
        self.ltr_btn.setChecked(not rtl)
        self.update_mode_buttons()
        
    def update_mode_buttons(self):
        if self.rtl_btn.isChecked():
            self.rtl_btn.setStyleSheet(f"background-color: {COLORS['crimson']}; border-color: {COLORS['crimson_light']};")
            self.ltr_btn.setStyleSheet(f"background-color: {COLORS['bg_panel']};")
        else:
            self.ltr_btn.setStyleSheet(f"background-color: {COLORS['crimson']}; border-color: {COLORS['crimson_light']};")
            self.rtl_btn.setStyleSheet(f"background-color: {COLORS['bg_panel']};")
    
    def set_active(self, active):
        if active:
            self.status_indicator.setStyleSheet(f"color: {COLORS['green_light']}; font-size: 14px;")
            self.setStyleSheet(f"QFrame#keyboardCard {{ background-color: {COLORS['bg_card']}; border: 2px solid {COLORS['green']}; border-radius: 8px; }}")
        else:
            self.status_indicator.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 14px;")
            self.setStyleSheet(f"QFrame#keyboardCard {{ background-color: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 8px; }}")
    
    def update_note(self, in_note, out_note):
        self.note_label.setText(f"{midi_to_name(in_note)}→{midi_to_name(out_note)}")
    
    def get_settings(self):
        return {
            'in_port_index': self.in_port_combo.currentIndex() - 1,
            'out_port_index': self.out_port_combo.currentIndex() - 1,
            'rtl_mode': self.rtl_btn.isChecked(),
            'physical_center': name_to_midi(self.physical_combo.currentText()),
            'target_center': name_to_midi(self.target_combo.currentText()),
            'low': self.low_spin.value(),
            'high': self.high_spin.value()
        }
    
    def refresh_ports(self, input_ports, output_ports):
        current_in = self.in_port_combo.currentText()
        current_out = self.out_port_combo.currentText()
        self.in_port_combo.clear()
        self.in_port_combo.addItem("-- None --")
        for port in input_ports:
            self.in_port_combo.addItem(port)
        self.out_port_combo.clear()
        self.out_port_combo.addItem("-- None --")
        for port in output_ports:
            self.out_port_combo.addItem(port)
        idx = self.in_port_combo.findText(current_in)
        if idx >= 0:
            self.in_port_combo.setCurrentIndex(idx)
        idx = self.out_port_combo.findText(current_out)
        if idx >= 0:
            self.out_port_combo.setCurrentIndex(idx)


# ============== MAIN WINDOW ==============
class SinistraKeysDualCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signals = MIDISignals()
        self.signals.note_processed.connect(self.on_note_processed)
        self.keyboard_inputs = []
        self.keyboard_cards = []
        self.running = False
        self.init_ui()
        
    def get_input_ports(self):
        return rtmidi.MidiIn().get_ports()
    
    def get_output_ports(self):
        return rtmidi.MidiOut().get_ports()
        
    def init_ui(self):
        self.setWindowTitle("Sinistra Keys — Dual Center Mapping")
        self.setMinimumSize(950, 650)
        self.setStyleSheet(STYLESHEET)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(16, 16, 16, 16)
        
        header = QHBoxLayout()
        logo_label = QLabel("k.I.")
        logo_label.setFont(QFont("Arial Black", 22, QFont.Weight.Bold))
        logo_label.setStyleSheet(f"color: {COLORS['gold']};")
        header.addWidget(logo_label)
        title_label = QLabel("SINISTRA KEYS")
        title_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {COLORS['crimson_light']};")
        header.addWidget(title_label)
        header.addStretch()
        refresh_btn = QPushButton("↻ Refresh Ports")
        refresh_btn.clicked.connect(self.refresh_all_ports)
        header.addWidget(refresh_btn)
        version_label = QLabel("v4.1")
        version_label.setStyleSheet(f"color: {COLORS['text_dim']};")
        header.addWidget(version_label)
        layout.addLayout(header)
        
        subtitle = QLabel("Phys = what your keyboard sends | Target = what you want to hear")
        subtitle.setStyleSheet(f"color: {COLORS['text_dim']};")
        layout.addWidget(subtitle)
        
        keyboards_group = QGroupBox("Keyboards")
        keyboards_layout = QGridLayout(keyboards_group)
        keyboards_layout.setSpacing(10)
        
        input_ports = self.get_input_ports()
        output_ports = self.get_output_ports()
        
        for i in range(6):
            card = KeyboardCard(i, input_ports, output_ports)
            self.keyboard_cards.append(card)
            keyboard_input = KeyboardInput(i, self.note_callback)
            self.keyboard_inputs.append(keyboard_input)
            keyboards_layout.addWidget(card, i // 3, i % 3)
        
        layout.addWidget(keyboards_group)
        
        control_layout = QHBoxLayout()
        self.start_btn = QPushButton("▶ START ALL")
        self.start_btn.setObjectName("startBtn")
        self.start_btn.clicked.connect(self.toggle_processing)
        control_layout.addWidget(self.start_btn)
        self.stop_btn = QPushButton("■ STOP ALL")
        self.stop_btn.clicked.connect(self.stop_all)
        control_layout.addWidget(self.stop_btn)
        layout.addLayout(control_layout)
        
        self.status_label = QLabel("Status: Stopped")
        self.status_label.setStyleSheet(f"color: {COLORS['text_dim']};")
        layout.addWidget(self.status_label)
        
        self.routing_label = QLabel("")
        self.routing_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 11px;")
        self.routing_label.setWordWrap(True)
        layout.addWidget(self.routing_label)
        
        footer = QLabel("kidD Icarus • kidDicarus Inc. • Notatio Sinistra")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet(f"color: {COLORS['text_dim']}; margin-top: 4px;")
        layout.addWidget(footer)
    
    def refresh_all_ports(self):
        input_ports = self.get_input_ports()
        output_ports = self.get_output_ports()
        for card in self.keyboard_cards:
            card.refresh_ports(input_ports, output_ports)
        self.status_label.setText("Status: Ports refreshed")
    
    def note_callback(self, keyboard_idx, in_note, out_note, event_type):
        self.signals.note_processed.emit(keyboard_idx, in_note, out_note, event_type)
    
    def on_note_processed(self, keyboard_idx, in_note, out_note, event_type):
        if event_type == 'ON':
            self.keyboard_cards[keyboard_idx].update_note(in_note, out_note)
    
    def toggle_processing(self):
        if self.running:
            self.stop_all()
        else:
            self.start_all()
    
    def start_all(self):
        active_count = 0
        routing_info = []
        
        for i, (card, kb_input) in enumerate(zip(self.keyboard_cards, self.keyboard_inputs)):
            settings = card.get_settings()
            if settings['in_port_index'] < 0 or settings['out_port_index'] < 0:
                card.set_active(False)
                continue
            
            kb_input.rtl_mode = settings['rtl_mode']
            kb_input.physical_center = settings['physical_center']
            kb_input.target_center = settings['target_center']
            kb_input.low = settings['low']
            kb_input.high = settings['high']
            
            success, msg = kb_input.start(settings['in_port_index'], settings['out_port_index'])
            card.set_active(success)
            
            if success:
                active_count += 1
                mode = "RTL" if settings['rtl_mode'] else "LTR"
                routing_info.append(f"KB{i+1}: {card.physical_combo.currentText()}→{card.target_combo.currentText()} ({mode})")
        
        if active_count > 0:
            self.running = True
            self.start_btn.setText("▶ RUNNING")
            self.status_label.setText(f"Status: {active_count} keyboard(s) active")
            self.status_label.setStyleSheet(f"color: {COLORS['gold']};")
            self.routing_label.setText(" | ".join(routing_info))
        else:
            self.status_label.setText("Status: No keyboards configured (select In + Out)")
    
    def stop_all(self):
        for kb_input, card in zip(self.keyboard_inputs, self.keyboard_cards):
            kb_input.stop()
            card.set_active(False)
        self.running = False
        self.start_btn.setText("▶ START ALL")
        self.status_label.setText("Status: Stopped")
        self.status_label.setStyleSheet(f"color: {COLORS['text_dim']};")
        self.routing_label.setText("")
    
    def closeEvent(self, event):
        self.stop_all()
        event.accept()


# ============== MAIN ==============
def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(COLORS['bg_dark']))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(COLORS['text']))
    palette.setColor(QPalette.ColorRole.Base, QColor(COLORS['bg_panel']))
    palette.setColor(QPalette.ColorRole.Text, QColor(COLORS['text']))
    palette.setColor(QPalette.ColorRole.Button, QColor(COLORS['bg_panel']))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(COLORS['text']))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(COLORS['crimson']))
    app.setPalette(palette)
    
    # Show splash screen
    splash_pixmap = create_splash_pixmap()
    splash = QSplashScreen(splash_pixmap)
    splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
    splash.show()
    app.processEvents()
    
    # Initialize
    time.sleep(1.5)
    
    window = SinistraKeysDualCenter()
    window.show()
    splash.finish(window)
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
