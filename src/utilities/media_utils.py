import json
import logging
import subprocess
from pathlib import Path

from pymediainfo import MediaInfo


class FFProbeResult:
    def __init__(
        self, return_code: int = None, output: str = "", error: str = "", format=None
    ):
        self.return_code = return_code
        self.output = output
        self.error = error
        self.format = format
        self._output_as_dict = None

    def get_output_as_dict(self):
        if self._output_as_dict is None:
            if self.format == "json":
                self._output_as_dict = json.loads(self.output)
            elif self.format == "flat":
                output = [e.split("=") for e in self.output.strip().split("\n")]
                self._output_as_dict = {key_val[0]: key_val[1] for key_val in output}
            else:
                raise ValueError(
                    "ffprobe format '%s' not supported to build dict" % self.format
                )
        return self._output_as_dict

    def to_json_file(self, path: Path, mode="w", **kwargs):
        """
        :param mode: file open mode
        :param kwargs: kwargs for pathlib.Path().open()
        """
        path = path if isinstance(path, Path) else Path(path)
        with path.open(mode, **kwargs) as f:
            json.dump(self.get_output_as_dict(), f, indent=4)
            logging.debug("Dumped ffprobe output into %s", path)


def ffprobe(
    file_path, ffprobe_format="json", format_optn="", log_level="error"
) -> FFProbeResult:
    result = None
    assert ffprobe_format in ["json", "flat"], (
        "format must be json or flat, not %s" % ffprobe_format
    )
    format_optn = "=" + format_optn if format_optn else format_optn
    command_array = [
        "ffprobe",
        "-v",
        log_level,
        "-print_format",
        ffprobe_format + format_optn,
        "-show_programs",
        "-show_format",
        "-show_streams",
        f"{file_path}",
    ]
    try:
        result = subprocess.run(
            command_array,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except Exception as e:
        logging.critical(
            "ffprobe failed to run on %s, with the following error: '%s'\n"
            " check first that cmd is in your path",
            file_path,
            result.stderr,
            exc_info=True,
        )
        raise e

    return FFProbeResult(
        return_code=result.returncode,
        output=result.stdout,
        error=result.stderr,
        format=ffprobe_format,
    )


def test_ffprobe():
    # d = ffprobe(r'C:\\Users\\taynq\\Downloads\\CanNhaDiVangVinhSu-NhuQuynh-Tuon_n9hj.mp3')
    d = ffprobe(r"C:\\Users\\taynq\\Downloads\\AnhLoChoEmHet.mp3")
    print(d)
    f = json.loads(d.output)
    # print(f)
    streams = f.get("streams", [])
    media_formats = f.get("format", {})
    # print(media_formats)
    for stream in streams:
        # print(f'{stream.get("codec_type", "unknown")}: {stream.get("codec_long_name")}')
        print(stream.get("codec_type"))

    # for media_format in media_formats:
    #     print(f'{media_format.get("format_name")}: {media_format.get("duration")}')


def check_audio_video(file_name):
    raw_data = ffprobe(file_name)
    json_data = json.loads(raw_data.output)
    streams = json_data.get("streams", [])
    # print(streams)
    str_streams = set()
    for stream in streams:
        str_streams.add(stream.get("codec_type"))
    if len(str_streams) == 0:
        logging.info("Media file error")
        return "error"
    elif len(str_streams) >= 1 and "video" in str_streams:
        return "video"
    else:
        return "audio"

    # print(len(streams))


def test_check_audio_video():
    print(check_audio_video(r"C:\\Users\\taynq\\Downloads\\a.mp4"))
    print(
        check_audio_video(
            r"C:\\Users\\taynq\\Downloads\\CanNhaDiVangVinhSu-NhuQuynh-Tuon_n9hj.mp3"
        )
    )
    print(check_audio_video(r"C:\\Users\\taynq\\Downloads\\AnhLoChoEmHet.mp3"))


def test_duration():
    # print(get_length(r'C:\\Users\\taynq\\Downloads\\CanNhaDiVangVinhSu-NhuQuynh-Tuon_n9hj.mp3'))
    # print(with_opencv(r'C:\\Users\\taynq\\Downloads\\a.mp4'))
    print(get_media_duration(r"C:\\Users\\taynq\\Downloads\\a.mp4"))
    print(
        get_media_duration(
            r"C:\\Users\\taynq\\Downloads\\CanNhaDiVangVinhSu-NhuQuynh-Tuon_n9hj.mp3"
        )
    )
    print(get_media_duration(r"C:\\Users\\taynq\\Downloads\\AnhLoChoEmHet.mp3"))


def get_media_duration(file_name):
    media_info = MediaInfo.parse(file_name)
    duration_ms = media_info.tracks[0].duration / 1000
    duration_format = convert_seconds_to_hour_minute_second(int(duration_ms))
    # print(media_info.tracks)
    return duration_format


# Refer link https://pymediainfo.readthedocs.io/en/stable/pymediainfo.html
def check_media_type(file_name):
    media_info = MediaInfo.parse(file_name)
    track_types = set()
    for track in media_info.tracks:
        track_types.add(track.track_type)

    if len(track_types) <= 0:
        print("Media with error format")
        return "error"
    elif len(track_types) >= 1 and "Video" in track_types:
        return "video"
    elif len(track_types) >= 1 and "Audio" in track_types:
        return "audio"
    elif len(track_types) >= 1 and "Image" in track_types:
        return "image"
    elif len(track_types) >= 1 and "General" in track_types:
        return "general"
    elif len(track_types) >= 1 and "Menu" in track_types:
        return "menu"
    else:
        return "other"


def convert_seconds_to_hour_minute_second(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


# Print media info to json
def print_media_info(file_name_with_path):
    media_info = MediaInfo.parse(file_name_with_path, output="JSON")
    print(media_info)
