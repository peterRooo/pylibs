import whisper
import logging 
import json
import datetime

def transcribe(audio_path):
    logging.info("start to transcribe: " + audio_path)
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    logging.info(result["text"])
    return result['text']


def extract_subtitles(audio_file_path, model_size='base', target_language='English', use_gpu=False):
    """
    提取音频文件中的字幕。

    参数:
    audio_file_path (str): 音频文件的路径。
    model_size (str): 使用的whisper模型大小，例如 'tiny', 'base', 'small', 'medium', 'large'。
    target_language (str): 目标语言，例如 'English'。
    use_gpu (bool): 是否使用GPU。如果为None，则自动检测系统是否支持GPU。
    output_format (str): 输出格式，可以是 'txt', 'vtt', 'srt', 'tsv', 'json'。
    """

    # 加载模型
    model = whisper.load_model(model_size, device="cuda" if use_gpu else "cpu")

    # 加载音频并进行转录
    audio = whisper.load_audio(audio_file_path)
    # audio = whisper.pad_or_trim(audio)

    # 进行模型推理
    options = whisper.DecodingOptions(fp16=use_gpu, language=target_language)
    initial_prompt = None
    # 设置初始提示，保证输出简体中文
    # if target_language == 'Chinese':
    #     initial_prompt = '以下是普通话的句子。'
    result = model.transcribe(audio, initial_prompt=initial_prompt, **vars(options))

    out_res = {}

    logging.info(result)
    out_res['txt'] = format_transcript(result['segments'], output_format='txt')
    out_res['json'] = format_transcript(result['segments'], output_format='json')
    out_res['srt'] = format_transcript(result['segments'], output_format='srt')
    out_res['tsv'] = format_transcript(result['segments'], output_format='tsv')
    out_res['vtt'] = format_transcript(result['segments'], output_format='vtt')

    return out_res


def format_time(seconds):
    """将秒数转换为字幕文件中使用的时间格式。"""
    return str(datetime.timedelta(seconds=seconds)).replace('.', ',')

def format_transcript(transcript, output_format='txt'):
    """将转录结果转换为指定的字幕格式。"""
    if output_format == 'txt':
        return "\n".join(segment['text'] for segment in transcript)

    elif output_format == 'json':
        return json.dumps(transcript, ensure_ascii=False, indent=4)

    elif output_format == 'srt':
        srt_content = []
        for index, segment in enumerate(transcript, start=1):
            start_time = format_time(segment['start'])
            end_time = format_time(segment['end'])
            text = segment['text']
            srt_content.append(f"{index}\n{start_time} --> {end_time}\n{text}\n")
        return "\n".join(srt_content)

    elif output_format == 'vtt':
        vtt_content = ["WEBVTT\n"]
        for segment in transcript:
            start_time = format_time(segment['start'])
            end_time = format_time(segment['end'])
            text = segment['text']
            vtt_content.append(f"{start_time} --> {end_time}\n{text}\n")
        return "\n".join(vtt_content)

    elif output_format == 'tsv':
        tsv_content = ["start\tend\ttext"]
        for segment in transcript:
            start_time = format_time(segment['start'])
            end_time = format_time(segment['end'])
            text = segment['text']
            tsv_content.append(f"{start_time}\t{end_time}\t{text}")
        return "\n".join(tsv_content)

    else:
        raise ValueError(f"Unsupported output format: {output_format}")


g_language_map = {
    '简体中文': 'Chinese',
    '英语': 'English',
    '亚美尼亚语': 'Armenian',
    '阿萨姆语': 'Assamese',
    '阿塞拜疆语': 'Azerbaijani',
    '巴什基尔语': 'Bashkir',
    '巴斯克语': 'Basque',
    '白俄罗斯语': 'Belarusian',
    '孟加拉语': 'Bengali',
    '波斯尼亚语': 'Bosnian',
    '布列塔尼语': 'Breton',
    '保加利亚语': 'Bulgarian',
    '缅甸语': 'Burmese',
    '粤语': 'Cantonese',
    '卡斯蒂利亚语': 'Castilian',
    '加泰罗尼亚语': 'Catalan',
    '克罗地亚语': 'Croatian',
    '捷克语': 'Czech',
    '丹麦语': 'Danish',
    '荷兰语': 'Dutch',
    '爱沙尼亚语': 'Estonian',
    '法罗语': 'Faroese',
    '芬兰语': 'Finnish',
    '佛兰德语': 'Flemish',
    '法语': 'French',
    '加利西亚语': 'Galician',
    '格鲁吉亚语': 'Georgian',
    '德语': 'German',
    '希腊语': 'Greek',
    '古吉拉特语': 'Gujarati',
    '海地语': 'Haitian',
    '海地克里奥尔语': 'Haitian Creole',
    '豪萨语': 'Hausa',
    '夏威夷语': 'Hawaiian',
    '希伯来语': 'Hebrew',
    '印地语': 'Hindi',
    '匈牙利语': 'Hungarian',
    '冰岛语': 'Icelandic',
    '印度尼西亚语': 'Indonesian',
    '意大利语': 'Italian',
    '日语': 'Japanese',
    '爪哇语': 'Javanese',
    '卡纳达语': 'Kannada',
    '哈萨克语': 'Kazakh',
    '高棉语': 'Khmer',
    '韩语': 'Korean',
    '老挝语': 'Lao',
    '拉丁语': 'Latin',
    '拉脱维亚语': 'Latvian',
    '卢森堡语': 'Letzeburgesch',
    '林加拉语': 'Lingala',
    '立陶宛语': 'Lithuanian',
    '卢森堡语': 'Luxembourgish',
    '马其顿语': 'Macedonian',
    '马尔加什语': 'Malagasy',
    '马来语': 'Malay',
    '马拉雅拉姆语': 'Malayalam',
    '马耳他语': 'Maltese',
    '普通话': 'Mandarin',
    '毛利语': 'Maori',
    '马拉地语': 'Marathi',
    '摩尔多瓦语': 'Moldavian',
    '摩尔多瓦语': 'Moldovan',
    '蒙古语': 'Mongolian',
    '缅甸语': 'Myanmar',
    '尼泊尔语': 'Nepali',
    '挪威语': 'Norwegian',
    '新挪威语': 'Nynorsk',
    '奥克语': 'Occitan',
    '旁遮普语': 'Panjabi',
    '普什图语': 'Pashto',
    '波斯语': 'Persian',
    '波兰语': 'Polish',
    '葡萄牙语': 'Portuguese',
    '旁遮普语': 'Punjabi',
    '普什图语': 'Pushto',
    '罗马尼亚语': 'Romanian',
    '俄语': 'Russian',
    '梵语': 'Sanskrit',
    '塞尔维亚语': 'Serbian',
    '绍纳语': 'Shona',
    '信德语': 'Sindhi',
    '僧伽罗语': 'Sinhala',
    '僧伽罗语': 'Sinhalese',
    '斯洛伐克语': 'Slovak',
    '斯洛文尼亚语': 'Slovenian',
    '索马里语': 'Somali',
    '西班牙语': 'Spanish',
    '巽他语': 'Sundanese',
    '斯瓦希里语': 'Swahili',
    '瑞典语': 'Swedish',
    '他加禄语': 'Tagalog',
    '塔吉克语': 'Tajik',
    '泰米尔语': 'Tamil',
    '鞑靼语': 'Tatar',
    '泰卢固语': 'Telugu',
    '泰语': 'Thai',
    '藏语': 'Tibetan',
    '土耳其语': 'Turkish',
    '土库曼语': 'Turkmen',
    '乌克兰语': 'Ukrainian',
    '乌尔都语': 'Urdu',
    '乌兹别克语': 'Uzbek',
    '瓦伦西亚语': 'Valencian',
    '越南语': 'Vietnamese',
    '威尔士语': 'Welsh',
    '意第绪语': 'Yiddish',
    '约鲁巴语': 'Yoruba',
}