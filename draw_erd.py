import os
from PIL import Image, ImageDraw, ImageFont

def draw_erd():
    # 1. Initialize Canvas
    # High-resolution canvas for crystal clear text rendering
    width, height = 1800, 1200
    image = Image.new("RGB", (width, height), "#060314")  # Modern obsidian dark background matching the theme
    draw = ImageDraw.Draw(image)
    
    # 2. Set Up Professional Anti-Aliased Typography
    try:
        font_title = ImageFont.truetype("segoeuib.ttf", 32)
        font_subtitle = ImageFont.truetype("segoeui.ttf", 16)
        font_header = ImageFont.truetype("segoeuib.ttf", 18)
        font_bold = ImageFont.truetype("segoeuib.ttf", 13)
        font_regular = ImageFont.truetype("segoeui.ttf", 13)
        font_type = ImageFont.truetype("segoeui.ttf", 11)
    except IOError:
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 32)
            font_subtitle = ImageFont.truetype("arial.ttf", 16)
            font_header = ImageFont.truetype("arialbd.ttf", 18)
            font_bold = ImageFont.truetype("arialbd.ttf", 13)
            font_regular = ImageFont.truetype("arial.ttf", 13)
            font_type = ImageFont.truetype("arial.ttf", 11)
        except IOError:
            # Fallback to default bitmap fonts if system fonts fail
            font_title = font_subtitle = font_header = font_bold = font_regular = font_type = ImageFont.load_default()
            
    # Draw Title Block Header
    draw.text((50, 40), "Secure Digital Voting Platform - Database ERD", fill="#f8fafc", font=font_title)
    draw.text((50, 85), "Active Database Schema Map & Referencing Integrity Constraints (Normalized to 3NF)", fill="#94a3b8", font=font_subtitle)
    
    # Draw clean divider line
    draw.line([(50, 115), (width - 50, 115)], fill="#2b2654", width=2)
    
    # 3. Define Table Data Structure
    tables = {
        "address": {
            "name": "address",
            "x": 100, "y": 180, "w": 300, "h": 220,
            "cols": [
                ("DistrictId", "INT", "PK"),
                ("Locality", "VARCHAR(30)", ""),
                ("City", "VARCHAR(30)", ""),
                ("State", "VARCHAR(30)", ""),
                ("Zip", "VARCHAR(10)", "")
            ]
        },
        "voter_table": {
            "name": "voter_table",
            "x": 100, "y": 480, "w": 320, "h": 360,
            "cols": [
                ("Aadhaar", "CHAR(15)", "PK"),
                ("FirstName", "VARCHAR(30)", ""),
                ("MiddleName", "VARCHAR(30)", ""),
                ("LastName", "VARCHAR(50)", ""),
                ("Sex", "CHAR(7)", ""),
                ("Birthday", "DATE", ""),
                ("Age", "INT", ""),
                ("Phone", "NUMERIC", ""),
                ("Email", "VARCHAR(50)", ""),
                ("DistrictId", "INT", "FK")
            ]
        },
        "user_table": {
            "name": "user_table",
            "x": 100, "y": 920, "w": 300, "h": 200,
            "cols": [
                ("VoterId", "VARCHAR(10)", "PK"),
                ("Aadhaar", "CHAR(15)", "FK"),
                ("_Password", "VARCHAR(255)", ""),
                ("IsActive", "BOOLEAN", "")
            ]
        },
        "party_table": {
            "name": "party_table",
            "x": 1380, "y": 180, "w": 320, "h": 240,
            "cols": [
                ("PartyId", "INT", "PK"),
                ("PartyName", "VARCHAR(50)", ""),
                ("Symbol", "VARCHAR(20)", ""),
                ("PartyLeader", "VARCHAR(50)", ""),
                ("LeaderAadhaar", "CHAR(15)", "FK")
            ]
        },
        "candidate_table": {
            "name": "candidate_table",
            "x": 720, "y": 480, "w": 320, "h": 240,
            "cols": [
                ("CandidateId", "INT", "PK"),
                ("Aadhaar", "CHAR(15)", "FK"),
                ("CandidateName", "VARCHAR(100)", ""),
                ("PartyId", "INT", "FK"),
                ("DistrictId", "INT", "FK")
            ]
        },
        "vote_table": {
            "name": "vote_table",
            "x": 720, "y": 840, "w": 320, "h": 240,
            "cols": [
                ("VoteId", "INT", "PK"),
                ("Aadhaar", "CHAR(15)", "FK"),
                ("PartyId", "INT", "FK"),
                ("CandidateId", "INT", "FK"),
                ("DistrictId", "INT", "FK")
            ]
        },
        "result": {
            "name": "result",
            "x": 1380, "y": 840, "w": 320, "h": 240,
            "cols": [
                ("ResultId", "INT", "PK"),
                ("CandidateId", "INT", "FK"),
                ("PartyId", "INT", "FK"),
                ("DistrictId", "INT", "FK"),
                ("Vote_Count", "INT", "")
            ]
        }
    }
    
    # Helper to draw rounded card boxes
    def draw_table_card(t):
        x, y, w, h = t["x"], t["y"], t["w"], t["h"]
        # Background glass card
        draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill="#0d082c", outline="#2b2654", width=2)
        # Header background
        draw.rounded_rectangle([x, y, x + w, y + 45], radius=12, fill="#1e1b4b")
        # Header title
        draw.text((x + 18, y + 12), t["name"].upper(), fill="#f8fafc", font=font_header)
        # Divider line
        draw.line([(x, y + 45), (x + w, y + 45)], fill="#2b2654", width=2)
        
        # Render columns
        start_y = y + 60
        for name, col_type, key in t["cols"]:
            key_fill = "#f8fafc"
            key_label = ""
            if key == "PK":
                key_fill = "#2dd4bf"
                key_label = "[PK]"
            elif key == "FK":
                key_fill = "#a855f7"
                key_label = "[FK]"
                
            # Column attribute text
            draw.text((x + 18, start_y), name, fill=key_fill if key else "#e2e8f0", font=font_bold if key else font_regular)
            
            # Key indicator annotation
            if key_label:
                try:
                    name_width = draw.textlength(name, font=font_bold)
                except AttributeError:
                    name_width = len(name) * 8
                draw.text((x + 18 + name_width + 8, start_y + 1), key_label, fill=key_fill, font=font_type)
                
            # Data Types right aligned
            try:
                type_width = draw.textlength(col_type, font=font_type)
            except AttributeError:
                type_width = len(col_type) * 7
            draw.text((x + w - 18 - type_width, start_y + 1), col_type, fill="#64748b", font=font_type)
            
            start_y += 26
            
    # Draw all schema cards
    for t_name, t_data in tables.items():
        draw_table_card(t_data)
        
    # 4. Draw Relational Connector Tracks
    def draw_connector(start, end, label=""):
        draw.line(start + end, fill="#818cf8", width=2)
        # Draw connector nodes
        draw.ellipse([start[0]-4, start[1]-4, start[0]+4, start[1]+4], fill="#2dd4bf")
        draw.ellipse([end[0]-4, end[1]-4, end[0]+4, end[1]+4], fill="#a855f7")
        if label:
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            draw.text((mid_x + 10, mid_y - 10), label, fill="#64748b", font=font_type)

    # 1. address -> voter_table (DistrictId)
    draw_connector((250, 400), (250, 480), "1:N")
    
    # 2. voter_table -> user_table (Aadhaar)
    draw_connector((250, 840), (250, 920), "1:1")
    
    # 3. voter_table -> party_table (LeaderAadhaar)
    draw_connector((420, 520), (1380, 360), "1:1")
    
    # 4. party_table -> candidate_table (PartyId)
    draw_connector((1540, 420), (880, 480), "1:N")
    
    # 5. candidate_table -> vote_table (CandidateId)
    draw_connector((880, 720), (880, 840), "1:N")
    
    # 6. user_table -> vote_table (Aadhaar)
    draw_connector((400, 1020), (720, 960), "1:1")
    
    # 7. vote_table -> result (CandidateId)
    draw_connector((1040, 960), (1380, 960), "1:N")
    
    # Save generated canvas directly as ERD.jpg
    image.save("ERD.jpg", "JPEG", quality=95)
    print("ERD.jpg drawn programmatically using PIL successfully!")

if __name__ == "__main__":
    draw_erd()
