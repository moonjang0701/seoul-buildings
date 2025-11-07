import xml.etree.ElementTree as ET

# 2.5km 파일 로드
tree = ET.parse('cheongna_buildings_2.5km_perfect.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')

# LookAt 범위 조정
lookat = root.find('.//kml:LookAt', ns)
if lookat is not None:
    range_elem = lookat.find('kml:range', ns)
    if range_elem is not None:
        old_range = range_elem.text
        range_elem.text = '2500'  # 2.5km
        print(f"LookAt 범위 조정: {old_range} → 2500m")

# 저장
tree.write('cheongna_buildings_2.5km_perfect.kml', encoding='utf-8', xml_declaration=True)
print("✅ 업데이트 완료")
