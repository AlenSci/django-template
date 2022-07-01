from django.conf import settings


def save_frame_from_video(video_path, millisecond):
    import cv2
    vidcap = cv2.VideoCapture(video_path)

    vidcap.set(cv2.CAP_PROP_POS_MSEC, millisecond)
    success, image = vidcap.read()
    if success: cv2.imwrite("framed.jpg", image)  # save frame as JPEG file

    return f'{settings.BASE_DIR}/framed.jpg'
