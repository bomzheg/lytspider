from dataclasses import dataclass
from lxml import etree


@dataclass
class ParsedData:
    links: list[str]
    target: str


def parse_page(content: str, base_url: str, xpath: str):
    html_tree = etree.HTML(content, base_url=base_url)
    return ParsedData(
        links=parse_links(html_tree=html_tree, base_url=base_url),
        target=parse_content(html_tree=html_tree, xpath=xpath),
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


def parse_content(html_tree, xpath: str) -> str:
    """
    get target content from all html

    :param xpath: path of target content
    :param html_tree: HTML of all page
    :return: target html tag and all
    """
    return str(html_tree.xpath(xpath))
