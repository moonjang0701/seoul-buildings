import xml.etree.ElementTree as ET
import re

# KML 파일 파싱
tree = ET.parse('cheongna_buildings_5km.kml')
root = tree.getroot()

# 네임스페이스
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

placemarks = root.findall('.//kml:Placemark', ns)
print(f"총 Placemark 개수: {len(placemarks)}\n")

# 좌표 포맷 문제 찾기
format_issues = []

for idx, placemark in enumerate(placemarks[:100]):  # 처음 100개 샘플링
    name_elem = placemark.find('.//kml:name', ns)
    name = name_elem.text if name_elem is not None else f"Building_{idx}"
    
    coords_elem = placemark.find('.//kml:coordinates', ns)
    if coords_elem is not None:
        coords_text = coords_elem.text
        
        # 원본 좌표 텍스트 확인
        has_issue = False
        issues = []
        
        # 줄바꿈 체크
        if '\n' in coords_text:
            lines = coords_text.strip().split('\n')
            if len(lines) > 1:
                has_issue = True
                issues.append(f"줄바꿈 {len(lines)}개 라인")
        
        # 좌표 분리 확인
        coords_text_clean = coords_text.strip()
        
        # 공백으로 분리된 좌표
        space_separated = coords_text_clean.split()
        # 줄바꿈으로 분리된 좌표
        newline_separated = [c.strip() for c in coords_text_clean.split('\n') if c.strip()]
        
        if len(space_separated) != len(newline_separated):
            has_issue = True
            issues.append(f"공백구분={len(space_separated)}, 줄구분={len(newline_separated)}")
        
        # 각 좌표 검증
        for i, coord in enumerate(space_separated[:3]):  # 처음 3개만
            parts = coord.split(',')
            if len(parts) < 2:
                has_issue = True
                issues.append(f"좌표{i} 파싱 실패: {coord}")
        
        if has_issue:
            format_issues.append({
                'name': name,
                'index': idx,
                'issues': issues,
                'sample': coords_text[:200]  # 처음 200자
            })

print(f"포맷 문제 발견: {len(format_issues)}개\n")

for i, issue in enumerate(format_issues[:10]):
    print(f"{i+1}. {issue['name']}")
    print(f"   문제: {', '.join(issue['issues'])}")
    print(f"   샘플: {repr(issue['sample'][:100])}")
    print()

# 전체 파일에서 좌표 구분 패턴 분석
print("\n=== 좌표 구분 패턴 분석 (전체) ===")
space_only = 0
newline_only = 0
mixed = 0

for placemark in placemarks:
    coords_elem = placemark.find('.//kml:coordinates', ns)
    if coords_elem is not None:
        text = coords_elem.text.strip()
        has_space = ' ' in text
        has_newline = '\n' in text
        
        if has_space and not has_newline:
            space_only += 1
        elif has_newline and not has_space:
            newline_only += 1
        elif has_space and has_newline:
            mixed += 1

print(f"공백만 사용: {space_only}개")
print(f"줄바꿈만 사용: {newline_only}개")
print(f"혼합 사용: {mixed}개")
