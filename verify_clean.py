import xml.etree.ElementTree as ET

# 정리된 파일 검증
tree = ET.parse('cheongna_buildings_5km_clean.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}

placemarks = root.findall('.//kml:Placemark', ns)
print(f"총 건물 수: {len(placemarks)}")

# 샘플 검증
print("\n=== 샘플 검증 (처음 5개) ===\n")

for i, placemark in enumerate(placemarks[:5]):
    name_elem = placemark.find('.//kml:name', ns)
    name = name_elem.text if name_elem is not None else "Unknown"
    
    # extrude 확인
    polygon = placemark.find('.//kml:Polygon', ns)
    if polygon:
        extrude = polygon.find('.//kml:extrude', ns)
        extrude_val = extrude.text if extrude is not None else "없음"
        
        coords_elem = polygon.find('.//kml:coordinates', ns)
        if coords_elem:
            coords_text = coords_elem.text.strip()
            coord_count = len(coords_text.split())
            
            # 첫 좌표 확인
            first_coord = coords_text.split()[0] if coords_text else "없음"
            
            print(f"{i+1}. {name}")
            print(f"   extrude: {extrude_val}")
            print(f"   좌표 개수: {coord_count}")
            print(f"   첫 좌표: {first_coord}")
            print(f"   줄바꿈 포함: {'예' if chr(10) in coords_text else '아니오'}")
            print()

# 전체 통계
print("=== 전체 통계 ===")
with_extrude = 0
without_extrude = 0

for placemark in placemarks:
    polygon = placemark.find('.//kml:Polygon', ns)
    if polygon:
        extrude = polygon.find('.//kml:extrude', ns)
        if extrude is not None and extrude.text == '1':
            with_extrude += 1
        else:
            without_extrude += 1

print(f"extrude=1 건물: {with_extrude}개 (3D 입체)")
print(f"extrude 없음: {without_extrude}개")
print(f"\n✅ 3D 효과가 유지됩니다!" if with_extrude > 0 else "❌ 3D 효과가 제거되었습니다")
