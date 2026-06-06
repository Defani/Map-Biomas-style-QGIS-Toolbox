# startup.py — MapBiomas ID Quick Launch Button
# Letakkan file ini di:
#   Windows : C:\Users\<nama>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\startup.py
#   Linux   : ~/.local/share/QGIS/QGIS3/profiles/default/python/startup.py
#
# QGIS akan otomatis menjalankan file ini setiap kali dibuka.
# Tombol "MapBiomas ID Style" akan muncul di toolbar QGIS.

from qgis.PyQt.QtCore import QTimer

def _add_mapbiomas_button():
    from qgis.utils import iface
    from qgis.PyQt.QtWidgets import QAction, QMessageBox
    from qgis.core import QgsApplication

    def run_tool():
        reg = QgsApplication.processingRegistry()
        target = None
        for alg in reg.algorithms():
            if 'mapbiomas_raster_to_vector' in alg.id():
                target = alg.id()
                break
        if target:
            import processing
            processing.execAlgorithmDialog(target)
        else:
            QMessageBox.warning(
                iface.mainWindow(),
                'MapBiomas ID Style',
                'Script tidak ditemukan.\n\n'
                'Pastikan mapbiomas_01_raster_to_vector.py\n'
                'sudah ada di folder Scripts Processing.\n\n'
                'Processing Toolbox > Scripts > Open Scripts Folder'
            )

    action = QAction('MapBiomas ID Style', iface.mainWindow())
    action.setToolTip(
        'Simbolisasi Raster MapBiomas\n'
        'Penulis: Defani Arman Alfitriansyah\n'
        'github.com/Defani'
    )
    action.triggered.connect(run_tool)
    iface.addToolBarIcon(action)
    iface.mainWindow()._mapbiomas_btn = action

QTimer.singleShot(3000, _add_mapbiomas_button)
