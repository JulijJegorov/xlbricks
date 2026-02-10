"""
PyQt UI for editing xlbricks.json configuration.
Loaded from Excel in the same way as XLBricks Wizard.
"""

import json
import os
import os.path as osp
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QMessageBox,
    QGroupBox,
    QLabel,
    QAbstractItemView,
)
from PyQt5.QtCore import Qt


def get_default_config_path():
    """Return the path to xlbricks.json in the xlbricks package directory."""
    pkg_dir = osp.dirname(osp.dirname(osp.abspath(__file__)))
    return osp.join(pkg_dir, 'xlbricks.json')


def load_config(path):
    """Load config from JSON file. Returns dict or None on error."""
    if not path or not osp.isfile(path):
        return _default_config()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return _normalize_config(data)
    except Exception:
        return _default_config()


def _default_config():
    return {
        'INTERPRETER': '',
        'PYTHONPATH': '',
        'CONTEXT': {},
    }


def _normalize_config(data):
    """Ensure required keys exist."""
    out = _default_config()
    out['INTERPRETER'] = data.get('INTERPRETER', '')
    out['PYTHONPATH'] = data.get('PYTHONPATH', '')
    out['CONTEXT'] = dict(data.get('CONTEXT', {}))
    return out


def save_config(path, data):
    """Save config to JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class ConfigEditorDialog(QDialog):
    """User-friendly dialog to edit xlbricks.json."""

    def __init__(self, config_path=None, parent=None):
        super(ConfigEditorDialog, self).__init__(parent)
        self._config_path = config_path or get_default_config_path()
        self.setWindowTitle('XLBricks Config')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Window)
        self.setMinimumSize(520, 480)
        self._build_ui()
        self._load_into_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # --- Interpreter ---
        grp_interpreter = QGroupBox('Python interpreter')
        grp_interpreter.setToolTip('Path to pythonw.exe or python.exe used by the add-in')
        fl_interpreter = QFormLayout(grp_interpreter)
        self._interpreter_edit = QLineEdit()
        self._interpreter_edit.setPlaceholderText(r'C:\...\pythonw.exe')
        self._interpreter_edit.setMinimumWidth(320)
        btn_browse = QPushButton('Browse...')
        btn_browse.setMaximumWidth(90)
        btn_browse.clicked.connect(self._browse_interpreter)
        row = QHBoxLayout()
        row.addWidget(self._interpreter_edit)
        row.addWidget(btn_browse)
        fl_interpreter.addRow('Path:', row)
        layout.addWidget(grp_interpreter)

        # --- PYTHONPATH ---
        grp_path = QGroupBox('PYTHONPATH')
        grp_path.setToolTip('Paths added to Python when running from Excel. One path per row.')
        path_layout = QVBoxLayout(grp_path)
        self._path_table = QTableWidget()
        self._path_table.setColumnCount(1)
        self._path_table.setHorizontalHeaderLabels(['Path'])
        self._path_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self._path_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._path_table.setMinimumHeight(100)
        path_layout.addWidget(self._path_table)
        path_btn_row = QHBoxLayout()
        btn_add_path = QPushButton('Add path')
        btn_add_path_browse = QPushButton('Browse...')
        btn_remove_path = QPushButton('Remove selected')
        btn_add_path.clicked.connect(self._add_path_row)
        btn_add_path_browse.clicked.connect(self._browse_path_row)
        btn_remove_path.clicked.connect(self._remove_path_row)
        path_btn_row.addWidget(btn_add_path)
        path_btn_row.addWidget(btn_add_path_browse)
        path_btn_row.addWidget(btn_remove_path)
        path_btn_row.addStretch()
        path_layout.addLayout(path_btn_row)
        layout.addWidget(grp_path)

        # --- CONTEXT ---
        grp_context = QGroupBox('Context')
        grp_context.setToolTip('Context name → module path. Used to resolve context objects.')
        ctx_layout = QVBoxLayout(grp_context)
        self._context_table = QTableWidget()
        self._context_table.setColumnCount(2)
        self._context_table.setHorizontalHeaderLabels(['Context name', 'Module path'])
        self._context_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self._context_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._context_table.setMinimumHeight(140)
        ctx_layout.addWidget(self._context_table)
        btn_row = QHBoxLayout()
        btn_add_ctx = QPushButton('Add context')
        btn_remove_ctx = QPushButton('Remove selected')
        btn_add_ctx.clicked.connect(self._add_context_row)
        btn_remove_ctx.clicked.connect(self._remove_context_row)
        btn_row.addWidget(btn_add_ctx)
        btn_row.addWidget(btn_remove_ctx)
        btn_row.addStretch()
        ctx_layout.addLayout(btn_row)
        layout.addWidget(grp_context)

        # --- Config file path (read-only) ---
        self._path_label = QLabel(self._config_path)
        self._path_label.setStyleSheet('color: gray; font-size: 11px;')
        self._path_label.setWordWrap(True)
        layout.addWidget(self._path_label)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self._save_btn = QPushButton('Save')
        self._save_btn.setDefault(True)
        self._save_btn.setMinimumWidth(90)
        self._cancel_btn = QPushButton('Cancel')
        self._cancel_btn.setMinimumWidth(90)
        self._save_btn.clicked.connect(self._save)
        self._cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self._save_btn)
        btn_layout.addWidget(self._cancel_btn)
        layout.addLayout(btn_layout)

    def _browse_interpreter(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Select Python interpreter',
            os.path.expanduser('~'),
            'Executables (*.exe);;All files (*)',
        )
        if path:
            self._interpreter_edit.setText(path)

    def _add_context_row(self):
        row = self._context_table.rowCount()
        self._context_table.insertRow(row)
        self._context_table.setItem(row, 0, QTableWidgetItem(''))
        self._context_table.setItem(row, 1, QTableWidgetItem(''))

    def _remove_context_row(self):
        row = self._context_table.currentRow()
        if row >= 0:
            self._context_table.removeRow(row)

    def _add_path_row(self):
        row = self._path_table.rowCount()
        self._path_table.insertRow(row)
        self._path_table.setItem(row, 0, QTableWidgetItem(''))

    def _browse_path_row(self):
        path = QFileDialog.getExistingDirectory(self, 'Select folder to add to PYTHONPATH')
        if path:
            row = self._path_table.rowCount()
            self._path_table.insertRow(row)
            self._path_table.setItem(row, 0, QTableWidgetItem(path))

    def _remove_path_row(self):
        row = self._path_table.currentRow()
        if row >= 0:
            self._path_table.removeRow(row)

    def _load_into_ui(self):
        data = load_config(self._config_path)
        self._interpreter_edit.setText(data.get('INTERPRETER', ''))
        path_str = data.get('PYTHONPATH', '')
        # Support both newline and semicolon separation
        if ';' in path_str and '\n' not in path_str:
            paths = [p.strip() for p in path_str.split(';') if p.strip()]
        else:
            paths = [p.strip() for p in path_str.replace(';', '\n').splitlines() if p.strip()]
        self._path_table.setRowCount(0)
        for p in paths:
            row = self._path_table.rowCount()
            self._path_table.insertRow(row)
            self._path_table.setItem(row, 0, QTableWidgetItem(p))
        ctx = data.get('CONTEXT', {})
        self._context_table.setRowCount(0)
        for name, mod in ctx.items():
            row = self._context_table.rowCount()
            self._context_table.insertRow(row)
            self._context_table.setItem(row, 0, QTableWidgetItem(name))
            self._context_table.setItem(row, 1, QTableWidgetItem(mod))

    def _collect_from_ui(self):
        paths = []
        for r in range(self._path_table.rowCount()):
            item = self._path_table.item(r, 0)
            p = (item.text() if item else '').strip()
            if p:
                paths.append(p)
        path_sep = os.pathsep
        ctx = {}
        for r in range(self._context_table.rowCount()):
            name_item = self._context_table.item(r, 0)
            mod_item = self._context_table.item(r, 1)
            name = (name_item.text() if name_item else '').strip()
            mod = (mod_item.text() if mod_item else '').strip()
            if name:
                ctx[name] = mod
        return {
            'INTERPRETER': self._interpreter_edit.text().strip(),
            'PYTHONPATH': path_sep.join(paths),
            'CONTEXT': ctx,
        }

    def _save(self):
        data = self._collect_from_ui()
        try:
            dir_path = osp.dirname(self._config_path)
            if dir_path and not osp.isdir(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            save_config(self._config_path, data)
            QMessageBox.information(self, 'Saved', 'Config saved to:\n' + self._config_path)
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self,
                'Save failed',
                'Could not save config:\n' + str(e),
            )


def show_config_editor(config_path=None, parent=None):
    """Show the config editor dialog. Returns True if saved, False if cancelled."""
    dlg = ConfigEditorDialog(config_path=config_path, parent=parent)
    return dlg.exec_() == QDialog.Accepted
