from  argparse import ArgumentParser
from xml.etree import ElementTree


parser = ArgumentParser()
parser.add_argument('-cld', '--common_cloud', dest='common_cloud')
parser.add_argument('-srv', '--realisation_service', dest='realis_serv_dir')
parser.add_argument('-app', '--common_application', dest='common_application')
result = parser.parse_args()

tree = ElementTree.parse(result.realis_serv_dir)
root = tree.getroot()
realis_service_id = root.attrib['id']

tree = ElementTree.parse(result.common_cloud)
root = tree.getroot()
items = root.find('.//cloud_template/item')
elem = ElementTree.Element('service', attrib={'id': realis_service_id})
items.append(elem)
file = open(result.common_cloud, 'wb')
tree._setroot(root)
tree.write(file, encoding='WINDOWS-1251', xml_declaration=True)
file.close()

tree = ElementTree.parse(result.common_application)
root = tree.getroot()
items = root.find('./items')
elem = ElementTree.Element('service', attrib={'id':realis_service_id, 'name':'Realisation', 'url':'../../realisation/service/Модули/Realisation.s3srv'})
items.append(elem)
file = open(result.common_application, 'wb')
tree._setroot(root)
tree.write(file, encoding='WINDOWS-1251', xml_declaration=True)
file.close()