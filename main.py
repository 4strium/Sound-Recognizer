import speech_recognition as sr
import os
from pydub import AudioSegment
import tkinter                      # Module pour créer une interface graphique, et ses dépendances.
from tkinter import *               
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk 


def analyse_fichier():
    """
    Procédure appelée quand l'user. appuie sur le bouton "Analyser un fichier"
    """

    # L'utilisateur ne pourra sélectionner que les fichiers textes :
    filetypes = [
        ('Fichiers audios', '*.wav', '*mp3')
    ]
    
    # Un pop-up apparaît sur l'écran pour séléctionner le fichier à compresser.
    file_opened = fd.askopenfilename(
        title='Selectionnez le fichier à analyser...',
        initialdir='/',
        filetypes=filetypes
    )

    file_extension = os.path.splitext(os.path.abspath(file_opened))[1]

    # Conversion en d'un fichier .mp3 en .wav :
    if file_extension == '.mp3' :
        sound = AudioSegment.from_mp3(file_opened)
        dst = open("mp3_to_wav.wav", "w")
        sound.export(dst, format="wav")
        file_opened = open("mp3_to_wav.wav", "r")
        file_extension = '.wav'
    
    if file_extension == '.wav' :

        # Ouverture et lecture du fichier :
        r = sr.Recognizer()
        with sr.AudioFile(file_opened) as source:
            audio = r.record(source)
            try:
                datafr = r.recognize_google(audio, language="fr-FR")
            except:
                print("Ressayez s'il vous plaît...")


        file = open("résultat.txt", "w")
        file.write("J'ai compris le texte suivant : \n" + datafr)

        file.close()
    
    else :
        return 'Erreur'
    
# On génère la fenêtre :
root = tkinter.Tk()

# Je défini des paramètres à cette fenêtre :
root.title("Logiciel de reconnaissance vocale")  # Un titre
root.geometry("1080x720")                                # Une résolution d'affichage, ici HD
root.minsize(1080, 720)                                  # Je bloque cette résolution, pour éviter que l'utilisateur ne redimensionne n'importe comment.
root.maxsize(1080, 720)
root.iconbitmap(default='icon\micro_icon.ico') # Je défini un icon pour la fenêtre

# J'importe et j'affiche une image de fond pour mon accueil :
bg = PhotoImage(file = "img\Background_IMAGE.png")
canvas_accueil = Canvas( root, width = 1080, height = 720)
canvas_accueil.pack(fill = "both", expand = True)
canvas_accueil.create_image( 0, 0, image = bg, anchor = "nw")


def msg_remerciement():
    '''
    Cette procédure affiche un message de remerciement lorsque l'utilisateur ferme la fenêtre principale.
    Puis elle met fin au fonctionnement de celle-ci.
    '''
    messagebox.showinfo('Dev : Romain MELLAZA',"Merci d'avoir utilisé mon logiciel ! :)")
    root.destroy()

# Ces lignes de codes permettent au programme d'actionner la fonction de remerciement si il reçoit l'information que l'utilisateur essaie de fermer le logiciel :
try:
    root.protocol('WM_DELETE_WINDOW', msg_remerciement)
except:
    pass


# Je rafraîchis continuellement mon application via cette commande :
root.mainloop()