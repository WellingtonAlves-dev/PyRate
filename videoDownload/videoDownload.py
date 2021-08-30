from pytube import YouTube, Playlist
from threading import Thread
import ptoaster
import PySimpleGUI as sg
class DownloadPlaylist(Thread):
    def __init__(self, streames, output):
        Thread.__init__(self)
        self.streames = streames
        self.output = output
    def run(self):
        for video in self.streames:
            try:
                video.streams.filter(file_extension='mp4', only_audio=True).first().download(output_path=self.output)
                ptoaster.notify("Sucesso", f" O arquivo {video.title} foi baixado com sucesso")
            except:
                ptoaster.notify("Erro", f"Ocorreu um erro ao baixar o arquivo {video.title}", icon=ptoaster.icon_error)
        ptoaster.notify("Parabéns", f" Todos os arquivos foram baixados")


class Download:
    def __init__(self, link):
        self.link = link
    def showStreamers(self):
        try:
            you = YouTube(self.link)
            return {
                "titulo": you.title,
                "streams": you.streams
            }
        except:
            return None
    def showPlaylist(self):
        try:
            playlist = Playlist(self.link)
            return {
                "titulo": "playlist: " + playlist.title,
                "streams": playlist.videos
            }
        except:
            return None