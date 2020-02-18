{
  'name': 'Serial Number',
  'author': 'Bayu Dwi Saputra & Ibnu Nur Khawarizmi',
  'version': '0.1',
  'depends': [
    'sale','product'
  ],
  'data': [
    
    'views/serial_number.xml',
    'views/serial_number_86.xml',
    'views/serial_number1.xml',
    'views/serial_number2.xml',
    'views/serial_number3.xml',
    'views/serial_number4.xml',
    'views/menuitem.xml',
    'report/report_serial_number.xml',
    'views/sale_order_line.xml',
  ],
  'qweb': [
    # 'static/src/xml/nama_widget.xml',
  ],
  'sequence': 4,
  'auto_install': False,
  'installable': True,
  'application': True,
  'category': 'Serial Number',
  'summary': 'Add Product With Serial Number at Sale Order',
  'license': 'OPL-1',
  'images': ['static/description/icon.png'],
  'description': '-'
}