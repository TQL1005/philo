import tkinter as tk
import time
import random
import os


class Speech():
    def __init__(self, standing_point, direction, callback):
        self.callback = callback
        self.window = tk.Toplevel()  # Use Toplevel instead of Tk to create a separate window
        self.window.overrideredirect(True)  # Frameless window
        self.window.attributes('-topmost', True)  # Keep speech on top

        # Get screen width and height
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Choose random speech GIF

        # Assuming GIF files are in 'assets' folder relative to the script
        gif_dir = os.path.join('assets')

        # Combine relative path with GIF filenames
        if direction > 0:
            gif_files = [os.path.join(gif_dir, f'duck-speech{i}.gif') for i in range(1, 4)]
        else:
            gif_files = [os.path.join(gif_dir, f'duck-speech{i}.gif') for i in range(4, 9)]

        # Randomly select a GIF
        chosen_gif = random.choice(gif_files)

        # Example of assigning frame counts to GIFs using os.path.join to ensure correct path formatting
        gif_frame_counts = {
            os.path.join(gif_dir, 'duck-speech1.gif'): 21,
            os.path.join(gif_dir, 'duck-speech2.gif'): 57,
            os.path.join(gif_dir, 'duck-speech3.gif'): 43,
            os.path.join(gif_dir, 'duck-speech4.gif'): 29,
            os.path.join(gif_dir, 'duck-speech5.gif'): 45,
            os.path.join(gif_dir, 'duck-speech6.gif'): 40,
            os.path.join(gif_dir, 'duck-speech7.gif'): 13,
            os.path.join(gif_dir, 'duck-speech8.gif'): 27,
        }

        # Get the number of frames for the chosen GIF
        num_frames = gif_frame_counts[chosen_gif]

        # Load the GIF frames
        self.speech = [tk.PhotoImage(file=chosen_gif, format=f'gif -index {j}') for j in range(num_frames)]

        self.frame_index = 0
        self.img = self.speech[self.frame_index]
        self.timestamp = time.time()

        self.window.config(background='black')
        self.window.wm_attributes('-transparentcolor', 'black')
        self.window.overrideredirect(True)  # makes window frameless
        self.window.attributes('-topmost', True)  # puts window on top
        self.label = tk.Label(self.window, bd=0, bg='black')  # creates a label as a container for a gif

        # Starting position
        self.x = standing_point - 350
        self.y = self.screen_height - 140
        if direction > 0:  # currently moving right
            self.window.geometry('1040x1040+{}+{}'.format(self.x, self.y))
        else:
            self.window.geometry('1040x1040+{}+{}'.format(self.x - 220, self.y))
        self.label.configure(image=self.img)
        self.label.pack()

        self.speaking = False
        self.speech_index = 0
        self.speech_timestamp = time.time()
        self.animation_running = True  # Flag to control the animation running

        # Start updating the speech animation
        self.update()

    def update(self):
        if self.animation_running:
            self.frame_index += 1
            if self.frame_index < len(self.speech):
                self.img = self.speech[self.frame_index]
                self.label.configure(image=self.img)
                self.window.after(100, self.update)  # Adjust timing as necessary
            else:
                self.window.after(1000)
                self.animation_running = False  # Stop the animation after the last frame
                self.window.destroy()  # Close the window

                # After speech is done, wait 2 seconds before calling the callback
                if self.callback:
                    self.callback()


class pet():
    def __init__(self):
        self.window = tk.Tk()

        # Get screen width and height
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # code below generates string for each frame in gif
        self.moveleft = [tk.PhotoImage(file='duck-left.gif', format='gif -index %i' % (i)) for i in range(10)]
        self.moveright = [tk.PhotoImage(file='duck-right.gif', format='gif -index %i' % (i)) for i in range(10)]
        self.sleep_left = [tk.PhotoImage(file='duck-sleep-left.gif', format='gif -index %i' % (i)) for i in range(16)]
        self.sleep_right = [tk.PhotoImage(file='duck-sleep-right.gif', format='gif -index %i' % (i)) for i in range(16)]

        self.frame_index = 0  # setting starting frame
        self.img = self.moveleft[self.frame_index]  # starting direction gif
        self.timestamp = time.time()
        self.window.config(background='black')
        self.window.wm_attributes('-transparentcolor', 'black')
        self.window.overrideredirect(True)  # makes window frameless
        self.window.attributes('-topmost', True)  # puts window on top
        self.label = tk.Label(self.window, bd=0, bg='black')  # creates a label as a container for a gif

        # starting points
        self.x = self.screen_width - 100
        self.y = self.screen_height - 100
        self.window.geometry('104x100+{}+{}'.format(str(self.x), str(self.y)))
        self.label.configure(image=self.img)
        self.label.pack()
        self.window.after(0, self.update)

        self.dir = -1  # starting direction
        self.standing = False  # Flag to check if standing still
        self.sleep = False
        # Variable to hold the after() method's ID for cancellation
        self.animation_job = None

        self.window.after(0, self.update)
        self.window.mainloop()

    def changetime(self, direction):
        frame_count = len(direction)
        if time.time() > self.timestamp + 0.05:
            self.timestamp = time.time()
            if self.sleep:
                if self.frame_index < frame_count - 1:
                    self.frame_index += 1
            else:
                self.frame_index = (self.frame_index + 1) % 8  # speed of frames change
            self.img = direction[self.frame_index]

    def stop_animation(self):
        # Stop the current animation by canceling the update cycle
        if self.animation_job:
            self.window.after_cancel(self.animation_job)
            self.animation_job = None

    def start_animation(self, direction):
        # Start a new animation loop with the provided direction (frames)
        self.frame_index = 0  # Reset frame index
        self.animate(direction)

    def animate(self, direction):
        # Animate the current motion
        self.changetime(direction)

        # Schedule the next frame update and store the after() ID
        self.animation_job = self.window.after(50, self.animate, direction)

    def Sleep(self):
        self.sleep = True
        direction = self.sleep_left if self.dir < 0 else self.sleep_right
        self.stop_animation()  # Stop current motion
        self.start_animation(direction)  # Start sleep animation

        # Wake up after 45 seconds
        self.window.after(5000, self.resume_movement)

    def changedir(self):
        self.dir = -self.dir

    def go(self):

        if not self.standing and not self.sleep:
            self.x = self.x + self.dir
            if self.dir < 0:
                direction = self.moveleft
            else:
                direction = self.moveright
            self.changetime(direction)

    def standstill(self):
        # Handle random standstill and transition to sleep
        self.standing = True
        self.stop_animation()

        # 70% chance to transition to sleep, otherwise, call Speech (if implemented)
        if random.randint(0, 100) < 55:
            self.Sleep()
            # self.window.after(1500, self.resume_movement)
        elif random.randint(0, 100) < 25:
            self.window.after(3500, self.resume_movement)
        else:
            # Assuming Speech is implemented elsewhere
            Speech(self.x, self.dir, self.resume_movement)

    def resume_movement(self):
        self.standing = False
        self.sleep = False
        self.stop_animation()

        # Resume movement with a 0-4% chance to change direction
        if random.randint(0, 7500) < 2:
            self.changedir()

        # Start the movement animation again
        self.start_animation(self.moveleft if self.dir < 0 else self.moveright)

    def update(self):
        if not self.standing and not self.sleep and random.randint(0, 7500) < 5:  # 5% chance to stand randomly
            self.standstill()  # Call standstill randomly
        else:
            self.go()  # Otherwise, keep moving

        if self.x <= -100 or self.x >= self.screen_width - 5:
            self.changedir()  # Call change direction when hitting the screen edges

        self.window.geometry('104x100+{}+{}'.format(str(self.x), str(self.y)))
        self.label.configure(image=self.img)
        self.label.pack()
        self.window.after(13, self.update)  # 10 is frames number for my gif
        self.window.lift()


pet()
