
import cv2

# Function to extract video segment between start_time and end_time
def extract_video_segment(input_path, output_path, start_time, end_time):
    # Open the input video
    cap = cv2.VideoCapture(input_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Calculate start and end frame numbers
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Set the starting frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Create VideoWriter object
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    current_frame = start_frame
    while cap.isOpened() and current_frame <= end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        current_frame += 1

    # Release resources
    cap.release()
    out.release()
    print(f"Video segment saved to {output_path}")

# Example usage
if __name__ == '__main__':
    input_path = r'C:\Users\uie68285\Videos\Video Project.mp4'
    output_path = r'C:\Users\uie68285\Videos\HumanWins.mp4'
    start_time = 55   # seconds
    end_time = 99    # seconds

    extract_video_segment(input_path, output_path, start_time, end_time)
