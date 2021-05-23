import click
from sedi.engine import Baidu, Sogou, T360


@click.command()
@click.option('--save_path', '-s', default='./img', help='Picture save path (relative path or absolute path) [./img].')
@click.option('--engine', '-e', default='baidu', help='Search engine ([baidu], sogou, 360).')
@click.argument('keyword')
def execute(keyword, save_path, engine):
    search_engine = {
        'baidu': Baidu,
        'sogou': Sogou,
        '360': T360
    }
    search_engine.get(engine, Baidu)(keyword, save_path).begin()
