from lxml import etree


def parse_links(content: str, base_url: str) -> list[str]:
    """
    get all internal links in site

    :param base_url: url of site for
    :param content: HTML with all content
    :return: list of all internal links of site
    """
    html_tree = etree.HTML(content, base_url=base_url)
    links = html_tree.xpath(f'//a[contains(@href, "{base_url}")]/@href')
    return list(map(str, links))


def parse_content(content: str, xpath: str) -> str:
    """
    get target content from all html

    :param xpath: path of target content
    :param content: HTML of all page
    :return: target html tag and all
    """
    return content
