import javatools
import zipfile
import os


class JyStub:
    def __init__(self, jar_path: str):
        self.jar_path = jar_path
        self.jar = zipfile.ZipFile(self.jar_path, "r")
        self.source_path = self.get_source_path()

    def get_source_path(self) -> str:
        manifest_text = self.jar.read("META-INF/MANIFEST.MF").decode(
            "utf-8", errors="replace"
        )
        key = "Implementation-Vendor-Id: "
        error_msg = "Manifest is missing Implementation-Vendor-Id"
        if key not in manifest_text:
            raise RuntimeError(error_msg)

        source = manifest_text.split(key, 1)[1].splitlines()[0].strip()
        if not source:
            raise RuntimeError(error_msg)

        return source.replace(".", "/")

    def get_all_classes(self):
        return [
            file.filename
            for file in self.jar.filelist
            if file.filename.startswith(self.source_path)
            and file.filename.endswith(".class")
        ]

    def generate_stub(self):
        classes = self.get_all_classes()
        for class_file in classes:
            unpacked_class = None
            class_path = "/".join(class_file.split("/")[0:-1])
            with self.jar.open(class_file) as f:
                class_data = f.read()
                unpacked_class = javatools.unpack_class(class_data)

            os.makedirs(class_path, exist_ok=True)
            file_name = unpacked_class.get_sourcefile().replace(".java", ".pyi")

            # Just learned something new today, set intersection:
            # if set("<>") & set(m.get_name()): continue

            with open(f"{class_path}/{file_name}", "w") as f:
                for m in unpacked_class.methods:
                    if m.is_public() and not set("<>") & set(m.get_name()):
                        f.write(f"def {m.get_name()}(*args, **kwargs): ...\n")

    def __str__(self):
        return f"{self.jar_path} ({self.source_path})"


jyStub = JyStub("../libs/HytaleServer.jar")
jyStub.generate_stub()
