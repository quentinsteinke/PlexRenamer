import ffmpeg

video_file = ffmpeg.probe("L:\\Plex-Media-Server\\TV\\The Walking Dead (2010)\\Season 03\\The Walking Dead- Season 3 - Disc 5-B7_t12.mkv")

for metadata in video_file["streams"]:
    print(metadata)
    print("\n")