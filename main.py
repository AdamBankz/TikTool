import customtkinter
import os
from PIL import Image
import threading
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.captcha import CaptchaWindow
import requests




driver = None
webhook = None

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("dark")

        self.title("TikTool V1.4")
        self.geometry("950x650") 


        self.total_views = 0
        self.total_likes = 0
        self.total_followers = 0
        self.total_shares = 0
        self.total_favourites = 0
        self.total_comment_likes = 0



        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        try:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            image_path = os.path.join(script_dir, "assets")

            if not os.path.isdir(image_path):
                 raise FileNotFoundError("Assets directory not found at expected location")

            self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
            self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(200, 200))
            self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
            self.home_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
            self.chat_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
            self.add_user_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
            self.webhook = customtkinter.CTkImage(Image.open(os.path.join(image_path, "discord.png")), size=(20, 20))
            self.generic_action_image = self.add_user_image

            self.webhook_image = self.webhook

        except (FileNotFoundError, NameError): 
            print("Warning: Asset images not found or PIL library issue. Using placeholders.")

            placeholder_img_26 = Image.new('RGB', (26, 26), color = 'grey')
            placeholder_img_200 = Image.new('RGB', (200, 200), color='darkgrey')
            placeholder_img_20 = Image.new('RGB', (20, 20), color = 'grey')


            self.logo_image = customtkinter.CTkImage(light_image=placeholder_img_26, dark_image=placeholder_img_26, size=(26, 26))
            self.large_test_image = customtkinter.CTkImage(light_image=placeholder_img_200, dark_image=placeholder_img_200, size=(200, 200))
            self.image_icon_image = customtkinter.CTkImage(light_image=placeholder_img_20, dark_image=placeholder_img_20, size=(20, 20))
            self.home_image = customtkinter.CTkImage(light_image=placeholder_img_20, dark_image=placeholder_img_20, size=(20, 20))
            self.chat_image = customtkinter.CTkImage(light_image=placeholder_img_20, dark_image=placeholder_img_20, size=(20, 20))
            self.add_user_image = customtkinter.CTkImage(light_image=placeholder_img_20, dark_image=placeholder_img_20, size=(20, 20))
            self.generic_action_image = self.add_user_image

            self.webhook_image = self.generic_action_image

        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        self.navigation_frame.grid_rowconfigure(8, weight=1) 

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  sharkpc.xd", 
                                                               image=self.logo_image,
                                                               compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Configuration",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Likes",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Followers",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")


        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Views",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")


        self.shares_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Shares",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.generic_action_image, anchor="w", command=self.shares_button_event)
        self.shares_button.grid(row=5, column=0, sticky="ew")

        self.favourites_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Favourites",
                                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                         image=self.generic_action_image, anchor="w", command=self.favourites_button_event)
        self.favourites_button.grid(row=6, column=0, sticky="ew")

        self.comment_likes_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Comment Likes",
                                                             fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                             image=self.generic_action_image, anchor="w", command=self.comment_likes_button_event)
        self.comment_likes_button.grid(row=7, column=0, sticky="ew")

        self.webhook_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Webhook",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.webhook_image, 
                                                      anchor="w", command=self.webhook_button_event) 

        self.webhook_button.grid(row=8, column=0, sticky="sew", pady=(10, 10))


        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # Logo
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=5)

        # Statistics frame
        self.stats_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=10)
        self.stats_frame.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
        self.stats_frame.grid_columnconfigure(0, weight=1) # Ensure labels align left

        self.stats_label = customtkinter.CTkLabel(self.stats_frame, text="Nhin Thg Cha M", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.stats_label.grid(row=0, column=0, padx=20, pady=5, sticky="w") # Align left

        self.views_stat = customtkinter.CTkLabel(self.stats_frame, text=f"Tổng View: {self.total_views}", font=customtkinter.CTkFont(size=16))
        self.views_stat.grid(row=1, column=0, padx=20, pady=2, sticky="w") # Align left

        self.likes_stat = customtkinter.CTkLabel(self.stats_frame, text=f"Tổng Like: {self.total_likes}", font=customtkinter.CTkFont(size=16))
        self.likes_stat.grid(row=2, column=0, padx=20, pady=2, sticky="w") # Align left

        self.followers_stat = customtkinter.CTkLabel(self.stats_frame, text=f"Tổng Followers: {self.total_followers}", font=customtkinter.CTkFont(size=16))
        self.followers_stat.grid(row=3, column=0, padx=20, pady=2, sticky="w") # Align left

        self.shares_stat = customtkinter.CTkLabel(self.stats_frame, text=f"Tổng Shares: {self.total_shares}", font=customtkinter.CTkFont(size=16))
        self.shares_stat.grid(row=4, column=0, padx=20, pady=2, sticky="w")

        self.favourites_stat = customtkinter.CTkLabel(self.stats_frame, text=f"Tổng Favourites: {self.total_favourites}", font=customtkinter.CTkFont(size=16))
        self.favourites_stat.grid(row=5, column=0, padx=20, pady=2, sticky="w")

        self.comment_likes_stat = customtkinter.CTkLabel(self.stats_frame, text=f"Tổng Comment Likes: {self.total_comment_likes}", font=customtkinter.CTkFont(size=16))
        self.comment_likes_stat.grid(row=6, column=0, padx=20, pady=2, sticky="w")


        # Configuration Section Label
        self.home_frame_config_label = customtkinter.CTkLabel(self.home_frame, text="Cấu Hình", font=customtkinter.CTkFont(size=20, weight="bold")) # Renamed variable for clarity
        self.home_frame_config_label.grid(row=2, column=0, padx=20, pady=10, sticky="w") # Align left

        # Entry Fields
        self.entry1 = customtkinter.CTkEntry(self.home_frame, width=300, placeholder_text="Profile Link")
        self.entry1.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew") # Stretch horizontally
        self.entry1.configure(state="disabled") # As per original code

        self.entry2 = customtkinter.CTkEntry(self.home_frame, width=300, placeholder_text="Video Link")
        self.entry2.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew") # Stretch horizontally

        # create second frame (Likes)
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure((0, 1, 2), weight=1) 
        self.like_switch = customtkinter.CTkSwitch(
            master=self.second_frame,
            text="Start the bot",
            font=customtkinter.CTkFont(size=14),
            onvalue="on",
            offvalue="off",
            fg_color="#2f2f2f",
            progress_color="#1e90ff",
            button_color="#ffffff",
            button_hover_color="#cccccc",
            command=lambda: self.handle_switch_toggle(self.like_switch, "likes"))
        self.like_switch.grid(row=0, column=1, padx=195, pady=10, sticky="nsew") 

        self.second_frame_textbox = customtkinter.CTkTextbox(self.second_frame, width=350, height=350)
        self.second_frame_textbox.grid(row=1, column=1, padx=(7, 0), pady=(20, 0), sticky="nsew") 

        # create third frame (Followers)
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure((0, 1, 2), weight=1) 
        self.follower_switch = customtkinter.CTkSwitch(
            master=self.third_frame,
            text="Start the bot",
            font=customtkinter.CTkFont(size=14),
            onvalue="on",
            offvalue="off",
            fg_color="#2f2f2f",
            progress_color="#1e90ff",
            button_color="#ffffff",
            button_hover_color="#cccccc",
            command=lambda: self.handle_switch_toggle(self.follower_switch, "followers"))

        self.follower_switch.grid(row=0, column=1, padx=195, pady=10, sticky="nsew") 
        self.follower_switch.configure(state="disabled") 
        self.third_frame_textbox = customtkinter.CTkTextbox(self.third_frame, width=350, height=350)
        self.third_frame_textbox.grid(row=1, column=1, padx=(7, 0), pady=(20, 0), sticky="nsew") 

        # create fourth frame (Views)
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fourth_frame.grid_columnconfigure((0, 1, 2), weight=1) 
        self.views_switch = customtkinter.CTkSwitch(
            master=self.fourth_frame,
            text="Start the bot",
            font=customtkinter.CTkFont(size=14),
            onvalue="on",
            offvalue="off",
            fg_color="#2f2f2f",
            progress_color="#1e90ff",
            button_color="#ffffff",
            button_hover_color="#cccccc",
            command=lambda: self.handle_switch_toggle(self.views_switch, "views"))
        self.views_switch.grid(row=0, column=1, padx=195, pady=10, sticky="nsew")

        self.fourth_frame_textbox = customtkinter.CTkTextbox(self.fourth_frame, width=350, height=350)
        self.fourth_frame_textbox.grid(row=1, column=1, padx=(7, 0), pady=(20, 0), sticky="nsew") 


        self.shares_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.shares_frame.grid_columnconfigure((0, 1, 2), weight=1) 
        self.shares_switch = customtkinter.CTkSwitch(
            master=self.shares_frame,
            text="Start the bot",
            font=customtkinter.CTkFont(size=14),
            onvalue="on",
            offvalue="off",
            fg_color="#2f2f2f",
            progress_color="#1e90ff",
            button_color="#ffffff",
            button_hover_color="#cccccc",
            command=lambda: self.handle_switch_toggle(self.shares_switch, "shares"))
        self.shares_switch.grid(row=0, column=1, padx=195, pady=10, sticky="nsew")

        self.shares_frame_textbox = customtkinter.CTkTextbox(self.shares_frame, width=350, height=350)
        self.shares_frame_textbox.grid(row=1, column=1, padx=(7, 0), pady=(20, 0), sticky="nsew")

        # create favourites frame (Sixth Frame)
        self.favourites_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.favourites_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.favourites_switch = customtkinter.CTkSwitch(
            master=self.favourites_frame,
            text="Start the bot",
            font=customtkinter.CTkFont(size=14),
            onvalue="on",
            offvalue="off",
            fg_color="#2f2f2f",
            progress_color="#1e90ff",
            button_color="#ffffff",
            button_hover_color="#cccccc",
            command=lambda: self.handle_switch_toggle(self.favourites_switch, "favourites"))
        self.favourites_switch.grid(row=0, column=1, padx=195, pady=10, sticky="nsew")

        self.favourites_frame_textbox = customtkinter.CTkTextbox(self.favourites_frame, width=350, height=350)
        self.favourites_frame_textbox.grid(row=1, column=1, padx=(7, 0), pady=(20, 0), sticky="nsew")

        # create comment likes frame (Seventh Frame)
        self.comment_likes_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.comment_likes_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.comment_likes_switch = customtkinter.CTkSwitch(
            master=self.comment_likes_frame,
            text="Start the bot",
            font=customtkinter.CTkFont(size=14),
            onvalue="on",
            offvalue="off",
            fg_color="#2f2f2f",
            progress_color="#1e90ff",
            button_color="#ffffff",
            button_hover_color="#cccccc",
            command=lambda: self.handle_switch_toggle(self.comment_likes_switch, "comment_likes"))
        self.comment_likes_switch.grid(row=0, column=1, padx=195, pady=10, sticky="nsew")
        self.comment_likes_switch.configure(state="disabled")

        self.comment_likes_frame_textbox = customtkinter.CTkTextbox(self.comment_likes_frame, width=350, height=350)
        self.comment_likes_frame_textbox.grid(row=1, column=1, padx=(7, 0), pady=(20, 0), sticky="nsew")

        self.webhook_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.webhook_frame.grid_columnconfigure(0, weight=1) 
        self.webhook_frame.grid_columnconfigure(1, weight=0)
        self.webhook_frame.grid_rowconfigure(0, weight=1) 
        self.webhook_frame.grid_rowconfigure(3, weight=1) 


        self.webhook_label = customtkinter.CTkLabel(self.webhook_frame, text="Webhook URL:", font=customtkinter.CTkFont(size=14))
        self.webhook_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="sw") 


        self.webhook_entry = customtkinter.CTkEntry(self.webhook_frame, placeholder_text="Enter Discord Webhook URL", width=400) 
        self.webhook_entry.grid(row=2, column=0, padx=(20, 5), pady=(5, 20), sticky="ew")


        self.webhook_switch = customtkinter.CTkSwitch(master=self.webhook_frame,
                                                      text="Enable",
                                                      command=self.toggle_webhook_state,
                                                      onvalue="on", offvalue="off") 
        self.webhook_switch.grid(row=2, column=1, padx=(0, 20), pady=(5, 20), sticky="w") 



        self.likes_bot_thread = None
        self.followers_bot_thread = None
        self.views_bot_thread = None
 
        self.shares_bot_thread = None
        self.favourites_bot_thread = None
        self.comment_likes_bot_thread = None

        self.likes_bot_running = False
        self.followers_bot_running = False
        self.views_bot_running = False

        self.shares_bot_running = False
        self.favourites_bot_running = False
        self.comment_likes_bot_running = False




        self.select_frame_by_name("home")


    def toggle_webhook_state(self):
        global webhook 
        if self.webhook_switch.get() == "on":

            current_url = self.webhook_entry.get()
            self.webhook_entry.configure(state="disabled")
            webhook = current_url
        else:
            self.webhook_entry.configure(state="normal")
            webhook = None 



    def select_frame_by_name(self, name):

        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        self.shares_button.configure(fg_color=("gray75", "gray25") if name == "shares_frame" else "transparent")
        self.favourites_button.configure(fg_color=("gray75", "gray25") if name == "favourites_frame" else "transparent")
        self.comment_likes_button.configure(fg_color=("gray75", "gray25") if name == "comment_likes_frame" else "transparent")

        self.webhook_button.configure(fg_color=("gray75", "gray25") if name == "webhook_frame" else "transparent")


        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()


        if name == "shares_frame":
            self.shares_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.shares_frame.grid_forget()
        if name == "favourites_frame":
            self.favourites_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.favourites_frame.grid_forget()
        if name == "comment_likes_frame":
            self.comment_likes_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.comment_likes_frame.grid_forget()

        if name == "webhook_frame":
            self.webhook_frame.grid(row=0, column=1, sticky="nsew")
        else:

            if hasattr(self, 'webhook_frame'):
                self.webhook_frame.grid_forget()


    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")


    def shares_button_event(self):
        self.select_frame_by_name("shares_frame")

    def favourites_button_event(self):
        self.select_frame_by_name("favourites_frame")

    def comment_likes_button_event(self):
        self.select_frame_by_name("comment_likes_frame")

    def webhook_button_event(self):
        self.select_frame_by_name("webhook_frame")



    def handle_switch_toggle(self, activated_switch, bot_type):

        all_switches = [
            self.like_switch, self.follower_switch, self.views_switch,
            self.shares_switch, self.favourites_switch, self.comment_likes_switch
        ]

        if activated_switch.get() == "on":

            for switch in all_switches:
                if switch != activated_switch and switch.get() == "on":

                    if switch == self.like_switch: self.likes_bot_running = False
                    elif switch == self.follower_switch: self.followers_bot_running = False
                    elif switch == self.views_switch: self.views_bot_running = False
                    elif switch == self.shares_switch: self.shares_bot_running = False
                    elif switch == self.favourites_switch: self.favourites_bot_running = False
                    elif switch == self.comment_likes_switch: self.comment_likes_bot_running = False
                    switch.deselect() 


            if bot_type == "likes":
                if not self.likes_bot_running: 
                    self.likes_bot_running = True
                    self.likes_bot_thread = threading.Thread(target=self.run_likes_bot, daemon=True) 
                    self.likes_bot_thread.start()
            elif bot_type == "followers":
                 if not self.followers_bot_running:
                    self.followers_bot_running = True
                    self.followers_bot_thread = threading.Thread(target=self.run_followers_bot, daemon=True)
                    self.followers_bot_thread.start()
            elif bot_type == "views":
                 if not self.views_bot_running:
                    self.views_bot_running = True
                    self.views_bot_thread = threading.Thread(target=self.run_views_bot, daemon=True)
                    self.views_bot_thread.start()

            elif bot_type == "shares":
                if not self.shares_bot_running:
                    self.shares_bot_running = True
                    self.shares_bot_thread = threading.Thread(target=self.run_shares_bot, daemon=True)
                    self.shares_bot_thread.start()
            elif bot_type == "favourites":
                 if not self.favourites_bot_running:
                    self.favourites_bot_running = True
                    self.favourites_bot_thread = threading.Thread(target=self.run_favourites_bot, daemon=True)
                    self.favourites_bot_thread.start()
            elif bot_type == "comment_likes":
                if not self.comment_likes_bot_running:
                    self.comment_likes_bot_running = True
                    self.comment_likes_bot_thread = threading.Thread(target=self.run_comment_likes_bot, daemon=True)
                    self.comment_likes_bot_thread.start()


        else:
            if bot_type == "likes":
                self.likes_bot_running = False
            elif bot_type == "followers":
                self.followers_bot_running = False
            elif bot_type == "views":
                self.views_bot_running = False
            elif bot_type == "shares":
                self.shares_bot_running = False
            elif bot_type == "favourites":
                self.favourites_bot_running = False
            elif bot_type == "comment_likes":
                self.comment_likes_bot_running = False

    def run_likes_bot(self):
        global driver
        payload = {
            "content": "15 likes sent successfully."
            }
        try:
            openZefoy()
            like = driver.find_element(By.XPATH, "//button[@class='btn btn-primary rounded-0 t-hearts-button']").click()
            time.sleep(1)
            input = driver.find_element(By.XPATH, '/html/body/div[8]/div/form/div/input')
            input.send_keys(self.entry2.get())
            time.sleep(1)
            self.second_frame_textbox.insert("end", "Likebot started!\n")
            while self.likes_bot_running:
                try:
                    search_button = driver.find_element(By.XPATH, '/html/body/div[8]/div/form/div/div/button')
                    search_button.click()
                    time.sleep(1)
                    try:
                        target_button = driver.find_element(By.XPATH, '/html/body/div[8]/div/div/div[1]/div/form/button')
                        target_button.click()
                        self.total_likes += 15
                        self.likes_stat.configure(text=f"Total Likes: {self.total_likes}")
                        self.second_frame_textbox.insert("end", "15 likes sent successfully!\n")
                        self.second_frame_textbox.see("end")
                        requests.post(webhook, payload)
                    except:
                        self.second_frame_textbox.see("end")
                    
                    time.sleep(3)
                    
                except Exception as e:
                    self.second_frame_textbox.insert("end", f"Error: {str(e)}\n")
                    self.second_frame_textbox.see("end")
                    time.sleep(3)
                    
            driver.quit()
            self.second_frame_textbox.insert("end", "Likes bot stopped.\n")
            self.second_frame_textbox.see("end")
        except Exception as e:
            self.second_frame_textbox.insert("end", f"Error: {str(e)}\n")
            self.second_frame_textbox.see("end")

  
    def run_followers_bot(self):
        global driver
        payload = {
            "content": "Follows sent successfully!"
            }
        try:
            openZefoy()
            follower = driver.find_element(By.XPATH, "//button[@class='btn btn-primary rounded-0 t-followers-button']").click()
            time.sleep(1)
            input = driver.find_element(By.XPATH, '/html/body/div[16]/div/form/div/input')
            input.send_keys(self.entry1.get())
            time.sleep(1)
            self.third_frame_textbox.insert("end", "Followbot started!\n")
            while self.followers_bot_running:
                try:
                    search_button = driver.find_element(By.XPATH, '/html/body/div[6]/div/form/div/div/button')
                    search_button.click()
                    time.sleep(1)

                    try:
                        target_button = driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div[1]/div/form/button')
                        target_button.click()
                        self.total_followers += 1
                        self.followers_stat.configure(text=f"Total Followers: {self.total_followers}")
                        self.third_frame_textbox.insert("end", "Followers sent successfully!\n")
                        self.third_frame_textbox.see("end")
                        requests.post(webhook, payload)
                    except:
                        self.third_frame_textbox.see("end")
                    
                    time.sleep(3)  
                    
                except Exception as e:
                    self.third_frame_textbox.insert("end", f"Error: {str(e)}\n")
                    self.third_frame_textbox.see("end")
                    time.sleep(3) 
                    
            driver.quit()
            self.third_frame_textbox.insert("end", "Followers bot stopped.\n")
            self.third_frame_textbox.see("end")
        except Exception as e:
            self.third_frame_textbox.insert("end", f"Error: {str(e)}\n")
            self.third_frame_textbox.see("end")


    def run_views_bot(self):
        global driver
        payload = {
            "content": "1000 views sent successfully!"
            }
        try:
            openZefoy()
            view = driver.find_element(By.XPATH, "//button[@class='btn btn-primary rounded-0 t-views-button']").click()
            time.sleep(1)
            input = driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/input')
            input.send_keys(self.entry2.get())
            time.sleep(1)
            self.fourth_frame_textbox.insert("end", "Viewbot started!\n")
            while self.views_bot_running:
                try:
                    search_button = driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/div/button')
                    search_button.click()
                    time.sleep(1)
                    try:
                        target_button = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div[1]/div/form/button')
                        target_button.click()
                        self.total_views += 1000
                        self.views_stat.configure(text=f"Total Views: {self.total_views}")
                        self.fourth_frame_textbox.insert("end", "1000 views sent successfully!\n")
                        self.fourth_frame_textbox.see("end")
                        requests.post(webhook, payload)
                    except:
                        self.fourth_frame_textbox.see("end")
                    
                    time.sleep(3)
                    
                except Exception as e:
                    self.fourth_frame_textbox.insert("end", f"Error: {str(e)}\n")
                    self.fourth_frame_textbox.see("end")
                    time.sleep(3)
                    
            driver.quit()
            self.fourth_frame_textbox.insert("end", "Views bot stopped.\n")
            self.fourth_frame_textbox.see("end")
        except Exception as e:
            self.fourth_frame_textbox.insert("end", f"Error: {str(e)}\n")
            self.fourth_frame_textbox.see("end")

    def run_shares_bot(self):
        global driver
        
        try:
            openZefoy()
            share = driver.find_element(By.XPATH, "//button[@class='btn btn-primary rounded-0 t-shares-button']").click()
            time.sleep(1)
            input = driver.find_element(By.XPATH, '/html/body/div[11]/div/form/div/input')
            input.send_keys(self.entry2.get())
            time.sleep(1)
            self.shares_frame_textbox.insert("end", "Sharebot started!\n")
            while self.shares_bot_running:
                try:
                    search_button = driver.find_element(By.XPATH, '/html/body/div[11]/div/form/div/div/button')
                    search_button.click()
                    time.sleep(1)
                    try:
                        target_button = driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div[1]/div/form/button')
                        target_button.click()
                        self.shares_stat += 150
                        self.views_stat.configure(text=f"Total Views: {self.total_views}")
                        self.shares_frame_textbox.insert("end", "150 shares sent successfully!\n")
                        self.shares_frame_textbox.see("end")
                    except:
                        self.fourth_frame_textbox.see("end")
                    
                    time.sleep(3)
                    
                except Exception as e:
                    self.shares_frame_textbox.insert("end", f"Error: {str(e)}\n")
                    self.shares_frame_textbox.see("end")
                    time.sleep(3)
                    
            driver.quit()
            self.shares_frame_textbox.insert("end", "Share bot stopped.\n")
            self.shares_frame_textbox.see("end")
        except Exception as e:
            self.shares_frame_textbox.insert("end", f"Error: {str(e)}\n")
            self.shares_frame_textbox.see("end")



    def run_favourites_bot(self):
        global driver
        payload = {
            "content": "90 favourites sent successfully."
            }
        try:
            openZefoy()
            fav = driver.find_element(By.XPATH, "//button[@class='btn btn-primary rounded-0 t-favorites-button']").click()
            time.sleep(1)
            input = driver.find_element(By.XPATH, '/html/body/div[12]/div/form/div/input')
            input.send_keys(self.entry2.get())
            time.sleep(1)
            self.favourites_frame_textbox.insert("end", "Favourite bot started!\n")
            while self.favourites_bot_running:
                try:
                    search_button = driver.find_element(By.XPATH, '/html/body/div[12]/div/form/div/div/button')
                    search_button.click()
                    time.sleep(1)
                    try:
                        target_button = driver.find_element(By.XPATH, '/html/body/div[12]/div/div/div[1]/div/form/button')
                        target_button.click()
                        self.favourites_stat += 90
                        self.views_stat.configure(text=f"Total Views: {self.total_views}")
                        self.favourites_frame_textbox.insert("end", "90 Favourites sent successfully!\n")
                        self.favourites_frame_textbox.see("end")
                        requests.post(webhook, payload)
                    except:
                        self.favourites_frame_textbox.see("end")
                    
                    time.sleep(3)
                    
                except Exception as e:
                    self.favourites_frame_textbox.insert("end", f"Error: {str(e)}\n")
                    self.favourites_frame_textbox.see("end")
                    time.sleep(3)
                    
            driver.quit()
            self.favourites_frame_textbox.insert("end", "Favourite bot stopped.\n")
            self.favourites_frame_textbox.see("end")
        except Exception as e:
            self.favourites_frame_textbox.insert("end", f"Error: {str(e)}\n")
            self.favourites_frame_textbox.see("end")

    def run_comment_likes_bot(self):
        print("")



def openZefoy():
    global driver
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    driver = uc.Chrome(options=chrome_options)

    try:
        driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["https://fundingchoicesmessages.google.com/*"]})
        driver.execute_cdp_cmd("Network.enable", {})
    except Exception as cdp_err:
        print(f"Warning: Could not set CDP network blocking: {cdp_err}")

    driver.get("https://zefoy.com/")
    time.sleep(3)
    if captcha():
        print("Captcha successful")


def captcha():
    """Original captcha function structure."""
    global driver 
    is_retry = False
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        attempts+=1
        try:

            time.sleep(1) 
            input_field = driver.find_element(By.ID, "captchatoken") 
            input_field.clear()
            solution = captchaSave(is_retry)
            if solution is None: 
                print("Captcha solving cancelled or failed.")
                return False

            input_field.send_keys(solution)
            time.sleep(1)

            submit_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary.btn-lg.btn-block.rounded-0.submit-captcha[type="submit"]')
            submit_button.click()
            time.sleep(3) 


            try:
                error_popup_close_button = driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[3]/button") 
                error_popup_close_button.click()
                time.sleep(1)
                is_retry = True
                print("Captcha incorrect, retrying...")
                time.sleep(2)
                continue 
            except:
                try:
                    driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]') 
                    print("Captcha likely successful.")
                    return True 
                except:
                    print("Captcha state uncertain, assuming retry needed...")
                    is_retry = True
                    time.sleep(2)
                    continue 
        except Exception as e:
             print(f"Error during captcha attempt {attempts}: {e}")

             time.sleep(5)
             is_retry = True 
             continue 
    print("Failed to solve captcha after multiple attempts.")
    return False 


def captchaSave(is_retry=False):
    """Original captchaSave function structure."""
    global driver
    time.sleep(1)
    possible_div_numbers = [4, 5, 6] 
    for div_num in possible_div_numbers:
        xpath = f'/html/body/div[{div_num}]/div[2]/form/div/div/img' 
        try:
            l = driver.find_element(By.XPATH, xpath)
            captcha_file = 'captcha.png'
            with open(captcha_file, 'wb') as file:
                file.write(l.screenshot_as_png)
            captcha_window = CaptchaWindow(is_retry) 
            return captcha_window.result
        except Exception as e: 
            continue 


    print("Could not find captcha image after trying multiple XPaths.")
    return None 


if __name__ == "__main__":
    app = App()
    app.mainloop()
