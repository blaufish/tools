import os
import argparse
import glob
import zlib
import zipfile
import xml.etree.ElementTree as ET
from xml.dom import minidom

GPX_HEADER = """<?xml version="1.0" encoding="utf-8"?>
<gpx xmlns:xsi="[http://www.w3.org/2001/XMLSchema-instance](http://www.w3.org/2001/XMLSchema-instance)" xmlns:xsd="[http://www.w3.org/2001/XMLSchema](http://www.w3.org/2001/XMLSchema)" version="1.0" creator="Geocaching Convert Tool" xsi:schemaLocation="[http://www.topografix.com/GPX/1/0](http://www.topografix.com/GPX/1/0) [http://www.topografix.com/GPX/1/0/gpx.xsd](http://www.topografix.com/GPX/1/0/gpx.xsd) [http://www.groundspeak.com/cache/1/0/1](http://www.groundspeak.com/cache/1/0/1) [http://www.groundspeak.com/cache/1/0/1/cache.xsd](http://www.groundspeak.com/cache/1/0/1/cache.xsd)" xmlns="[http://www.topografix.com/GPX/1/0](http://www.topografix.com/GPX/1/0)">
"""
GPX_FOOTER = "</gpx>\n"

def convert_size(size_str):
    mapping = {
        'micro': 2.0,
        'small': 3.0,
        'regular': 4.0,
        'large': 5.0
    }
    val = mapping.get(size_str.lower(), -1.0)
    return f"{val:.6f}"

def format_rating(rating_str):
    try:
        return f"{float(rating_str):.6f}"
    except ValueError:
        return "3.000000"

def format_coord(coord_str):
    try:
        return f"{float(coord_str):.6f}"
    except ValueError:
        return "0.000000"

class GGZWriter:
    def __init__(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        self.ggz_path = os.path.join(output_dir, 'geocaches.ggz')
        self.zip_file = zipfile.ZipFile(self.ggz_path, 'w', compression=zipfile.ZIP_DEFLATED)
        
        self.seen_waypoints = set()
        self.part_number = 1
        
        self.current_gpx_data = bytearray()
        self.current_waypoints_count = 0
        self.current_byte_pos = 0
        
        self.index_caches = []
        
        self._init_new_gpx_part()

    def _init_new_gpx_part(self):
        self.current_gpx_data = bytearray()
        self.current_waypoints_count = 0
        self.current_byte_pos = 0
        
        header_bytes = GPX_HEADER.encode('utf-8')
        self.current_gpx_data.extend(header_bytes)
        self.current_byte_pos += len(header_bytes)

    def _commit_current_gpx(self):
        if self.current_waypoints_count == 0:
            return

        footer_bytes = GPX_FOOTER.encode('utf-8')
        self.current_gpx_data.extend(footer_bytes)
        
        file_crc = zlib.crc32(self.current_gpx_data) & 0xFFFFFFFF
        
        filename = f"data/part-{self.part_number}.gpx"
        self.zip_file.writestr(filename, bytes(self.current_gpx_data))
        
        print(f"  [+] Wrote {filename} to archive ({self.current_waypoints_count} waypoints, {len(self.current_gpx_data)} bytes)")
        
        for cache in self.index_caches:
            if cache['file'] == filename:
                cache['crc'] = file_crc

        self.part_number += 1
        self._init_new_gpx_part()

    def process_gpx_file(self, file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            for wpt in root:
                tag_name = wpt.tag.split('}')[-1] 
                if tag_name != 'wpt':
                    continue
                
                c_code = ""
                c_name = ""
                c_type = ""
                c_size = "3.000000"
                c_diff = "3.000000"
                c_terr = "3.000000"

                for child in wpt:
                    child_tag = child.tag.split('}')[-1]
                    if child_tag == 'name':
                        if child.text:
                            c_code = child.text.strip()
                        if not c_name:
                            c_name = c_code
                    elif child_tag == 'urlname':
                        if child.text:
                            c_name = child.text.strip()
                    
                    if child_tag == 'cache':
                        for gchild in child:
                            gtag = gchild.tag.split('}')[-1]
                            if gtag == 'name' and gchild.text:
                                c_name = gchild.text.strip()
                            elif gtag == 'type' and gchild.text:
                                c_type = gchild.text.strip()
                            elif gtag == 'container' and gchild.text:
                                c_size = convert_size(gchild.text.strip())
                            elif gtag == 'difficulty' and gchild.text:
                                c_diff = format_rating(gchild.text.strip())
                            elif gtag == 'terrain' and gchild.text:
                                c_terr = format_rating(gchild.text.strip())
                        
                if not c_code:
                    continue
                
                if c_code in self.seen_waypoints:
                    continue
                self.seen_waypoints.add(c_code)
                
                wpt_str = ET.tostring(wpt, encoding='utf-8').decode('utf-8')
                wpt_bytes = wpt_str.encode('utf-8')
                wpt_len = len(wpt_bytes)
                
                file_pos = self.current_byte_pos
                
                self.index_caches.append({
                    'code': c_code,
                    'name': c_name,
                    'lat': format_coord(wpt.get('lat', '0.0')),
                    'lon': format_coord(wpt.get('lon', '0.0')),
                    'file': f"data/part-{self.part_number}.gpx",
                    'file_pos': file_pos,
                    'file_len': wpt_len,
                    'crc': 0,
                    'type': c_type,
                    'diff': c_diff,
                    'terr': c_terr,
                    'size': c_size
                })
                
                self.current_gpx_data.extend(wpt_bytes)
                self.current_byte_pos += wpt_len
                self.current_waypoints_count += 1
                
                if self.current_byte_pos > 2 * 1024 * 1024 or self.current_waypoints_count >= 1000:
                    self._commit_current_gpx()
                    
        except ET.ParseError as e:
            print(f"Error parsing {file_path}: {e}")

    def _write_index(self):
        idx = ET.Element('ggz', xmlns="[http://www.opencaching.com/xmlschemas/ggz/1/0](http://www.opencaching.com/xmlschemas/ggz/1/0)")
        time_elem = ET.SubElement(idx, 'time')
        time_elem.text = "2026-10-09T22:05:00Z" 
        
        files_dict = {}
        for cache in self.index_caches:
            f = cache['file']
            if f not in files_dict:
                files_dict[f] = {'crc': cache['crc'], 'caches': []}
            files_dict[f]['caches'].append(cache)
            
        for f, data in files_dict.items():
            file_elem = ET.SubElement(idx, 'file')
            name_elem = ET.SubElement(file_elem, 'name')
            name_elem.text = f.split('/')[-1]
            crc_elem = ET.SubElement(file_elem, 'crc')
            crc_elem.text = format(data['crc'], '08X') 
            
            for cache in data['caches']:
                gch_elem = ET.SubElement(file_elem, 'gch')
                ET.SubElement(gch_elem, 'code').text = cache['code']
                ET.SubElement(gch_elem, 'name').text = cache['name']
                ET.SubElement(gch_elem, 'type').text = cache['type']
                ET.SubElement(gch_elem, 'lat').text = cache['lat']
                ET.SubElement(gch_elem, 'lon').text = cache['lon']
                ET.SubElement(gch_elem, 'file_pos').text = str(cache['file_pos'])
                ET.SubElement(gch_elem, 'file_len').text = str(cache['file_len'])
                
                ratings_elem = ET.SubElement(gch_elem, 'ratings')
                ET.SubElement(ratings_elem, 'awesomeness').text = "3.000000"
                ET.SubElement(ratings_elem, 'difficulty').text = cache['diff']
                ET.SubElement(ratings_elem, 'size').text = cache['size']
                ET.SubElement(ratings_elem, 'terrain').text = cache['terr']
        
        xmlstr = minidom.parseString(ET.tostring(idx)).toprettyxml(indent="  ")
        self.zip_file.writestr("index/com/garmin/geocaches/v0/index.xml", xmlstr.encode('utf-8'))

    def close(self):
        if self.current_waypoints_count > 0:
            self._commit_current_gpx()
        
        if self.index_caches:
            self._write_index()
            print(f"  [+] Wrote index.xml with {len(self.index_caches)} total caches mapped.")
        else:
            print("  [!] WARNING: No waypoints were processed. The index will be empty.")
            
        self.zip_file.close()

def main():
    parser = argparse.ArgumentParser(description="Convert GPX files to GGZ format")
    parser.add_argument('--gpx', required=True, help="Directory containing input GPX files")
    parser.add_argument('--ggz', required=True, help="Directory to output the geocaches.ggz file")
    args = parser.parse_args()

    gpx_dir = args.gpx
    ggz_dir = args.ggz

    writer = GGZWriter(ggz_dir)
    
    gpx_files = sorted(glob.glob(os.path.join(gpx_dir, '*.gpx')))
    for gpx_file in gpx_files:
        print(f"Processing {gpx_file}...")
        writer.process_gpx_file(gpx_file)
        
    writer.close()
    print(f"Successfully wrote {os.path.join(ggz_dir, 'geocaches.ggz')}")

if __name__ == "__main__":
    main()
