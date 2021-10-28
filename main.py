import PySimpleGUI as Sg
import os.path
import pathlib


def delete_files_recursively(path_abs, extension):
    count = 0
    path_abs = pathlib.Path(path_abs)
    extension = "*" + extension
    files = path_abs.rglob(extension)
    for f in files:
        f.unlink()
        count += 1
    return count


def remove_empty_folders(path_abs):
    count = 0
    permission_error = 0
    path_abs = pathlib.Path(path_abs)
    walk = list(os.walk(path_abs))
    for path, _, _ in walk[::-1]:
        try:
            if len(os.listdir(path)) == 0:
                os.rmdir(path)
                count += 1
        except PermissionError as tb:
            permission_error += 1
            print(tb)
    return count, permission_error


if __name__ == '__main__':
    main_column = [
        [
            Sg.Text("Escolher pasta:"),
            Sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            Sg.FolderBrowse(),
        ],
        [
            Sg.Text("Digite uma extensão para excluir arquivos:"),
            Sg.In(".ext", size=(5, 1), enable_events=True, key="-EXTENSAO-"),
            Sg.Button("Excluir agora!", key="-EXECUTAR-"),
        ],
        [
            Sg.Text("Status: Inicializado.", key="-STATUS-"),
        ],
        [
            Sg.Text("Excluir pastas vazias?"),
            Sg.Button("Excluir agora!", key="-PASTAS-"),
        ],
    ]

    layout = [
        [
            Sg.Column(main_column),
        ]
    ]

    window = Sg.Window("Removedor de Arquivos", layout)

    while True:
        event, values = window.read()
        folder = values["-FOLDER-"]
        if event == "Exit" or event == Sg.WIN_CLOSED:
            break
        elif event == "-FOLDER-":
            try:
                file_list = os.listdir(folder)
            except RuntimeError:
                file_list = []
            except TypeError:
                file_list = []
        elif event == "-EXECUTAR-":
            extensao = values["-EXTENSAO-"]
            res = delete_files_recursively(folder, extensao) if folder else 0
            window["-STATUS-"].update(f"Status: excluídos {res} arquivos.")
        elif event == "-PASTAS-":
            res = remove_empty_folders(folder)
            window["-STATUS-"].update(f"Status: removidas {res[0]} pastas, {res[1]} erros de permissão.")

    window.close()
