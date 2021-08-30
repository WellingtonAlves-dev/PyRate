import base64
import os.path

import PySimpleGUI as sg
from videoDownload.videoDownload import Download, DownloadPlaylist
import os
import base64
sg.theme("Black")
class Gui:
    def __init__(self):
        self.link = ""
        self.streames = []
        self.output = ""
        self.icon = ""
        self.logo = ""
        self.generateIcon()
        self.main()
    def generateIcon(self):
        icon = os.path.join(os.getcwd(), "gui", "ico.ico")
        logo = os.path.join(os.getcwd(), "gui", "logo.png")
        self.icon = icon
        self.logo = logo
    def main(self):
        layout = [
            [
                sg.Image(self.logo, size=(150, 150))
            ],

            [sg.Text("Link: ", size=(6, 1)),
             sg.InputText(size=(38, 1), key="-LINK-", enable_events=True)
             ],
            [
                sg.Text("Diretorio: ", size=(6, 1)),
                sg.In(size=(28, 1), key="-DIRETORIO-", enable_events=True),
                sg.FolderBrowse()
            ],
            [
                sg.Radio("Video", "-tipo video-",key="-tipo_video-", default=True, enable_events=True),
                sg.Radio("Playlist", "-tipo video-", key="-tipo_playlist-",enable_events=True),
            ],
            [
                sg.Text(size=(28, 1), key="-TITULO-")
            ],
            [
                sg.Text("Tipo: ", size=(8, 1))
            ],
            [
                sg.Listbox(values=self.streames,size=(48, 16), key="-TIPOS-", enable_events=True)
            ],
            [
                sg.Button("Download", key="-BAIXAR-", size=(8,1)),
                sg.Text("Por preguiça a playlist só baixa em mp4 :D")
            ]
        ]
        window = sg.Window("Pyrate", layout=layout, icon=self.icon)
        self.window = window
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "-LINK-" or event == "-tipo_video-" or event == "-tipo_playlist-":
                link = values["-LINK-"]
                if(len(link) > 5):
                    print(values)
                    if(values["-tipo_video-"] == True):
                        print("Video")
                        self.link = link
                        down = Download(link)
                        result = down.showStreamers()
                        if (result != None):
                            self.streames = result['streams']
                            window["-TIPOS-"].update(self.streames)
                            window["-TITULO-"].update(value=result['titulo'])
                        else:
                            sg.PopupError("Insira um link valido")
                            window["-LINK-"].update(value="")
                            self.streames = []
                            window["-TIPOS-"].update(self.streames)
                            window["-TITULO-"].update(value="")

                    else:
                        self.link = link
                        playlist = Download(link)
                        result = playlist.showPlaylist()
                        if(result != None):
                            self.streames = result['streams']
                            window["-TIPOS-"].update(self.streames)
                            window["-TITULO-"].update(value=result['titulo'])
                        else:
                            sg.PopupError("Insira um link valido")
                            window["-LINK-"].update(value="")
                            self.streames = []
                            window["-TIPOS-"].update(self.streames)
                            window["-TITULO-"].update(value="")
            if event == "-BAIXAR-":
                if(values["-tipo_video-"] == True):
                    selecionado = values['-TIPOS-'][0]
                    indice = self.streames.index(selecionado)
                    output = values["-DIRETORIO-"]
                    stream = self.streames[indice]
                    try:
                        stream.download(output_path=output)
                        sg.Popup("Arquivo baixado com sucesso")
                    except:
                        sg.PopupError("Não foi possivel baixar o arquivo ;-;")
                else:
                    output = values["-DIRETORIO-"]
                    window["-BAIXAR-"].update(disabled=True)
                    downPlaylist = DownloadPlaylist(self.streames, output)
                    downPlaylist.start()
