import pptx

prs = pptx.Presentation('template_reference.pptx')
print(f"Presentation width: {prs.slide_width.inches} in, height: {prs.slide_height.inches} in")

for i, slide in enumerate(prs.slides):
    print(f"\n--- Slide {i+1} ---")
    for shape in slide.shapes:
        s_info = f"Shape: {shape.name} | Type: {shape.shape_type} | pos: ({shape.left.inches:.2f}, {shape.top.inches:.2f}, {shape.width.inches:.2f}, {shape.height.inches:.2f})"
        print(s_info)
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                p_text = p.text.strip()
                if p_text:
                    font_info = ""
                    if p.runs:
                        r = p.runs[0]
                        fname = r.font.name
                        fsize = r.font.size.pt if r.font.size else "auto"
                        fcolor = r.font.color.rgb if (r.font.color and hasattr(r.font.color, 'rgb')) else "none"
                        font_info = f"[Font: {fname}, {fsize}pt, {fcolor}]"
                    print(f"   P: {p_text[:80]} {font_info}")
