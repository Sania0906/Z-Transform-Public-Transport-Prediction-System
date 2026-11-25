import pptx

prs = pptx.Presentation('template_reference.pptx')
print("--- SLIDE 4 TABLE ---")
s4 = prs.slides[3]
for shape in s4.shapes:
    if shape.has_table:
        table = shape.table
        for r_idx, row in enumerate(table.rows):
            vals = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
            print(f"Row {r_idx}: {vals}")

print("\n--- SLIDE 17 REFERENCES ---")
s17 = prs.slides[16]
for shape in s17.shapes:
    if shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            if p.text.strip():
                print(f"Ref: {p.text.strip()}")
