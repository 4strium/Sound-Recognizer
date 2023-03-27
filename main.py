import speech_recognition as sr
import os
import tkinter                      # Module pour créer une interface graphique, et ses dépendances.
from tkinter import *               
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk 
from pydub import AudioSegment




def analyse_fichier():
    """
    Procédure appelée quand l'user. appuie sur le bouton "Analyser un fichier"
    """
    global button_ouverture_window, i, r

    # L'utilisateur ne pourra sélectionner que les fichiers textes :
    filetypes = [
        ('Fichiers audios', '.wav .mp3')
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
        input_path = os.path.abspath(file_opened)
        output_path = str(os.getcwd() + '/temp/audio_file_converted.wav')
        #conversion
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="wav")
        file_opened = open(output_path, "rb")
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

# J'affiche un titre sur ma page d'accueil :
i=canvas_accueil.create_text(540.45, 137, text=" Cliquez sur ce bouton pour ouvrir \n le fichier audio à analyser : ", font=("Helvetica", 42), fill="white", justify = CENTER)
r=canvas_accueil.create_rectangle(canvas_accueil.bbox(i),fill="#7900ce", width = 1)                                                            
canvas_accueil.tag_lower(r,i)

# Définition du bouton pour ouvrir le fichier :
button_ouverture = Button(root, text="Ouvrir un fichier audio", command=analyse_fichier, font=("Helvetica", 26), fg='white', bg="#7900ce", height = 2, width = 24)
button_ouverture_window = canvas_accueil.create_window(300, 425, anchor='nw', window=button_ouverture)

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