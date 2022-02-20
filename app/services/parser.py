import logging
from dataclasses import dataclass
from lxml import etree

from app.models.config.main import ParserConfig

logger = logging.getLogger(__name__)


@dataclass
class ParsedData:
    links: list[str]
    target: str


def parse_page(content: str, url: str, config: ParserConfig):
    html_tree = etree.HTML(content, base_url=url)
    return ParsedData(
        links=parse_links(html_tree=html_tree, base_url=config.url),
        target=parse_content(html_tree=html_tree, url=url, config=config),
    )


def parse_links(html_tree, base_url: str) -> list[str]:
    """
    get all internal links in site

    :param base_url: url of site for
    :param html_tree: HTML with all content
    :return: list of all internal links of site
    """
    links = html_tree.xpath(f'//a[contains(@href, "{base_url}")]/@href')
    return list(map(str, links))


def parse_content(html_tree, url: str, config: ParserConfig) -> str:
    """
    get target content from all html
    """
    xpath = config.get_xpath(url)
    result = html_tree.xpath(xpath)
    try:
        return etree.tostring(result[0]).decode()
    except IndexError:
        logger.warning("not found element by xpath %s", xpath)
        return ""
