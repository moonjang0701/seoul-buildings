import xml.etree.ElementTree as ET
import os

def create_variant(input_file, output_file, fill, outline, alpha_hex, description):
    """KML 변형 생성"""
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    ET.register_namespace('', 'http://www.opengis.net/kml/2.2')
    
    # PolyStyle 수정
    for poly_style in root.findall('.//kml:PolyStyle', ns):
        fill_elem = poly_style.find('kml:fill', ns)
        outline_elem = poly_style.find('kml:outline', ns)
        
        if fill_elem is not None:
            fill_elem.text = str(fill)
        if outline_elem is not None:
            outline_elem.text = str(outline)
        
        # 투명도 조정
        if alpha_hex:
            color_elem = poly_style.find('kml:color', ns)
            if color_elem is not None:
                color = color_elem.text
                color_elem.text = alpha_hex + color[2:]
    
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    size = os.path.getsize(output_file) / 1024 / 1024
    
    return {
        'file': output_file,
        'size': f'{size:.2f} MB',
        'description': description
    }

print("=== 다양한 3D 건물 옵션 생성 ===\n")

variants = []

# 옵션 1: 벽면만, 진한 색상 (권장)
variants.append(create_variant(
    'cheongna_buildings_5km_clean.kml',
    'cheongna_buildings_5km_walls_opaque.kml',
    fill=1, outline=0, alpha_hex='ff',
    "벽면 100% 불투명, 선 없음 - 최고 입체감"
))

# 옵션 2: 벽면만, 적당한 투명도
variants.append(create_variant(
    'cheongna_buildings_5km_clean.kml',
    'cheongna_buildings_5km_walls_semi.kml',
    fill=1, outline=0, alpha_hex='cc',
    "벽면 80% 불투명, 선 없음 - 적당한 입체감"
))

# 옵션 3: 벽면 + 얇은 선
variants.append(create_variant(
    'cheongna_buildings_5km_clean.kml',
    'cheongna_buildings_5km_walls_outline.kml',
    fill=1, outline=1, alpha_hex='cc',
    "벽면 80% + 테두리선 - 강한 입체감 (깜빡임 있을 수 있음)"
))

# 결과 출력
print("생성된 파일:\n")
for i, v in enumerate(variants, 1):
    print(f"{i}. {v['file']}")
    print(f"   크기: {v['size']}")
    print(f"   설명: {v['description']}")
    print()

print("\n=== 추천 ===")
print("⭐⭐⭐ cheongna_buildings_5km_walls_opaque.kml")
print("     → 입체감 최고, 진한 색상, 깜빡임 적음")
print()
print("⭐⭐ cheongna_buildings_5km_walls_semi.kml")
print("     → 입체감 좋음, 적당한 색상")
print()
print("⭐ cheongna_buildings_5km_walls_outline.kml")
print("     → 입체감 강함, 테두리 있음 (깜빡임 가능)")
