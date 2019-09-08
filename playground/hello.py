
import click
@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)
#  helllllll
@click.command()
@click.option('--force', default=True, help='drop db anyway')
@click.argument('name')
def dropdb(force, name):
    click.echo(force)
    click.echo('Droped the database:%s' % name)

if ('3'=='dd'):
    print 'aa'






if __name__ == '__main__':
    hello()
    if (True):
        print('hahaha')
    os.path.join('a','b


print('hah1')

print('hah2')
print('hah3')
print('hah4')
print('hah5')
print('hah6')


# if __name__ == '__main__':
#     hello()
