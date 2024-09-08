import json
import os
import tiktokgen


def generate_tiktok(itinerary, city, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    script = []
    for day, data in itinerary.items():
        day_parsed = day.replace("_", " ").replace("day", "Day")
        for i, d in enumerate(data):
            if i == 0:
                text = f"{day_parsed}: {d['description']}"
            else:
                text = d["description"]
            script.append(
                {
                    "text": text,
                    "foreground_img": None,
                    "prompt": f"{city} {d['location']}",
                }
            )

    prompt = tiktokgen.prompt_to_stock_video.prompt_to_stock_video(
        parsed_script=script, filedir=save_dir, augment_prompt=False
    )

    output_video_paths = []
    for i, item in enumerate(prompt):
        # create audio from script
        audio_filename = f"{os.path.basename(save_dir)}_speech_{i}"
        audio_path, transcription_data = (
            tiktokgen.script_snippet_to_audio.generate_speech_and_transcription(
                item["text"], filename=audio_filename
            )
        )
        print(f"Audio File Saved: {audio_path}")
        print(f"transcription_data: {transcription_data}")

        # combine video and audio
        output_video_path = f"{save_dir}/output_" + str(i) + ".mp4"
        tiktokgen.audio_video.combine_video_audio(
            item["video_path"],
            audio_path,
            transcription_data.words,
            output_video_path,
            item["foreground_img"],
        )
        output_video_paths.append(output_video_path)

    print(output_video_paths)
    combined_script = " ".join([x["text"] for x in script])
    final_video_path = f"{save_dir}/final_video.mp4"
    tiktokgen.audio_video.combine_videos(
        output_video_paths,
        final_video_path,
        combined_script,
        logo_path="data/sundai_logo.png",
    )
    return final_video_path


if __name__ == "__main__":
    with open("data/dymmy_itirenary_paris.json", "r") as file:
        inp_script = json.loads(file.read())
    generate_tiktok(inp_script, save_dir=f"data/test_dir")
