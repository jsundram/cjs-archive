#!/usr/bin/env python3
"""
Generate static pages (index, cqc, court-monitor) using base template and content files.
"""

from pathlib import Path


# Page configurations
PAGES = [
    {
        'output': '../docs/index.html',
        'content_file': 'index-content.html',
        'meta_title': 'About Clarence J. Sundram',
        'meta_description': 'Clarence J. Sundram is a nationally recognized expert on conditions in institutions and community programs for persons with mental disabilities, serving as court monitor, special advisor, and founding chairman of the NY Commission on Quality of Care.',
        'canonical_url': 'index.html',
        'page_title': 'About',
    },
    {
        'output': '../docs/cqc.html',
        'content_file': 'cqc-content.html',
        'meta_title': 'Commission on Quality of Care for the Mentally Disabled',
        'meta_description': 'Overview of the New York State Commission on Quality of Care for the Mentally Disabled and Clarence J. Sundram\'s work as founding Chairman.',
        'canonical_url': 'cqc.html',
        'page_title': 'Commission on Quality of Care',
    },
    {
        'output': '../docs/court-monitor.html',
        'content_file': 'court-monitor-content.html',
        'meta_title': 'Court Monitor Work',
        'meta_description': 'Clarence J. Sundram\'s work as Court Monitor and Special Master in class action lawsuits involving the rights of persons with mental disabilities.',
        'canonical_url': 'court-monitor.html',
        'page_title': 'Court Monitor',
    },
    {
        'output': '../docs/404.html',
        'content_file': '404-content.html',
        'meta_title': 'Page Not Found',
        'meta_description': 'The page you are looking for could not be found.',
        'canonical_url': '404.html',
        'page_title': '404 - Page Not Found',
    },
]


def main():
    """Generate all static pages using base template and content files."""

    # Load base template
    template_path = Path('base-template.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        base_template = f.read()

    print("Generating static pages...\n")

    for page_config in PAGES:
        # Load content file
        content_path = Path(page_config['content_file'])
        with open(content_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Populate base template
        html = base_template.replace('{meta_title}', page_config['meta_title'])
        html = html.replace('{meta_description}', page_config['meta_description'])
        html = html.replace('{canonical_url}', page_config['canonical_url'])
        html = html.replace('{breadcrumb}', '')  # No breadcrumb for static pages
        html = html.replace('{page_title}', page_config['page_title'])
        html = html.replace('{content}', content)
        html = html.replace('{path_prefix}', './')

        # Write output file
        output_path = Path(page_config['output'])
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ Generated {output_path.name}")

    print(f"\n{'='*60}")
    print(f"Static pages generated with search functionality!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
