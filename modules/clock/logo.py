def make_logo(icons):
    try:
        with open("icon.txt") as f:
            for icon in f.readlines():
                icons.export_icon(icon.strip("\n"), 50)
        return "Done"
    except Exception as e:
        return str(e)

def test():
    print("=======================")
    print("***********************")
    print("=======================")