from config import get_logger
import re
import html

logger = get_logger("bot.services")

#handle json-body of response
def format_json_body(response_body: dict) -> str:
    #TODO: check response-body format logic
    logger.debug("format response-json body")

    answer = response_body.get("response", "")
    if not answer:
        answer: str = _format_uncertain_payload(response_body)
       
    
    return answer


def _format_uncertain_payload(payload: dict) -> str:
    logger.warning(f"format uncertain payload. Response json structure differs from default: {payload}")
    response_str: str
    for (k,v) in payload.items():
        response_str += f"\n\n {v}"
    
    return response_str


def clean_tags(f_text:str, parsemode: str) -> str:
    logger.debug(f"clean text for parse mode {parsemode}")
    match parsemode:
        case "MARKDOWN" | "MARKDOWN_V2":
            return _clean_markdown(f_text)
        case "HTML":
            return _clean_html(f_text)
        case _:
            return f_text



def _clean_markdown(text: str) -> str:
    """
    Очищает текст от Markdown разметки, сохраняя читаемость.
    """
    text = re.sub(r"(?m)^\s{0,3}#+\s*", "", text)

    text = re.sub(r"(\*\*|__|~~|[*_`])", "", text)

    text = text.replace("```", "")

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"\1 (\2)", text)

    return text.strip()


def _clean_html(text: str) -> str:
    """
    Удаляет HTML теги и декодирует сущности (например, &quot; -> ").
    """
    text = re.sub(r"<[^>]+>", "", text)

    text = html.unescape(text)

    return text.strip()

