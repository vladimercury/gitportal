from string import Template
import yaml
import os


def read_settings():
    with open("settings.yaml", "r") as file:
        return yaml.load(file)


def do_template(template_string, **kwargs):
    template_object = Template(template_string)
    return template_object.safe_substitute(**kwargs)


def do_compile(source_dir, source_file_name, target_dir, data):
    print("Compiling %s..." % source_file_name, end="")
    try:
        with open(source_dir + source_file_name, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("FAIL: file not found")
        return
    if data is not None:
        text = do_template(text, **data)
    with open(target_dir + source_file_name, "w", encoding="utf-8") as file:
        print(text, file=file)
        print("OK")


settings = read_settings()
if not os.path.exists(settings["source"]["dir"]):
    print("Source path not exists. Aborting")
    exit(1)
if not os.path.exists(settings["target"]["dir"]):
    print("Target path not exists. Creating one")
    os.makedirs(settings["target"]["dir"])


for file_name in settings["source"]["files"]:
    do_compile(settings["source"]["dir"], file_name, settings["target"]["dir"], settings["defines"])

