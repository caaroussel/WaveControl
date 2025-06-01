import threading
import queue
import wave_control
import hand_control

img_queue = queue.Queue(maxsize=1)

threading.Thread(target=hand_control.run_hand_tracking, kwargs={"image_queue": img_queue}, daemon=True).start()

wave_control.run_wave_animation(evolutive=False, image_queue=img_queue)
