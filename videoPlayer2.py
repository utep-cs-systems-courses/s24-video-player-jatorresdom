#!/usr/bin/env python3

import cv2
import threading
import queue
import argparse

# Constants
FRAME_RATE = 24
MAX_QUEUE_SIZE = 10

# Queues
color_frames = queue.Queue(maxsize=MAX_QUEUE_SIZE)
gray_frames = queue.Queue(maxsize=MAX_QUEUE_SIZE)

def extract_frames(video_path, frame_limit):
    cap = cv2.VideoCapture(video_path)
    count = 0
    while count < frame_limit:
        ret, frame = cap.read()
        if not ret:
            break
        color_frames.put(frame)  # Blocks if full
        print(f"Extracting frame {count}")
        count += 1
    color_frames.put(None)  # Signal that extraction is done

def convert_to_grayscale(frame_limit):
    count = 0
    while count < frame_limit:
        frame = color_frames.get()  # Blocks if empty
        if frame is None:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frames.put(gray_frame)  # Blocks if full
        print(f"Converting frame {count}")
        count += 1
    gray_frames.put(None)  # Signal that conversion is done

def display_frames(frame_limit):
    count = 0
    while count < frame_limit:
        frame = gray_frames.get()  # Blocks if empty
        if frame is None:
            break
        cv2.imshow('Video', frame)
        print(f"Displaying frame {count}")
        if cv2.waitKey(int(1000 / FRAME_RATE)) & 0xFF == ord('q'):
            break
        count += 1
    cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description="Process a video file to extract, convert, and display a specified number of frames.")
    parser.add_argument("video_path", type=str, help="Path to the video file.")
    parser.add_argument("frame_limit", type=int, help="Number of frames to process.")
    args = parser.parse_args()

    threads = [
        threading.Thread(target=extract_frames, args=(args.video_path, args.frame_limit)),
        threading.Thread(target=convert_to_grayscale, args=(args.frame_limit,)),
        threading.Thread(target=display_frames, args=(args.frame_limit,))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
