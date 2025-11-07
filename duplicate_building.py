import xml.etree.ElementTree as ET
import re

# 2.5km 파일 로드
tree = ET.parse('cheongna_buildings_2.5km_perfect.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')

# 청라더샵레이크파크 찾기
placemarks = root.findall('.//kml:Placemark', ns)
lake_park = None

for placemark in placemarks:
    name_elem = placemark.find('.//kml:name', ns)
    if name_elem is not None and '청라더샵레이크파크' in name_elem.text:
        lake_park = placemark
        print(f"✅ 찾음: {name_elem.text}")
        
        # 좌표 확인
        coords_elem = placemark.find('.//kml:coordinates', ns)
        if coords_elem is not None:
            coords_text = coords_elem.text.strip()
            coord_points = re.split(r'\s+', coords_text)
            coord_points = [c.strip() for c in coord_points if c.strip()]
            print(f"   좌표 개수: {len(coord_points)}개")
            
            # 중심점 계산
            lons = []
            lats = []
            for coord in coord_points:
                parts = coord.split(',')
                if len(parts) >= 2:
                    lons.append(float(parts[0]))
                    lats.append(float(parts[1]))
            
            if lons and lats:
                center_lon = sum(lons) / len(lons)
                center_lat = sum(lats) / len(lats)
                print(f"   원본 중심: ({center_lon:.6f}, {center_lat:.6f})")
        
        # 높이 확인
        height_match = re.search(r'\((\d+(?:\.\d+)?)m?\)', name_elem.text)
        if height_match:
            print(f"   높이: {height_match.group(1)}m")
        
        break

if lake_park is None:
    print("❌ 청라더샵레이크파크를 찾을 수 없습니다.")
    print("\n사용 가능한 건물 이름 (샘플):")
    for i, placemark in enumerate(placemarks[:20]):
        name_elem = placemark.find('.//kml:name', ns)
        if name_elem is not None:
            print(f"  {i+1}. {name_elem.text}")
else:
    print("\n✅ 건물을 찾았습니다. 이제 복사를 진행합니다.")
