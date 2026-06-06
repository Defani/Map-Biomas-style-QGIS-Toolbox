# Simbolisasi Raster MapBiomas
# Penulis : Defani Arman Alfitriansyah
# GitHub  : https://github.com/Defani
# Toolbox : MapBiomas ID Custom Visualization Toolbox

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing, QgsProcessingAlgorithm,
    QgsProcessingParameterRasterLayer, QgsProcessingParameterBand,
    QgsProcessingParameterVectorDestination, QgsProcessingParameterBoolean,
    QgsVectorLayer, QgsField,
    QgsRendererCategory, QgsCategorizedSymbolRenderer, QgsFillSymbol,
    QgsProject, QgsProcessingException,
)
import processing

MAPBIOMAS_CLASSES = {
    1:  ("Forest",                   "Hutan",                      "Forest",                    "Hutan",             "#1f8d49"),
    3:  ("Forest Formation",         "Formasi Hutan",              "Forest",                    "Hutan",             "#1f8d49"),
    5:  ("Mangrove",                 "Mangrove",                   "Forest",                    "Hutan",             "#04381d"),
    76: ("Peat Swamp Forest",        "Hutan Rawa Gambut",          "Forest",                    "Hutan",             "#2f7360"),
    10: ("Non-Forest Natural Form.", "Tumbuhan Non-Hutan",         "Non-Forest Natural Form.",  "Tumbuhan Non-Hutan","#d6bc74"),
    13: ("Other Natural Vegetation", "Tumbuhan Non-Hutan Lainnya", "Non-Forest Natural Form.",  "Tumbuhan Non-Hutan","#d89f5c"),
    18: ("Agriculture",              "Pertanian",                  "Agriculture",               "Pertanian",         "#E974ED"),
    40: ("Rice Paddy",               "Sawah",                      "Agriculture",               "Pertanian",         "#c71585"),
    35: ("Oil Palm",                 "Sawit",                      "Agriculture",               "Pertanian",         "#9065d0"),
    9:  ("Pulpwood Plantation",      "Kebun Kayu",                 "Agriculture",               "Pertanian",         "#7a5900"),
    21: ("Other Agriculture",        "Pertanian Lainnya",          "Agriculture",               "Pertanian",         "#ffefc3"),
    22: ("Non-Vegetated Area",       "Non-Vegetasi",               "Non-Vegetated Area",        "Non-Vegetasi",      "#d4271e"),
    30: ("Mining Pit",               "Lubang Tambang",             "Non-Vegetated Area",        "Non-Vegetasi",      "#9c0027"),
    24: ("Urban Area",               "Permukiman",                 "Non-Vegetated Area",        "Non-Vegetasi",      "#d4271e"),
    25: ("Other Non-Vegetation",     "Non-Vegetasi Lainnya",       "Non-Vegetated Area",        "Non-Vegetasi",      "#db4d4f"),
    26: ("Water Body",               "Tubuh Air",                  "Water Body",                "Tubuh Air",         "#2532e4"),
    31: ("Aquaculture",              "Tambak",                     "Water Body",                "Tubuh Air",         "#091077"),
    33: ("River, Lake, Ocean",       "Sungai, Danau, Laut",        "Water Body",                "Tubuh Air",         "#2532e4"),
    27: ("Not Observed",             "Citra Tertutup Awan",        "Not Defined",               "Tdk Terdefinisi",   "#ffffff"),
}
LEGEND_ORDER = [3, 5, 76, 13, 40, 35, 9, 21, 30, 24, 25, 31, 33, 27, 1, 10, 18, 22, 26]


def _apply_symbology(layer, field='gridcode'):
    """
    Membuat legenda hanya dari kelas yang benar-benar ada di data.
    Kelas yang tidak hadir di layer tidak ditampilkan di legenda.
    """
    # Kumpulkan nilai gridcode unik yang ada di layer
    present_values = set()
    for feat in layer.getFeatures():
        try:
            val = int(feat[field])
            present_values.add(val)
        except (TypeError, ValueError):
            pass

    categories = []

    # Urutkan sesuai LEGEND_ORDER, hanya yang ada di data
    ordered = [k for k in LEGEND_ORDER if k in present_values and k in MAPBIOMAS_CLASSES]
    # Tambahkan kelas yang ada di data tapi tidak ada di LEGEND_ORDER
    ordered += [k for k in present_values if k not in ordered and k in MAPBIOMAS_CLASSES]

    for pid in ordered:
        _, c_id, _, _, hx = MAPBIOMAS_CLASSES[pid]
        sym = QgsFillSymbol.createSimple({'color': hx, 'outline_style': 'no'})
        categories.append(QgsRendererCategory(pid, sym, f"[{pid}]  {c_id}"))

    # Kelas tidak diketahui — hanya tampil jika ada nilai di luar MAPBIOMAS_CLASSES
    unknown_present = present_values - set(MAPBIOMAS_CLASSES.keys())
    if unknown_present:
        sym_unk = QgsFillSymbol.createSimple({'color': '#aaaaaa', 'outline_style': 'no'})
        categories.append(QgsRendererCategory('', sym_unk, '[?]  Tidak Diketahui'))

    layer.setRenderer(QgsCategorizedSymbolRenderer(field, categories))
    layer.triggerRepaint()


class MapBiomasRasterToVectorAlgorithm(QgsProcessingAlgorithm):
    INPUT_RASTER   = 'INPUT_RASTER'
    BAND           = 'BAND'
    OUTPUT_VECTOR  = 'OUTPUT_VECTOR'
    LOAD_TO_CANVAS = 'LOAD_TO_CANVAS'

    def tr(self, s): return QCoreApplication.translate('Processing', s)
    def createInstance(self): return MapBiomasRasterToVectorAlgorithm()
    def name(self):        return 'mapbiomas_raster_to_vector'
    def displayName(self): return self.tr('Simbolisasi Raster MapBiomas')
    def group(self):       return self.tr('MapBiomas ID Custom Visualization Toolbox')
    def groupId(self):     return 'mapbiomas_id'

    def shortHelpString(self):
        return self.tr(
            "<b>Simbolisasi Raster MapBiomas Indonesia</b>"
            "<hr>"
            "Alur kerja otomatis:<br>"
            "1. Polygonize raster ke vektor polygon<br>"
            "2. Isi atribut berdasarkan gridcode<br>"
            "3. Simbologi warna ATBD<br>"
            "4. Legenda hanya menampilkan kelas yang ada di data<br>"
            "<hr>"
            "Penulis : Defani Arman Alfitriansyah<br>"
            "GitHub  : <a href='https://github.com/Defani'>github.com/Defani</a>")

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            self.INPUT_RASTER, self.tr('Raster MapBiomas Indonesia')))
        self.addParameter(QgsProcessingParameterBand(
            self.BAND, self.tr('Band (default Band 1)'),
            parentLayerParameterName=self.INPUT_RASTER, defaultValue=1))
        self.addParameter(QgsProcessingParameterVectorDestination(
            self.OUTPUT_VECTOR, self.tr('Output Vektor Polygon'),
            type=QgsProcessing.TypeVectorPolygon))
        self.addParameter(QgsProcessingParameterBoolean(
            self.LOAD_TO_CANVAS,
            self.tr('Muat ke kanvas dengan simbologi ATBD'), defaultValue=True))

    def processAlgorithm(self, parameters, context, feedback):
        raster   = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        band     = self.parameterAsInt(parameters, self.BAND, context)
        out_path = self.parameterAsOutputLayer(parameters, self.OUTPUT_VECTOR, context)
        load     = self.parameterAsBool(parameters, self.LOAD_TO_CANVAS, context)

        if raster is None:
            raise QgsProcessingException(self.tr('Raster layer tidak valid.'))

        feedback.setProgressText('Langkah 1/4 — Polygonize raster ke vektor ...')
        poly = processing.run('gdal:polygonize', {
            'INPUT': raster, 'BAND': band, 'FIELD': 'gridcode',
            'EIGHT_CONNECTEDNESS': False, 'EXTRA': '', 'OUTPUT': 'TEMPORARY_OUTPUT',
        }, context=context, feedback=feedback, is_child_algorithm=True)
        if feedback.isCanceled(): return {}
        feedback.setProgress(30)

        feedback.setProgressText('Langkah 2/4 — Menambahkan field atribut ...')
        tmp = QgsVectorLayer(poly['OUTPUT'], 'tmp', 'ogr')
        if not tmp.isValid():
            raise QgsProcessingException(self.tr('Polygonize gagal.'))
        dp = tmp.dataProvider()
        dp.addAttributes([
            QgsField('class_id',   QVariant.Int,    len=10),
            QgsField('class_en',   QVariant.String, len=80),
            QgsField('class_id_b', QVariant.String, len=80),
            QgsField('lv1_en',     QVariant.String, len=80),
            QgsField('lv1_id',     QVariant.String, len=80),
            QgsField('hex_color',  QVariant.String, len=10),
        ])
        tmp.updateFields()
        feedback.setProgress(38)

        feedback.setProgressText('Langkah 3/4 — Mengisi tabel atribut ...')
        flds = tmp.fields()
        i = {n: flds.indexOf(n) for n in
             ['gridcode','class_id','class_en','class_id_b','lv1_en','lv1_id','hex_color']}
        tmp.startEditing()
        n_feat = tmp.featureCount()
        step   = max(1, n_feat // 50)
        unknown = set()

        for idx, feat in enumerate(tmp.getFeatures()):
            if feedback.isCanceled():
                tmp.rollBack(); return {}
            if idx % step == 0:
                feedback.setProgress(38 + int(37 * idx / max(n_feat, 1)))
            try:   gc = int(feat[i['gridcode']])
            except: gc = -1
            if gc in MAPBIOMAS_CLASSES:
                c_en, c_id, l1_en, l1_id, hx = MAPBIOMAS_CLASSES[gc]
            else:
                unknown.add(gc)
                c_en, c_id, l1_en, l1_id, hx = (
                    f'Unknown({gc})', f'Tidak Diketahui({gc})',
                    'Unknown', 'Unknown', '#aaaaaa')
            fid = feat.id()
            tmp.changeAttributeValue(fid, i['class_id'],   gc)
            tmp.changeAttributeValue(fid, i['class_en'],   c_en)
            tmp.changeAttributeValue(fid, i['class_id_b'], c_id)
            tmp.changeAttributeValue(fid, i['lv1_en'],     l1_en)
            tmp.changeAttributeValue(fid, i['lv1_id'],     l1_id)
            tmp.changeAttributeValue(fid, i['hex_color'],  hx)
        tmp.commitChanges()
        feedback.setProgress(75)

        if unknown:
            feedback.pushWarning(f'Gridcode tidak ada di ATBD: {sorted(unknown)}')

        feedback.setProgressText('Langkah 4/4 — Menyimpan output ...')
        saved = processing.run('native:savefeatures', {
            'INPUT': tmp, 'OUTPUT': out_path,
        }, context=context, feedback=feedback, is_child_algorithm=True)
        final = saved['OUTPUT']
        feedback.setProgress(92)

        if load:
            lyr = QgsVectorLayer(final, 'MapBiomas Indonesia LULC Map', 'ogr')
            if lyr.isValid():
                _apply_symbology(lyr)
                QgsProject.instance().addMapLayer(lyr)
                feedback.pushInfo('Layer dimuat ke kanvas dengan simbologi ATBD')
                feedback.pushInfo(
                    'Legenda hanya menampilkan kelas yang ada di data.'
                )
            else:
                feedback.reportError('Layer output tidak bisa dimuat ke kanvas.')

        feedback.setProgress(100)
        return {self.OUTPUT_VECTOR: final}
