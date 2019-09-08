# /usr/bin/python
# encoding=utf-8
import os
import sys
import click
import functools


def singleton(cls):
    _instance = {}

    def inner(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return inner

# class singleton(object):
#     def __init__(self, cls):
#         self._cls = cls
#         self._instance = {}
#     def __call__(self):
#         if self._cls not in self._instance:
#             self._instance[self._cls] = self._cls()
#         return self._instance[self._cls]


# common
CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    default_map={
        'cli': {'stage': 'pp'},
        'run': {'tag': 'common_tag'},
    }
)

# # offline
# CONTEXT_SETTINGS = dict(
#     default_map={'runserver': {'port': 5000}}
# )

# # Apsara Stack
# CONTEXT_SETTINGS = dict(
#     default_map={'runserver': {'port': 5000}}
# )


def stage(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # import logging
        # logger = logging.getLogger(name)
        # logger.info('Async Function {}, {}, {}'.format(
        #     func.__name__, str(args), str(kwargs)))
        try:
            click.secho('{} args: {}, kwargs: {} start !'.format(
                func.__name__, args, kwargs), fg=u'blue', bg=u'black', underline=True, bold=True)
            result = func(*args, **kwargs)
            print('{} success!'.format(func.__name__))
            return result
        except Exception as e:
            print('{} failed! message: {}'.format(func.__name__, e))
            return False
            # import traceback
            # logger.error(str(e), traceback.format_exc())
            # raise e
    return wrapper


@singleton
class Operater(object):

    def __init__(self, *args, **kwargs):
        import random
        self.num = random.random()

    @stage
    def stage_setup(self, *args, **kwargs):
        pass

    @stage
    def stage_init(self, *args, **kwargs):
        pass

    @stage
    def stage_migration(self, *args, **kwargs):
        pass

    @stage
    def stage_lock(self, *args, **kwargs):
        pass

    @stage
    def stage_run(self, *args, **kwargs):
        pass

    @stage
    def stage_parser(self, *args, **kwargs):
        pass

    @stage
    def stage_collect(self, *args, **kwargs):
        pass

    @stage
    def stage_upload(self, *args, **kwargs):
        pass

    @stage
    def stage_clean(self, *args, **kwargs):
        pass

    @stage
    def tool_status(self, *args, **kwargs):
        pass


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0, Powered by Ecs-Lab')
    ctx.exit()


class Product(object):
    def __init__(self, debug=False):
        self.debug = debug


pass_product = click.make_pass_decorator(Product, ensure=True)


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.option('-s', '--stage', type=click.STRING, default='all', help=u'兼容旧命令')
@click.option('-c', '--clean', type=click.BOOL, default=False, help=u'兼容旧命令, 测试结束释放vm')
@click.option('-m', '--mode', type=click.Choice(('simple', 'full')), default=u'full', help=u'兼容旧命令, 解析模式， 默认: full')
@click.option('--debug/--no-debug', default=False, help=u'开启debug模式，默认: --no-debug')
@click.pass_context
def cli(ctx, stage, clean, mode, debug):
    """
    欢迎使用CLI。 本工具由ECS-Lab提供。

    \b
    这是一套用于测试云主机的自动化测试框架，部分功能完善中，欢迎使用。这是一套用于测试云主机的自动化测试框架，部分功能完善中，欢迎使用这是一套用于测试云主机的自动化测试框架，部分功能完善中，欢迎使用这是一套用于测试云主机的自动化测试框架，部分功能完善中，欢迎使用
    """
    click.echo('prepare some thing')
    if ctx.invoked_subcommand is None:
        click.echo('stage = {}'.format(stage))
        click.echo('clean = {}'.format(clean))
        click.echo('I was invoked without subcommand')
    else:
        click.echo('I am about to invoke %s' % ctx.invoked_subcommand)
    ctx.ensure_object(dict)
    ctx.obj = Product(debug)


@cli.command(help=u'完整测试流程，setup -> init -> run -> parser -> collect -> upload')
@click.option('-t', '--tag', envvar='tag')
@click.option('-c', '--clean/--keep', default=False, help=u'测试结束是否释放vm， 默认: --keep')
@click.pass_context
def all(ctx, **kwargs):
    # ctx.forward(setup) and ctx.forward(init) and ctx.forward(run) and ctx.forward(clean)
    ctx.forward(setup)
    ctx.forward(init)
    ctx.forward(run)
    ctx.forward(clean)


@cli.command(help=u'创建实例操作')
@click.option('-t', '--tag', envvar='tag')
@click.option('-c', '--clean/--keep', default=False, help=u'开vm失败是否释放vm， 默认: --keep')
def setup(**kwargs):
    op = Operater()
    click.echo(op.num)
    op.stage_setup(**kwargs)


@cli.command(help=u'vm迁移操作')
@click.option('-t', '--tag', envvar='tag')
# @click.option('-f', '--force/--no-force', default=False, help=u'是否强制迁移，默认值: False')
def migration(**kwargs):
    op = Operater()
    op.stage_migration(**kwargs)


@cli.command(help=u'锁nc操作')
@click.option('-t', '--tag', envvar='tag')
@click.option('-f', '--force/--no-force', envvar='force_lock', default=False, help=u'是否强制锁nc，锁定失败则任务终止，默认值: False')
@pass_product
def lock(repo, **kwargs):
    click.echo(repo.__dict__)
    click.echo(repo.debug)
    Operater().stage_lock(**kwargs)


@cli.command(help=u'初始化实例操作')
@click.option('-t', '--tag', envvar='tag')
@click.option('-f', '--force/--no-force', default=False, help=u'是否强制初始化，会重复初始化, 默认: False')
@click.option('-u', '--update/--no-update', default=False, help=u'是否更新代码，默认: False')
@click.option('-r', '--run/--no-run', default=False, help=u'初始化结束是否进行压测，默认: False')
@click.pass_context
def init(ctx, **kwargs):
    op = Operater()
    click.echo(op.num)
    op.stage_init(**kwargs)
    return False


@cli.command(help=u'性能压测操作')
@click.option('-t', '--tag', envvar='tag')
@click.option('-p', '--parser', type=click.BOOL, default=True, help=u'是否同步解析， 默认: True')
@click.option('-l', '--loop', type=click.INT, default=1, help=u'循环跑几轮， 默认: 1')
@click.option('-u', '--upload', type=click.BOOL, default=True, help=u'是否同步上传结果， 默认: True')
@click.option('-n', '--new_task_id/--old_task_id', default=False, help=u'是否生成新到task_id， 默认: False')
@click.option('-f', '--force/--no-force', default=False, help=u'是否忽略case状态强制重跑， 默认: False')
@click.option('-c', '--clean/--keep', default=False, help=u'测试结束是否释放vm， 默认: --keep')
@click.option('-m', '--parallel/--common', default=False, help=u'是否是多vm并行压测， 默认: False')
@click.option('--case_type', type=click.Choice(('cpu', 'io', 'memory', 'network')), multiple=True, help=u'指定跑那些case_type到case，支持多选，默认全跑')
@click.option('-s', '--scenario_name', type=click.STRING, multiple=True, help=u'指定跑哪几个case，支持多选，默认全跑')
@click.pass_context
def run(ctx, **kwargs):
    Operater().stage_run(**kwargs)


@cli.command(help=u'结果解析操作')
@click.option('-t', '--tag', envvar='tag')
@click.option('-r', '--remote/--local', default=False, help=u'是否在远端解析, 默认: False')
@click.option('-u', '--upload', type=click.BOOL, default=True, help=u'是否同步上传结果， 默认: True')
@click.option('-m', '--mode', type=click.Choice(('simple', 'full')), default=u'full', help=u'解析模式， 默认: full')
def parser(**kwargs):
    Operater().stage_parser(**kwargs)


@cli.command(help=u'结果收集操作')
@click.option('-t', '--tag', envvar='tag')
@click.option('-r', '--result', type=click.BOOL, default=True, help=u'收集结果数据， 默认: True')
@click.option('-i', '--instance', type=click.BOOL, default=True, help=u'收集实例信息， 默认: True')
@click.option('-v', '--verbose', type=click.BOOL, default=False, help=u'详细信息， 默认: False')
def collect(**kwargs):
    Operater().stage_collect(**kwargs)


@cli.command(help=u'结果上传操作')
@click.option('-t', '--tag', envvar='tag')
@click.option('-b', '--backup', type=click.BOOL, default=True, help=u'结果备份到oss， 默认: True')
@click.option('-i', '--instance', type=click.BOOL, default=True, help=u'上传实例信息， 默认: True')
@click.option('-t', '--task', type=click.BOOL, default=True, help=u'上传task信息， 默认: True')
@click.option('-r', '--result', type=click.BOOL, default=True, help=u'上传结果信息， 默认: True')
@click.option('-s', '--status', type=click.BOOL, default=True, help=u'上传case状态信息， 默认: True')
def upload(**kwargs):
    Operater().stage_upload(**kwargs)


@cli.command(help=u'实例释放操作')
@click.option('-t', '--tag', envvar='tag')
@click.option('-n', '--unlock_nc', type=click.BOOL, default=True, help=u'是否解锁nc， 默认: True')
def clean(**kwargs):
    Operater().stage_clean(**kwargs)


@cli.command(help=u'各种状态检查')
@click.option('-t', '--tag', envvar='tag')
@click.option('-a', '--all', type=click.BOOL, default=True, help=u'全部状态')
@click.option('-c', '--case/--no-case', default=False, help=u'case状态')
@click.option('-i', '--instance/--no-instance', default=False, help=u'实例状态')
@click.option('-u', '--upload/--no-upload', default=False, help=u'上传状态')
@click.option('-p', '--parser/--no-parser', default=False, help=u'解析状态')
@click.option('-v', '--verbose/--no-verbose', default=False, help=u'显示详细信息')
def status(**kwargs):
    Operater().tool_status(**kwargs)


@cli.command(help=u'nc 相关操作及信息展示')
@click.option('-t', '--tag', envvar='tag')
def nc(**kwargs):
    # “”“
    # # TODO： 这里考虑要不要搞成交互式的，使用prompt_toolkit库可以实现。
    # 1. 输入nc_id或者nc_ip可以查看nc上存在的vm信息和nc状态，cpu、内存数等。
    # 2. 可执行迁移vm命令、锁定nc，解锁nc等。
    # ”“”
    pass


@cli.command(help=u'vm 操作及信息展示')
@click.option('-t', '--tag', envvar='tag')
def vm(**kwargs):
    # “”“
    # # TODO： 这里考虑要不要搞成交互式的，使用prompt_toolkit库可以实现。prettytable 可输出表表格
    # 1. 输入instance_id或者pub_ip可以查看vm信息和状态，cpu、内存数等。
    # 2. 可执行迁移vm命令、锁定nc，解锁nc等。
    # 3. 可挂在磁盘、网卡、操作安全组等命令，可查看安全组等命令。
    # ”“”

    from prettytable import PrettyTable
    x = PrettyTable(["City name", "Area", "Population", "Annual Rainfall"])
    x.align["City name"] = "l"  # Left align city names
    # One space between column edges and contents (default)
    x.padding_width = 1
    x.add_row(["Adelaide", 1295, 1158259, 600.5])
    x.add_row(["Brisbane", 5905, 1857594, 1146.4])
    x.add_row(["Darwin", 112, 120900, 1714.7])
    x.add_row(["Hobart", 1357, 205556, 619.5])
    x.add_row(["Sydney", 2058, 4336374, 1214.8])
    x.add_row(["Melbourne", 1566, 3806092, 646.9])
    x.add_row(["Perth", 5386, 1554769, 869.4])
    click.echo(x)


if __name__ == "__main__":
    cli(obj={})
