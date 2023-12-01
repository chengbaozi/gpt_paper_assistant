import json
from datetime import datetime
import re


def render_paper(paper_entry: dict, idx: int) -> str:
    """
    :param paper_entry: is a dict from a json. an example is
    {"paperId": "2754e70eaa0c2d40972c47c4c23210f0cece8bfc", "externalIds": {"ArXiv": "2310.16834", "CorpusId": 264451832}, "title": "Discrete Diffusion Language Modeling by Estimating the Ratios of the Data Distribution", "abstract": "Despite their groundbreaking performance for many generative modeling tasks, diffusion models have fallen short on discrete data domains such as natural language. Crucially, standard diffusion models rely on the well-established theory of score matching, but efforts to generalize this to discrete structures have not yielded the same empirical gains. In this work, we bridge this gap by proposing score entropy, a novel discrete score matching loss that is more stable than existing methods, forms an ELBO for maximum likelihood training, and can be efficiently optimized with a denoising variant. We scale our Score Entropy Discrete Diffusion models (SEDD) to the experimental setting of GPT-2, achieving highly competitive likelihoods while also introducing distinct algorithmic advantages. In particular, when comparing similarly sized SEDD and GPT-2 models, SEDD attains comparable perplexities (normally within $+10\\%$ of and sometimes outperforming the baseline). Furthermore, SEDD models learn a more faithful sequence distribution (around $4\\times$ better compared to GPT-2 models with ancestral sampling as measured by large models), can trade off compute for generation quality (needing only $16\\times$ fewer network evaluations to match GPT-2), and enables arbitrary infilling beyond the standard left to right prompting.", "year": 2023, "authors": [{"authorId": "2261494043", "name": "Aaron Lou"}, {"authorId": "83262128", "name": "Chenlin Meng"}, {"authorId": "2490652", "name": "Stefano Ermon"}], "ARXIVID": "2310.16834", "COMMENT": "The paper shows a significant advance in the performance of diffusion language models, directly meeting one of the criteria.", "RELEVANCE": 10, "NOVELTY": 8}, "2310.16779": {"paperId": "edc8953d559560d3237fc0b27175cdb1114c0ca5", "externalIds": {"ArXiv": "2310.16779", "CorpusId": 264451949}, "title": "Multi-scale Diffusion Denoised Smoothing", "abstract": "Along with recent diffusion models, randomized smoothing has become one of a few tangible approaches that offers adversarial robustness to models at scale, e.g., those of large pre-trained models. Specifically, one can perform randomized smoothing on any classifier via a simple\"denoise-and-classify\"pipeline, so-called denoised smoothing, given that an accurate denoiser is available - such as diffusion model. In this paper, we investigate the trade-off between accuracy and certified robustness of denoised smoothing: for example, we question on which representation of diffusion model would maximize the certified robustness of denoised smoothing. We consider a new objective that aims collective robustness of smoothed classifiers across multiple noise levels at a shared diffusion model, which also suggests a new way to compensate the cost of accuracy in randomized smoothing for its certified robustness. This objective motivates us to fine-tune diffusion model (a) to perform consistent denoising whenever the original image is recoverable, but (b) to generate rather diverse outputs otherwise. Our experiments show that this fine-tuning scheme of diffusion models combined with the multi-scale smoothing enables a strong certified robustness possible at highest noise level while maintaining the accuracy closer to non-smoothed classifiers.", "year": 2023, "authors": [{"authorId": "83125078", "name": "Jongheon Jeong"}, {"authorId": "2261688831", "name": "Jinwoo Shin"}], "ARXIVID": "2310.16779", "COMMENT": "The paper presents an advancement in the performance of diffusion models, specifically in the context of denoised smoothing.", "RELEVANCE": 9, "NOVELTY": 7}
    :return: a markdown formatted string showing the arxiv id, title, arxiv url, abstract, authors, score and comment (if those fields exist)
    """
    # get the arxiv id
    arxiv_id = paper_entry["arxiv_id"]
    # get the title
    title = paper_entry["title"]
    # get the arxiv url
    arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
    # get the abstract
    abstract = paper_entry["abstract"]
    # get the authors
    authors = paper_entry["authors"]
    paper_string = f'## {idx}. [{title}]({arxiv_url})\n'
    paper_string += f"**ArXiv:** {arxiv_id}\n"
    paper_string += f'**Authors:** {", ".join(authors)}\n\n'
    paper_string += f"**Abstract:** {abstract}\n\n"
    if "COMMENT" in paper_entry:
        comment = paper_entry["COMMENT"]
        paper_string += f"**Comment:** {comment}\n\n"
    if "RELEVANCE" in paper_entry and "NOVELTY" in paper_entry:
        # get the relevance and novelty scores
        relevance = paper_entry["RELEVANCE"]
        novelty = paper_entry["NOVELTY"]
        paper_string += f"**Relevance:** {relevance}\n"
        paper_string += f"**Novelty:** {novelty}\n"
    paper_string += f"[back to top](#topics)\n"
    return paper_string + "\n---\n"


def render_title_and_author(paper_entry: dict, idx: int) -> str:
    # get the arxiv id
    arxiv_id = paper_entry["arxiv_id"]
    # get the title
    title = paper_entry["title"]
    # get the arxiv url
    arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
    authors = paper_entry["authors"]
    
    raw_title_url = f'{idx} {title}'
    # Keep only English letters, numbers, and spaces
    cleaned = re.sub(r'[^a-zA-Z0-9 -]', '', raw_title_url)
    
    # Replace spaces with dashes
    cleaned = cleaned.replace(' ', '-').lower()
    paper_string = f'{idx}. [{title}]({arxiv_url}) [[More](#{cleaned})] \\\n'
    paper_string += f'**Authors:** {", ".join(authors)}\n'
    return paper_string


def render_criterion(criterions: list[str]) -> str:
    criterion_string = ""
    for criteria in criterions:
        topic_idx = int(criteria.split('.')[0])
        criterion_string += f"[{criteria}](#topic-{topic_idx})\n\n"
    criterion_string += '[Unknown](#topic-unknown)\n\n'
    return criterion_string

def extract_criterion_from_paper(paper_entry: dict) -> int:
    if "COMMENT" not in paper_entry:
        return 0
    # Regular expression pattern to find 'criterion' followed by a number
    pattern = r'criterion (\d+)'
    # Search for the pattern in the text
    match = re.search(pattern, paper_entry["COMMENT"])
    if match:
        # Extract the number (group 1 in the match)
        criterion_number = match.group(1)
        return int(criterion_number)
    else:
        return 0 # not sure

def render_md_paper_title_by_topic(topic_idx, paper_in_topic: list[str]) -> str: 
    return f"### Topic {topic_idx}\n[back to top](#topics)\n\n" +  "\n".join(paper_in_topic) + "\n---\n"
        

def render_md_string(papers_dict):
    # header
    with open("configs/paper_topics.txt", "r") as f:
        criterion = f.readlines()
        
    filtered_criterion = [i for i in criterion if len(i.strip()) and i.strip()[0] in '0123456789']
    
    criterion_string = render_criterion(filtered_criterion)
        
    output_string = (
        "# Personalized Daily Arxiv Papers "
        + datetime.today().strftime("%m/%d/%Y")
        + "\n\n## Topics\n\nPaper selection prompt and criteria (jump to the section by clicking the link):\n\n"
        + criterion_string
        + "\n---\n"
        # + "## All\n Total relevant papers: "
        # + str(len(papers_dict))
        # + "\n\n"
        # + "Table of contents with paper titles:\n\n"
    )
    '''
    title_strings = [
        render_title_and_author(paper, i)
        for i, paper in enumerate(papers_dict.values())
    ]
    # output_string = output_string + "\n".join(title_strings) + "\n---\n"
    '''
    # render each topic
    paper_str_group_by_topic = [[] for _ in range(len(filtered_criterion) + 1)]
    for i, paper in enumerate(papers_dict.values()):
        paper_topic_idx = extract_criterion_from_paper(paper)
        title_string = render_title_and_author(paper, i)
        paper_str_group_by_topic[paper_topic_idx].append(title_string)
        
    for topic_idx, paper_in_topic in enumerate(paper_str_group_by_topic):
        if topic_idx == 0:
            # unknown topic
            continue
        output_string += render_md_paper_title_by_topic(topic_idx, paper_in_topic) 
    output_string += render_md_paper_title_by_topic("unknown", paper_str_group_by_topic[0])

    # render each paper
    paper_strings = [
        render_paper(paper, i) for i, paper in enumerate(papers_dict.values())
    ]
    # join all papers into one string
    output_string += "## Full paper list\n"
    output_string = output_string + "\n".join(paper_strings)
    # output_string += "\n\n---\n\n"
    # output_string += f"## Paper selection prompt\n{criterion}"
    return output_string


if __name__ == "__main__":
    # parse output.json into a dict
    with open("out/output.json", "r") as f:
        output = json.load(f)
    # write to output.md
    with open("out/output.md", "w") as f:
        f.write(render_md_string(output))
