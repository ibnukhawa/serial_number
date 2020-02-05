{
  'name': 'Serial Number',
  'author': 'Bayu Dwi Saputra & Ibnu Nur Khawarizmi',
  'version': '0.1',
  'depends': [
    'sale','product'
  ],
  'data': [
    
    'views/serial_number.xml',
    # 'views/sale_order.xml'
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