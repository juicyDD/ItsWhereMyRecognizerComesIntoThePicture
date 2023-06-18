import tkinter
import tkinter.messagebox
import customtkinter
import os
import concurrent.futures
from PIL import Image
from tkinter import filedialog
import threading, queue, time
import uuid
from voicerecognizer.enroll_speaker import get_voiceprint
from mydatabase import crud
from mydatabase.models import Being, EmbeddingVector, Session, engine

class App(customtkinter.CTk):
    width = 900
    height = 600
    
    def __init__(self):
        super().__init__()
        
        self.title("The Voice Recognizer you might need on the fly")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        
        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "webpc.png")), size=(50, 50))
        self.enroll_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "enrolluser-light.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "enrolluser-dark.png")), size=(25, 25))
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  是dd不是弟弟", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        self.enroll_user_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Enroll new speaker",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.enroll_user_image, anchor="w", command=self.enroll_user_button_event)
        self.enroll_user_button.grid(row=1, column=0, sticky="ew")
        
        # create home frame
        self.enroll_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.enroll_frame.grid_columnconfigure(0, weight=1)
        
        #enrolling variables
        self.enroll_frame_speaker_name = None
        self.enroll_frame_speaker_id = None
        self.enroll_frame_speaker_ssn = None
        self.enroll_frame_audio_files = set()
        self.enroll_frame_clustering_results = []
        
        self.enroll_frame_entry_name = customtkinter.CTkEntry(master=self.enroll_frame, placeholder_text="Speaker name")
        self.enroll_frame_entry_name.grid(row=1, column=0, columnspan=2, padx=20,pady=(90,0), sticky='nsew')
        self.enroll_frame_entry_name_error = customtkinter.CTkLabel(self.enroll_frame,padx=30,  text="", font=customtkinter.CTkFont(size=10))
        self.enroll_frame_entry_name_error.grid(row=2,column=0, sticky='W')
        
        self.enroll_frame_entry_speaker_id = customtkinter.CTkEntry(master=self.enroll_frame, placeholder_text="Speaker id (nullable)")
        self.enroll_frame_entry_speaker_id.grid(row=3, column=0, columnspan=2, padx=20, pady=(0,20), sticky='nsew')
        
        self.enroll_frame_upload_button = customtkinter.CTkButton(self.enroll_frame, text='Upload audio files', command=self.enroll_frame_upload_enroll_files)
        self.enroll_frame_upload_button.grid(row=4, column=0, padx=20, pady=(20,0), sticky='nsew')
        self.enroll_frame_upload_error = customtkinter.CTkLabel(self.enroll_frame,padx=30,  text="", font=customtkinter.CTkFont(size=10))
        self.enroll_frame_upload_error.grid(row=5,column=0, sticky='W')
        
        self.enroll_frame_submit_enroll_button = customtkinter.CTkButton(master=self.enroll_frame, text='Enroll', fg_color="transparent", border_width=2, 
                                                            text_color=("gray10", "#DCE4EE"), command=self.enroll_frame_submit_enroll_user)
        self.enroll_frame_submit_enroll_button.grid(row=6, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.enroll_frame_enroll_msg = customtkinter.CTkLabel(self.enroll_frame,padx=30,  text="", font=customtkinter.CTkFont(size=10))
        self.enroll_frame_enroll_msg.grid(row=7,column=2, sticky='W')
        # select default frame
        self.select_frame_by_name("enroll")
        
    """Event switch frame"""
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.enroll_user_button.configure(fg_color=("gray75", "gray25") if name == "enroll" else "transparent")
        # self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        # self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "enroll":
            self.enroll_frame.grid(row=0, column=1, sticky="nsew")    
    def enroll_user_button_event(self):
        self.select_frame_by_name('enroll')
        print('enroll user frame')
    
    """Event nhấn button upload *.flac files"""
    def enroll_frame_upload_enroll_files(self):
        files = filedialog.askopenfilenames(filetypes=[("FLAC files", '*.flac')])
        self.enroll_frame_audio_files |= set(files)
        # print("selected files:",self.enroll_frame_audio_files)
        
    """Event nhấn submit để start enrolling"""
    def enroll_frame_submit_enroll_user(self):
        self.enroll_frame_speaker_name = self.enroll_frame_entry_name.get()
        self.enroll_frame_speaker_id = self.enroll_frame_entry_speaker_id.get()
        invalid_flag = False
        
        if self.enroll_frame_speaker_name.replace(' ','') == '':
            self.enroll_frame_entry_name_error.configure(text='Speaker name is required ┐ (︶ ▽ ︶) ┌')
            invalid_flag = True
            
        if len(self.enroll_frame_audio_files) == 0:
            self.enroll_frame_upload_error.configure(text="Speaker's utterances is required ┐ (︶ ▽ ︶) ┌")
            invalid_flag = True
            
        if invalid_flag:
            return
        self.enroll_frame_upload_button.configure(state="disabled")
        self.enroll_frame_submit_enroll_button.configure(state="disabled")
        
        self.enroll_frame_entry_name_error.configure(text='')
        self.enroll_frame_upload_error.configure(text='')
        self.enroll_frame_enroll_msg.configure(text='')

        print('Name:',self.enroll_frame_speaker_name)
        print('Speaker Id:', self.enroll_frame_speaker_id)
        
        
        my_thread = threading.Thread(target=get_voiceprint,args=[self.enroll_frame_audio_files,self.enroll_frame_clustering_results,
                                                                 self.enroll_frame_on_done_submit]) #enroll_frame_on_done_submit là hàm callback
        my_thread.start()
        
        # while my_thread.is_alive():
        #     time.sleep(0.1)
        # print('ress',results)
        # self.enroll_frame_on_done_submit()

    def enroll_frame_on_done_submit(self):
        self.enroll_frame_upload_button.configure(state="normal")
        self.enroll_frame_submit_enroll_button.configure(state="normal")
        self.enroll_frame_speaker_ssn = str(uuid.uuid4())
        crud.createBeing(name=self.enroll_frame_speaker_name, speaker_id=self.enroll_frame_speaker_id, ssn=self.enroll_frame_speaker_ssn)
        crud.createEmbedding(embeddings=self.enroll_frame_clustering_results, speaker_ssn = self.enroll_frame_speaker_ssn)
        print(self.enroll_frame_speaker_ssn)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
    
"""Uyen Nhi on the dotted line"""