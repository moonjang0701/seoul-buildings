import xml.etree.ElementTree as ET
import re

# 원본 파일 로드
tree = ET.parse('cheongna_buildings_5km.kml')
root = tree.getroot()

ns = {'kml': 'http://www.opengis.net/kml/2.2'}
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')

print("=== 샘플 양식대로 변환 중... ===\n")

# 1. 모든 색상을 완전 불투명(ff)으로 변경
modified_colors = 0
for poly_style in root.findall('.//kml:PolyStyle', ns):
    color_elem = poly_style.find('kml:color', ns)
    if color_elem is not None:
        old_color = color_elem.text
        # aabbggrr 형식에서 aa(alpha)를 ff로 변경
        if old_color and len(old_color) == 8:
            new_color = 'ff' + old_color[2:]  # ff = 완전 불투명
            color_elem.text = new_color
            modified_colors += 1
            print(f"색상 변경: {old_color} → {new_color}")
    
    # fill과 outline 둘 다 활성화 (샘플처럼)
    fill_elem = poly_style.find('kml:fill', ns)
    outline_elem = poly_style.find('kml:outline', ns)
    if fill_elem is not None:
        fill_elem.text = '1'
    if outline_elem is not None:
        outline_elem.text = '1'

print(f"\n수정된 색상: {modified_colors}개")

# 2. 좌표 정규화 및 줄바꿈 형식으로 변환
def format_coordinates(coords_text):
    """좌표를 샘플처럼 줄바꿈 형식으로 포맷"""
    # 모든 공백/줄바꿈으로 분리
    coord_points = re.split(r'\s+', coords_text.strip())
    coord_points = [c.strip() for c in coord_points if c.strip()]
    
    # 좌표 정밀도 조정 (소수점 7자리)
    formatted_coords = []
    for coord in coord_points:
        parts = coord.split(',')
        if len(parts) >= 3:
            lon = round(float(parts[0]), 7)
            lat = round(float(parts[1]), 7)
            alt = round(float(parts[2]), 1)
            formatted_coords.append(f"{lon},{lat},{alt}")
    
    # 샘플처럼 줄바꿈으로 구분 (들여쓰기 포함)
    return '\n              ' + '\n              '.join(formatted_coords) + '\n            '

formatted_count = 0
for coords_elem in root.findall('.//kml:coordinates', ns):
    if coords_elem.text:
        coords_elem.text = format_coordinates(coords_elem.text)
        formatted_count += 1

print(f"포맷된 좌표: {formatted_count}개")

# 저장
output_file = 'cheongna_buildings_5km_perfect.kml'
tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f"\n✅ 완료: {output_file}")
print("\n특징:")
print("  • 완전 불투명 색상 (ff) - 깜빡임 제거")
print("  • fill=1, outline=1 - 입체감 최고")
print("  • 줄바꿈 형식 좌표 - 가독성 좋음")
print("  • 좌표 정밀도 최적화 (소수점 7자리)")

import os
original_size = os.path.getsize('cheongna_buildings_5km.kml')
new_size = os.path.getsize(output_file)
print(f"\n파일 크기:")
print(f"  원본: {original_size/1024/1024:.2f} MB")
print(f"  변환: {new_size/1024/1024:.2f} MB")
print(f"  변화: {((new_size-original_size)/original_size*100):+.1f}%")
